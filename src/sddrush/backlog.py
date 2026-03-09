from __future__ import annotations

import re
import shutil
import xml.etree.ElementTree as ET
from argparse import ArgumentParser
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from sddrush.shared import (
    ensure_sdd_dir,
    extract_agent_notes,
    extract_bullets,
    extract_status,
    read_text,
    replace_status,
    resolve_backlog_paths,
    slugify,
)

TICKETS_PATTERN = re.compile(r"<tickets>.*?</tickets>", re.DOTALL)


@dataclass(frozen=True)
class TicketRecord:
    ticket_id: str
    slug: str
    title: str
    ticket_type: str
    summary: str
    depends_on: list[str]
    spec_refs: list[str]
    objective: str
    definition_of_done: list[str]
    steps: list[str]
    affected_paths: list[str]
    tests: list[str]
    risks: list[str]
    janitor_signals: list[str]


def parse_args(argv: Sequence[str] | None) -> ArgumentParser:
    """Build the CLI parser for backlog commands."""
    parser = ArgumentParser(description="Manage SDD backlog files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="Sync tickets from .sdd/architect.md")
    sync_parser.add_argument("project_root", help="Project root containing .sdd/")

    janitor_parser = subparsers.add_parser(
        "janitor",
        help="Close tickets whose janitor signals pass",
    )
    janitor_parser.add_argument("project_root", help="Project root containing .sdd/")
    return parser


def normalize_text(value: str) -> str:
    """Trim XML text while preserving paragraphs where practical."""
    lines = [line.strip() for line in value.strip().splitlines()]
    return "\n".join(line for line in lines if line)


def child_text(parent: ET.Element, tag: str) -> str:
    """Read a single child text node."""
    child = parent.find(tag)
    if child is None:
        return ""
    return normalize_text("".join(child.itertext()))


def child_items(parent: ET.Element, tag: str) -> list[str]:
    """Read <item> children from a nested XML list node."""
    section = parent.find(tag)
    if section is None:
        return []
    items: list[str] = []
    for item in section.findall("item"):
        text = normalize_text("".join(item.itertext()))
        if text:
            items.append(text)
    return items


def extract_ticket_records(architect_markdown: str) -> list[TicketRecord]:
    """Parse the machine-readable <tickets> appendix from architect.md."""
    match = TICKETS_PATTERN.search(architect_markdown)
    if match is None:
        raise ValueError("No <tickets> appendix found in .sdd/architect.md.")

    root = ET.fromstring(match.group(0))
    records: list[TicketRecord] = []
    for ticket in root.findall("ticket"):
        ticket_id = child_text(ticket, "id")
        title = child_text(ticket, "title")
        slug = child_text(ticket, "slug") or slugify(title)
        if not ticket_id or not title:
            raise ValueError("Each <ticket> must include <id> and <title>.")

        records.append(
            TicketRecord(
                ticket_id=ticket_id,
                slug=slug,
                title=title,
                ticket_type=child_text(ticket, "type") or "feature",
                summary=child_text(ticket, "summary"),
                depends_on=child_items(ticket, "depends_on"),
                spec_refs=child_items(ticket, "spec_refs"),
                objective=child_text(ticket, "objective"),
                definition_of_done=child_items(ticket, "definition_of_done"),
                steps=child_items(ticket, "steps"),
                affected_paths=child_items(ticket, "affected_paths"),
                tests=child_items(ticket, "tests"),
                risks=child_items(ticket, "risks"),
                janitor_signals=child_items(ticket, "janitor_signals"),
            )
        )
    return records


def find_ticket_by_prefix(directory: Path, ticket_id: str) -> Path | None:
    """Find a ticket file by id prefix inside a single backlog directory."""
    matches = sorted(directory.glob(f"{ticket_id}-*.md"))
    if matches:
        return matches[0]
    return None


def preserve_ticket_state(ticket_path: Path) -> tuple[str, str]:
    """Keep status and agent notes when resyncing an open ticket."""
    if not ticket_path.exists():
        return ("open", "")
    existing = read_text(ticket_path)
    return (extract_status(existing), extract_agent_notes(existing))


def format_bullets(items: list[str], *, fallback: str = "- none") -> str:
    """Render bullet lists consistently."""
    if not items:
        return fallback
    return "\n".join(f"- {item}" for item in items)


def format_steps(items: list[str]) -> str:
    """Render ordered implementation steps."""
    if not items:
        return "\n".join(
            [
                "1. Define the concrete implementation change.",
                "2. Add verification.",
                "3. Update the ticket notes.",
            ]
        )
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def build_ticket_markdown(record: TicketRecord, *, status: str, agent_notes: str) -> str:
    """Convert a machine-readable ticket record into the canonical markdown ticket file."""
    depends_on = ", ".join(record.depends_on) if record.depends_on else "none"
    spec_refs = ", ".join(record.spec_refs) if record.spec_refs else "none"
    notes_body = (
        agent_notes
        or "- Reserved for the implementing agent: progress notes, blockers, receipts."
    )
    sections = [
        f"# Ticket: {record.ticket_id} {record.title}",
        f"Status: {status}",
        f"Type: {record.ticket_type}",
        f"Slug: {record.slug}",
        f"Depends on: {depends_on}",
        f"Spec refs: {spec_refs}",
        "Source: .sdd/architect.md",
        "",
        "## Summary",
        record.summary or "No summary provided.",
        "",
        "## Objective & Definition of Done",
        record.objective or "Clarify the desired outcome before implementation.",
        format_bullets(record.definition_of_done),
        "",
        "## Steps",
        format_steps(record.steps),
        "",
        "## Affected Paths",
        format_bullets(record.affected_paths),
        "",
        "## Tests & Verification",
        format_bullets(record.tests),
        "",
        "## Risks & Edge Cases",
        format_bullets(record.risks),
        "",
        "## Janitor Signals",
        format_bullets(record.janitor_signals),
        "",
        "## Agent Notes",
        notes_body,
        "",
    ]
    return "\n".join(sections)


def sync_tickets(project_root: Path) -> int:
    """Create or refresh backlog ticket files from architect.md."""
    sdd_dir = ensure_sdd_dir(project_root)
    architect_path = sdd_dir / "architect.md"
    architect_markdown = read_text(architect_path)
    if not architect_markdown:
        raise FileNotFoundError(f"{architect_path} is missing or empty.")

    records = extract_ticket_records(architect_markdown)
    backlog_paths = resolve_backlog_paths(sdd_dir, create=True)

    created_or_updated = 0
    skipped_closed = 0
    for record in records:
        target_name = f"{record.ticket_id}-{record.slug}.md"
        target_path = backlog_paths.open_dir / target_name
        open_match = find_ticket_by_prefix(backlog_paths.open_dir, record.ticket_id)
        closed_match = find_ticket_by_prefix(backlog_paths.closed_dir, record.ticket_id)

        if closed_match is not None and open_match is None:
            skipped_closed += 1
            continue

        source_path = open_match or target_path
        status, agent_notes = preserve_ticket_state(source_path)
        rendered = build_ticket_markdown(record, status=status, agent_notes=agent_notes)

        if open_match is not None and open_match != target_path:
            shutil.move(str(open_match), str(target_path))

        target_path.write_text(rendered, encoding="utf-8")
        created_or_updated += 1

    print(f"sync: {created_or_updated} ticket(s) written")
    if skipped_closed:
        print(f"sync: skipped {skipped_closed} closed ticket(s)")
    return 0


def evaluate_signal(project_root: Path, signal: str) -> bool:
    """Evaluate a minimal janitor signal against the repo."""
    if ":" not in signal:
        return False

    kind, raw_value = signal.split(":", 1)
    value = raw_value.strip()
    if kind == "path_exists":
        return (project_root / value).exists()
    if kind == "glob_exists":
        return any(project_root.glob(value))
    if kind == "path_contains":
        path_text = value.split("::", 1)
        if len(path_text) != 2:
            return False
        relative_path, expected_text = path_text
        file_path = project_root / relative_path.strip()
        if not file_path.is_file():
            return False
        return expected_text.strip() in file_path.read_text(encoding="utf-8")
    return False


def run_janitor(project_root: Path) -> int:
    """Close tickets when all of their janitor signals pass."""
    sdd_dir = ensure_sdd_dir(project_root)
    backlog_paths = resolve_backlog_paths(sdd_dir, create=True)
    closed_count = 0

    for ticket_path in sorted(backlog_paths.open_dir.glob("*.md")):
        markdown = read_text(ticket_path)
        signals = extract_bullets(markdown, "Janitor Signals")
        if not signals:
            continue
        if not all(evaluate_signal(project_root, signal) for signal in signals):
            continue

        closed_markdown = replace_status(markdown, "closed")
        destination = backlog_paths.closed_dir / ticket_path.name
        destination.write_text(f"{closed_markdown}\n", encoding="utf-8")
        ticket_path.unlink()
        closed_count += 1
        print(f"closed {ticket_path.name}")

    print(f"janitor: {closed_count} ticket(s) closed")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run backlog subcommands."""
    parser = parse_args(argv)
    args = parser.parse_args(argv)
    project_root = Path(args.project_root).resolve()
    if args.command == "sync":
        return sync_tickets(project_root)
    return run_janitor(project_root)

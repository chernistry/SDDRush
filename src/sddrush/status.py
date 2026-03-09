from __future__ import annotations

import re
from argparse import ArgumentParser
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

from sddrush.shared import ensure_sdd_dir, extract_status, read_text, resolve_backlog_paths

ADR_PATTERN = re.compile(r"(ADR-\d{3}[^\n]*)")


def parse_args(argv: Sequence[str] | None) -> ArgumentParser:
    """Build the CLI parser for status reporting."""
    parser = ArgumentParser(description="Summarize SDD progress for a project.")
    parser.add_argument("project_root", help="Project root containing .sdd/")
    return parser


def collect_latest_adrs(architect_markdown: str, *, limit: int = 5) -> list[str]:
    """Extract recent ADR lines from architect.md."""
    matches = [match.group(1).strip(" -") for match in ADR_PATTERN.finditer(architect_markdown)]
    deduped: list[str] = []
    for item in matches:
        if item not in deduped:
            deduped.append(item)
    return deduped[-limit:]


def main(argv: Sequence[str] | None = None) -> int:
    """Print a compact backlog and ADR summary."""
    parser = parse_args(argv)
    args = parser.parse_args(argv)

    project_root = Path(args.project_root).resolve()
    sdd_dir = ensure_sdd_dir(project_root)
    backlog_paths = resolve_backlog_paths(sdd_dir, create=True)

    open_tickets = sorted(backlog_paths.open_dir.glob("*.md"))
    closed_tickets = sorted(backlog_paths.closed_dir.glob("*.md"))
    status_counts = Counter(extract_status(read_text(path)) for path in open_tickets)
    total = len(open_tickets) + len(closed_tickets)
    done_ratio = (len(closed_tickets) / total * 100) if total else 0.0

    architect_markdown = read_text(sdd_dir / "architect.md")
    adrs = collect_latest_adrs(architect_markdown)

    print(f"project: {project_root.name}")
    print(f"backlog_root: {backlog_paths.open_dir.parent}")
    print(
        f"tickets: total={total} open={len(open_tickets)} "
        f"closed={len(closed_tickets)} done={done_ratio:.1f}%"
    )
    if status_counts:
        statuses = ", ".join(f"{status}={count}" for status, count in sorted(status_counts.items()))
        print(f"open_statuses: {statuses}")
    else:
        print("open_statuses: none")

    if adrs:
        print("latest_adrs:")
        for adr in adrs:
            print(f"- {adr}")
    else:
        print("latest_adrs: none")
    return 0


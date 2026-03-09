from __future__ import annotations

import json
import re
from argparse import ArgumentParser
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from typing import TypedDict, cast

from sddrush.shared import (
    IGNORED_DISCOVERY_NAMES,
    ensure_sdd_dir,
    has_repo_content,
    read_text,
    resolve_backlog_paths,
)

CONDITIONAL_PATTERN = re.compile(
    r"\{\{#IF\s+(?P<negate>!?)(?P<name>[A-Z0-9_]+)\}\}(?P<body>.*?)\{\{/IF\}\}",
    re.DOTALL,
)
PLACEHOLDER_PATTERN = re.compile(r"\{\{(?P<name>[A-Z0-9_]+)\}\}")


class SDDConfig(TypedDict, total=False):
    project_name: str
    tech_stack: str
    domain: str
    year: str


def short_description(full_text: str, *, limit: int = 240) -> str:
    """Compress project.md into a single prompt-friendly sentence."""
    normalized = " ".join(full_text.split())
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[:limit].rstrip()}..."


def truthy(value: object) -> bool:
    """Interpret template values using simple prompt-friendly truthiness rules."""
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    lowered = str(value).strip().lower()
    return lowered not in {"", "0", "false", "no", "none"}


def render_template(template: str, values: dict[str, object]) -> str:
    """Render placeholders and simple conditional blocks."""
    rendered = template

    while True:
        match = CONDITIONAL_PATTERN.search(rendered)
        if match is None:
            break
        flag_value = truthy(values.get(match.group("name"), ""))
        include_block = not flag_value if match.group("negate") == "!" else flag_value
        replacement = match.group("body") if include_block else ""
        rendered = f"{rendered[:match.start()]}{replacement}{rendered[match.end():]}"

    return PLACEHOLDER_PATTERN.sub(
        lambda matched: str(values.get(matched.group("name"), matched.group(0))),
        rendered,
    )


def discover_repo_snapshot(project_root: Path, *, max_depth: int = 2, max_entries: int = 40) -> str:
    """Generate a small tree to ground prompts without wasting tokens."""
    lines: list[str] = []

    def walk(path: Path, depth: int) -> None:
        if depth > max_depth or len(lines) >= max_entries:
            return

        entries = sorted(
            (
                entry
                for entry in path.iterdir()
                if entry.name not in IGNORED_DISCOVERY_NAMES
            ),
            key=lambda entry: (entry.is_file(), entry.name.lower()),
        )
        for entry in entries:
            if len(lines) >= max_entries:
                return
            prefix = "  " * depth
            label = f"{entry.name}/" if entry.is_dir() else entry.name
            lines.append(f"{prefix}- {label}")
            if entry.is_dir():
                walk(entry, depth + 1)

    walk(project_root, 0)
    if not lines:
        return "- <no repo files detected beyond .sdd>"
    if len(lines) >= max_entries:
        lines.append("- ...")
    return "\n".join(lines)


def build_progress_summary(project_root: Path, sdd_dir: Path) -> str:
    """Summarize current SDD state for prompt grounding."""
    backlog_paths = resolve_backlog_paths(sdd_dir)
    open_count = (
        len(sorted(backlog_paths.open_dir.glob("*.md")))
        if backlog_paths.open_dir.exists()
        else 0
    )
    closed_count = (
        len(sorted(backlog_paths.closed_dir.glob("*.md")))
        if backlog_paths.closed_dir.exists()
        else 0
    )
    best_practices_state = "present" if (sdd_dir / "best_practices.md").exists() else "missing"
    architect_state = "present" if (sdd_dir / "architect.md").exists() else "missing"
    summary_lines = [
        f"- project_root: {project_root}",
        f"- best_practices.md: {best_practices_state}",
        f"- architect.md: {architect_state}",
        f"- backlog_open_tickets: {open_count}",
        f"- backlog_closed_tickets: {closed_count}",
    ]
    return "\n".join(summary_lines)


def load_config(config_path: Path) -> SDDConfig:
    """Load .sdd/config.json with a typed fallback."""
    raw_text = config_path.read_text(encoding="utf-8")
    loaded = cast(SDDConfig, json.loads(raw_text))
    return loaded


def parse_args(argv: Sequence[str] | None) -> ArgumentParser:
    """Build the CLI parser for prompt generation."""
    parser = ArgumentParser(description="Render SDD prompts for a project root.")
    parser.add_argument("project_root", help="Project root containing .sdd/")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Render prompt templates into .sdd/prompts/."""
    parser = parse_args(argv)
    args = parser.parse_args(argv)

    project_root = Path(args.project_root).resolve()
    if not project_root.exists():
        parser.error(f"Project root not found: {project_root}")

    sdd_dir = ensure_sdd_dir(project_root)
    config_path = sdd_dir / "config.json"
    if not config_path.exists():
        parser.error(f"Missing config file: {config_path}")

    config = load_config(config_path)
    templates_dir = Path(__file__).resolve().parents[2] / "templates"
    prompts_dir = sdd_dir / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    project_md = read_text(sdd_dir / "project.md")
    repo_exists = has_repo_content(project_root)
    repo_snapshot = discover_repo_snapshot(project_root) if repo_exists else ""
    current_year = str(config.get("year", datetime.now().year))

    values: dict[str, object] = {
        "ADDITIONAL_CONTEXT": "",
        "ARCHITECTURE_REPLACEMENTS": "",
        "BACKLOG_CLOSED_PATH": ".sdd/backlog/closed",
        "BACKLOG_OPEN_PATH": ".sdd/backlog/open",
        "DOMAIN": config.get("domain", ""),
        "DOMAIN_REPLACEMENTS": "",
        "OBSERVABILITY_REPLACEMENTS": "",
        "PATH_REPLACEMENTS": "",
        "PROJECT_DESCRIPTION": short_description(project_md),
        "PROJECT_DESCRIPTION_CONTENT": project_md,
        "PROJECT_NAME": config.get("project_name", project_root.name),
        "PROJECT_ROOT": str(project_root),
        "QUALITY_REPLACEMENTS": "",
        "REPO_EXISTS": repo_exists,
        "REPO_SNAPSHOT": repo_snapshot,
        "SDD_PROGRESS_SUMMARY": build_progress_summary(project_root, sdd_dir),
        "SOURCE_PROMPT": "",
        "TECH_REPLACEMENTS": "",
        "TECH_STACK": config.get("tech_stack", ""),
        "TESTING_REPLACEMENTS": "",
        "YEAR": current_year,
    }

    mapping = [
        ("research_template.md", "01_research.prompt.md"),
        ("research_template_ui.md", "01b_research_ui.prompt.md"),
        ("architect_template.md", "02_architect.prompt.md"),
        ("architect_delta_template.md", "02b_architect_delta.prompt.md"),
        ("agent_template.md", "03_agent.prompt.md"),
        ("adapt_prompt.md", "99_adapt.prompt.md"),
    ]

    for template_name, output_name in mapping:
        template_path = templates_dir / template_name
        template = read_text(template_path)
        if not template:
            print(f"WARN  missing template: {template_path}")
            continue
        rendered = render_template(template, values).strip()
        (prompts_dir / output_name).write_text(f"{rendered}\n", encoding="utf-8")
        print(f"rendered {output_name}")

    print("done")
    return 0

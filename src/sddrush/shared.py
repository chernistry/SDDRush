from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

IGNORED_DISCOVERY_NAMES = {
    ".DS_Store",
    ".git",
    ".idea",
    ".pytest_cache",
    ".ruff_cache",
    ".sdd",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "venv",
}

STATUS_PATTERN = re.compile(r"^Status:\s*(?P<status>.+)$", re.MULTILINE)


@dataclass(frozen=True)
class BacklogPaths:
    open_dir: Path
    closed_dir: Path


def ensure_sdd_dir(project_root: Path) -> Path:
    """Return the .sdd directory or raise a helpful error."""
    sdd_dir = project_root / ".sdd"
    if not sdd_dir.is_dir():
        raise FileNotFoundError(
            f"{sdd_dir} was not found. Run `bin/sdd-init {project_root}` first."
        )
    return sdd_dir


def read_text(path: Path) -> str:
    """Read a UTF-8 text file and return an empty string when it does not exist."""
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""


def resolve_backlog_paths(sdd_dir: Path, *, create: bool = False) -> BacklogPaths:
    """Resolve the active backlog layout, preferring the v2 structure."""
    v2_paths = BacklogPaths(
        open_dir=sdd_dir / "backlog" / "open",
        closed_dir=sdd_dir / "backlog" / "closed",
    )
    legacy_paths = BacklogPaths(
        open_dir=sdd_dir / "backlog" / "tickets" / "open",
        closed_dir=sdd_dir / "backlog" / "tickets" / "closed",
    )
    if (
        v2_paths.open_dir.exists()
        or v2_paths.closed_dir.exists()
        or not legacy_paths.open_dir.exists()
    ):
        active_paths = v2_paths
    else:
        active_paths = legacy_paths

    if create:
        active_paths.open_dir.mkdir(parents=True, exist_ok=True)
        active_paths.closed_dir.mkdir(parents=True, exist_ok=True)

    return active_paths


def slugify(value: str) -> str:
    """Convert a title into a simple kebab-case slug."""
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    return normalized.strip("-") or "ticket"


def extract_status(markdown: str) -> str:
    """Read the ticket status line, defaulting to open."""
    match = STATUS_PATTERN.search(markdown)
    if match is None:
        return "open"
    return match.group("status").strip() or "open"


def replace_status(markdown: str, status: str) -> str:
    """Replace the ticket status line or inject one below the title."""
    if STATUS_PATTERN.search(markdown):
        return STATUS_PATTERN.sub(f"Status: {status}", markdown, count=1)

    lines = markdown.splitlines()
    if not lines:
        return f"Status: {status}\n"
    if lines[0].startswith("# "):
        return "\n".join([lines[0], f"Status: {status}", *lines[1:]])
    return f"Status: {status}\n{markdown}"


def extract_section(markdown: str, heading: str) -> str:
    """Extract the body of a markdown section by heading text."""
    lines = markdown.splitlines()
    target = f"## {heading}"
    collecting = False
    collected: list[str] = []

    for line in lines:
        if line.strip() == target:
            collecting = True
            continue
        if collecting and line.startswith("## "):
            break
        if collecting:
            collected.append(line)

    return "\n".join(collected).strip()


def extract_bullets(markdown: str, heading: str) -> list[str]:
    """Return bullet items from a markdown section."""
    section = extract_section(markdown, heading)
    bullets: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
    return bullets


def extract_agent_notes(markdown: str) -> str:
    """Preserve free-form agent notes across ticket syncs."""
    return extract_section(markdown, "Agent Notes")


def has_repo_content(project_root: Path) -> bool:
    """Report whether the project root contains real repo files beyond .sdd/noise."""
    for entry in sorted(project_root.iterdir()):
        if entry.name in IGNORED_DISCOVERY_NAMES:
            continue
        return True
    return False


from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_script(
    script_name: str,
    *args: str,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a repository script and return the captured result."""
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "bin" / script_name), *args],
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )


def run_bash_script(
    script_name: str,
    *args: str,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a bash repository script and return the captured result."""
    return subprocess.run(
        ["bash", str(REPO_ROOT / "bin" / script_name), *args],
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )


def make_project(tmp_path: Path) -> Path:
    """Create a minimal SDD project for CLI tests."""
    project_root = tmp_path / "demo"
    (project_root / ".sdd").mkdir(parents=True)
    (project_root / ".sdd" / "config.json").write_text(
        textwrap.dedent(
            """\
            {
              "project_name": "demo",
              "tech_stack": "Python/FastAPI",
              "domain": "legal",
              "year": "2026"
            }
            """
        ),
        encoding="utf-8",
    )
    (project_root / ".sdd" / "project.md").write_text(
        "# Project Description\n\nShip an agent-first workflow.\n",
        encoding="utf-8",
    )
    return project_root


def test_sdd_prompts_renders_xml_flow_with_repo_context(tmp_path: Path) -> None:
    """Prompt rendering should resolve conditionals and ground prompts in the repo."""
    project_root = make_project(tmp_path)
    (project_root / "src").mkdir()
    (project_root / "src" / "app.py").write_text(
        "def main() -> None:\n    pass\n",
        encoding="utf-8",
    )

    run_script("sdd-prompts", str(project_root))

    architect_prompt = (project_root / ".sdd" / "prompts" / "02_architect.prompt.md").read_text(
        encoding="utf-8"
    )
    agent_prompt = (project_root / ".sdd" / "prompts" / "03_agent.prompt.md").read_text(
        encoding="utf-8"
    )

    assert "<prompt>" in architect_prompt
    assert "<repo_exists>true</repo_exists>" in architect_prompt
    assert "- src/" in architect_prompt
    assert "{{#IF" not in architect_prompt
    assert ".sdd/backlog/open" in agent_prompt
    assert "python bin/sdd-backlog janitor" in agent_prompt


def test_sdd_init_scaffolds_research_pack_templates(tmp_path: Path) -> None:
    """Init should scaffold a research packs directory with reusable templates."""
    project_root = tmp_path / "demo-init"

    run_bash_script(
        "sdd-init",
        str(project_root),
        "--stack",
        "Python/FastAPI",
        "--domain",
        "legal",
        "--year",
        "2026",
    )

    researches_readme = project_root / ".sdd" / "researches" / "README.md"
    closeout_template = (
        project_root
        / ".sdd"
        / "researches"
        / "_templates"
        / "research_closeout_template.md"
    )

    assert researches_readme.exists()
    assert "Research Packs" in researches_readme.read_text(encoding="utf-8")
    assert closeout_template.exists()


def test_sdd_backlog_sync_writes_open_tickets_from_architect_xml(tmp_path: Path) -> None:
    """Structured architect output should produce canonical ticket files."""
    project_root = make_project(tmp_path)
    (project_root / ".sdd" / "architect.md").write_text(
        textwrap.dedent(
            """\
            # Architecture Spec

            ## ADR Log
            - ADR-001 Use XML ticket appendix

            ## Machine-Readable Backlog Appendix
            <tickets>
              <ticket>
                <id>01</id>
                <slug>bootstrap-flow</slug>
                <title>Bootstrap prompt flow</title>
                <type>feature</type>
                <summary>Set up the new prompt workflow.</summary>
                <depends_on />
                <spec_refs>
                  <item>ADR-001</item>
                </spec_refs>
                <objective>Generate the new backlog bootstrap.</objective>
                <definition_of_done>
                  <item>Ticket sync works.</item>
                </definition_of_done>
                <steps>
                  <item>Render prompt updates.</item>
                  <item>Sync tickets.</item>
                </steps>
                <affected_paths>
                  <item>templates/architect_template.md</item>
                </affected_paths>
                <tests>
                  <item>pytest tests/test_cli_flow.py</item>
                </tests>
                <risks>
                  <item>XML appendix drifts from schema.</item>
                </risks>
                <janitor_signals>
                  <item>path_exists: templates/architect_template.md</item>
                </janitor_signals>
              </ticket>
            </tickets>
            """
        ),
        encoding="utf-8",
    )

    run_script("sdd-backlog", "sync", str(project_root))

    ticket_path = project_root / ".sdd" / "backlog" / "open" / "01-bootstrap-flow.md"
    ticket_markdown = ticket_path.read_text(encoding="utf-8")

    assert ticket_path.exists()
    assert "Status: open" in ticket_markdown
    assert "## Janitor Signals" in ticket_markdown
    assert "path_exists: templates/architect_template.md" in ticket_markdown


def test_sdd_backlog_janitor_moves_ticket_when_signals_pass(tmp_path: Path) -> None:
    """Janitor should close tickets whose file-based completion signals are satisfied."""
    project_root = make_project(tmp_path)
    open_dir = project_root / ".sdd" / "backlog" / "open"
    closed_dir = project_root / ".sdd" / "backlog" / "closed"
    open_dir.mkdir(parents=True)
    closed_dir.mkdir(parents=True)
    (project_root / "src").mkdir()
    (project_root / "src" / "done.py").write_text(
        "def finished() -> None:\n    pass\n",
        encoding="utf-8",
    )
    (open_dir / "01-close-me.md").write_text(
        textwrap.dedent(
            """\
            # Ticket: 01 Close me
            Status: in_progress
            Type: feature
            Slug: close-me
            Depends on: none
            Spec refs: ADR-001
            Source: .sdd/architect.md

            ## Janitor Signals
            - path_exists: src/done.py
            - path_contains: src/done.py :: def finished(
            """
        ),
        encoding="utf-8",
    )

    run_script("sdd-backlog", "janitor", str(project_root))

    assert not (open_dir / "01-close-me.md").exists()
    closed_ticket = (closed_dir / "01-close-me.md").read_text(encoding="utf-8")
    assert "Status: closed" in closed_ticket


def test_sdd_status_reports_progress_and_latest_adrs(tmp_path: Path) -> None:
    """Status output should summarize counts and recent ADRs."""
    project_root = make_project(tmp_path)
    open_dir = project_root / ".sdd" / "backlog" / "open"
    closed_dir = project_root / ".sdd" / "backlog" / "closed"
    open_dir.mkdir(parents=True)
    closed_dir.mkdir(parents=True)
    (project_root / ".sdd" / "architect.md").write_text(
        textwrap.dedent(
            """\
            # Architecture Spec

            ## ADR Log
            - ADR-001 Keep prompts XML-first
            - ADR-002 Use machine-readable ticket appendix
            """
        ),
        encoding="utf-8",
    )
    (open_dir / "01-open.md").write_text(
        "# Ticket: 01 Open\nStatus: open\n",
        encoding="utf-8",
    )
    (closed_dir / "02-closed.md").write_text(
        "# Ticket: 02 Closed\nStatus: closed\n",
        encoding="utf-8",
    )

    result = run_script("sdd-status", str(project_root))

    assert "tickets: total=2 open=1 closed=1 done=50.0%" in result.stdout
    assert "ADR-002 Use machine-readable ticket appendix" in result.stdout

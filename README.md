# SDDRush

Minimal, pragmatic toolkit for Spec-Driven Development with prompts and lightweight automation designed for 2026 AI agents.

## Why

- Faster setup for any task with a consistent SDD flow.
- Prompts are optimized for tool-using agents, not manual prompt babysitting.
- Backlog creation and cleanup are scriptable instead of copy-paste heavy.
- Works with CLI and IDE agents such as Codex, Cursor, Windsurf, Gemini, and similar tools.

## Agent-First Flow

```mermaid
flowchart LR
  A[Task] --> B[.sdd/project.md]
  B --> C[Research]
  C --> D[Architecture]
  D --> E["<tickets> appendix"]
  E --> F[backlog/open]
  F --> G[Agent]
  G --> H[backlog/closed]
```

SDDRush keeps the original research -> architect -> agent sequence, but removes the fragile manual loop. The core shift is simple: prompts assume the agent can read and write the repo directly, keep backlog files in sync, and use MCP only when local context is insufficient.

## Quick Start

1. Initialize inside a project directory.
   `bash bin/sdd-init /path/to/project --stack "Python/FastAPI" --domain "legal"`
2. Describe the work in `.sdd/project.md`.
3. Render prompts.
   `python bin/sdd-prompts /path/to/project`
4. Run research and write the result to `.sdd/best_practices.md`.
5. Run architecture and write the result to `.sdd/architect.md`.
   The architect prompt ends with a machine-readable `<tickets>` appendix.
6. Sync the appendix into real ticket files.
   `python bin/sdd-backlog sync /path/to/project`
7. Run the implementation agent against `.sdd/backlog/open/`.
8. Run janitor and status.
   `python bin/sdd-backlog janitor /path/to/project`
   `python bin/sdd-status /path/to/project`

## What Changed In 2.0

- Prompts are XML-structured, so role, context, constraints, and output contracts are easier for agents to parse.
- Research and architecture prompts explicitly require internal MCDM/ADR reasoning before final output, but expose only compact decision artifacts.
- The architect prompt emits a `<tickets>` appendix, so ticket creation is scriptable instead of manual.
- The agent prompt assumes file tools and MCP access, and tells the agent exactly which repo files to update.
- Ticket files include `Janitor Signals`, which lets a lightweight script close tickets from concrete repo evidence.
- `sdd-prompts` now supports simple conditionals and repo-aware grounding via a compact repo snapshot.

## Working Files

- `.sdd/project.md`: task description and Definition of Done.
- `.sdd/best_practices.md`: research brief.
- `.sdd/architect.md`: architecture spec and XML backlog appendix.
- `.sdd/backlog/open/`: active tickets.
- `.sdd/backlog/closed/`: completed tickets.
- `.sdd/context/`: receipts from MCP, docs, schemas, benchmarks, or operational notes.
- `.sdd/issues.md`: conflicts, blockers, and missing decisions.

## Templates

- `templates/research_template.md`: evidence-backed research brief with 2026 defaults, verification recipes, and ADR candidates.
- `templates/architect_template.md`: architecture spec with repo discovery, decision matrix, ADR log, and machine-readable tickets.
- `templates/agent_template.md`: implementing agent workflow with direct file access, MCP guidance, and backlog hygiene rules.
- `templates/ticket_template.md`: canonical open/closed ticket format with janitor signals.
- `templates/architect_delta_template.md`: surgical change prompt for updating an existing spec.
- `templates/adapt_prompt.md`: 1:1 prompt adaptation template between stacks and domains.

## Scripts

- `bin/sdd-init`: scaffold `.sdd/`, backlog directories, context receipts, and issue log.
- `bin/sdd-prompts`: render prompts with project context, conditional blocks, and repo snapshot grounding.
- `bin/sdd-backlog sync`: convert the architect `<tickets>` appendix into `.md` files in `.sdd/backlog/open/`.
- `bin/sdd-backlog janitor`: move completed tickets into `.sdd/backlog/closed/` when janitor signals pass.
- `bin/sdd-status`: print total tickets, percent done, and latest ADRs.

## Notes

- You can re-run `bin/sdd-prompts` anytime; it refreshes prompts using the latest repo context.
- Automation is intentionally small. The toolkit stays prompt-first and agent-first, not framework-heavy.
- If an agent has MCP access, store durable external receipts in `.sdd/context/` so the next agent does not repeat the same discovery.

## License

MIT

## Tags

spec-driven-development, prompt-engineering, ai-agents, software-architecture, templates, research, best-practices, automation, cli-tools, llm, developer-tools, engineering-workflows, multi-agent-systems, decision-making, mcdm

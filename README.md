# SDDRush — Spec‑Driven Development, fast

Minimal, pragmatic toolkit to kick off Spec‑Driven Development (SDD) with prompt templates and tiny scripts. Keep the core simple, automate the boring parts.

## Why
- Faster setup for any task with a consistent SDD flow
- High‑quality prompts (research, architect, agent) with coding rules integrated into architect.md
- Works with your favorite CLI agents (Q, Qwen, Codex, Gemini, Cursor)

## Flow
```mermaid
flowchart LR
  A[Task] --> B[Description]
  B --> C[Research]
  C --> D[Architecture (+ Coding Rules)]
  D --> E[Agent]
  E --> F[Tickets]
  F --> G[Code]
```

## Quick Start (recommended: single‑project mode)
- Initialize inside a project directory
  - `bash bin/sdd-init /path/to/project --stack "Node.js/Web Audio API" --domain audio`
- Write the description
  - Edit `/path/to/project/.sdd/project.md`
- Render prompts
  - `python bin/sdd-prompts /path/to/project`
- Run in your agent
  - `01_research` → paste to `.sdd/best_practices.md`
  - Re‑render → `02_architect` → paste to `.sdd/architect.md` (includes coding standards & backlog tickets)
  - Re‑render → `03_agent` → implement tickets in `backlog/open/`

## Templates
- `templates/research_template.md` — evidence‑based best practices ({{YEAR}})
- `templates/architect_template.md` — Architecture, code standards, ADRs, SLOs, MCDM for major choices
- `templates/agent_template.md` — implementing agent with file references
- `templates/adapt_prompt.md` — 1:1 prompt rewrites between stacks/domains

## Notes
- You can re‑run `bin/sdd-prompts` anytime — it updates prompts with latest context.
- Agent prompt uses file references instead of inlining content — saves tokens, agent reads what it needs.
- Web search stays manual by design; paste results into files.


## License
MIT

## Tags
spec-driven-development, prompt-engineering, ai-agents, software-architecture, templates, research, best-practices, automation, cli-tools, llm, developer-tools, engineering-workflows, multi-agent-systems, decision-making, mcdm

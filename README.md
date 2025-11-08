# SDDRush — Spec‑Driven Development, fast

Minimal, pragmatic toolkit to kick off Spec‑Driven Development (SDD) with prompt templates and tiny scripts. Keep the core simple, automate the boring parts.

## Why
- Faster setup for any task with a consistent SDD flow
- High‑quality prompts (task solver, research, architect, coding rules, agent)
- Works with your favorite CLI agents (Q, Qwen, Codex, Gemini, Cursor)

## Flow
```mermaid
flowchart LR
  A[Task] --> B[Description]
  B --> C[Research]
  C --> D[Architecture]
  D --> E[Coding Rules]
  E --> F[Agent]
  F --> G[Tickets]
  G --> H[Code]
```

## Quick Start
- Scaffold a task
  - `bash bin/sdd-scaffold my-website --stack "Python/FastAPI" --domain web`
- Write the description
  - Edit `tasks/my-website/input/project.md`
- Render prompts
  - `python bin/sdd-prompts tasks/my-website`
- Run in your agent
  - Use `prompts/00_task_solver.prompt.md` (or `00_solution_ideation`) → `spec/solution_plan.md`
  - `01_research` → paste to `research/best_practices.md`
  - Re‑render → `02_architect` → `spec/architect.md`
  - `03_coding_rules` → `spec/coding_rules.md`
  - Re‑render → `04_agent` → `agent/agent.md` (optional)

## Templates
- `templates/task_solver_template.md` — solution designer with MCDM step
- `templates/solution_ideation_template.md` — alternatives→recommendation, verification
- `templates/research_template.md` — evidence‑based best practices ({{YEAR}})
- `templates/architect_template.md` — ADRs, SLOs, and MCDM table for major choices
- `templates/coding_rules_template.md` — concrete commands/configs
- `templates/agent_template.md` — implementing agent with inline context
- `templates/adapt_prompt.md` — 1:1 prompt rewrites between stacks/domains

## Notes
- You can re‑run `bin/sdd-prompts` anytime — it inlines latest context into the agent prompt.
- Web search stays manual by design; paste results into files.

## License
MIT

## Tags
spec-driven-development, prompt-engineering, ai-agents, software-architecture, templates, research, best-practices, automation, cli-tools, llm, developer-tools, engineering-workflows, multi-agent-systems, decision-making, mcdm


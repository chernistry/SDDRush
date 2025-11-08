# SDD (Spec‑Driven Development) — minimal algorithm and starter

Goal: minimize manual steps without over‑engineering. This repo provides only what’s needed plus light automation to generate prompts.

Core chain:
Task → Description → Research → Architecture → Rules → Agent → Tickets → Code

Automate: prompt generation and file structure. Manual: web research (browser), running prompts in your preferred CLI agent (Q, Qwen, Codex, Gemini, Cursor), pasting outputs into files.

—

What’s here
- `templates/`: simple prompt templates (task solver, ideation, research, architect, coding rules, agent, adapt).
- `bin/sdd-init`: initialize Single‑Project SDD in an existing project dir.
- `bin/sdd-prompts`: render ready‑to‑paste prompts with context substitution.
- (Legacy) `bin/sdd-scaffold`: scaffold a task in `tasks/<task>`.

Minimal single‑project structure
```
.sdd/
├── config.json                # name, stack, domain, year
├── project.md                 # short description (manual)
├── best_practices.md          # research result (manual paste)
├── architect.md               # final architecture (includes Backlog)
├── coding_rules.md            # final rules
└── prompts/                   # prompts for each step

backlog/
├── open/                      # ticket files (created by Architect)
└── closed/
```

—

SDD algorithm (short)
0) Input task
- Manually write `tasks/<task>/input/project.md`.

1) Decide the solution (Task Solver / Ideation)
- Render prompts: `python bin/sdd-prompts /path/to/project`.
- Use `00_task_solver` or `00_solution_ideation` (optional plan only).

2) Research → Best Practices / Stack
- Open `01_research`, run in your AI, use the browser for sources.
- Paste the result to `.sdd/best_practices.md`.

3) Architect (also generates Backlog tickets)
- Re‑render: `python bin/sdd-prompts /path/to/project` (so architect/agent absorb best_practices).
- Open `02_architect`, run in AI.
- Paste to `.sdd/architect.md`. Create ticket files under `backlog/open/`.

4) Coding rules
- Open `03_coding_rules`, run in AI.
- Paste to `.sdd/coding_rules.md`.

5) Agent
- Re‑render: `python bin/sdd-prompts /path/to/project` — it inlines description, best practices, architecture, rules.
- Open `04_agent`, run in AI → implement tickets in `backlog/open/`.

6) Tickets (optional)
- From `spec/solution_plan.md` and `spec/architect.md`, build the backlog (manually or via AI) and execute.

—

Notes
- You can re‑run `python bin/sdd-prompts` anytime — it inlines the latest best_practices/architect/coding_rules into the agent prompt.
- Use `templates/adapt_prompt.md` to quickly rewrite a template to a new stack/domain 1:1.

Done. Extend automation only when it pays off — keep the core simple.

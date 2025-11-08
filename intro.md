# SDD (Spec‑Driven Development) — minimal algorithm and starter

Goal: minimize manual steps without over‑engineering. This repo provides only what’s needed plus light automation to generate prompts.

Core chain:
Task → Description → Research → Architecture → Rules → Agent → Tickets → Code

Automate: prompt generation and file structure. Manual: web research (browser), running prompts in your preferred CLI agent (Q, Qwen, Codex, Gemini, Cursor), pasting outputs into files.

—

What’s here
- `templates/`: simple prompt templates (task solver, ideation, research, architect, coding rules, agent, adapt).
- `bin/sdd-scaffold`: scaffold a new task in `tasks/<task>`.
- `bin/sdd-prompts`: render ready‑to‑paste prompts with context substitution.

Minimal task structure
```
tasks/<task>/
├── config.json                # name, stack, domain, year
├── input/
│   └── project.md             # short description (manual)
├── research/
│   └── best_practices.md      # research result (manual paste)
├── spec/
│   ├── architect.md           # final architecture (manual paste)
│   └── coding_rules.md        # final rules (manual paste)
├── prompts/                   # prompts for each step
└── agent/
    └── agent.md               # assembled agent prompt (optional)
```

—

SDD algorithm (short)
0) Input task
- Manually write `tasks/<task>/input/project.md`.

1) Decide the solution (Task Solver / Ideation)
- Render prompts: `python bin/sdd-prompts tasks/<task>`.
- Use `prompts/00_task_solver.prompt.md` or `prompts/00_solution_ideation.prompt.md`.
- Save to `spec/solution_plan.md` (optional) — this seeds tickets.

2) Research → Best Practices / Stack
- Open `prompts/01_research.prompt.md`, run in your AI, use the browser for sources.
- Paste the result to `research/best_practices.md`.

3) Architect
- Re‑render: `python bin/sdd-prompts tasks/<task>` (so architect/agent absorb best_practices).
- Open `prompts/02_architect.prompt.md`, run in AI.
- Paste to `spec/architect.md`.

4) Coding rules
- Open `prompts/03_coding_rules.prompt.md`, run in AI.
- Paste to `spec/coding_rules.md`.

5) Agent
- Re‑render: `python bin/sdd-prompts tasks/<task>` — it inlines description, best practices, architecture, rules.
- Open `prompts/04_agent.prompt.md`, run in AI → if needed, save to `agent/agent.md`.

6) Tickets (optional)
- From `spec/solution_plan.md` and `spec/architect.md`, build the backlog (manually or via AI) and execute.

—

Notes
- You can re‑run `python bin/sdd-prompts` anytime — it inlines the latest best_practices/architect/coding_rules into the agent prompt.
- Use `templates/adapt_prompt.md` to quickly rewrite a template to a new stack/domain 1:1.

Done. Extend automation only when it pays off — keep the core simple.


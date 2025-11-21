# SDD (Spec‑Driven Development) — Optimized 3-Step Flow

**Goal**: Minimize manual steps and cognitive overhead. Research → Plan → Execute.

**Core chain**: Task → Research → Architecture (+ Coding Rules + Tickets) → Implementation

**Automate**: Prompt generation, file structure, progress tracking.  
**Manual**: Web research, running prompts in AI (ChatGPT/Claude/Q), pasting outputs.

---

## Document Hierarchy

```
project.md (project description)
    ↓
best_practices.md (industry knowledge, tech landscape)
    ↓
architect.md (architecture + coding rules + tickets)
    ↓
tickets (concrete implementation tasks)
```

### Reference Logic

**architect.md** references:
- `project.md` (project goals and constraints)
- `best_practices.md` (applies industry best practices to architecture)

**tickets** reference:
- `architect.md` (architecture, components, coding rules)
- NOT `best_practices.md` directly (already digested in architect.md)

**agent** reads:
- All files (project.md, best_practices.md, architect.md)
- Current ticket

### Separation of Concerns

- **best_practices.md** = reusable industry knowledge (can be reused across projects with same stack)
- **architect.md** = project-specific decisions (already incorporates best practices)
- **tickets** = implementation tasks following architect.md

This simplifies implementation: developers/agents read architect.md + ticket, without digging into best_practices.

---

## Single-Project Structure

```
.sdd/
├── config.json                # name, stack, domain, year
├── project.md                 # project description (manual)
├── best_practices.md          # research output (paste from AI)
├── architect.md               # architecture + coding rules + ADRs (paste from AI)
└── prompts/                   # generated prompts for each step
    ├── 01_research.prompt.md
    ├── 02_architect.prompt.md
    └── 03_agent.prompt.md

backlog/
├── open/                      # tickets created by architect
│   ├── 01-setup.md
│   ├── 02-api.md
│   └── ...
└── closed/                    # completed tickets
```

---

## Optimized SDD Flow (3 Steps)

### Step 0: Initialization

```bash
# Initialize SDD in your project
sdd-init -p /path/to/project --stack "Python/FastAPI" --domain "search"

# Describe your project in .sdd/project.md:
# - What the project does
# - Problems it solves
# - Goals, users, constraints, Definition of Done
```

### Step 1: Research (Industry Landscape)

```bash
# Generate prompts
python bin/sdd-prompts /path/to/project

# Copy 01_research.prompt.md to ChatGPT/Claude
# AI researches:
# - What's new in 2025 for your stack
# - Best practices for your domain
# - Architecture patterns
# - Tools, libraries, approaches

# Save result to .sdd/best_practices.md
```

### Step 2: Architect (Planning)

```bash
# Regenerate prompts (so architect sees best_practices.md)
python bin/sdd-prompts /path/to/project

# Copy 02_architect.prompt.md to ChatGPT/Claude
# AI creates:
# - Architecture (components, API, data model)
# - Coding rules (style, linters, tests, security)
# - ADRs (architectural decisions)
# - Tickets in backlog/open/ (numbered tasks with dependencies)

# Save result to .sdd/architect.md
# Create ticket files in backlog/open/01-setup.md, 02-api.md, etc.
```

### Step 3: Agent (Implementation)

```bash
# Regenerate prompts one last time
python bin/sdd-prompts /path/to/project

# Copy 03_agent.prompt.md to Q/Claude/Cursor
# AI:
# - Reads .sdd/project.md, best_practices.md, architect.md
# - Takes first ticket from backlog/open/
# - Implements it
# - Moves to backlog/closed/
# - Takes next ticket

# Work iteratively through tickets until completion
```

---

## What's Included

- **templates/**: Prompt templates (research, architect, agent, adapt)
- **bin/sdd-init**: Initialize SDD structure in existing project
- **bin/sdd-prompts**: Render ready-to-paste prompts with context substitution

---

## Notes

- Re-run `python bin/sdd-prompts` anytime to update prompts with latest context
- Agent prompt uses file references instead of inlining content (saves tokens)
- Web search stays manual by design; paste results into files
- Use `templates/adapt_prompt.md` to rewrite templates for different stacks/domains

---

## Why 3 Steps (Not 4)?

Previous flow had separate `coding_rules` step, which duplicated content from architect (testing, security, API contracts). Now coding rules are integrated into architect.md as a dedicated section, reducing redundancy and cognitive load.

**Before**: Research → Architect → Coding Rules → Agent  
**After**: Research → Architect (includes coding rules) → Agent

Keep the core simple. Extend automation only when it pays off.

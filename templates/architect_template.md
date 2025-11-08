# Architect Prompt Template (Improved)

Instruction for AI: based on the project description and best practices, prepare an implementation‑ready architecture specification.

Context:
- Project: {{PROJECT_NAME}}
- Description: {{PROJECT_DESCRIPTION}}
- Domain: {{DOMAIN}}
- Tech stack: {{TECH_STACK}}
- Year: {{YEAR}}
- Best practices (inlined below):

```md
{{BEST_PRACTICES_CONTENT}}
```

Task:
Produce architect.md as the source of truth for implementation.

Output Structure (Markdown):
## Goals & Non‑Goals
- Goals: [1–5]
- Non‑Goals: [1–5]

## Architecture Overview
- Diagram (text): components and connections
- Data schema (high‑level)
- External integrations

## Discovery (optional, if a repo is available)
- Map structure, entry points, integration boundaries, and cross‑cutting concerns.
- Identify dead code, high‑complexity modules, and extension points (minimal change surface).
- Output a short tree of key files and where your plan plugs in.

## MCDM for Major Choices
- Criteria: PerfGain, SecRisk, DevTime, Maintainability, Cost, Scalability, DX
- Weights: justify briefly (SMART/BWM)
- Alternatives table: scores 1–9 → normalize → TOPSIS rank
- Recommendation: pick highest closeness; note trade‑offs and rollback plan

### Decision Matrix (template)
| Alternative | PerfGain | SecRisk | DevTime | Maintainability | Cost | Scalability | DX | Notes |
|-------------|----------|---------|---------|-----------------|------|------------|----|-------|
| A           |          |         |         |                 |      |            |    |       |
| B           |          |         |         |                 |      |            |    |       |
| C           |          |         |         |                 |      |            |    |       |

## Key Decisions (ADR‑style)
- [ADR‑001] Choice with rationale (alternatives, trade‑offs)
- [ADR‑002] ...

## Components
- Component A: responsibility, interfaces, dependencies
- Component B: ...

## API Contracts
- Endpoint/Function → contract (input/output, errors)
- Versioning and compatibility

## Data Model
- Models/tables: fields, keys, indexes
- Migration policies

## Quality & Operations
- Testing strategy (unit/integration/e2e/perf/security)
- Observability (metrics/logs/traces, alerts)
- Security (authn/authz, secrets, data protection)
- CI/CD (pipeline, gates, rollbacks)

## Domain Doctrine & Grounding (optional)
- Grounding sources (DBs/APIs/files) and how to cite/verify.
- Policies & prohibitions (e.g., no heuristics for routing, scraping doctrine, robots/ToS).
- Receipts/verification discipline and provenance requirements.

## Affected Modules/Files (if repo is available)
- Files to modify → short rationale.
- Files to create → paths, responsibilities, and initial signatures.

## Implementation Steps
- Numbered, observable plan with concrete function names and signatures.
- Include timeouts, retries, validation, and error shapes.

## Backlog (Tickets)
- Break the work into tickets with clear dependencies and DoD.
- File structure:
  - Single‑project: `backlog/open/<nn>-<kebab>.md`
  - Legacy tasks/: `tasks/<name>/backlog/open/<nn>-<kebab>.md`
- Ticket format (each file):
  - Title, Objective, Acceptance Criteria (DoD)
  - Steps (concrete), Affected files, Tests, Risks
  - Dependencies: [ticket ids]

## Interfaces & Contracts
- API endpoints/functions: input/output schemas, error shapes, versioning.
- Compatibility strategy and migration notes.

## Stop Rules & Preconditions
- Go/No‑Go prerequisites (secrets, corpora, env flags, licenses).
- Conditions to halt and escalate (security/compliance conflicts, blocked dependencies).

## SLOs & Guardrails
- SLOs: latency/throughput/error rate
- Performance/Cost budgets and limits

Requirements
1) No chain‑of‑thought. Provide final decisions with brief, verifiable reasoning.
2) Be specific to {{TECH_STACK}} and up‑to‑date for {{YEAR}}; flag outdated items.

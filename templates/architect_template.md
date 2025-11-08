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

## MCDM for Major Choices
- Criteria: PerfGain, SecRisk, DevTime, Maintainability, Cost, Scalability, DX
- Weights: justify briefly (SMART/BWM)
- Alternatives table: scores 1–9 → normalize → TOPSIS rank
- Recommendation: pick highest closeness; note trade‑offs and rollback plan

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

## SLOs & Guardrails
- SLOs: latency/throughput/error rate
- Performance/Cost budgets and limits

Requirements
1) No chain‑of‑thought. Provide final decisions with brief, verifiable reasoning.
2) Be specific to {{TECH_STACK}} and up‑to‑date for {{YEAR}}; flag outdated items.

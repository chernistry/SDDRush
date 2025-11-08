# Coding Rules Template

Instruction for AI: produce pragmatic coding rules for the project.

Context:
- Project: {{PROJECT_NAME}}
- Stack: {{TECH_STACK}}
- Domain: {{DOMAIN}}
- Year: {{YEAR}}

Output Structure (concise and concrete):
## Language & Style
- Versions; linters/formatters; naming; typing rules

## Framework & Project Layout
- Folders/modules conventions; environment configs (dev/stage/prod)

## API & Contracts
- REST/GraphQL/gRPC style; error handling; versioning
- Input/output validation

## Testing
- Coverage targets; libraries; fixtures
- Unit/Integration/E2E/Perf/Security

## Security
- AuthN/AuthZ; secrets; dependencies; PII

## Observability
- Metrics/logs/traces; alerts; dashboards

## Performance & Cost
- Budgets; limits; profiling

## Git & PR Process
- Branching; commits; review checklists

## Tooling
- Formatters; linters; pre-commit; CI steps

Requirements
1) Provide concrete commands/flags/configs.
2) For {{TECH_STACK}} recommend specific libs with rationale.

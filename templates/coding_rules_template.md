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
- SSRF guards, input validation, signature verification
- Secrets management (env vars, secret stores, never in code/logs)
- Allowlists for external domains/APIs

## Resilience
- Explicit timeouts on all external calls (network, DB, APIs)
- Retry policies: exponential backoff + jitter, max attempts
- Circuit breakers for fragile integrations
- Rate limiting (per-user, per-endpoint)
- Idempotency keys for side-effects

## Observability
- Metrics/logs/traces; alerts; dashboards
- Structured logging (JSON, no secrets)
- Health endpoints (/healthz, /metrics)
- Correlation IDs across requests
- Performance budgets and monitoring

### Metric Naming Conventions (if applicable)
- Use descriptive names with units: `tool_latency_ms`, `requests_total`
- Labels for dimensions: `{tool=, status=, code=}`
- Avoid high-cardinality labels (no user IDs, timestamps in labels)
- Examples: `http_request_duration_seconds{method=,status=}`, `db_query_errors_total{table=,error_type=}`

## Performance & Cost
- Budgets; limits; profiling

## Git & PR Process
- Branching; commits; review checklists

## Tooling
- Formatters; linters; pre-commit; CI steps

## Commands
Provide concrete commands for common tasks:
```bash
# Format code
<format-command>

# Lint
<lint-command>

# Run tests
<test-command>

# Build
<build-command>

# Type check
<typecheck-command>
```

## Anti-Patterns (Do NOT do this)
- No timeouts/retries on external calls
- Hardcoded secrets, URLs, or configuration
- Silent error swallowing (empty catch blocks)
- Print statements instead of structured logging
- Missing tests for critical paths
- No idempotency for side-effects
- Mutable global state
- Circular dependencies
- Files >400 LOC without clear separation

## Configuration-Driven Policy
- All thresholds, limits, and environment-specific values must be configurable
- Use environment variables or config files (never hardcode)
- Document all configuration options with defaults and valid ranges
- Validate configuration on startup
- Examples: timeouts, rate limits, feature flags, API endpoints, batch sizes

## File Creation Policy
- Prefer in-memory operations and existing modules
- Create new files only for substantial, reusable functionality
- Organize by purpose:
  - Ephemeral/debug scripts → `debug/` or `scripts/`
  - Tests → `tests/` or `__tests__/`
  - Shared utilities → `utils/` or `lib/`
- Avoid file sprawl: consolidate related functionality
- Split files only when they exceed ~400 LOC or have distinct responsibilities

Requirements
1) Provide concrete commands/flags/configs.
2) For {{TECH_STACK}} recommend specific libs with rationale.

Optional Deep Sections (use when relevant)
## No-Heuristic Policy (for AI/LLM projects)
- No deterministic heuristics for ranking/selection (no keyword lists, domain hardcoding)
- No regex-based parsers for entities/slots/brands
- No local ML models (Transformers/NER) - use LLM or tool APIs
- No hardcoded prompt content - store in files, load dynamically
- Tool-first grounding: answers must cite tool outputs or stored receipts

## Frontend Standards
- Framework specifics (e.g., Next.js/SvelteKit): server/client components; data fetching; accessibility.
- Performance budgets (bundle sizes, Web Vitals); image/font optimization.

## Backend Standards
- Web framework conventions; schema validation; error shapes; retries/timeouts.
- Data modeling/migrations; background jobs; idempotency.

## Governance & Decisions (MCDM)
- For notable changes, run a lightweight MCDM with criteria {PerfGain, Maintainability, DevTime, Cost, Security, Scalability, DX}. Record the choice and rationale.

## Acceptance Criteria
- A short checklist mapping rules to verifiable checks (build, lint, tests, perf, security, docs).

## Acceptance Checklist (adapt to project)
- [ ] Code builds without errors
- [ ] Linter passes with no warnings
- [ ] All tests pass (unit, integration, e2e as applicable)
- [ ] Test coverage meets target (if defined)
- [ ] Security checks pass (no secrets in code, input validation present)
- [ ] Performance budgets met (if defined)
- [ ] Documentation updated (API docs, README, comments)
- [ ] Configuration externalized (no hardcoded values)
- [ ] Error handling covers expected failures
- [ ] Observability in place (logs, metrics where applicable)

## File Hygiene
- Create new files only for reusable functionality; remove dead code; split >400 LOC; avoid shared mutable state.

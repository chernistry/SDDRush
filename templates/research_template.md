# Best Practices Research Template (Improved)

Instruction for AI: produce a practical, evidence‑backed best practices guide tailored to this project and stack.

---

## Project Context
- Project: {{PROJECT_NAME}}
- Description: {{PROJECT_DESCRIPTION}}
- Tech stack: {{TECH_STACK}}
- Domain: {{DOMAIN}}
- Year: {{YEAR}}

## Task
Create a comprehensive best‑practices guide for {{PROJECT_NAME}} that is:
1) Current — relevant to {{YEAR}}; mark deprecated/outdated items.
2) Specific — tailored to {{TECH_STACK}} and {{DOMAIN}}.
3) Practical — include concrete commands/config/code.
4) Complete — cover architecture, quality, ops, and security.

## Output Structure (Markdown)
### 1. TL;DR (≤10 bullets)
- Key decisions and patterns (why, trade‑offs, MVP vs later)
- Observability posture; Security posture; CI/CD; Performance & Cost guardrails
- What changed in {{YEAR}}; SLOs summary

### 2. Landscape — What’s new in {{YEAR}}
For {{TECH_STACK}}:
- Standards/framework updates; deprecations/EOL; pricing changes
- Tooling maturity: testing, observability, security
- Cloud/vendor updates
- Alternative approaches and when to choose them

### 3. Architecture Patterns (2–4 for {{DOMAIN}} with {{TECH_STACK}})
Pattern A — [NAME] (MVP)
- When to use; Steps; Pros/Cons; Optional later features

Pattern B — [NAME] (Scale‑up)
- When to use; Migration from A

### 4. Priority 1 — [AREA]
Why → relation to goals and mitigated risks
Scope → In/Out
Decisions → with rationale and alternatives
Implementation outline → 3–6 concrete steps
Guardrails & SLOs → metrics and limits/quotas
Failure Modes & Recovery → detection→remediation→rollback

### 5–6. Priority 2/3 — [AREA]
Repeat the structure from 4.

### 7. Testing Strategy (for {{TECH_STACK}})
- Unit / Integration / E2E / Performance / Security
- Frameworks, patterns, coverage targets

### 8. Observability & Operations
- Metrics, Logging, Tracing, Alerting, Dashboards

### 9. Security Best Practices
- AuthN/AuthZ, Data protection (PII, encryption), Secrets, Dependency security
- OWASP Top 10 ({{YEAR}}) coverage; Compliance (if any)

### 10. Performance & Cost
- Budgets (concrete numbers), optimization techniques, cost monitoring, resource limits

### 11. CI/CD Pipeline
- Build/Test/Deploy; quality gates; environments

### 12. Code Quality Standards
- Style, linters/formatters, typing, docs, review, refactoring

### 13. Reading List (with dates and gists)
- [Source] (Last updated: YYYY‑MM‑DD) — gist

### 14. Decision Log (ADR style)
- [ADR‑001] [Choice] over [alternatives] because [reason]

### 15. Anti‑Patterns to Avoid
- For {{TECH_STACK}}/{{DOMAIN}} with “what, why bad, what instead”

### 16. Evidence & Citations
- List sources inline near claims; add links; include “Last updated” dates when possible.

### 17. Verification
- Self‑check: how to validate key recommendations (scripts, smoke tests, benchmarks)
- Confidence: [High/Medium/Low] per section

## Requirements
1) No chain‑of‑thought. Provide final answers with short, verifiable reasoning.
2) If browsing is needed, state what to check and why; produce a provisional answer with TODOs.
3) Keep it implementable today; prefer defaults that reduce complexity.

## Additional Context
{{ADDITIONAL_CONTEXT}}

---
Start the research now and produce the guide for {{PROJECT_NAME}}.

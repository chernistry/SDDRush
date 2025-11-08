# Solution Ideation Template (Improved)

Instruction for AI: craft a realistic solution and break it into a concise, verifiable plan without excessive deliberation.

Input:
- Project: {{PROJECT_NAME}}
- Description: {{PROJECT_DESCRIPTION}}
- Domain: {{DOMAIN}}
- Tech stack (if any): {{TECH_STACK}}
- Year: {{YEAR}}

Operating principles:
- Brevity and applicability: minimal fluff, maximum concrete steps.
- Plan → solution: start with a short plan (3–6 steps), then details.
- Hallucination control: flag uncertainty, propose checks.
- Verifiability: always add self‑check and Definition of Done.

Task:
1) Provide 2–3 solution alternatives with comparisons and trade‑offs.
2) Pick a default for MVP with rationale; outline scale‑up path.
3) Draft the Architecture Outline (components, data, integrations, NFRs/SLOs).
4) Split into Milestones and Backlog with brief DoD and dependencies.
5) List Risks/Unknowns/Assumptions and how to test them.

Output format (Markdown):
## Clarifying Questions (only if blocking)

## Assumptions & Constraints
- Acceptance Criteria / Definition of Done: [...]
- Constraints: timeline, environment, stack

## Alternatives
- A) [Name]: when; pros/cons; constraints
- B) [Name]: when; pros/cons; constraints
- C) [Optional]

## MCDM (optional but recommended)
- Criteria (PerfGain, SecRisk, DevTime, Maintainability, Cost, Scalability, DX) with weights (SMART/BWM)
- Score table 1–9; normalize; TOPSIS rank; brief rationale

## Recommendation
- MVP choice and why; scale‑up path; rollback plan

## Architecture Outline
- Components: [Component → purpose]
- Data/Stores: [models/tables/indexes]
- Integrations: [services, protocols]
- NFRs: SLOs/latency/throughput/availability

## Milestones
- M1: [goal, artifacts, DoD]
- M2: ...

## Backlog (Tickets)
- [T‑001] Short title — 1–2 sentences; dependency: [..]; DoD: [...]
- [T‑002] ...

## Verification
- Unit/Integration/E2E/Perf/Security: what/how to check
- Local checks with sample inputs/outputs

## Risks / Unknowns / Assumptions
- Risk: [what] → mitigation
- Unknown: [what] → how to test
- Assumption: [what] → how to confirm/refute

## References (optional)
- 1–4 authoritative links if they add value

Requirements:
- Be specific to {{YEAR}} with concrete steps and DoD; avoid genericities.
- Adapt examples and solutions to {{TECH_STACK}} (if provided).

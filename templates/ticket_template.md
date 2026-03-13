# Ticket Template (SDD 2.0)

Use this as the canonical structure for files in `.sdd/backlog/open/` and `.sdd/backlog/closed/`.

```markdown
# Ticket: <nn> <short-title>
Status: open
Type: feature
Slug: <kebab-slug>
Depends on: <comma-separated ids or none>
Spec refs: <comma-separated refs or none>
Source: .sdd/architect.md

## Summary
One short paragraph describing why this ticket exists.

## Objective & Definition of Done
Short objective paragraph.
- Observable completion condition 1
- Observable completion condition 2

## Steps
1. Concrete implementation step.
2. Concrete implementation step.
3. Concrete implementation step.

## Affected Paths
- path/to/file.ext
- path/to/other.ext

## Tests & Verification
- Command or test case.
- Smoke check, benchmark, or dashboard to inspect.

## Evidence Bundle (optional)
- `.sdd/researches/<pack>/run_manifest.md`
- `.sdd/researches/<pack>/closeout.md`

## Risks & Edge Cases
- Failure mode or edge case.

## Janitor Signals
- path_exists: path/to/file.ext
- path_contains: path/to/file.ext :: def important_symbol(

## Agent Notes
- Reserved for the implementing agent: progress, receipts, commands run, blockers.
```

Rules:
- Keep ids zero-padded so file ordering matches dependency order.
- Keep tickets agent-executable in one focused work session.
- Keep `Janitor Signals` concrete and machine-checkable.
- Use `Evidence Bundle` when the ticket depends on probes, benchmarks, or risky comparisons.
- Move completed tickets to `.sdd/backlog/closed/` with `Status: closed`.

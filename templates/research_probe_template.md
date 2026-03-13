# Bounded Probe

- label: `<short-run-label>`
- date: `<YYYY-MM-DD>`
- owner: `<agent-or-human>`
- related_ticket: `<ticket-id or none>`
- related_adr: `<ADR-id or none>`

## Hypothesis

State the smallest claim you are trying to verify.

## Scope

- target slice: `...`
- control slice: `...`
- excluded surfaces: `...`

## Guardrails

- What must not change while this probe runs
- What would make the probe invalid

## Success Gate

- Observable condition that would justify promotion

## Kill Gate

- Observable condition that should reject or hold the idea

## Commands

- Exact commands to run

## Output Artifacts

- `.sdd/researches/<pack>/probe.json`
- `.sdd/researches/<pack>/notes.md`

## Notes

- Record anomalies, blockers, or environment limits

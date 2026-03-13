# Run Manifest

- label: `<short-run-label>`
- hypothesis: `<one-line statement>`
- fingerprint: `<artifact or config fingerprint>`
- git_sha: `<commit>`
- git_branch: `<branch>`
- git_dirty: `<true|false>`
- owner: `<agent-or-human>`
- related_ticket: `<ticket-id or none>`

## Inputs

- dataset / corpus: `...`
- slice / cohort: `...`
- environment: `...`

## Models / Services / Dependencies

- `service-or-model-name`: `version or identifier`

## Touched Files

- `path/to/file.ext` sha256=`...`

## Commands

- `...`

## Output Artifacts

- `probe.json`
- `results.jsonl`
- `closeout.md`

## Reproduction Notes

- Anything required for another agent to replay the run safely

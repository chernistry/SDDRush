# Research Packs

Use `.sdd/researches/` for durable experiment and validation artifacts.

This directory is not for generic notes. It is for evidence bundles that justify a decision, reject an idea, or prove a risky claim.

## When to Create a Research Pack

- Benchmark or latency comparison
- Quality, accuracy, or grounding probe
- Migration safety check
- Ablation, A/B, or counterfactual comparison
- Risk validation before merge or release
- Any ticket whose recommendation depends on measured evidence rather than repo inspection alone

## Naming Convention

- `<ticket-id>_<slug>_<YYYY-MM-DD>/`
- `<topic>_<YYYY-MM-DD>/` if there is no ticket yet

Examples:

- `ticket12_cache_latency_probe_2026-03-13/`
- `reranker_tradeoff_2026-03-13/`

## Recommended Contents

- `run_manifest.md` for reproducibility
- `closeout.md` for the final recommendation
- Optional machine-readable outputs such as `probe.json`, `results.jsonl`, `table.csv`, `trace.json`
- Optional supporting notes such as `production_mimic.md`, `counterfactual.md`, or `ranking.md`

## Rules

- Keep raw outputs immutable once they have informed a decision.
- Record git sha, branch, dirty state, touched files, commands, datasets, and model/service choices.
- End each pack with a clear recommendation such as `promote`, `hold`, `reject`, `ship`, or `do_not_ship`.
- Link the pack from the ticket, ADR, or `.sdd/issues.md` entry that depends on it.
- Keep source receipts in `.sdd/context/`; keep measured evidence in `.sdd/researches/`.

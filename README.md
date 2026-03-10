# SDDRush

SDDRush is a small toolkit for Spec-Driven Development in agent-heavy workflows.
It keeps the loop short: define the work, render the prompts, sync the backlog, and let the agent do the typing.

## Quick Start

Initialize with `bash bin/sdd-init /path/to/project --stack "Python/FastAPI" --domain "legal"`, describe the work in `.sdd/project.md`, then render prompts with `python bin/sdd-prompts /path/to/project`.
From there the flow is research -> architecture -> backlog sync -> implementation -> janitor, using `bin/sdd-backlog` and `bin/sdd-status` to keep the repo honest.

## How It Works

SDDRush turns one vague task into a durable sequence of files: project brief, best practices, architecture, tickets, and closed-loop backlog state.
It is prompt-first, repo-aware, and intentionally light on ceremony because the ceremony tends to breed when left unsupervised.

## Perks

- Agent-first SDD flow without a large framework tax.
- Real scripts for init, prompt rendering, backlog sync, janitor, and status.
- Clean fit for repos that want structure without building a religion around it.

Built by Alex Chernysh — alex@hireex.ai

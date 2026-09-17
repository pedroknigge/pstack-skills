# Changelog

All notable changes to the **pstack-skills** pack.

Versioning: patch bumps `0.0.1` → `0.0.99`, then `0.1.0`.

## [Unreleased]

## [0.0.1] — 2026-09-17

First public port of the Cursor pstack plugin skills as an installable Agent Skills pack.

This GitHub repo is **Pedro Knigge's public port**. It is **not** published by poteto or Cursor. Skill bodies keep poteto/pstack meaning; this cut does not invent new skill verbs.

### Added

- Parent router `skills/pstack` (`name: pstack`, aliases `/pstack` `/ps`) listing every leaf and when to use it
- All 47 Desktop leaves under `skills/ps-<original-slug>/` with frontmatter `name:` matching the folder
- Internal skill invokes and sibling links rewritten to `ps-*` (e.g. `/how` → `/ps-how`, `the how skill` → `the ps-how skill`)
- Pack files: `README.md`, `LICENSE` (MIT, Copyright (c) 2026 Pedro Knigge), `VERSION`, `CHANGELOG.md`, `install.sh`, `AGENTS.md`
- Glance version on **every** `SKILL.md` (parent + 47 leaves): `description` starts with `v0.0.1`; `license: MIT`; `metadata.version: "0.0.1"`; `metadata.author: pedroknigge`. Stale-install sentence matches vibe-proof-auditor.
- HITL issue module: `scripts/ps-issue.sh` always targets `pedroknigge/pstack-skills` (never consumer origin). Documented in parent `SKILL.md` and `skills/pstack/references/issue.md`. Children draft only; leader confirms in the same turn.
- Sibling bridges (sensor, not fusion) under `skills/pstack/references/`: ArkGate, Orderfield, documentation-manager (reciprocal; live names `ps-architect` / `ps-figure-it-out` / parent `pstack`), vibe-proof-auditor. Parent announces `ArkGate|Orderfield|Docs|Vibe-proof: none|detected`. Optional `scripts/ps-detect-siblings.sh`.
- Stdlib HTML renderer `scripts/render-report.py` (also `skills/pstack/scripts/`). Parent and `ps-show-me-your-work` emit an `.html` twin when the user asks for a report / HTML / dashboard. No invented scores.
- Dogfood → backlog → release cycle: `docs/dogfood-cycle.md`, parent triggers (`dogfood` / `blindtest` / `probar pstack en un repo random`), `evals/` planted-vs-live stub. Issue labels: `dogfood`, `blindtest`, `bug`, `enhancement` (repeatable `--label`).

### Notes

- Primary install path: `npx skills add pedroknigge/pstack-skills -g -y`
- `./install.sh` copies every `skills/*` folder into detected agent skill dirs (Claude, Grok, Cursor / `~/.agents/skills`, Gemini/AGY when present)
- Registry publish is not part of this cut

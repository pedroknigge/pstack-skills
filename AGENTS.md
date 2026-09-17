# AGENTS.md — pstack-skills (skill pack)

**Status:** first public cut · pack version **0.0.1**

## What this folder is

This workspace is the **source repository for the pstack-skills Agent Skills pack**.

| This repo **is** | This repo **is not** |
|------------------|----------------------|
| Public port of Cursor pstack plugin leaves as installable skills | The official poteto / Cursor pstack plugin |
| Parent router `skills/pstack` + 47 `skills/ps-*` leaves | A product app that consumes the pack |
| What gets installed via `npx skills add` or `./install.sh` | A place to invent new pstack verbs |

When working here, assume you are **authoring or shipping the pack**, not running poteto-mode against an unrelated product unless the user explicitly asks to dogfood.

## Layout

```
pstack-skills/                 ← this git root
├── AGENTS.md                  ← this hub
├── README.md                  ← human-facing install
├── LICENSE                    ← MIT, Pedro Knigge 2026
├── VERSION                    ← 0.0.1
├── CHANGELOG.md
├── install.sh                 ← copies skills/* into agent skill dirs
├── docs/                      ← dogfood-cycle.md
├── evals/                     ← planted vs live dogfood scaffold
├── scripts/                   ← ps-issue.sh, render-report.py, detect
└── skills/
    ├── pstack/SKILL.md        ← parent router (/pstack, /ps)
    ├── pstack/references/     ← issue HITL + sibling bridges
    ├── pstack/scripts/        ← same helpers (npx skills add ships these)
    └── ps-<slug>/             ← one Desktop leaf each
```

`.agents/` is a local host copy (gitignored). Edit `skills/`, then reinstall if hosts need the copy.

## Instructions for AI agents

1. Read this hub and `skills/pstack/SKILL.md` before changing pack behavior.
2. Do **not** invent new skill verbs or rewrite poteto/pstack meaning.
3. Leaf folder names and frontmatter `name:` must stay `ps-<original-slug>`. Parent stays `pstack`.
4. Every `SKILL.md` `description` starts with `v0.0.1` (e.g. `v0.0.1. …` or `v0.0.1 — …`) and includes `license: MIT` plus `metadata.version: "0.0.1"` / `metadata.author: pedroknigge`. If the leading version is not the latest in `VERSION` / changelog, update the skill before using it.
5. Internal cross-refs to other leaves use `ps-*` (`/ps-how`, the `ps-why` skill, `../ps-principle-…/`). Keep Cursor built-ins (`/create-skill`, `/loop`) and `cursor-team-kit` (`/deslop`) unprefixed.
6. Role labels in `ps-setup-pstack` (`how explorer`, `why synthesizer`, …) are config keys, not skill invokes — leave them.
7. Keep `README.md`, `install.sh`, `VERSION`, and `CHANGELOG.md` aligned when the pack surface changes. Bumping the pack version means `VERSION`, every `description` prefix, every `metadata.version`, changelog, and README together.
8. Do not force-push `main`. Do not publish to a skills registry unless the user asks.
9. Pack self-telemetry uses `scripts/ps-issue.sh` → **always** `pedroknigge/pstack-skills`. Never consumer origin. Never `gh issue create` without explicit human confirmation in the same turn. Children (`PS_CHILD` / `OF_CHILD`) draft only.
10. Sibling bridges under `skills/pstack/references/` are sensors: detect + HITL-propose. Do not vendor ArkGate, Orderfield, documentation-manager, or vibe-proof-auditor bodies. Announce `ArkGate|Orderfield|Docs|Vibe-proof: none|detected`.
11. HTML reports: `scripts/render-report.py` styles existing markdown/TSV. Do not invent scores. Emit an `.html` twin when the user asks for a report / HTML / dashboard and Python stdlib is available.
12. Dogfood / blindtest is a parent-router pass, not a new leaf. Public third-party repos only. Backlog via the issue module (HITL) with labels `dogfood`, `blindtest`, `bug`, `enhancement`. Then implement, bump `VERSION`, dogfood again. See [docs/dogfood-cycle.md](docs/dogfood-cycle.md).

## How to use the pack (when invoked)

- User says `/pstack` or `/ps` and has not named a leaf → read `skills/pstack/SKILL.md` and pick one child.
- User names a leaf (`/ps-poteto-mode`, `/ps-how`, a principle, …) → read that leaf's `SKILL.md` in full and follow it.
- Default for non-trivial work → `ps-poteto-mode`.
- Configure models → `ps-setup-pstack`.
- “report this to pstack” / “sugerí mejora al skill” / “file a pstack issue” → [skills/pstack/references/issue.md](skills/pstack/references/issue.md), not a new leaf.
- “dogfood” / “blindtest” / “probar pstack en un repo random” → [skills/pstack/references/dogfood.md](skills/pstack/references/dogfood.md).
- Report / HTML / dashboard → write markdown (or the `ps-show-me-your-work` TSV), then `scripts/render-report.py`.

## Navigation

- Parent router: [skills/pstack/SKILL.md](skills/pstack/SKILL.md)
- Issue HITL: [skills/pstack/references/issue.md](skills/pstack/references/issue.md)
- Dogfood cycle: [docs/dogfood-cycle.md](docs/dogfood-cycle.md)
- Bridges: [skills/pstack/references/](skills/pstack/references/)
- Install: [README.md](README.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)

## Attribution

Upstream is the Cursor pstack plugin. This GitHub repo is Pedro Knigge's public port, not a poteto or Cursor release.

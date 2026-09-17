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
└── skills/
    ├── pstack/SKILL.md        ← parent router (/pstack, /ps)
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

## How to use the pack (when invoked)

- User says `/pstack` or `/ps` and has not named a leaf → read `skills/pstack/SKILL.md` and pick one child.
- User names a leaf (`/ps-poteto-mode`, `/ps-how`, a principle, …) → read that leaf's `SKILL.md` in full and follow it.
- Default for non-trivial work → `ps-poteto-mode`.
- Configure models → `ps-setup-pstack`.

## Navigation

- Parent router: [skills/pstack/SKILL.md](skills/pstack/SKILL.md)
- Install: [README.md](README.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)

## Attribution

Upstream is the Cursor pstack plugin. This GitHub repo is Pedro Knigge's public port, not a poteto or Cursor release.

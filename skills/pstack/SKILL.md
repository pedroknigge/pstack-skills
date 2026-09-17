---
name: pstack
description: "v0.0.1. Parent router for the pstack-skills pack. Use for /pstack, /ps, or when you need to pick which pstack leaf to run. Lists every ps-* skill and when to use it. Also use when the user says report this to pstack, file a pstack issue, sugerí mejora al skill, dogfood, blindtest, probar pstack en un repo random, or asks for a pstack report / HTML / dashboard. Public port of the Cursor pstack plugin; this GitHub repo is not published by poteto or Cursor. If the leading version is not the latest in VERSION / changelog, update the skill before using it."
license: MIT
metadata:
  version: "0.0.1"
  author: pedroknigge
---

# pstack

Parent router for this pack. Aliases: `/pstack`, `/ps`.

This repo is a **public port** of the **Cursor pstack plugin** (not an official GitHub repo from poteto or Cursor). Leaf skills keep poteto/pstack meaning and live under `ps-*` so they do not collide with other skill names.

Do not invent new skill verbs. Pick an existing leaf and read its `SKILL.md` in full before acting.

## When to use the parent

Use `/pstack` or `/ps` when:

- you know you want pstack rigor but not which leaf
- you are new to the pack and need the catalog
- a request names several jobs (understand, design, verify, write) and you need an order

If the user already named a leaf (`/ps-how`, `/ps-poteto-mode`, `/ps-setup-pstack`, a principle, …), run that leaf. Do not re-route through this parent first.

If the request is pack telemetry (“report this to pstack”, “sugerí mejora al skill”, “file a pstack issue”), skip the catalog and follow [references/issue.md](references/issue.md). If they said “dogfood”, “blindtest”, or “probar pstack en un repo random”, skip the catalog and follow [references/dogfood.md](references/dogfood.md). If they asked for a report / HTML / dashboard, follow **HTML reports** below.

## Session announce

When this parent (or a leaf that needs siblings) runs, print sensor lines. Do not invent green. Missing stays Missing.

```text
ArkGate: none|detected
Orderfield: none|detected
Docs: none|detected
Vibe-proof: none|detected
```

`scripts/ps-detect-siblings.sh` (also `skills/pstack/scripts/ps-detect-siblings.sh`) is the optional sensor. If a line is `detected` **and** the work is relevant, read the matching bridge and HITL-propose. **No silent auto-run.** Do not vendor sibling bodies.

| Bridge | Note |
|---|---|
| [references/arkgate-bridge.md](references/arkgate-bridge.md) | Ark signals (`ark.config.json`, ark-check, ark skills). Fold with HITL. Do not rewrite `ark.config.json`. |
| [references/orderfield-bridge.md](references/orderfield-bridge.md) | `of` / `.orderfield` pairing only. Never consumer-origin issues. Orderfield self-telemetry stays on orderfield. |
| [references/documentation-manager-bridge.md](references/documentation-manager-bridge.md) | Docs sibling. Reciprocal to their `pstack-bridge.md`. Live names here: `ps-architect` / `ps-figure-it-out` / parent `pstack`. |
| [references/vibe-proof-bridge.md](references/vibe-proof-bridge.md) | Auditor sibling. Propose/fold findings. Do not copy checklist or scoring. |

### Related skills

- [ArkGate](https://github.com/pedroknigge/arkgate) (+ addons) — architecture-contract sibling
- [Orderfield](https://github.com/pedroknigge/orderfield) — field kernel / `of` CLI
- [documentation-manager](https://github.com/pedroknigge/documentation-manager) — docs sibling
- [vibe-proof-auditor](https://github.com/pedroknigge/vibe-proof-auditor) — auditor sibling

## How to pick a child

1. **Default for non-trivial work:** `ps-poteto-mode`. It matches a playbook and calls the other leaves as steps need them.
2. **Configure models / budget:** `ps-setup-pstack`.
3. **Your own -mode skill from how you actually work:** `ps-automate-me`.
4. **Understand existing code:** `ps-how` (runtime / placement), `ps-why` (motivation / evidence), `ps-teach` (plain explanation that runs both), `ps-recall` (catch-up brief), `ps-blast-radius` (what else a small change could break).
5. **Shape before code:** `ps-architect`. Parallel bakeoffs: `ps-arena`. Coverage / races: `ps-swarm`. Adversarial review: `ps-interrogate`.
6. **No bundled playbook fits:** `ps-figure-it-out`. Auditable trail: `ps-show-me-your-work`. After a long run, capture the recipe: `ps-reflect`.
7. **Cheap local failing test first:** `ps-tdd` only when asked or the target is obvious.
8. **Project-local verify skill:** `ps-create-verification-skill`, then `ps-maintain-verification-skill`.
9. **Prose:** `ps-unslop` on writing, `ps-technical-writing` for docs/PRs/commits, `ps-bro` to restate the last message, `ps-no-comments` before review.
10. **TypeScript files:** `ps-typescript-best-practices`. **Webhook bot UI:** `ps-make-bot-ui`.
11. **A named principle:** the matching `ps-principle-*` leaf. Read that leaf in full; do not apply from the title alone.

`ps-poteto-mode` already indexes the principles and routes the workflow leaves. Reach for a leaf directly when you want only that job.

Built-ins this pack does **not** ship: Cursor `/create-skill`, and `cursor-team-kit` skills (`/deslop`, `control-cli`, `control-ui`). `poteto-agent` / Comment Sicko are Cursor plugin subagents, not folders in this pack.

## Catalog

Every Desktop leaf is listed once. One-line when-to-use is taken from that leaf's description.

### Entry and style

| Skill | When to use |
|---|---|
| `ps-poteto-mode` | Use for poteto, /ps-poteto-mode, or requests to work in this style |
| `ps-setup-pstack` | Use for /ps-setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices |
| `ps-automate-me` | Use for "automate me", "create/update/refresh my -mode skill", "turn/capture my preferences or working style into a skill", or wanting agents to follow how the user works |

### Understand

| Skill | When to use |
|---|---|
| `ps-how` | Use for "how does X work", code walkthroughs before changing something, and placement / ownership / layering questions ("where should this live", "which package owns this", "is this the right layer") |
| `ps-why` | Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds |
| `ps-recall` | Use for 'recall my work on X', 'catch me up', 'what have I been working on', 'where did I leave off', before starting or resuming work |
| `ps-blast-radius` | Use for 'blast radius of X', 'what could this break', or reviewing a small diff you don't trust |
| `ps-teach` | Use for 'teach me this', 'help me really understand X', 'explain this change or subsystem to me' |

### Design and parallelism

| Skill | When to use |
|---|---|
| `ps-architect` | Use for /ps-architect, 'architect this', 'design this', or non-trivial work where jumping to code would lock in the wrong shape |
| `ps-arena` | Use for /ps-arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape |
| `ps-swarm` | Use for /ps-swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration |
| `ps-interrogate` | Use for "interrogate", "adversarial review", "multi-model review", "challenge this", "stress test this code", "find blind spots", or "tear this apart" |

### Workflow

| Skill | When to use |
|---|---|
| `ps-figure-it-out` | Use for /ps-figure-it-out, 'figure it out', a large migration, or when no narrower playbook applies |
| `ps-show-me-your-work` | Use for /ps-show-me-your-work, autonomous or multi-phase runs, or work a human reviews after stepping away |
| `ps-reflect` | Use when the user says reflect |
| `ps-tdd` | Use only when the user explicitly asks for TDD, a failing test, or a regression test, OR when the bug has an obvious cheap local test target |

### Verification skills

| Skill | When to use |
|---|---|
| `ps-create-verification-skill` | Use for /ps-create-verification-skill, "make a control skill for this repo", or when a project has no scripted way to prove UI/CLI/service behavior |
| `ps-maintain-verification-skill` | Use for /ps-maintain-verification-skill or "audit the verify skill" |

### Prose and review

| Skill | When to use |
|---|---|
| `ps-unslop` | Cut AI tells from any writing |
| `ps-bro` | Restate the last message in plain human language, with no jargon |
| `ps-technical-writing` | Use for /ps-technical-writing or when writing or reviewing docs, RFCs, readmes, PR descriptions, or commit messages |
| `ps-no-comments` | Spawn Comment Sicko, fix accepted findings, and offer encodings for claimed constraints |

### Specialized

| Skill | When to use |
|---|---|
| `ps-typescript-best-practices` | Use when reading or editing any .ts or .tsx file |
| `ps-make-bot-ui` | Use when building a custom UI (page, dashboard, buttons) that should wake a Grok Bot over a webhook, when the user must provide a webhook sender key, or when exposing that UI on Tailscale |

### Principles — core

| Skill | When to use |
|---|---|
| `ps-principle-laziness-protocol` | Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading |
| `ps-principle-foundational-thinking` | Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share |
| `ps-principle-redesign-from-first-principles` | Apply when integrating a new requirement into an existing design |
| `ps-principle-attack-the-premise` | Apply when two or more fixes that share one premise have failed the same gate |
| `ps-principle-subtract-before-you-add` | Apply when sequencing an addition, refactor, or rewrite |
| `ps-principle-minimize-reader-load` | Apply when reviewing or shaping code that's hard to trace |
| `ps-principle-outcome-oriented-execution` | Apply during planned rewrites and migrations with explicit phase boundaries |
| `ps-principle-experience-first` | Apply when product, UX, or feature-scope tradeoffs come up |
| `ps-principle-exhaust-the-design-space` | Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase |
| `ps-principle-build-the-lever` | Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks |

### Principles — architecture

| Skill | When to use |
|---|---|
| `ps-principle-model-the-domain` | Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files |
| `ps-principle-boundary-discipline` | Apply when wiring validation, error handling, or framework adapters |
| `ps-principle-type-system-discipline` | Apply when designing types, reviewing a function signature, or writing code in any statically-typed language |
| `ps-principle-make-operations-idempotent` | Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries |
| `ps-principle-migrate-callers-then-delete-legacy-apis` | Apply when introducing a new internal API while old callers still exist |
| `ps-principle-separate-before-serializing-shared-state` | Apply when concurrent actors might write to the same file, branch, key, or state object |

### Principles — verification

| Skill | When to use |
|---|---|
| `ps-principle-prove-it-works` | Apply after completing a task, before declaring done |
| `ps-principle-fix-root-causes` | Apply when debugging |
| `ps-principle-sequence-verifiable-units` | Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs |
| `ps-principle-test-behavior-not-implementation` | Apply when you write, change, or keep a test |

### Principles — delegation and meta

| Skill | When to use |
|---|---|
| `ps-principle-guard-the-context-window` | Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning |
| `ps-principle-never-block-on-the-human` | Apply when tempted to ask 'should I do X?' on reversible work |
| `ps-principle-encode-lessons-in-structure` | Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction |

## After you pick

Read the chosen leaf's `SKILL.md` (and any `references/` it names) before you act. Preserve poteto/pstack meaning. Do not substitute a different verb or invent a new skill.

## Dogfood / blindtest

Triggers: “dogfood”, “blindtest”, “probar pstack en un repo random”.

Full procedure: [references/dogfood.md](references/dogfood.md). Cycle (pack repo): [`docs/dogfood-cycle.md`](../../docs/dogfood-cycle.md).

1. Pick or accept a **public** repo you do not know. Not this pack. Not a private tree.
2. Exercise a small set of `ps-*` / this parent **cold**. Read each `SKILL.md` in full. Do not push or ticket the target.
3. Summarize pack friction (missing refs, wrong routing, stale descriptions).
4. Offer to file backlog via the issue module (HITL). Labels: `dogfood`, `blindtest`, plus `bug` or `enhancement`.
5. Implementing that backlog, bumping `VERSION` (`0.0.1` … `0.0.99` then `0.1.0`), and dogfooding again is the release loop.

## Report a defect or improvement in this pack

Triggers: “report this to pstack”, “file a pstack issue”, “sugerí mejora al skill”, “abre un issue en pstack”. Dogfood findings use the same desk.

Full procedure: [references/issue.md](references/issue.md). Wrapper: `scripts/ps-issue.sh` (also `skills/pstack/scripts/ps-issue.sh`).

- Target **always** `pedroknigge/pstack-skills`. Never consumer `origin`.
- Search open issues first (`--search`). Skip duplicates.
- **Never** create a GitHub issue without explicit human confirmation **in the same turn**.
- `--dry-run` is not HITL. Children (`PS_CHILD` / `OF_CHILD`) draft only (`--dry-run` or scratch `ISSUE.md`). The leader asks, then `--confirm`.
- Labels: `bug`, `enhancement`, `dogfood`, `blindtest` (repeat `--label` or comma-separate). No secrets, tokens, or private transcripts in bodies.

## HTML reports

When the user asks for a **report**, **HTML**, or **dashboard**, write structured markdown (parent session summary, or the `ps-show-me-your-work` trail) and, if the host can run Python stdlib, emit an `.html` twin beside it:

```bash
python3 scripts/render-report.py path/to/report.md
# TSV decision logs work too:
python3 scripts/render-report.py decisions.tsv
```

After install the same renderer is `…/skills/pstack/scripts/render-report.py`. Open the HTML in a browser (`open`, `xdg-open`, or drop the file on Chrome). The renderer styles what the markdown already contains. It does not invent scores. If `python3` is missing, skip HTML and say so.

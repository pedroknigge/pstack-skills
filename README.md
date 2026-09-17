# pstack-skills

**Public port of the Cursor pstack plugin as an installable Agent Skills pack — parent `pstack` router plus `ps-*` leaf skills.**

```bash
npx skills add pedroknigge/pstack-skills -g -y
```

Version **0.0.1**. MIT. Every `SKILL.md` `description` starts with `v0.0.1` and `metadata.version` is `"0.0.1"` so a stale install is obvious. This GitHub repo is Pedro Knigge's public port. It is **not** an official poteto or Cursor publication.

pstack is poteto's answer to slop-heavy agent output: less code, higher quality, fearless parallelism. The Cursor plugin is the upstream origin. This pack makes those same skill bodies installable via the [Skills CLI](https://github.com/vercel-labs/skills) (`npx skills add`) and `./install.sh`.

Leaf folders are prefixed `ps-*` so they do not collide with other skill names. The parent router is `pstack` (`/pstack`, `/ps`).

## Install

Primary path — whole pack, all detected agents, all projects:

```bash
npx skills add pedroknigge/pstack-skills -g -y
```

`-g` installs globally. Omit it for the current repo only. `-y` skips prompts. The CLI auto-detects installed agents (Claude, Grok, Cursor, Gemini, and others).

Also ship `./install.sh` so one command copies **every** folder under `skills/` (parent `pstack` + all `ps-*` leaves) into every detected agent skill dir: Claude, Grok, Cursor / `~/.agents/skills`, and Gemini / AGY trees when those parents exist.

```bash
./install.sh
./install.sh --project
./install.sh --uninstall
```

Antigravity (`agy`) sometimes needs explicit agents on the Skills CLI:

```bash
npx skills add pedroknigge/pstack-skills -g -y -a antigravity -a antigravity-cli
# or close the gap without the skills CLI:
./install.sh
```

### Update

```bash
npx skills update pstack-skills -g -y
```

Then re-run `./install.sh` if you use the classic installer paths.

### One-off without installing

```bash
npx skills use pedroknigge/pstack-skills
```

## How to invoke

- **Parent router:** `/pstack` or `/ps` — pick a leaf when you know you want pstack but not which skill.
- **Default for non-trivial work:** `/ps-poteto-mode` — matches a playbook and calls other leaves as steps need them.
- **Configure models / budget:** `/ps-setup-pstack`.
- **A specific job:** the matching `/ps-<slug>` (for example `/ps-how`, `/ps-why`, `/ps-architect`).

If you already named a leaf, run that leaf. Do not bounce through the parent first.

Built-ins this pack does **not** ship: Cursor `/create-skill`, and `cursor-team-kit` (`/deslop`, `control-cli`, `control-ui`). `poteto-agent` and Comment Sicko are Cursor plugin subagents, not folders here.

## Report a defect or improvement in this pack

Triggers: “report this to pstack”, “file a pstack issue”, “sugerí mejora al skill”, “abre un issue en pstack”.

The parent skill owns the HITL loop ([skills/pstack/references/issue.md](skills/pstack/references/issue.md)). Wrapper:

```bash
scripts/ps-issue.sh --search "short query"
scripts/ps-issue.sh --title "…" --label dogfood,enhancement \
  --body "…" --dry-run
# after an explicit human yes in the same turn:
scripts/ps-issue.sh --title "…" --label enhancement --body-file ISSUE.md --confirm
```

Suggested labels: `dogfood`, `blindtest`, `bug`, `enhancement`. `--label` may be repeated or comma-separated.

- Target is **always** [`pedroknigge/pstack-skills`](https://github.com/pedroknigge/pstack-skills). Never the consumer working-tree origin.
- Never create a GitHub issue without explicit human confirmation in the same turn. `--dry-run` is not HITL.
- Search open issues first; skip duplicates. No secrets, tokens, or private transcripts in bodies.
- Child / subagent sessions draft only (`--dry-run` or scratch `ISSUE.md`). The leader asks, then submits.

After `npx skills add` / `./install.sh`, the same scripts live under `…/skills/pstack/scripts/`.

## Dogfood → backlog → release

Periodic **blindtest** on a public repo you do not know. Findings become backlog issues on this skill repo. Implementing that backlog is how the next release gets tested. Then dogfood again.

1. Pick a public repo you do not know (or pass a URL).
2. Run relevant `ps-*` / parent `pstack` skills **cold**.
3. Capture friction, missing refs, wrong routing, stale descriptions.
4. File backlog via the issue module (HITL) with labels `dogfood`, `blindtest`, `bug`, `enhancement`.
5. Implement → bump `VERSION` (`0.0.1` … `0.0.99` then `0.1.0`) → re-dogfood.

Parent triggers: “dogfood”, “blindtest”, “probar pstack en un repo random”. Procedure: [`docs/dogfood-cycle.md`](docs/dogfood-cycle.md) and [`skills/pstack/references/dogfood.md`](skills/pstack/references/dogfood.md). Evals scaffold (planted vs live): [`evals/README.md`](evals/README.md).

## Sibling bridges (sensor, not fusion)

Parent `/pstack` announces when a sibling is in play (`ArkGate: none|detected`, `Orderfield: …`, `Docs: …`, `Vibe-proof: …`). Bridges **detect + HITL-propose**. They do not vendor sibling bodies or silent auto-run.

| Sibling | Note | Repo |
|---|---|---|
| ArkGate (+ addons) | Detect `ark.config.json` / ark-check / ark skills. Fold with HITL. Do not rewrite `ark.config.json`. | [arkgate](https://github.com/pedroknigge/arkgate) |
| Orderfield | Pairing with `of` / `.orderfield` only. Self-telemetry stays on orderfield. Never consumer-origin issues. | [orderfield](https://github.com/pedroknigge/orderfield) |
| documentation-manager | Docs sibling. Reciprocal to their `pstack-bridge.md`. Live names here: `ps-architect` / `ps-figure-it-out` / parent `pstack`. | [documentation-manager](https://github.com/pedroknigge/documentation-manager) |
| vibe-proof-auditor | Auditor sibling. Propose/fold findings. Do not copy checklist or scoring. | [vibe-proof-auditor](https://github.com/pedroknigge/vibe-proof-auditor) |

Notes live in [`skills/pstack/references/`](skills/pstack/references/). Optional sensor: `scripts/ps-detect-siblings.sh`.

## HTML reports

When you ask for a **report**, **HTML**, or **dashboard**, the parent (and `ps-show-me-your-work`) write structured markdown and, if Python stdlib is available, an `.html` twin beside it:

```bash
python3 scripts/render-report.py path/to/report.md
python3 scripts/render-report.py decisions.tsv   # show-me-your-work log
```

Open the HTML in a browser (`open report.html`, `xdg-open report.html`, or drop the file on Chrome). The renderer is offline, stdlib-only, and styles what the markdown already contains. It does not invent scores. After install: `…/skills/pstack/scripts/render-report.py`.

## Catalog

One-line when-to-use is taken from each leaf's description. Full routing notes live in [`skills/pstack/SKILL.md`](skills/pstack/SKILL.md).

### Entry and style

| Skill | When to use |
|---|---|
| [`pstack`](skills/pstack/SKILL.md) | Parent router. `/pstack` `/ps`. |
| [`ps-poteto-mode`](skills/ps-poteto-mode/SKILL.md) | poteto's style and playbooks. Default entry for non-trivial work. |
| [`ps-setup-pstack`](skills/ps-setup-pstack/SKILL.md) | Configure which models pstack uses per role and at what reasoning budget. |
| [`ps-automate-me`](skills/ps-automate-me/SKILL.md) | Draft or revise a personal `-mode` skill from how you actually work. |

### Understand

| Skill | When to use |
|---|---|
| [`ps-how`](skills/ps-how/SKILL.md) | How a subsystem works; placement / ownership / layering. |
| [`ps-why`](skills/ps-why/SKILL.md) | Why it was built this way; cited evidence across sources. |
| [`ps-recall`](skills/ps-recall/SKILL.md) | Catch-up brief from your history and the shared record. |
| [`ps-blast-radius`](skills/ps-blast-radius/SKILL.md) | What else a small change could break, proven by running code. |
| [`ps-teach`](skills/ps-teach/SKILL.md) | Plain explanation. Runs `ps-how` and `ps-why`. |

### Design and parallelism

| Skill | When to use |
|---|---|
| [`ps-architect`](skills/ps-architect/SKILL.md) | Types, signatures, and module shape before code. |
| [`ps-arena`](skills/ps-arena/SKILL.md) | N parallel candidates; pick a base and graft. |
| [`ps-swarm`](skills/ps-swarm/SKILL.md) | N parallel workers across slices or races; one report. |
| [`ps-interrogate`](skills/ps-interrogate/SKILL.md) | Multi-model adversarial review. |

### Workflow and verification

| Skill | When to use |
|---|---|
| [`ps-figure-it-out`](skills/ps-figure-it-out/SKILL.md) | No narrower playbook fits; design an auditable one. |
| [`ps-show-me-your-work`](skills/ps-show-me-your-work/SKILL.md) | Reviewable decision trail (TSV). |
| [`ps-reflect`](skills/ps-reflect/SKILL.md) | After a long task, capture the recipe as a skill edit. |
| [`ps-tdd`](skills/ps-tdd/SKILL.md) | Failing test first, only when asked or the local target is obvious. |
| [`ps-create-verification-skill`](skills/ps-create-verification-skill/SKILL.md) | Generate a project-local verify skill / feature map. |
| [`ps-maintain-verification-skill`](skills/ps-maintain-verification-skill/SKILL.md) | Keep that verify skill honest as the app changes. |

### Prose, review, specialized

| Skill | When to use |
|---|---|
| [`ps-unslop`](skills/ps-unslop/SKILL.md) | Cut AI tells from writing. |
| [`ps-bro`](skills/ps-bro/SKILL.md) | Restate the last message in plain language. |
| [`ps-technical-writing`](skills/ps-technical-writing/SKILL.md) | Docs, RFCs, READMEs, PR descriptions, commits. |
| [`ps-no-comments`](skills/ps-no-comments/SKILL.md) | Comment Sicko pass before review. |
| [`ps-typescript-best-practices`](skills/ps-typescript-best-practices/SKILL.md) | Reading or editing `.ts` / `.tsx`. |
| [`ps-make-bot-ui`](skills/ps-make-bot-ui/SKILL.md) | Page or dashboard that wakes a Grok Bot over a webhook. |

### Principles (23)

Each `ps-principle-*` leaf is one rule. `ps-poteto-mode` indexes them and reads the leaf in full when it applies.

| Group | Skills |
|---|---|
| Core | `ps-principle-laziness-protocol`, `ps-principle-foundational-thinking`, `ps-principle-redesign-from-first-principles`, `ps-principle-attack-the-premise`, `ps-principle-subtract-before-you-add`, `ps-principle-minimize-reader-load`, `ps-principle-outcome-oriented-execution`, `ps-principle-experience-first`, `ps-principle-exhaust-the-design-space`, `ps-principle-build-the-lever` |
| Architecture | `ps-principle-model-the-domain`, `ps-principle-boundary-discipline`, `ps-principle-type-system-discipline`, `ps-principle-make-operations-idempotent`, `ps-principle-migrate-callers-then-delete-legacy-apis`, `ps-principle-separate-before-serializing-shared-state` |
| Verification | `ps-principle-prove-it-works`, `ps-principle-fix-root-causes`, `ps-principle-sequence-verifiable-units`, `ps-principle-test-behavior-not-implementation` |
| Delegation / meta | `ps-principle-guard-the-context-window`, `ps-principle-never-block-on-the-human`, `ps-principle-encode-lessons-in-structure` |

## Layout

```
pstack-skills/
├── README.md
├── LICENSE
├── VERSION                 # 0.0.1
├── CHANGELOG.md
├── install.sh
├── AGENTS.md
├── docs/                   # dogfood-cycle.md
├── evals/                  # planted vs live dogfood scaffold
├── scripts/                # ps-issue.sh, render-report.py, ps-detect-siblings.sh
└── skills/
    ├── pstack/
    │   ├── SKILL.md        # parent router
    │   ├── references/     # issue HITL + sibling bridges
    │   └── scripts/        # same helpers, shipped with the parent
    ├── ps-poteto-mode/
    ├── ps-how/
    ├── ps-why/
    └── ps-<slug>/          # one folder per Desktop leaf
```

This repo is a valid Agent Skills pack (`SKILL.md` under each `skills/*` folder) per [agentskills.io](https://agentskills.io/specification).

## Attribution

Upstream origin is the **Cursor pstack plugin** (poteto / Lauren Tan). That plugin is not an official public GitHub repo yet. Skill text, playbooks, and principles in this pack are a port of those Desktop leaves — names rewritten to `ps-*`, meaning preserved.

This repository (`pedroknigge/pstack-skills`) is the **public port** by Pedro Knigge. Do not treat it as a poteto or Cursor release.

Packaging for this repo is MIT, Copyright (c) 2026 Pedro Knigge. See [LICENSE](LICENSE). Do not strip license or attribution from skill text.

## Version

`VERSION` is `0.0.1`. Every skill `description` starts with `v0.0.1` and `metadata.version` is `"0.0.1"`. Later cuts: patch bumps `0.0.1` → `0.0.99`, then `0.1.0` — bump the file, every prefix, and every `metadata.version` together. See [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE)

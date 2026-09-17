# ArkGate bridge (sensor, not fusion)

pstack may **detect** ArkGate (+ addons) and **HITL-propose** a fold. It does **not** embed Ark's runtime, rewrite `ark.config.json`, or vendor ark skill bodies.

Shared axioms: **human captain** · **Missing stays Missing** · **no greenwash** · **no silent auto-run** · **do not vendor sibling bodies**.

Pattern (docs sibling): documentation-manager `arkgate-bridge.md`. This note is pairing guidance only.

## Detection

| Signal | How to detect | Confidence |
|--------|---------------|------------|
| Config | `ark.config.json` (repo root or documented path) | high |
| CLI | `ark-check` on PATH; `ark-check` / `arkgate` in `package.json` | high |
| Snapshots | `.ark/` (reports, history) | high |
| Skills | Host skills `ark-*` / `/ark-check` / `/ark-adopt` / `/ark-loop` | medium |
| Session | User said “ark”, “ark-check”, “after ark”, “gate passed” | high (session) |

**If no signal:** `ArkGate: none`. Do not install Ark. Do not mention it as required.

Parent announce:

```text
ArkGate: none|detected
```

Optional sensor: `scripts/ps-detect-siblings.sh` (also under `skills/pstack/scripts/`).

## When relevant

HITL-propose only when pstack work touches architecture boundaries (typically `ps-architect`, `ps-blast-radius`, or a design the user already tied to Ark):

> Hay señales de ArkGate. ¿Corro / consulto ark-check (o el skill ark del host) y pliego residuales en el diseño pstack? No reescribo `ark.config.json`.

Captain **no** / silence → stop. Do not ask again this session. Captain **yes** → load the **host** ark skill and follow **its** workflow. Fold findings as pointers (paths, violation kinds). Do not copy ark reports into pstack leaves.

## Non-writes

- `ark.config.json` and Ark runtime files
- Application source “to match the gate”
- Silent `/ark-*` / `ark-check`
- Installing Ark for the user
- Greenwash: a missing gate is `none` / Missing, not a pass

## Pairing

```text
code / design
  → Ark skills / ark-check (architecture contract) — only after HITL
  → pstack leaf already in play (ps-architect / ps-how / …)
  → user commits
```

Ark stays the architecture-contract sibling. pstack stays the rigor/router pack. Documentation-manager stays the docs sibling.

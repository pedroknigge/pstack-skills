# documentation-manager bridge (sensor, not fusion)

**Reciprocal** to documentation-manager's existing `pstack-bridge.md`. They already bake portable pstack plan rules and may HITL-propose `/architect` / `/figure-it-out`. On this side, those live names are **`ps-architect`**, **`ps-figure-it-out`**, and the parent **`pstack`** router.

documentation-manager is the **docs sibling**. This pack does not vendor their modes, templates, or dashboard.

Shared axioms: **human captain** · **Missing stays Missing** · **no greenwash** · **no silent auto-run** · **do not vendor sibling bodies**.

## Detection

| Signal | How to detect | Confidence |
|--------|---------------|------------|
| Host skill | `documentation-manager` / `/documentation-manager` | high |
| Session | User said “docs skill”, “documentation-manager”, “sync the docs” | high (session) |

Mere `docs/` in a tree is **not** enough. Missing stays Missing.

**If no signal:** `Docs: none`. Do not install the sibling. Bake nothing into consumer docs from this pack.

Parent announce:

```text
Docs: none|detected
```

## Name map (their propose → this pack)

| Their `pstack-bridge.md` (host may still say) | This pack |
|-----------------------------------------------|-----------|
| `/architect` · skill `architect` | **`ps-architect`** / `/ps-architect` |
| `/figure-it-out` · skill `figure-it-out` | **`ps-figure-it-out`** / `/ps-figure-it-out` |
| pstack plugin / `setup-pstack` | parent **`pstack`** + **`ps-setup-pstack`** |
| poteto pstack | **`ps-poteto-mode`** (style), not a docs verb |

If a host still has unprefixed Desktop names, follow whatever `SKILL.md` is actually installed. Do not invent a third alias.

## HITL propose (when docs sibling is present)

When this pack is writing or handing back a **design** (`ps-architect`, `ps-figure-it-out`, or parent routing into those) **and** documentation-manager is on the host, ask **once**:

> Hay documentation-manager (docs sibling). ¿Lo corro **with checkpoint** y pliego el diseño pstack en Acceptance / MVP / Next actions / Open questions del plan? No reescribo docs en silencio.

Captain **no** / silence → `skip:declined`. Captain **yes** → load **their** `SKILL.md` and follow **their** workflow. Fold pointers into the plan they own. Do not paste a full pstack dump into their hub. Do not copy `modes.md`.

If they already proposed `/architect` or `/figure-it-out` toward this pack, honor that as captain yes for the matching **`ps-*`** leaf — still announce `Docs: detected`, still no silent docs writes.

## What they bake (do not re-implement)

Their portable plan rules (subtract-before-add, attack the premise, falsifiable acceptance, verifiable next actions, one-way doors, experience/outcome first) live **in documentation-manager**. This pack's meaning for those ideas stays in the matching `ps-principle-*` leaves and `ps-architect` / `ps-figure-it-out`. Do not duplicate the bake table here.

## Non-writes

- documentation-manager skill trees, modes, or HTML dashboard
- Silent `/documentation-manager` / plan refresh
- Product-vision rewrites “to match pstack”
- Installing the sibling for the user

## Pairing

```text
pstack design (ps-architect / ps-figure-it-out / parent pstack)
  → HITL propose docs sibling
  → documentation-manager plan fold
  → user commits
```

ArkGate stays architecture-contract. vibe-proof-auditor stays auditor. Orderfield stays field kernel. This bridge does not replace them.

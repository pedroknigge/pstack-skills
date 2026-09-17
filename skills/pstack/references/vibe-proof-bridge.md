# vibe-proof-auditor bridge (sensor, not fusion)

pstack may **detect** the auditor sibling and **HITL-propose** a run, then fold findings. It does **not** copy the checklist, scoring, or gates, and it does not merge the products.

Shared axioms: **human captain** · **Missing stays Missing** · **no greenwash** · **no silent auto-run** · **do not vendor sibling bodies**.

Sibling: [pedroknigge/vibe-proof-auditor](https://github.com/pedroknigge/vibe-proof-auditor).

## Detection

| Signal | How to detect | Confidence |
|--------|---------------|------------|
| Host skill | `vibe-proof-auditor` / `/vibe-proof-auditor` | high |
| Report | `vibe-proof-audit-report.md` already in the tree | medium |
| Session | User said “vibe-proof”, “auditor”, “dunk this” | high (session) |

**If no signal:** `Vibe-proof: none`. One friendly hint + GitHub link is allowed. Do not install it. Do not invent scores.

Parent announce:

```text
Vibe-proof: none|detected
```

## When to propose

Offer **once** when the work is claiming a product/skill surface is done (often after `ps-principle-prove-it-works` / a verify leaf) **and** the sibling is present **and** there is auditable code. Docs-only trees stay skipped (`none` / skip).

> Hay vibe-proof-auditor. ¿Lo corro (rápido, unless you asked Deep) y pliego P0–P1 en lo que pstack ya está haciendo? No copio el checklist.

Captain **no** / silence → stop. Mandate phrases already in this session (“run vibe-proof”, “with vibe-proof-auditor”) count as yes — still announce, still not silent.

## Fold (not a second SSOT)

1. Load the sibling `SKILL.md`. Follow **its** workflow.
2. Read Findings. Do **not** paste the full report into a pstack leaf or invent a score.
3. Fold as pointers (`id` + path + note) into the work already in play (open questions, verify gaps, Attention in `ps-show-me-your-work`).
4. Optional one-line pointer to `vibe-proof-audit-report.md` if they wrote it.
5. Sibling missing after yes → hint once; leave gaps Missing.

## Non-writes

- Auditor checklist / scoring / gates copied into this pack
- Invented overall scores or “READY” stamps
- Silent harden / `agy` / Deep
- Installing the sibling for the user

## Pairing

```text
pstack work (prove-it / verify / handback)
  → HITL propose vibe-proof-auditor
  → fold findings as pointers
  → user commits
```

documentation-manager stays the docs sibling. ArkGate stays architecture-contract. This bridge does not replace either.

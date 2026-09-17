# Orderfield bridge (sensor, not fusion)

pstack may **detect** Orderfield / the `of` CLI and offer **pairing guidance**. It does **not** vendor Orderfield, post consumer-origin issues, or run `of` silently.

Shared axioms: **human captain** · **Missing stays Missing** · **no greenwash** · **no silent auto-run** · **do not vendor sibling bodies**.

## Detection

| Signal | How to detect | Confidence |
|--------|---------------|------------|
| Field home | `.orderfield/` | high |
| Manifest | `ORDER.json` | high |
| CLI | `of` on PATH | high |
| Skills | Host skill `of` / `orderfield` | high |
| Session | User said “orderfield”, “of issue”, “the field” | high (session) |

**If no signal:** `Orderfield: none`.

Parent announce:

```text
Orderfield: none|detected
```

## Pairing only

When a field is open, pstack leaves are ordinary work skills inside a packet (`ps-how`, `ps-architect`, `ps-figure-it-out`, …). Follow the leaf. Do not invent an Orderfield verb. Do not rewrite ORDER / SPEC / residuals.

HITL-propose a sibling run only if the captain's request actually needs Orderfield (`of status`, `of contrast`, …). Load **their** `SKILL.md`. No silent `of` auto-run.

## Two issue desks — do not mix

| Finding is about | File with | Target |
|------------------|-----------|--------|
| This pack / a `ps-*` skill / parent router / install | `scripts/ps-issue.sh` after HITL | **always** `pedroknigge/pstack-skills` |
| Orderfield kernel / CLI / skill / install pin | `of issue` after HITL | **always** `pedroknigge/orderfield` |
| Consumer product / “user is stuck” / app tests | stay on disk or the consumer tracker | **never** either self-telemetry desk |

Orderfield self-telemetry stays on Orderfield. **Never** create a GitHub issue on the consumer working-tree origin — not via `ps-issue.sh`, not via `of issue`, not via raw `gh`.

Children draft only. Leader asks. Same-turn confirm. See [issue.md](issue.md).

## Non-writes

- Consumer `origin` issues
- `.orderfield/` WAL / SPEC / CLOSE unless the captain asked Orderfield itself
- Installing `of` for the user
- Copying Orderfield CLI or SLAVE bodies into this pack

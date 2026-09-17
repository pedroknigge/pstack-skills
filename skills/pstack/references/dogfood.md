# Dogfood / blindtest pass

Parent-router procedure. Not a new leaf verb. Full cycle: [`docs/dogfood-cycle.md`](../../../docs/dogfood-cycle.md) in the pack repo.

## Triggers

Treat these (and close variants) as this pass:

- “dogfood”
- “blindtest”
- “probar pstack en un repo random”
- “cold run pstack on a public repo”

## Steps

1. **Announce** this is a pack dogfood pass, not consumer product work. Print sibling sensors as usual (`ArkGate: none|detected`, …). Do not silent-run siblings.
2. **Target.** If the user gave a public repo URL, use it. Else pick one public repo the session does not already know (`gh search repos --public`, or ask the captain for a URL). Refuse private trees. Refuse `pedroknigge/pstack-skills` as the target (that is the backlog desk, not the blind).
3. **Read-only.** Shallow clone to a scratch dir or browse via `gh`. Do **not** push, open PRs, or `gh issue create` on the target. Do not install this pack into that tree unless the captain asked.
4. **Exercise a small set, cold.** Read each chosen `SKILL.md` in full before acting. Typical mix:
   - parent routing (pick a leaf from a vague ask)
   - one understand leaf (`ps-how` / `ps-teach` / `ps-blast-radius`)
   - one design or workflow leaf if the tree has a real shape question (`ps-architect` / `ps-figure-it-out`)
   Stop after a handful of leaves. This is not a full poteto-mode rewrite of someone else's repo.
5. **Capture** only pack friction: missing refs, wrong routing, stale descriptions, steps that fail as written. Missing stays Missing. No greenwash.
6. **Summarize opportunities** for the captain (one list). Optional HTML twin via `scripts/render-report.py` if they asked for a report.
7. **Offer to file** on `pedroknigge/pstack-skills` via [issue.md](issue.md). Search first. One draft per distinct finding. Labels from `dogfood`, `blindtest`, `bug`, `enhancement` (repeat `--label` or comma-separate). **HITL in this turn.** Children draft only.

## Non-goals

- Inventing a new skill or rewriting poteto/pstack meaning to match the target
- Filing on consumer origin or on the dogfood target
- Leaking secrets, tokens, private transcripts, or target source dumps into issue bodies
- Vendoring sibling products; sensor + HITL only

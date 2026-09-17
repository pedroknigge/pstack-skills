# Report a defect or improvement in pstack-skills

Always leave this module so a user can file pack/skill defects **on this skill repo**. Human captain: the leader asks; confirm creates.

**Target is always** [`pedroknigge/pstack-skills`](https://github.com/pedroknigge/pstack-skills). Never the consumer working-tree `origin`. A host app that installed this pack cannot receive these issues.

Mirror Orderfield's `of issue` HITL pattern. This pack's wrapper is `scripts/ps-issue.sh` (also shipped at `skills/pstack/scripts/ps-issue.sh`).

## Triggers

Treat these (and close variants) as this module, not a new leaf verb:

- "report this to pstack"
- "file a pstack issue"
- "sugerí mejora al skill" / "sugeri una mejora al skill"
- "abre un issue en pstack"
- "pstack bug" / "this skill is wrong" when the finding is **about the pack**, not the consumer product

Do **not** file here: consumer product bugs, "the user is stuck", failed app tests, or Orderfield kernel defects (those stay on `of issue` → `pedroknigge/orderfield`). If unsure, draft + HITL, default to not posting.

## HITL lock

- **Never** create a GitHub issue without explicit human confirmation **in the same turn**.
- `--dry-run` previews argv and is **not** HITL.
- `--confirm` is legal only after the human said yes this turn, or a TTY `y/N`.
- Child / subagent sessions (`PS_CHILD` or `OF_CHILD` set) **draft only**: `--search`, `--dry-run`, or a scratch `ISSUE.md`. They never submit.
- The leader searches, shows the draft, asks, then submits.

## Procedure

1. **Search open issues first.** Skip duplicates.

   ```bash
   scripts/ps-issue.sh --search "short query"
   # empty query lists open issues on pedroknigge/pstack-skills
   ```

2. **Draft** title + body. Labels: `bug`, `enhancement`, `dogfood`, `blindtest` (repeat `--label` or comma-separate). Dogfood / blindtest findings should carry `dogfood` and usually `blindtest` plus `bug` or `enhancement`.
   - No secrets, tokens, private transcripts, home paths, or consumer source dumps.
   - One draft per distinct finding.
   - Children write `ISSUE.md` (or `issues/<slug>.md`) and name it for the leader.

3. **Ask** in this turn. Refuse / edit-later / silence does **not** create.

4. **Submit** only after yes:

   ```bash
   scripts/ps-issue.sh --title "…" --label dogfood,enhancement \
     --body "…" --confirm
   # or --body-file PATH --label blindtest --label bug
   ```

   Preview without posting:

   ```bash
   scripts/ps-issue.sh --title "…" --label enhancement \
     --body-file ISSUE.md --dry-run
   ```

## Script

`scripts/ps-issue.sh` wraps `gh issue list` / `gh issue create` with `--repo pedroknigge/pstack-skills`. It redacts common token shapes, refuses huge dumps, and refuses submit when `PS_CHILD` / `OF_CHILD` is set.

After `npx skills add` / `./install.sh`, the same file lives next to the parent skill: `…/skills/pstack/scripts/ps-issue.sh`.

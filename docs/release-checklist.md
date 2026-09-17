# Release checklist

For **Pstacky** (steward bot) and **Pedro**. After each tagged release, install this pack **globally** on whichever of Pedro's Macs are on — M5 and/or M1 (“ambas las que estén prendidas”).

Do **not** SSH to those machines from a cloud agent. Pedro (or Pstacky on a Mac that is already signed in) runs the install locally.

## Steps

1. **Tag / bump `VERSION`.** Patch `0.0.1` … `0.0.99`, then `0.1.0`. Lockstep: `VERSION`, every `SKILL.md` `description` prefix (`vX.Y.Z`), every `metadata.version`, changelog, README.
2. **Merge the PR** to `main`. Publish the git tag that matches `VERSION` if this cut uses tags.
3. **On each powered-on Mac** (M5 and/or M1 — skip the one that is off):

   ```bash
   npx skills add pedroknigge/pstack-skills -g -y
   # AGY / antigravity gap:
   ./install.sh
   # or:
   npx skills add pedroknigge/pstack-skills -g -y -a antigravity -a antigravity-cli
   ```

4. **Confirm** the installed `description` leading version matches `VERSION` on those machines. A stale global install is the usual miss: the prefix in `~/.agents/skills/pstack/SKILL.md` (and a sample `ps-*` leaf) must be `v` + the file `VERSION` you just shipped.

## After install

Dogfood again on a public repo you do not know ([dogfood-cycle.md](dogfood-cycle.md)). Findings stay on `pedroknigge/pstack-skills` via HITL `scripts/ps-issue.sh`.

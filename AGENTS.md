# AGENTS.md

This repo is Pedro Knigge's public port of the Cursor pstack plugin. It is not a poteto or Cursor release. Never strip the upstream license or attribution from skill text. See [LICENSE](LICENSE).

Do not invent skill verbs. Do not rewrite poteto or pstack meaning.

Ask before you publish this pack to a skills registry. Ask before you force-push `main`.

File an issue only after a human yes in the same turn. Child sessions draft only. The target is always `pedroknigge/pstack-skills`. The procedure is [skills/pstack/references/issue.md](skills/pstack/references/issue.md).

Sync from upstream with `python3 scripts/port-upstream.py <upstream-skills-dir> skills <version>`, then `bash scripts/verify-pack.sh`. Proof rows are [docs/feature-map.md](docs/feature-map.md).

`python3 scripts/check-pack.py` enforces frontmatter, the `VERSION` lock, router coverage, links, `ps-` prefixes, and install size. `bash scripts/verify-pack.sh` enforces the runtime proofs.

A line in this file that says "role label" is checked against [skills/ps-setup-pstack/SKILL.md](skills/ps-setup-pstack/SKILL.md). With no such line, the check skips.

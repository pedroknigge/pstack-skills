# Dogfood → backlog → release

Periodic **blindtest** on a public repo you do not know. Findings become backlog issues on [`pedroknigge/pstack-skills`](https://github.com/pedroknigge/pstack-skills). Implementing that backlog is how the next release gets tested. Then dogfood again.

This is a pack loop, not a CI product. No silent issue create. No consumer-origin tickets. Live targets stay **public** third-party repos.

The parent router runs the pass when you say **dogfood**, **blindtest**, or **probar pstack en un repo random**. Procedure the agent follows after install: [`skills/pstack/references/dogfood.md`](../skills/pstack/references/dogfood.md).

## Cycle

1. **Pick blind.** A public repo URL you do not know — or let the parent pick one. Not this pack. Not a private tree.
2. **Run cold.** Relevant `ps-*` leaves and/or parent `pstack`. Read each chosen `SKILL.md` in full. Do not invent a new verb. Do not push to the target. Do not file issues on the target.
3. **Capture friction.** Missing refs, wrong routing, stale descriptions, steps that do not work as written.
4. **File backlog (HITL).** `scripts/ps-issue.sh` → always `pedroknigge/pstack-skills`. Search first. Skip duplicates. Confirm in the same turn. Suggested labels: `dogfood`, `blindtest`, `bug`, `enhancement`.
5. **Implement** the backlog on this pack. Bump `VERSION` with every `description` prefix and `metadata.version` (patch `0.0.1` … `0.0.99`, then `0.1.0`).
6. **Re-dogfood** on a fresh public repo.

## Labels

| Label | Use |
|---|---|
| `dogfood` | Finding from this loop |
| `blindtest` | Cold run on a repo the agent did not know |
| `bug` | Pack/skill is wrong |
| `enhancement` | Pack/skill could be better |

`--label` may be repeated or comma-separated (`--label dogfood,enhancement`). `bug` and `enhancement` already exist on the repo; create `dogfood` / `blindtest` on GitHub once if `gh` refuses an unknown label.

## What never goes in an issue

Secrets, tokens, private transcripts, home paths, or source dumps from the target. Quote friction in your own words plus public paths / skill names.

Planted vs live: [`evals/README.md`](../evals/README.md).

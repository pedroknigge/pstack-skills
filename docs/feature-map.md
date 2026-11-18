# Feature map

Proofs `scripts/verify-pack.sh` runs. One PASS/FAIL line per row. Output: `verify-evidence.md`.

| Feature | How the user reaches it | What proves it works |
|---|---|---|
| Global install into every agent dir that exists | `./install.sh` | `HOME=$TMP ./install.sh --global` with `.agents` `.claude` `.grok` `.cursor` `.gemini`. 59 skills, counted from `skills/*/SKILL.md`. Each installed description starts with `v$(cat VERSION)`. `ps-poteto-mode/worker.md` is present. No `test/` or `tests/` directory is installed. |
| Registry install | `npx skills add pedroknigge/pstack-skills -g -y` | not run offline |
| Router lists and routes to every `ps-*` leaf | `/pstack`, `/ps` | `python3 scripts/check-pack.py` exits 0 |
| Issue dry-run targets this repo; children cannot submit | `scripts/ps-issue.sh` | `--dry-run` prints `pedroknigge/pstack-skills` and no other repo. `PS_CHILD=1` or `OF_CHILD=1` without `--dry-run` exits non-zero. |
| HTML twin of a markdown report | `python3 scripts/render-report.py REPORT.md` | `python3 scripts/render-report.py REPORT.md` writes a non-empty HTML file |
| Sibling detection | `scripts/ps-detect-siblings.sh` | `scripts/ps-detect-siblings.sh .` prints `ArkGate: none`, `Orderfield: none`, `Docs: none`, `Vibe-proof: none` |
| Upstream sync | `python3 scripts/port-upstream.py UPSTREAM DST VERSION` | `scripts/check-pack.py` runs after the port and its status is the porter's status |

# Upstream ps-statechart test suite (not installed)

Upstream `pstack/skills/statechart/scripts/test/` (cursor/plugins, MIT, Lauren Tan), moved here by
`scripts/port-upstream.py` so `install.sh` and `npx skills add` don't ship the ~4 MB TLC corpus.
Runtime scripts in `skills/ps-statechart/scripts/` don't import it.

To run it: copy `test/` back into `skills/ps-statechart/scripts/`, then `npm test` there (needs Node + Java/TLC).

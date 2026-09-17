# Evals (scaffold)

Two lanes. This folder is a **stub**, not a CI product.

| Lane | What it is | What it is not |
|---|---|---|
| **Planted** | A fixture in this repo that plants one known pack failure (stale description, wrong route) so a future eval can catch it. | A live run against a stranger's tree. |
| **Live dogfood** | Cold pass on a **public** third-party repo. Procedure: [`docs/dogfood-cycle.md`](../docs/dogfood-cycle.md) and parent [references/dogfood.md](../skills/pstack/references/dogfood.md). | A license to push, ticket, or dump that repo into GitHub issues. |

Live findings become backlog on `pedroknigge/pstack-skills` only after HITL (`scripts/ps-issue.sh`). Never leak private data, tokens, or transcripts into those issues. Never file on the dogfood target.

Stub: [`fixtures/live-dogfood.stub.md`](fixtures/live-dogfood.stub.md).

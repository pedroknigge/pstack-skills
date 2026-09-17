---
name: ps-principle-guard-the-context-window
description: "v0.0.1. Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads. If the leading version is not the latest in VERSION / changelog, update the skill before using it."
license: MIT
disable-model-invocation: true
metadata:
  version: "0.0.1"
  author: pedroknigge
---

# Guard the Context Window

The context window is finite and non-renewable within a session. Every token should be worth its cost.

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Isolate large payloads.** Route verbose outputs, screenshots, and large documents to subagents. The main context gets summaries, not raw data.
- **Don't read what you won't use.** Read selectively based on relevance. If a file isn't needed for the current task, skip it.
- **Keep frequently used content inline.** Templates and references used on every invocation belong in the skill file, not in separate files that cost a read each time.
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.

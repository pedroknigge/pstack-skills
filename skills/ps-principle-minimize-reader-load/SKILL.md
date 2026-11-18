---
name: ps-principle-minimize-reader-load
description: "v0.0.5. Apply when reviewing or shaping code that's hard to trace. Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope. If the leading version is not the latest in VERSION / changelog, update the skill before using it."
license: MIT
disable-model-invocation: true
metadata:
  version: "0.0.5"
  author: pedroknigge
---

# Minimize Reader Load

Reader load is the work a reader must do to understand code. It has two independent axes: layers to trace between the question and the answer, and hidden or mutable state to hold in their head. Guard both.

- Collapse layers that only forward: wrappers with one caller, adapters with no second implementation, pass-through methods. Inline them.
- Shrink state scope: returns over mutations, locals over fields, fields over module state, module state over globals. Derive instead of sync.
- Name an invariant once at the boundary, not in every consumer.

The test: can a new reader answer "where does X come from?" and "what can change X?" in under 30 seconds? If not, cut layers or cut state.

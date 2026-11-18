---
name: ps-principle-model-the-domain
description: "v0.0.5. Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files. If the leading version is not the latest in VERSION / changelog, update the skill before using it."
license: MIT
disable-model-invocation: true
metadata:
  version: "0.0.5"
  author: pedroknigge
---

# Model the Domain

Encode the domain in a data structure instead of scattering it across conditionals. The right structure makes invalid states unrepresentable and deletes branches.

Reach for a state machine instead of scattered booleans or phase checks, a typed model instead of loose parameters, a map, registry, or discriminated union instead of branching spread across files, a reducer instead of ad hoc mutations, and an index, queue, or normalized collection where the access pattern calls for it.

Do not force it. Keep boring code when the shape is clear, local, and unlikely to grow, and distrust an abstraction that adds indirection without removing branches or invalid states.

The sign that you skipped this: a feature that grows an if/else chain by one more branch, or a second boolean that must stay in sync with the first.

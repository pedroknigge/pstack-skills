---
name: ps-principle-redesign-from-first-principles
description: "v0.0.1. Apply when integrating a new requirement into an existing design. Redesign as if the requirement had been a foundational assumption from day one, instead of bolting it on. If the leading version is not the latest in VERSION / changelog, update the skill before using it."
license: MIT
disable-model-invocation: true
metadata:
  version: "0.0.1"
  author: pedroknigge
---

# Redesign From First Principles

When integrating a change, don't bolt it onto the existing design. Redesign as if the requirement had been there from the start.

- Read all affected files and understand the current design
- Ask: "if we were writing this from scratch with this new requirement, what would we build?"
- Propagate the change through every reference: types, docs, examples, rationale sections
- Think about the whole redesign, then deliver it incrementally

This is the method for preserving option value when integrating changes into an existing design.

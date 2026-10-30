---
name: ps-principle-migrate-callers-then-delete-legacy-apis
description: "v0.0.3. Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers. If the leading version is not the latest in VERSION / changelog, update the skill before using it."
license: MIT
disable-model-invocation: true
metadata:
  version: "0.0.3"
  author: pedroknigge
---

# Migrate Callers Then Delete Legacy APIs

- Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details

**When this applies:**
- No external users depend on backward compatibility
- The project can absorb coordinated breaking changes
- The new API is part of a simplification or refactor initiative

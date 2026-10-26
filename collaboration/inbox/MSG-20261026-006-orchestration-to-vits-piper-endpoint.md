---
id: MSG-20261026-006
from: orchestration
to: vits-piper-endpoint
date: 2026-10-26
subject: Vits-piper endpoint contract (generation deferred)
status: open
priority: normal
task: TASK-0007
in_reply_to: null
refs: ["docs/01-architecture.md"]
---

# Context

The runtime model and phonemizer config must be hash-identical to the training
bundle. The staging repo is private; public promotion is a later gate.

# Ask

Start `TASK-0007` with the contract only:

- document `version-manifest.json`, `phoneme/phonemizer-config.json`, model
  ONNX + `.onnx.json`;
- write the generation script and the map/dictionary hash-equality test;
- do not generate a staging tree until the first model release.

# Inputs

- archive `vits-piper` at `ae19f11`
- training bundle from `TASK-0004` when available

# Acceptance

Contract and script documented; hash-equality test defined; no Pages on the
private repo.

# Report

Reply with the contract path and the exact hashes that must match between
training and runtime. Confirm the `vector-index/` location; do not move it
without an ADR.

# Constraints

No public promotion. No training. No app changes.

# vits-piper (OC staging endpoint)

Private staging repository for the public model/phonemizer endpoint consumed by
SuttaPlayer.

**Status:** scaffolded · **Owner:** endpoint domain agent · **Task:**
`TASK-0007`

## Contract

Generated from a model release:

- `version-manifest.json`
- `phoneme/phonemizer-config.json` — map + dictionary references
- model ONNX + `.onnx.json` config

The model config, training map and endpoint phonemizer map must be
hash-identical. No hand edits.

## Publishing

`vits-piper-oc` is private staging. Public promotion to
`dhamma-initiative/vits-piper` is a gated release step (G5). GitHub Pages is
not enabled on the private repo.

## Confirmed contract

`vector-index/` stays in `suttas`; this endpoint carries only the model and
runtime phonemizer config. See `ADR-0005` in the orchestration repo.

## Collaboration

- `collaboration/inbox/` — director → agent
- `collaboration/sent/` — agent → director

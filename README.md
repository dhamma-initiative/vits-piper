# vits-piper — voice and phonemizer endpoint for SuttaPlayer

This repository is the public, static voice endpoint consumed by the SuttaPlayer
PWA (`sp3-nb`). It owns the Piper voice models and the runtime phonemizer
configuration. The suttas-owned phoneme maps and version metadata are hydrated
from a published
[`dt.o-suttas-builder`](https://github.com/dhamma-initiative/dt.o-suttas-builder)
release.

## Layout

- `model/` — Piper ONNX voice models and model configs. Owned by this repository.
- `phoneme/phonemizer-config.json` — generated runtime config used by the PWA.
  It pins the public `suttas` phoneme-map URLs and SHA-256 digests.
- `training/suttas/` — hydrated suttas inputs:
  - `phoneme/` — English and Pali IPA maps from the builder release.
  - `version-manifest.json` — source build version.
  - `verification-report.json` and `source-sync-report.json` — release evidence.
  - `release-manifest.json` — provenance for the hydrated inputs.
- `training/config/`, `training/corpus/` — frozen training inputs for the
  current model. These are not overwritten by hydration.
- `version-manifest.json` — model/corpus/source version metadata.
- `hydrate.json` — the builder hydration manifest for the suttas-owned inputs.

## Source of truth

There are two ownership boundaries:

1. **Suttas inputs** are owned by `dt.o-suttas-builder`. They are hydrated from
   the builder release and must not be edited by hand.
2. **Voice models and training artifacts** are owned by `vits-piper`. Hydration
   never replaces `model/`, `training/config/`, or `training/corpus/`.

The hydration manifest is:

```json
{
  "mappings": [
    { "from": "build/phoneme", "to": "training/suttas/phoneme", "mode": "replace" },
    { "from": "build/version-manifest.json", "to": "training/suttas/version-manifest.json", "mode": "file" }
  ],
  "provenanceFile": "training/suttas/release-manifest.json",
  "post": [
    { "command": "python3", "args": ["scripts/generate_phoneme_config.py", "--suttas-dir", "training/suttas"] }
  ],
  "pages": { "branch": "{branch}", "path": "/" }
}
```

The post-hydrate step regenerates `phoneme/phonemizer-config.json` from the
hydrated maps. Do not hand-edit that file.

## Publishing a release

### Recommended: publish from the builder

Publish the matching `suttas` endpoint first, then `vits-piper`:

```bash
cd /home/ash/dev/di/dt.o-suttas-builder

deno run -A tool/publish-suttaplayer.ts --version 261020 \
  --suttas-branch 261020 \
  --vits-piper-branch ver2-261020-9429 \
  --commit --push --pages
```

Publish only this endpoint:

```bash
cd /home/ash/dev/di/dt.o-suttas-builder

deno run -A tool/publish-suttaplayer.ts --version 261020 \
  --targets vits-piper \
  --vits-piper-branch ver2-261020-9429 \
  --commit --push --pages
```

For a new model branch, add `--create-branch` the first time.

### Direct hydration

Use this when the builder release already exists and `suttas` has already been
published:

```bash
cd /home/ash/dev/di/dt.o-suttas-builder

deno run -A tool/0.pipeline.ts hydrate --version 261020 \
  --target ../vits-piper \
  --commit --push --pages
```

The target worktree must have no tracked changes. Untracked files are allowed.
Use `--force` only when you intentionally want to override tracked changes.

### Regenerate the runtime config manually

From the `vits-piper` repository root:

```bash
python3 scripts/generate_phoneme_config.py --suttas-dir training/suttas
```

Verify the generated hashes against the public `suttas` endpoint:

```bash
python3 scripts/generate_phoneme_config.py --suttas-dir training/suttas --check-remote
```

The generator reads `version-manifest.json` for the model version and writes
`phoneme/phonemizer-config.json`. See `scripts/README.md` for all arguments and
the generated fields.

### GitHub Pages

The Pages source is the model branch (`ver2-261020-9429`) at `/`. The builder
updates it with the GitHub Pages REST API when `--pages` is supplied. If Pages is
not enabled, the builder creates it. The token needs Pages write permission.

## Deployment order

The runtime config pins the `suttas` map hashes, so the order matters:

1. Publish the `dt.o-suttas-builder` release.
2. Hydrate and publish `suttas`.
3. Hydrate `vits-piper` and regenerate `phoneme/phonemizer-config.json`.
4. Publish `vits-piper`.
5. Optionally verify with `--check-remote`.

Publishing `vits-piper` before `suttas` can leave the runtime config pointing at
map hashes that are not yet live.

## Verification

Check the public endpoint:

```bash
curl -fsSL https://dhamma-initiative.github.io/vits-piper/version-manifest.json
curl -fsSL https://dhamma-initiative.github.io/vits-piper/phoneme/phonemizer-config.json
```

The `english_ipa_map.sha256` and `pali_ipa_map.sha256` values must match the
hydrated files under `training/suttas/phoneme/`.

## Training

The current model is `ver2-261020-9429`, trained from the frozen `261020`
corpus. See:

- `training/README.md` — corpus, training run, and frozen artifact hashes.
- `training/manifest.md` — selected checkpoint, AB evidence, and model hashes.
- `scripts/README.md` — runtime config generator and UAT verification corpus
  generator.

## Consumers

`sp3-nb` uses:

- `https://dhamma-initiative.github.io/vits-piper/` as `endpoints.ttsBase`
- `phoneme/phonemizer-config.json` for runtime phonemization
- `model/en_gb-suttaplayer-medium-quant.onnx` and its config for the default
  quantized voice
- `model/en_gb-suttaplayer-medium.onnx` and its config for the full-fidelity
  voice
- `version-manifest.json` for model/cache metadata

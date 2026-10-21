# Runtime phonemizer config generator

`generate_phoneme_config.py` builds `../phoneme/phonemizer-config.json` from a
local `suttas` checkout. It computes the map digests and records the suttas
source/build versions, so the runtime config never contains hand-copied hashes.

## Prerequisites

- Python 3.10 or newer.
- A sibling `suttas` checkout by default:

```text
dev/di/
├── suttas/
│   ├── version-manifest.json
│   └── phoneme/
│       ├── pho_en[gb]-to-espeak-v1.51-ipa.json
│       └── pho_pi[si]-to-aksharamukha-2.1.0-ipa.json
└── vits-piper/
    ├── version-manifest.json
    └── scripts/generate_phoneme_config.py
```

## Usage

From the `vits-piper` repository root:

```bash
python3 scripts/generate_phoneme_config.py
```

This writes `phoneme/phonemizer-config.json` and reads the model version from
`version-manifest.json` (`modelVersion`, falling back to `version`).

Verify the generated hashes against the public artifacts:

```bash
python3 scripts/generate_phoneme_config.py --check-remote
```

For the current model:

```bash
python3 scripts/generate_phoneme_config.py \
  --suttas-dir ../suttas \
  --model-version ver2-261020-9429 \
  --check-remote
```

## CLI arguments

| Argument | Default | Description |
| --- | --- | --- |
| `--suttas-dir PATH` | `../suttas` | Local `suttas` checkout containing `version-manifest.json` and `phoneme/`. |
| `--base-url URL` | `https://dhamma-initiative.github.io/suttas/` | Public base URL written into the map dependencies. |
| `--model-version VERSION` | `version-manifest.json` `modelVersion` | Value written to the runtime config's `modelVersion`. |
| `--output PATH` | `phoneme/phonemizer-config.json` | Destination config file. |
| `--check-remote` | off | Download both public maps and verify their SHA-256 values. |

## Generated fields

- `schemaVersion`: must be `1` for the current runtime loader.
- `modelVersion`: model/cache key used by the PWA TTS service.
- `english_ipa_map` / `pali_ipa_map`:
  - `url`: public copy of the map.
  - `sha256`: digest of the local map file.
  - `sourceVersion`: suttas `version` (for example `2610.20.00`).
  - `sourceBuildVersion`: suttas `buildVersion` (for example `261020`).
- Phonemizer transformation rules, tokenizer flag, strict mode, custom
  phonemes, and invalid-term fallback.

The transformation rules live in `generate_phoneme_config.py`. Edit them there,
then regenerate; do not hand-edit the generated config.

## Deployment order

The runtime config pins the `suttas` map hashes. Publish the matching `suttas`
build first, then publish `vits-piper`:

1. Update/verify the local `suttas` checkout.
2. Regenerate this config.
3. Deploy `suttas`.
4. Deploy `vits-piper`.
5. Run `--check-remote` to confirm the public maps match.

`__pycache__/` is ignored by the repository.

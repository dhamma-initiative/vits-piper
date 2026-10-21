# Utility scripts

## Runtime phonemizer config generator

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

## UAT verification corpus generator

`generate_uat_verification.py` builds a vocabulary-verification corpus from
natural sutta prose. For every transliteration-list entry it selects a real
sentence or clause containing the term, synthesizes one WAV, and writes a
2-column LJSpeech metadata file:

```text
wav_name.wav|Natural sentence containing the target term.
```

Filenames include the target, for example `EN_00042_dhamma.wav` or
`PI_00107_sutta.wav`. The accompanying `uat-verification-manifest.csv` records
the target, language, source text file, fallback use, phonemes, and duration.

### Prerequisites

- Python 3.10 or newer with `numpy`, `onnxruntime`, and `soundfile`.
- The `piper` Python package, or `PIPER_SRC` pointing at its `src/` directory.
- A sibling `dt.o-suttas-builder` checkout with `build/text/` and
  `build/vocabulary/`.
- A sibling `suttas` checkout with `phoneme/`, or `--en-map` / `--pi-map`.
- The model and config in `../model/`.

### Usage

From `vits-piper/tmp/`:

```bash
python3 ../scripts/generate_uat_verification.py \
  --model ../model/en_gb-suttaplayer-medium.onnx \
  --config ../model/en_gb-suttaplayer-medium.onnx.json \
  --out-dir ./uat-verification-enpi
```

Start with a small review batch:

```bash
python3 ../scripts/generate_uat_verification.py \
  --model ../model/en_gb-suttaplayer-medium.onnx \
  --config ../model/en_gb-suttaplayer-medium.onnx.json \
  --out-dir ./uat-verification-enpi \
  --limit 20
```

Inspect the selection without synthesizing:

```bash
python3 ../scripts/generate_uat_verification.py --dry-run --limit 20 \
  --out-dir ./uat-verification-enpi
```

Continue a partial run, or generate only Pali targets:

```bash
python3 ../scripts/generate_uat_verification.py --resume \
  --model ../model/en_gb-suttaplayer-medium.onnx \
  --config ../model/en_gb-suttaplayer-medium.onnx.json \
  --out-dir ./uat-verification-enpi

python3 ../scripts/generate_uat_verification.py --language pi \
  --model ../model/en_gb-suttaplayer-medium.onnx \
  --config ../model/en_gb-suttaplayer-medium.onnx.json \
  --out-dir ./uat-verification-pi
```

Review with the existing server:

```bash
python3 ../../../tts/en-pi/scripts/review_corpus_server.py \
  -i ./uat-verification-enpi/metadata-uat-verification-enpi.csv \
  -w ./uat-verification-enpi/wavs/
```

### Output

```text
OUT/
├── metadata-uat-verification-enpi.csv
├── uat-verification-manifest.csv
└── wavs/
    ├── EN_00000_the.wav
    └── ...
```

`--start` and `--limit` select a stable slice using indices from the full
language list. `--resume` reuses valid existing WAVs. The metadata is rewritten
for the selected slice on each run.

### Selection rules

- Candidate utterances come from `build/text/**/*.txt`, not from concatenated
  vocabulary columns.
- Full sentences are preferred; clauses are used only when a sentence is too
  long.
- Headings, all-caps text, unbalanced quotes, and lines without the target are
  penalized.
- Inflected variants are accepted when they share the target stem.
- Terms with no source occurrence use a short carrier:
  `The term is <term>.` Use `--fallback skip` to omit them instead.
- Pali targets are currently demonstrated in English sutta prose that uses the
  Pali term. A separate grammatical Pali source corpus would be required for
  Pali-only sentences.

### CLI arguments

| Argument | Default | Description |
| --- | --- | --- |
| `--text-root PATH` | sibling `dt.o-suttas-builder/build/text` | Source `.txt` tree. |
| `--en-vocab PATH` | sibling `.../english-transliteration-freq-list.csv` | English vocabulary CSV. |
| `--pi-vocab PATH` | sibling `.../pali-transliteration-freq-list.csv` | Pali vocabulary CSV. |
| `--language {both,en,pi}` | `both` | Target languages. |
| `--out-dir PATH` | `uat-verification-enpi` | Output directory. |
| `--metadata PATH` | `OUT/metadata-uat-verification-enpi.csv` | LJSpeech metadata path. |
| `--manifest PATH` | `OUT/uat-verification-manifest.csv` | Detailed manifest path. |
| `--model PATH` | `model/en_gb-suttaplayer-medium.onnx` | Piper ONNX model. |
| `--config PATH` | `model/en_gb-suttaplayer-medium.onnx.json` | Piper model config. |
| `--phonemizer-config PATH` | `phoneme/phonemizer-config.json` | Runtime phonemizer rules. |
| `--en-map PATH` | sibling `suttas/phoneme/...` | English IPA map. |
| `--pi-map PATH` | sibling `suttas/phoneme/...` | Pali IPA map. |
| `--start N` | `0` | First target index. |
| `--limit N` | `0` | Maximum targets; `0` means all. |
| `--resume` | off | Reuse valid existing WAVs. |
| `--dry-run` | off | Report selection only. |
| `--min-words N` | `5` | Minimum words per utterance. |
| `--max-words N` | `28` | Maximum words per utterance. |
| `--max-chars N` | `240` | Maximum characters per utterance. |
| `--fallback {carrier,skip}` | `carrier` | Behavior when no source sentence contains the term. |
| `--warmup N` | `2` | Discarded model warm-up runs. |
| `--provider NAME` | `CPUExecutionProvider` | ONNX Runtime provider. |
| `--length-scale F` | model config | Piper duration scale. |
| `--noise-scale F` | model config | Piper noise scale. |
| `--noise-w F` | model config | Piper noise width. |
| `--subtype NAME` | `PCM_16` | WAV subtype. |
| `--progress-every N` | `100` | Progress interval. |

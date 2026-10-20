# SuttaPlayer TTS Model Manifest

- Generated: `2026-10-20T23:39:13Z`
- Model version: `ver2-261020-9429`
- Corpus version: `261020`
- Selected checkpoint: `epoch=9429-val_mel=0.2833.ckpt`
- Export directory: `/content/drive/MyDrive/sutta-tts-model-training/models/ver2-9429`
- Runtime config `modelVersion`: `ver2-261020-9429`

## Decision

Candidate checkpoints retained from this training run (3):

- `epoch=9253-val_mos=0.0000.ckpt`: epoch `9253`, val_mos `0.0`
- `epoch=9321-val_mel=0.2820.ckpt`: epoch `9321`, val_mel `0.282`
- `epoch=9429-val_mel=0.2833.ckpt`: epoch `9429`, val_mel `0.2833`

Selected over the `9321` checkpoint because the fixed-seed paired AB favored it on all three objective metrics and listening tests preferred it; `9321` had audible sibilant distortion. The `9253` checkpoint had `val_mos=0.0000` and was not AB-evaluated. `9429` has a marginally higher `val_mel` than `9321`, so the decision is based on paired/perceptual evidence rather than the validation label alone.

Paired AB used 99 validation utterances, split seed `0`, inference seed `1234`, 2 inference seeds per utterance. Report recommendation: `epoch=9429-val_mel=0.2833.ckpt`.

### Candidate checkpoints

| Checkpoint | Epoch | val_mel | val_mos | Size | AB role | Decision |
|---|---:|---:|---:|---:|---|---|
| `epoch=9253-val_mos=0.0000.ckpt` | 9253 | — | 0.0000 | 806.7 MiB | — | candidate, not selected |
| `epoch=9321-val_mel=0.2820.ckpt` | 9321 | 0.2820 | — | 806.7 MiB | A | candidate, not selected |
| `epoch=9429-val_mel=0.2833.ckpt` | 9429 | 0.2833 | — | 806.7 MiB | B | **selected** |
| `epoch=9713-val_mel=0.2950.ckpt` | 9713 | 0.2950 | — | 806.7 MiB | — | historical (ver1) |

## Objective AB evidence

| Checkpoint | Role | mel_l1_dtw | mfcc_dtw_l2 | dur_abs_log |
|---|---|---:|---:|---:|
| `epoch=9321-val_mel=0.2820.ckpt` | A | 0.318243 | 19.075948 | 0.031317 |
| `epoch=9429-val_mel=0.2833.ckpt` | B | 0.311828 | 18.467527 | 0.022412 |

- `mel_l1_dtw`: B better
- `mfcc_dtw_l2`: B better
- `dur_abs_log`: B better

AB report: `/content/drive/MyDrive/sutta-tts-model-training/models/model-ab-report.json` (21.1 KiB, `8536094d450ae655f1072f5de28f634e7d69c5fe2eb6ee2f17aa69d9c3547702`).

## Selected export artifacts

| Artifact | Size | SHA-256 |
|---|---:|---|
| `en_gb-suttaplayer-medium-quant.onnx` | 18.5 MiB | `628bc657ecf2a593d38325c412912d6382003f36da6a788e98302fe6e392e1a9` |
| `en_gb-suttaplayer-medium-quant.onnx.json` | 5.2 KiB | `d45cc4621779432bf6dc4bd700451405ad21eda076885e07446315ddd0683fe8` |
| `en_gb-suttaplayer-medium.onnx` | 60.6 MiB | `362c3f42dbb2e25de6cbbb20108ceaa8e9ce3473bcc6ce52041fd8bb98d3a51e` |
| `en_gb-suttaplayer-medium.onnx.json` | 5.2 KiB | `d45cc4621779432bf6dc4bd700451405ad21eda076885e07446315ddd0683fe8` |

## Training inputs

| Input | Rows | Size | SHA-256 | Expected |
|---|---:|---:|---|---|
| `metadata-text-enpi.csv` | 999 | 103.8 KiB | `ca7710cba8f1bd5e56842cee7bb2bff6a034a652d744adcd6003befb45ae08b9` | match |
| `metadata-phonemes-enpi.csv` | 999 | 158.8 KiB | `fb6eb170832e08ddbd8c11d0a3e6b166b9fbfee1fdbadcc0363b73cd9fd429df` | match |
| `espeak-v1.51[en-gb]_aksharamukha-2.1.0[pi]-map.json` | 480 | 6.4 KiB | `02529f3ee0dcb344ae84291b288a608ed4290be21cefb4e976d69264d47db701` | match |

### Training bundle

- Expected archive: `tts-en-pi-261020-training.tgz`
- Expected location: `release/tts-en-pi-261020-training.tgz`
- Located at: not present in this workspace
- Recorded SHA-256: `2cccf18401586146afa7b2a000ec02e851ae3ea22ea1fb0a1fc855f445d20bf9`

### Training config

| Config | SHA-256 |
|---|---|
| `applio_settings-en.json` | `7351c6cc5aef8199b05a0994b8dc83fb52a5a4d944197cb7772cebdee0308920` |
| `aud_punc_dur_targ.json` | `80d10e1a4a1d8a423f029d38ac0ab05318c98b29c9f119d3b33dd62b5a92ba8c` |
| `espeak-v1.51[en-gb]_aksharamukha-2.1.0[pi]-map.json` | `02529f3ee0dcb344ae84291b288a608ed4290be21cefb4e976d69264d47db701` |
| `g2p_blacklist_en.json` | `8eb95bcbc154530931e15fc418c8b1fe991095671409552099ea1aa596999ede` |
| `g2p_overrides_en.json` | `8eb95bcbc154530931e15fc418c8b1fe991095671409552099ea1aa596999ede` |
| `pho_en[gb]-to-espeak-v1.51-ipa.json` | `7e550320f8ec76134175541fa366225f78f598dd78a5e38c34d1a1ce8e58ef72` |
| `pho_pi[si]-to-aksharamukha-2.1.0-ipa.json` | `23b0aea76ec057288c7ec2f5b85620cc7ce9e92e25a3422af3c8679edf66713d` |

## Provenance

- Training repo branch: `rtx3050-trials`
- Training repo commit: `bb502f70fff144b0cb5f658124c794506dc1b3b1`
- vits-piper branch: `ver2-261020-9429`
- vits-piper commit: `48ecc4800a5e6d931c9ac7870d2efa67a104fb34`
- Manifest script: `scripts/sutta-model-manifest.py`

## Reproduce

```bash
python3 scripts/sutta-model-ab.py --split-seed 0 --seed 1234 --seeds 2
python3 scripts/sutta-model-manifest.py --selected-checkpoint 'epoch=9429-val_mel=0.2833.ckpt' --model-version 'ver2-261020-9429'
```


# EN-PI Corpus Integrity Audit

Generated: 2026-10-20T09:05:33+00:00
Root: `/home/ash/dev/tts/en-pi`
Verdict: **PASS**

## Counts

- Accepted: 999
- Rejected: 53
- Final text: 999
- Final phonemes: 999
- Map symbols: 172
- Map IDs defined: 172
- Release WAVs: 1052
- Audio-dir WAVs: 1052
- Expected training WAVs: 999
- Training bundle WAVs: 999

## Checks

| Status | Check | Detail |
| --- | --- | --- |
| PASS | accepted CSV structure | 999 data rows, 2 fields each, UTF-8/CRLF |
| PASS | rejected CSV structure | 53 data rows, 2 fields each, UTF-8/CRLF |
| PASS | text CSV structure | 999 data rows, 2 fields each, UTF-8/LF |
| PASS | phoneme CSV structure | 999 data rows, 2 fields each, UTF-8/LF |
| PASS | accepted IDs equal final text IDs and order | accepted=999, final_text=999, exact_order=True |
| PASS | final text IDs equal final phoneme IDs and order | text=999, phonemes=999, exact_order=True |
| PASS | accepted IDs unique | 999 unique IDs |
| PASS | rejected IDs unique | 53 unique IDs |
| PASS | text IDs unique | 999 unique IDs |
| PASS | phonemes IDs unique | 999 unique IDs |
| PASS | accepted and rejected IDs disjoint | no overlap |
| PASS | no empty text or phoneme rows | empty_text=0, empty_phonemes=0 |
| PASS | phoneme map JSON object of symbol -> integer ID | 172 symbols |
| PASS | phoneme map IDs unique and contiguous from 0 | min=0, max=171, unique=172, count=172 |
| PASS | every corpus phoneme character exists in map | 72 used characters, all mapped |
| PASS | phoneme strings are NFD-normalized | all NFD |
| PASS | no control characters in phoneme strings | none |
| PASS | no digit characters in phoneme strings | none |
| PASS | no literal ampersand in phoneme strings | none |
| PASS | text ampersands rendered as a spoken 'and' | 265 text rows contain &; all have spoken and |
| PASS | sidecar IDs match final text prefix | sidecar=999, final=999, prefix_match=True |
| PASS | sidecar has no extra records | none |
| PASS | sidecar text matches final text | all match |
| PASS | sidecar tokens reconstruct phoneme strings | all match |
| PASS | sidecar IDs equal map lookup of tokens | all match |
| PASS | release contains all accepted WAVs | 999 accepted present |
| PASS | release has expected UAT inventory | 53 extra WAVs, 53 rejected, 0 unexpected; expected UAT superset |
| PASS | release extras equal rejected set | extras=53, rejected=53, exact=True |
| PASS | audio dir contains all accepted WAVs | 999 accepted present |
| PASS | audio dir has expected UAT inventory | 53 extra WAVs, 53 rejected, 0 unexpected; expected UAT superset |
| PASS | audio dir extras equal rejected set | extras=53, rejected=53, exact=True |
| SKIP | release phoneme metadata matches final phoneme CSV | sha256 release=ab91c6160e3850bd, final=fb6eb170832e08dd; v1.1.0 is historical and predates the approved one-row phoneme cleanup |
| PASS | UAT release README is historical | contains historical 260808 reference |
| PASS | training bundle WAV inventory is exactly accepted | bundle=999, accepted=999, rejected=0 |
| PASS | training bundle metadata-text-enpi.csv matches source | metadata-text-enpi.csv |
| PASS | training bundle metadata-phonemes-enpi.csv matches source | metadata-phonemes-enpi.csv |
| PASS | training bundle phoneme-map.json matches source | phoneme-map.json |
| PASS | training bundle README is current | README documents 261020 and 999 utterances |
| PASS | training bundle has manifest and WAV hashes | manifest=True, wav_hashes=True |
| PASS | accepted WAVs readable with valid headers | 999 files read |
| PASS | accepted WAV format is consistent | formats={(1, 2, 22050): 999} |
| PASS | training config records builder commit | commit=a90f56440eb9f51b21b5588f559af7a2dfb6b54b |
| PASS | training config pins ampersand preprocess | 7 rules; amp_rule=True |
| PASS | config path exists: phoneme_id_map | ./config/espeak-v1.51[en-gb]_aksharamukha-2.1.0[pi]-map.json |
| PASS | config path exists: english_ipa_map | ./config/pho_en[gb]-to-espeak-v1.51-ipa.json |
| PASS | config path exists: pali_ipa_map | ./config/pho_pi[si]-to-aksharamukha-2.1.0-ipa.json |
| PASS | input-research books use 261020 stable names | no stale names |
| PASS | README documents current 261020 corpus | current section and training bundle present |

## Packaging

- `release/` and `build/4.enh/` are the historical UAT supersets: 1052 WAVs = 999 accepted plus 53 rejected.
- The clean training bundle contains exactly 999 accepted WAVs and excludes all rejected audio.
- The 999-row phoneme metadata references accepted IDs only.

## Map Coverage

- Used corpus characters: 72
- Map symbols unused by this corpus: 100
- Contains U+0303: True (24 uses)
- Contains U+0361: True (134 uses)

## Notes

- The sidecar contains exactly the 999 accepted records; the builder trailing-newline bug is fixed upstream and the stale empty record was removed.
- Final phonemes were regenerated with the pinned preprocess; the single leading-colon artifact in `KN_Ud_ud8_6_0069.wav` was removed.
- `v1.1.0` remains the historical 1052-WAV UAT archive; the 261020 training bundle is the clean 999-WAV artifact.
- The 100 unused map symbols are reserved or coverage headroom, not a corpus defect.

## Boundary

This audit is read-only. It does not regenerate text, phonemes, audio, or UAT data.
Packaging checks are separate from core corpus and map integrity.

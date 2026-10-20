# Piper1-gpl VITS english\pali training project

## Model manifest

See `training/manifest.md` for the selected model, candidate checkpoints, AB evidence, and artifact hashes.

## Current corpus (261020)

- Source books: `261020` stable names under `input-research/books/`
- Builder: `a90f564` on branch `261020`
- Training corpus: 999 accepted utterances
- Excluded: 53 rejected UAT utterances
- Clean training bundle: `release/tts-en-pi-261020-training.tgz`
- Integrity audit: `corpus/wip.2/report/corpus-integrity-audit-261020.md`
- Build command: `python3 scripts/build_training_bundle.py`
- Audit command: `python3 scripts/audit_corpus_integrity.py`

## Training run (261020)

- Status: training started 2026-10-20
- Corpus: 999 accepted / 53 rejected
- Frozen bundle: `release/tts-en-pi-261020-training.tgz`
- Bundle SHA-256: `2cccf18401586146afa7b2a000ec02e851ae3ea22ea1fb0a1fc855f445d20bf9`
- `corpus/metadata-text-enpi.csv` SHA-256: `ca7710cba8f1bd5e56842cee7bb2bff6a034a652d744adcd6003befb45ae08b9`
- `corpus/metadata-phonemes-enpi.csv` SHA-256: `fb6eb170832e08ddbd8c11d0a3e6b166b9fbfee1fdbadcc0363b73cd9fd429df`
- Training phoneme map (`di/vits-piper/training/phoneme/en[gb]_pi[si]-suttaplayer-phoneme-map.json`) SHA-256: `02529f3ee0dcb344ae84291b288a608ed4290be21cefb4e976d69264d47db701`
- Integrity audit: PASS 47 / WARN 0 / FAIL 0 / SKIP 1
- Historical UAT archive: `release/tts-en-pi-v1.1.0.tgz` (1,052 WAVs; not used for training)

The corpus and bundle above are frozen for this run. Rebuild them only for a new training run. The release bundle is gitignored; the hashes identify the exact artifact consumed by training.

The build log below is retained for historical provenance. It references older `260808`/`260914` paths, which are not the current corpus inputs.

## Input research

acquire the following input research structure:

```bash
ash@kassapa-l:~/dev/tts/en-pi$ tree input-research/
input-research/
├── ALL-suttas-text-characterset-report.json
├── ALL-suttas-text-characterset-report.md
├── books
│   ├── AN-book-with-file-hdrs.txt
│   ├── DN-book-with-file-hdrs.txt
│   ├── KN_Dhp-book-with-file-hdrs.txt
│   ├── KN_Iti-book-with-file-hdrs.txt
│   ├── KN_Khp-book-with-file-hdrs.txt
│   ├── KN_StNp-book-with-file-hdrs.txt
│   ├── KN_Thag-book-with-file-hdrs.txt
│   ├── KN_Thig-book-with-file-hdrs.txt
│   ├── KN_Ud-book-with-file-hdrs.txt
│   ├── MN-book-with-file-hdrs.txt
│   └── SN-book-with-file-hdrs.txt
├── english-transliteration-freq-list.csv
├── number-freq-list.csv
├── pali-ipa-freq-list.csv
├── pali-transliteration-freq-list.csv
└── sutta-words-freq-list.csv
```

the source applio\rvc model:

```bash
ash@kassapa-l:~/dev/tts/en-pi$ tree suttas.eng.lang-audio/
suttas.eng.lang-audio/
├── applio-model
│   ├── suttas_eng_lang_350e_90300s.pth
│   ├── suttas_eng_lang.index
│   └── suttas_eng_lang.tgz
├── Applio-prep-HP-norm-after-uvr5.txt
├── audacity
│   ├── export.step1
│   │   ├── suttas-set10.wav
│   │   ├── suttas-set11.wav
│   │   ├── suttas-set12.wav
│   │   ├── suttas-set13.wav
│   │   ├── suttas-set14.wav
│   │   ├── suttas-set15.wav
│   │   ├── suttas-set16.wav
│   │   ├── suttas-set17.wav
│   │   ├── suttas-set18.wav
│   │   ├── suttas-set19.wav
│   │   ├── suttas-set1.wav
│   │   ├── suttas-set2.wav
│   │   ├── suttas-set3.wav
│   │   ├── suttas-set4.wav
│   │   ├── suttas-set5.wav
│   │   ├── suttas-set6.wav
│   │   ├── suttas-set7.wav
│   │   ├── suttas-set8.wav
│   │   └── suttas-set9.wav
│   ├── macro-output
│   │   ├── 1_suttas-set10_(No Reverb).wav
│   │   ├── 1_suttas-set11_(No Reverb).wav
│   │   ├── 1_suttas-set12_(No Reverb).wav
│   │   ├── 1_suttas-set13_(No Reverb).wav
│   │   ├── 1_suttas-set14_(No Reverb).wav
│   │   ├── 1_suttas-set15_(No Reverb).wav
│   │   ├── 1_suttas-set16_(No Reverb).wav
│   │   ├── 1_suttas-set17_(No Reverb).wav
│   │   ├── 1_suttas-set18_(No Reverb).wav
│   │   ├── 1_suttas-set19_(No Reverb).wav
│   │   ├── 1_suttas-set1_(No Reverb).wav
│   │   ├── 1_suttas-set2_(No Reverb).wav
│   │   ├── 1_suttas-set3_(No Reverb).wav
│   │   ├── 1_suttas-set4_(No Reverb).wav
│   │   ├── 1_suttas-set5_(No Reverb).wav
│   │   ├── 1_suttas-set6_(No Reverb).wav
│   │   ├── 1_suttas-set7_(No Reverb).wav
│   │   ├── 1_suttas-set8_(No Reverb).wav
│   │   └── 1_suttas-set9_(No Reverb).wav
│   └── source-aup3
│       ├── suttas-set10.aup3
│       ├── suttas-set11.aup3
│       ├── suttas-set12.aup3
│       ├── suttas-set13.aup3
│       ├── suttas-set14.aup3
│       ├── suttas-set15.aup3
│       ├── suttas-set16.aup3
│       ├── suttas-set17.aup3
│       ├── suttas-set18.aup3
│       ├── suttas-set19.aup3
│       ├── suttas-set1.aup3
│       ├── suttas-set1b.aup3
│       ├── suttas-set2.aup3
│       ├── suttas-set3.aup3
│       ├── suttas-set4.aup3
│       ├── suttas-set5.aup3
│       ├── suttas-set6.aup3
│       ├── suttas-set7.aup3
│       ├── suttas-set8.aup3
│       └── suttas-set9.aup3
├── transcript-json
│   ├── suttas-set10.json
│   ├── suttas-set11.json
│   ├── suttas-set12.json
│   ├── suttas-set13.json
│   ├── suttas-set14.json
│   ├── suttas-set15.json
│   ├── suttas-set16.json
│   ├── suttas-set17.json
│   ├── suttas-set18.json
│   ├── suttas-set19.json
│   ├── suttas-set1.json
│   ├── suttas-set2.json
│   ├── suttas-set3.json
│   ├── suttas-set4.json
│   ├── suttas-set5.json
│   ├── suttas-set6.json
│   ├── suttas-set7.json
│   ├── suttas-set8.json
│   └── suttas-set9.json
├── transcript-text
│   ├── ashinw.list.txt
│   ├── suttas-set10.txt
│   ├── suttas-set11.txt
│   ├── suttas-set12.txt
│   ├── suttas-set13.txt
│   ├── suttas-set14.txt
│   ├── suttas-set15.txt
│   ├── suttas-set16.txt
│   ├── suttas-set17.txt
│   ├── suttas-set18.txt
│   ├── suttas-set19.txt
│   ├── suttas-set1.txt
│   ├── suttas-set2.txt
│   ├── suttas-set3.txt
│   ├── suttas-set4.txt
│   ├── suttas-set5.txt
│   ├── suttas-set6.txt
│   ├── suttas-set7.txt
│   ├── suttas-set8.txt
│   ├── suttas-set9.txt
│   └── transcript.txt
└── uvr5
    ├── 1_suttas-set10_(No Reverb).wav
    ├── 1_suttas-set11_(No Reverb).wav
    ├── 1_suttas-set12_(No Reverb).wav
    ├── 1_suttas-set13_(No Reverb).wav
    ├── 1_suttas-set14_(No Reverb).wav
    ├── 1_suttas-set15_(No Reverb).wav
    ├── 1_suttas-set16_(No Reverb).wav
    ├── 1_suttas-set17_(No Reverb).wav
    ├── 1_suttas-set18_(No Reverb).wav
    ├── 1_suttas-set19_(No Reverb).wav
    ├── 1_suttas-set1_(No Reverb).wav
    ├── 1_suttas-set2_(No Reverb).wav
    ├── 1_suttas-set3_(No Reverb).wav
    ├── 1_suttas-set4_(No Reverb).wav
    ├── 1_suttas-set5_(No Reverb).wav
    ├── 1_suttas-set6_(No Reverb).wav
    ├── 1_suttas-set7_(No Reverb).wav
    ├── 1_suttas-set8_(No Reverb).wav
    └── 1_suttas-set9_(No Reverb).wav
```


python version

```bash
ash@kassapa-l:~/dev/tts/en-pi$ cat .python-version 
3.11.9
```

pyenv

```bash
ash@kassapa-l:~/dev/tts/en-pi$ source .venv-3.11.9/bin/activate
(.venv-3.11.9) ash@kassapa-l:~/dev/tts/en-pi$ pip freeze > requirements.txt
```

---

```bash
# -m debugpy --listen 5678 --wait-for-client

python scripts/generate_piper_enpi_harvest.py \
    --sutta_texts_path ./input-research/books/ \
    --char_anal ./input-research/ALL-suttas-text-characterset-report.json \
    --english_anal ./input-research/english-transliteration-freq-list.csv \
    --pali_anal ./input-research/pali-transliteration-freq-list.csv \
    --max_utt_char_length 180 \
    --contingency 0.20 \
    --repunct_spec ./corpus/wip.1/repunct-extraction-spec.json \
    -o ./corpus/harvest/260808-book-enpi-harvest-180.csv > ./corpus/harvest/report/260808-book-enpi-harvest-180.csv-generate_piper_enpi_harvest.py.stdout.md
    
--pali_boost 5.0 > ./corpus/wip.1/metadata-enpi-180-v1.0.csv-generate_piper_enpi_corpus.py.stdout.md

python scripts/generate_piper_enpi_corpus.py \
    --harvest ./corpus/harvest/260808-book-enpi-harvest-180.csv \
    --pali_anal ./input-research/pali-transliteration-freq-list.csv \
    --black_list ./corpus/metadata-enpi-180-v0.0-defects.csv \
    -o ./corpus/wip.1/metadata-enpi-180-v1.0.csv \
    -n 1000 \
    --decay_beta 0.40 \
    --pali_boost 10.0 > ./corpus/wip.1/report/metadata-enpi-180-v1.0.csv-generate_piper_enpi_corpus.py.stdout.md

#  ([,–:;—.?!•…])\s*— -> $1
cat ./corpus/wip.1/addendum-enpi-v1.0.csv ./corpus/wip.1/metadata-enpi-180-v1.0.csv > ./corpus/wip.1/metadata-enpi-180-plus-v1.0.csv


python scripts/assess_pali_coverage.py \
    -i ./corpus/wip.1/metadata-enpi-180-plus-v1.0.csv \
    -p ./input-research/pali-transliteration-freq-list.csv > ./corpus/wip.1/report/metadata-enpi-180-plus-v1.0.csv-assess_pali_coverage.py.stdout.md


python scripts/score_piper_enpi_corpus.py \
    -i ./corpus/wip.1/metadata-enpi-180-plus-v1.0.csv \
    -o ./corpus/wip.1/metadata-enpi-180-plus-v1.0.csv.scorecard.csv  > ./corpus/wip.1/report/metadata-enpi-180-plus-v1.0.csv-score_piper_enpi_corpus.py.stdout.md


python scripts/extract_corpus_entries.py \
  -i ./corpus/wip.1/metadata-enpi-180-plus-v1.0.csv \
  -e ./corpus/wip.1/repunct-extraction-spec.json \
  --depunct_output ./corpus/wip.1/metadata-enpi-180-plus-depunct-v1.0.csv \
  --repunct_output ./corpus/wip.1/metadata-enpi-180-plus-repunct-v1.0.csv 


deno -A ~/dev/di/dt.o-suttas-builder/tool/2.phonemize-sources-for-tts.ts \
  --config-override ./corpus/wip.1/phonemizer-config-260914-685617a.json

```

```bash
# -------- TEST
python scripts/piper_onnx_corpus_gen.py  \
  -i ./corpus/wip.1/260914-685617a/metadata-TEST-punct-v1.0.csv.pho  \
  -w ./build/1.tts/repunct  \
  -m /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx \
  -c /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx.json \
  -j ./config/aud_punc_dur_targ.json \
  -g ./config/g2p_overrides_en.json \
  --length_scale 1.25 \
  --skip_existing --read_as_ipa --repunct_min 600

# --- 

python scripts/piper_onnx_corpus_gen.py  \
  -i ./corpus/wip.1/260914-685617a/metadata-enpi-180-plus-depunct-v1.0.csv.pho  \
  -w ./build/1.tts  \
  -m /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx \
  -c /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx.json \
  -j ./config/aud_punc_dur_targ.json \
  -g ./config/g2p_overrides_en.json \
  --length_scale 1.25 \
  --skip_existing --read_as_ipa --repunct_min 1200

python scripts/piper_onnx_corpus_gen.py  \
  -i ./corpus/wip.1/260914-685617a/metadata-enpi-180-plus-repunct-v1.0.csv.pho  \
  -w ./build/1.tts/repunct  \
  -m /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx \
  -c /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx.json \
  -j ./config/aud_punc_dur_targ.json \
  -g ./config/g2p_overrides_en.json \
  --length_scale 1.25 \
  --skip_existing --read_as_ipa --repunct_min 600 --dry_run
```

```bash
#   DEPUNCT

ash@kassapa-l:~/dev/tts/en-pi$ ls -1 -S ./build/1.out.tts/raw_base_wavs/too-long/ > ./corpus/wip.1/split/depunct-too-long-files.csv

ash@kassapa-l:~/dev/tts/en-pi$ wc -l ./corpus/wip.1/metadata-enpi-180-plus-depunct-v1.0.csv
698 ./corpus/wip.1/metadata-enpi-180-plus-depunct-v1.0.csv

awk -F'|' '
BEGIN {
    while ((getline line < "./corpus/wip.1/split/depunct-too-long-files.csv") > 0) {
        sub(/\r$/, "", line);
        too_long[line] = 1;
    }
    close("./corpus/wip.1/split/depunct-too-long-files.csv");
}
{
    if ($1 in too_long) {
        print > "./corpus/wip.1/split/metadata-enpi-180-plus-SPL-2-depunct-v1.0.csv";
    } else {
        print > "./corpus/wip.1/split/metadata-enpi-180-plus-STD-2-depunct-v1.0.csv";
    }
}
' ./corpus/wip.1/metadata-enpi-180-plus-depunct-v1.0.csv

ash@kassapa-l:~/dev/tts/en-pi$ wc -l ./corpus/wip.1/split/metadata-enpi-180-plus-???-depunct-2-*.csv
   50 ./corpus/wip.1/split/metadata-enpi-180-plus-SPL-depunct-2-v1.0.csv
  673 ./corpus/wip.1/split/metadata-enpi-180-plus-STD-depunct-2-v1.0.csv
  723 total

#   REPUNCT

ash@kassapa-l:~/dev/tts/en-pi$ ls -1 -S ./build/1.out.tts/repunct/raw_base_wavs/too-long/ > ./corpus/wip.1/split/repunct-too-long-files.csv

ash@kassapa-l:~/dev/tts/en-pi$ wc -l ./corpus/wip.1/metadata-enpi-180-plus-repunct-v1.0.csv
375 ./corpus/wip.1/metadata-enpi-180-plus-repunct-v1.0.csv

awk -F'|' '
BEGIN {
    while ((getline line < "./corpus/wip.1/split/repunct-too-long-files.csv") > 0) {
        sub(/\r$/, "", line);
        too_long[line] = 1;
    }
    close("./corpus/wip.1/split/repunct-too-long-files.csv");
}
{
    if ($1 in too_long) {
        print > "./corpus/wip.1/split/metadata-enpi-180-plus-SPL-repunct-2-v1.0.csv";
    } else {
        print > "./corpus/wip.1/split/metadata-enpi-180-plus-STD-repunct-2-v1.0.csv";
    }
}
' ./corpus/wip.1/metadata-enpi-180-plus-repunct-v1.0.csv

ash@kassapa-l:~/dev/tts/en-pi$ wc -l ./corpus/wip.1/split/metadata-enpi-180-plus-???-repunct-2-*.csv
  116 ./corpus/wip.1/split/metadata-enpi-180-plus-SPL-repunct-2-v1.0.csv
   58 ./corpus/wip.1/split/metadata-enpi-180-plus-SPL-repunct-v1.0.csv
  317 ./corpus/wip.1/split/metadata-enpi-180-plus-STD-repunct-2-v1.0.csv
  491 total


deno -A ~/dev/di/dt.o-suttas-builder/tool/2.phonemize-sources-for-tts.ts \
  --config-override ./corpus/wip.1/split/phonemizer-config-260914-685617a.json

```

```bash
python scripts/piper_onnx_corpus_gen.py  \
  -i ./corpus/wip.1/split/260914-685617a/metadata-enpi-180-plus-STD-depunct-2-v1.0.csv.pho  \
  -w ./build/1.tts/depunct.STD  \
  -m /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx \
  -c /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx.json \
  -j ./config/aud_punc_dur_targ.json \
  -g ./config/g2p_overrides_en.json \
  --length_scale 1.25 \
  --skip_existing --read_as_ipa --repunct_min 1200

python scripts/piper_onnx_corpus_gen.py  \
  -i ./corpus/wip.1/split/260914-685617a/metadata-enpi-180-plus-SPL-depunct-2-v1.0.csv.pho  \
  -w ./build/1.tts/depunct.SPL  \
  -m /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx \
  -c /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx.json \
  -j ./config/aud_punc_dur_targ.json \
  -g ./config/g2p_overrides_en.json \
  --length_scale 1.25 \
  --skip_existing --read_as_ipa --repunct_min 1200


python scripts/piper_onnx_corpus_gen.py  \
  -i ./corpus/wip.1/split/260914-685617a/metadata-enpi-180-plus-STD-repunct-2-v1.0.csv.pho  \
  -w ./build/1.tts/repunct.STD  \
  -m /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx \
  -c /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx.json \
  -j ./config/aud_punc_dur_targ.json \
  -g ./config/g2p_overrides_en.json \
  --length_scale 1.25 \
  --skip_existing --read_as_ipa --repunct_min 600 --dry_run

python scripts/piper_onnx_corpus_gen.py  \
  -i ./corpus/wip.1/split/260914-685617a/metadata-enpi-180-plus-SPL-repunct-2-v1.0.csv.pho  \
  -w ./build/1.tts/repunct.SPL  \
  -m /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx \
  -c /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx.json \
  -j ./config/aud_punc_dur_targ.json \
  -g ./config/g2p_overrides_en.json \
  --length_scale 1.25 \
  --skip_existing --read_as_ipa --repunct_min 600 --dry_run  
```

```bash
ash@kassapa-l:~/dev/tts/en-pi$ ls -1 ./corpus/wip.1/split/*-2-v1.0.csv
./corpus/wip.1/split/metadata-enpi-180-plus-SPL-depunct-2-v1.0.csv
./corpus/wip.1/split/metadata-enpi-180-plus-SPL-repunct-2-v1.0.csv
./corpus/wip.1/split/metadata-enpi-180-plus-STD-depunct-2-v1.0.csv
./corpus/wip.1/split/metadata-enpi-180-plus-STD-repunct-2-v1.0.csv

cat ./corpus/wip.1/split/*-2-v1.0.csv > ./corpus/wip.1/split-uat/metadata-enpi-180-plus-ALL-repunct-2-v1.0.csv

ash@kassapa-l:~/dev/tts/en-pi$ ls -1 ./corpus/wip.1/split/260914-685617a/*-2-v1.0.csv.pho
./corpus/wip.1/split/260914-685617a/metadata-enpi-180-plus-SPL-depunct-2-v1.0.csv.pho
./corpus/wip.1/split/260914-685617a/metadata-enpi-180-plus-SPL-repunct-2-v1.0.csv.pho
./corpus/wip.1/split/260914-685617a/metadata-enpi-180-plus-STD-depunct-2-v1.0.csv.pho
./corpus/wip.1/split/260914-685617a/metadata-enpi-180-plus-STD-repunct-2-v1.0.csv.pho

ash@kassapa-l:~/dev/tts/en-pi$ cat ./corpus/wip.1/split/260914-685617a/*-2-v1.0.csv.pho > ./corpus/wip.1/split-uat/metadata-enpi-180-plus-ALL-repunct-2-v1.0.csv.pho

ash@kassapa-l:~/dev/tts/en-pi$ wc -l ./corpus/wip.1/split-uat/*
  1156 ./corpus/wip.1/split-uat/metadata-enpi-180-plus-ALL-repunct-2-v1.0.csv
  1156 ./corpus/wip.1/split-uat/metadata-enpi-180-plus-ALL-repunct-2-v1.0.csv.pho
  2312 total

sort -V ./corpus/wip.1/split-uat/metadata-enpi-180-plus-ALL-repunct-2-v1.0.csv > ./tmp/sorted-text.csv
sort -V ./corpus/wip.1/split-uat/metadata-enpi-180-plus-ALL-repunct-2-v1.0.csv.pho > ./tmp/sorted-phonemes.csv


```

```bash
python ./scripts/enhance_corpus_audio.py \
  -i ./build/1.tts/raw_base_wavs.pre \
  -o ./build/1.tts/raw_base_wavs \
  --enable_hpf \
  --hpf_cutoff 80.0 \
  --peak_norm_db -3.0 \
  --trim_threshold_db -50.0 \
  --padding_ms 150.0


python ./scripts/applio_batch_pipeline.py \
  --stages="2" \
  --model ./suttas.eng.lang-audio/applio-model/suttas_eng_lang_350e_90300s.pth \
  --index ./suttas.eng.lang-audio/applio-model/suttas_eng_lang.index \
  --settings ./config/applio_settings-en.json \
  --applio_dir ./Applio \
  --input_wavs ./build/1.tts/raw_base_wavs \
  --out_dir ./build/2.rvc/ \
  --rvc-skip-existing


pushd ./build/2.rvc
for f in *_output.wav; do echo mv "$f" "${f/_output/}"; done
popd


python ./scripts/trim_long_pauses.py \
  -i ./build/2.rvc \
  -o ./build/3.capped \
  --max_pause_ms 900

python ./scripts/enhance_corpus_audio.py \
  -i ./build/3.capped \
  -o ./build/4.enh \
  --enable_hpf \
  --hpf_cutoff 80.0 \
  --peak_norm_db -3.0 \
  --trim_threshold_db -50.0 \
  --padding_ms 150.0


python scripts/report_qa_analytics.py \
  -w ./build/4.enh \
  -o ./build/4.enh/metadata/report_qa_analytics.csv \
  --io_resume_ckpt ./build/4.enh/metadata/.qa_checkpoint.json


python scripts/flag_glitch_outliers.py \
    --input_qa ./build/4.enh/metadata/report_qa_analytics.csv \
    --output_csv ./build/4.enh/metadata/flag_glitch_outliers.csv \
    --threshold 2.5 > ./corpus/wip.2/split/uat/metadata-enpi-180-plus-ALL-repunct-2-v2.0.csv.4.enh.flag_glitch_outliers.stdout.md
```


```bash

python scripts/piper_onnx_corpus_gen.py  \
  -i ./corpus/wip.1/split/260914-685617a/redo-depunct-2-v1.0.csv.pho  \
  -w ./build/1.tts/redo.d  \
  -m /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx \
  -c /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx.json \
  -j ./config/aud_punc_dur_targ.json \
  -g ./config/g2p_overrides_en.json \
  --length_scale 1.25 \
  --skip_existing --read_as_ipa --repunct_min 1200
```



/// -------------------------------------------------------- WIP.2


```bash

cat corpus/wip.1/split-uat/glitch-defect-list.csv corpus/wip.1/split-uat/juls-defect-list-v2.csv > corpus/wip.2/wip.1-uat-defects-list.csv


awk -F'|' '
BEGIN {
    while ((getline line < "./corpus/wip.2/wip.1-uat-defects-list.csv") > 0) {
        sub(/\r$/, "", line);
        reject_list[line] = 1;
    }
    close("./corpus/wip.2/wip.1-uat-defects-list.csv");
}
{
    if ($1 in reject_list) {
        print > "./corpus/wip.2/split/rejected/metadata-enpi-180-plus-STD-repunct-2-REJECTED-v2.0.csv";
    } else {
        print > "./corpus/wip.2/split/metadata-enpi-180-plus-STD-repunct-2-v2.0.csv";
    }
}
' ./corpus/wip.1/split/metadata-enpi-180-plus-STD-repunct-2-v1.0.csv

awk -F'|' '
BEGIN {
    while ((getline line < "./corpus/wip.2/wip.1-uat-defects-list.csv") > 0) {
        sub(/\r$/, "", line);
        reject_list[line] = 1;
    }
    close("./corpus/wip.2/wip.1-uat-defects-list.csv");
}
{
    if ($1 in reject_list) {
        print > "./corpus/wip.2/split/rejected/metadata-enpi-180-plus-STD-depunct-2-REJECTED-v2.0.csv";
    } else {
        print > "./corpus/wip.2/split/metadata-enpi-180-plus-STD-depunct-2-v2.0.csv";
    }
}
' ./corpus/wip.1/split/metadata-enpi-180-plus-STD-depunct-2-v1.0.csv

awk -F'|' '
BEGIN {
    while ((getline line < "./corpus/wip.2/wip.1-uat-defects-list.csv") > 0) {
        sub(/\r$/, "", line);
        reject_list[line] = 1;
    }
    close("./corpus/wip.2/wip.1-uat-defects-list.csv");
}
{
    if ($1 in reject_list) {
        print > "./corpus/wip.2/split/rejected/metadata-enpi-180-plus-SPL-repunct-2-REJECTED-v2.0.csv";
    } else {
        print > "./corpus/wip.2/split/metadata-enpi-180-plus-SPL-repunct-2-v2.0.csv";
    }
}
' ./corpus/wip.1/split/metadata-enpi-180-plus-SPL-repunct-2-v1.0.csv

awk -F'|' '
BEGIN {
    while ((getline line < "./corpus/wip.2/wip.1-uat-defects-list.csv") > 0) {
        sub(/\r$/, "", line);
        reject_list[line] = 1;
    }
    close("./corpus/wip.2/wip.1-uat-defects-list.csv");
}
{
    if ($1 in reject_list) {
        print > "./corpus/wip.2/split/rejected/metadata-enpi-180-plus-SPL-depunct-2-REJECTED-v2.0.csv";
    } else {
        print > "./corpus/wip.2/split/metadata-enpi-180-plus-SPL-depunct-2-v2.0.csv";
    }
}
' ./corpus/wip.1/split/metadata-enpi-180-plus-SPL-depunct-2-v1.0.csv

# hand remove [therīgāthā] from corpus/wip.2/split/metadata-enpi-180-plus-STD-depunct-2-v2.0.csv
```



```bash
ash@kassapa-l:~/dev/tts/en-pi$ wc -l ./corpus/wip.2/split/*2-v2.0.csv
    47 ./corpus/wip.2/split/metadata-enpi-180-plus-SPL-depunct-2-v2.0.csv
   104 ./corpus/wip.2/split/metadata-enpi-180-plus-SPL-repunct-2-v2.0.csv
   609 ./corpus/wip.2/split/metadata-enpi-180-plus-STD-depunct-2-v2.0.csv
   292 ./corpus/wip.2/split/metadata-enpi-180-plus-STD-repunct-2-v2.0.csv
  1052 total

deno -A ~/dev/di/dt.o-suttas-builder/tool/2.phonemize-sources-for-tts.ts \
  --config-override ./corpus/wip.2/split/phonemizer-config-260914-685617a.json

cat ./corpus/wip.2/split/260914-685617a/*-depunct*.pho > ./corpus/wip.2/split/260914-685617a/depunct.pho
cat ./corpus/wip.2/split/260914-685617a/*-repunct*.pho > ./corpus/wip.2/split/260914-685617a/repunct.pho

python scripts/piper_onnx_corpus_gen.py  \
  -i ./corpus/wip.2/split/260914-685617a/depunct.pho  \
  -w ./build/1.tts/  \
  -m /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx \
  -c /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx.json \
  -j ./config/aud_punc_dur_targ.json \
  -g ./config/g2p_overrides_en.json \
  --length_scale 1.25 \
  --skip_existing --read_as_ipa --repunct_min 1200

python scripts/piper_onnx_corpus_gen.py  \
  -i ./corpus/wip.2/split/260914-685617a/repunct.pho  \
  -w ./build/1.tts/  \
  -m /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx \
  -c /home/ash/dev/di/vits-piper/model/en_gb-suttaplayer-medium.onnx.json \
  -j ./config/aud_punc_dur_targ.json \
  -g ./config/g2p_overrides_en.json \
  --length_scale 1.25 \
  --skip_existing --read_as_ipa --repunct_min 600

#  SKIPPING TTS ENH

python ./scripts/applio_batch_pipeline.py \
  --stages="2" \
  --model ./suttas.eng.lang-audio/applio-model/suttas_eng_lang_350e_90300s.pth \
  --index ./suttas.eng.lang-audio/applio-model/suttas_eng_lang.index \
  --settings ./config/applio_settings-en.json \
  --applio_dir ./Applio \
  --input_wavs ./build/1.tts/raw_base_wavs \
  --out_dir ./build/2.rvc/ \
  --rvc-skip-existing


# run --dry-run first using echo
pushd ./build/2.rvc
for f in *_output.wav; do echo mv "$f" "${f/_output/}"; done
popd


python ./scripts/trim_long_pauses.py \
  -i ./build/2.rvc \
  -o ./build/3.capped \
  --max_pause_ms 900

python scripts/report_qa_analytics.py \
  -w ./build/4.enh \
  -o ./build/4.enh/metadata/report_qa_analytics.csv \
  --io_resume_ckpt ./build/4.enh/metadata/.qa_checkpoint.json


python scripts/flag_glitch_outliers.py \
    --input_qa ./build/4.enh/metadata/report_qa_analytics.csv \
    --output_csv ./build/4.enh/metadata/flag_glitch_outliers.csv \
    --threshold 2.5 > ./corpus/wip.2/split/uat/metadata-enpi-180-plus-ALL-repunct-2-v2.0.csv.4.enh.flag_glitch_outliers.stdout.md

```



// ------------------ REMOVE FINAL DEFECTS FOR UAT APPROVED


```bash
cat corpus/wip.2/split/uat/glitch-defect-list.csv corpus/wip.2/split/uat/juls-defect-list-v2.csv corpus/wip.2/split/uat/opencode-defect-list.csv > corpus/wip.2/split/uat/final-uat-defect-list.csv

cat corpus/wip.2/split/*-v2.0.csv > corpus/wip.2/split/metadata-enpi-180-plus-ALL-2-v2.0.csv

ash@kassapa-l:~/dev/tts/en-pi$ wc -l corpus/wip.2/split/*-v2.0.csv
  1052 corpus/wip.2/split/metadata-enpi-180-plus-ALL-2-v2.0.csv
    47 corpus/wip.2/split/metadata-enpi-180-plus-SPL-depunct-2-v2.0.csv
   104 corpus/wip.2/split/metadata-enpi-180-plus-SPL-repunct-2-v2.0.csv
   609 corpus/wip.2/split/metadata-enpi-180-plus-STD-depunct-2-v2.0.csv
   292 corpus/wip.2/split/metadata-enpi-180-plus-STD-repunct-2-v2.0.csv
  2104 total

awk -F'|' '
BEGIN {
    while ((getline line < "./corpus/wip.2/split/uat/final-uat-defect-list.csv") > 0) {
        sub(/\r$/, "", line);
        reject_list[line] = 1;
    }
    close("./corpus/wip.2/split/uat/final-uat-defect-list.csv");
}
{
    if ($1 in reject_list) {
        print > "./corpus/wip.2/uat/metadata-text-enpi-REJECTED-v2.0.csv";
    } else {
        print > "./corpus/wip.2/uat/metadata-text-enpi-ACCEPTED-v2.0.csv";
    }
}
' ./corpus/wip.2/split/metadata-enpi-180-plus-ALL-2-v2.0.csv


ash@kassapa-l:~/dev/tts/en-pi$ wc -l ./corpus/wip.2/uat/*.csv
   999 ./corpus/wip.2/uat/metadata-text-enpi-ACCEPTED-v2.0.csv
    53 ./corpus/wip.2/uat/metadata-text-enpi-REJECTED-v2.0.csv
  1052 total

```

// ------------ FINALISE


```bash
# fix utterances head & tail
python ./scripts/sanitize_punctuation.py \
  -i ./corpus/wip.2/uat/metadata-text-enpi-ACCEPTED-v2.0.csv \
  -o ./corpus/wip.2/uat/metadata-text-enpi-ACCEPTED-v2.0.csv.sanitized.csv
```

```bash
# finalise corpus with cleanup punctuation and balance brackets

sed "s/'… '…/'…/g" ./corpus/wip.2/uat/metadata-text-enpi-ACCEPTED-v2.0.csv.sanitized.csv > ./corpus/wip.2/metadata-text-enpi.csv 

perl -i -0777 -pe '
  $c1=0; s/\(/ ++$c1 <= 34 ? "(" : "{" /ge;
  $c2=0; s/\)/ ++$c2 <= 34 ? ")" : "}" /ge;
' ./corpus/wip.2/metadata-text-enpi.csv 

perl -i -0777 -pe '
  $c1=0; s/\(/ ++$c1 <= 25 ? "(" : "[" /ge;
  $c2=0; s/\)/ ++$c2 <= 25 ? ")" : "]" /ge;
' ./corpus/wip.2/metadata-text-enpi.csv 


grep -E "(\{|\(|\[)" ./corpus/wip.2/metadata-text-enpi.csv 
```


```bash
python scripts/assess_pali_coverage.py \
    -i ./corpus/wip.2/metadata-text-enpi.csv \
    -p ./input-research/pali-transliteration-freq-list.csv > ./corpus/wip.2/report/metadata-text-enpi.csv.assess_pali_coverage.md


python scripts/score_piper_enpi_corpus.py \
    -i ./corpus/wip.2/metadata-text-enpi.csv \
    -o ./corpus/wip.2/report/metadata-text-enpi.csv.scorecard.csv  > ./corpus/wip.2/report/metadata-text-enpi.csv.score_piper_enpi_corpus.md
```

```bash
deno -A ~/dev/di/dt.o-suttas-builder/tool/2.phonemize-sources-for-tts.ts \
  --config-override ./corpus/wip.2/phonemizer-config-261020-a90f564-training.json

mv ./corpus/wip.2/metadata-text-enpi.csv.pho ./corpus/wip.2/metadata-phonemes-enpi.csv

cp ./corpus/wip.2/*.csv ./corpus
```

```bash
# clean 999-utterance training bundle
python3 scripts/build_training_bundle.py \
  --output ./release/tts-en-pi-261020-training.tgz

# historical UAT archive: 1052 WAVs, including the 50 rejected utterances
# tar -zcvf ./release/tts-en-pi-v1.1.0.tgz ...

# bundle of applio rvc model 
tar -zcvf ./release/suttas.eng.lang-audio-raw-v1.0.0.tgz \
  suttas.eng.lang-audio/audacity/export.step1 suttas.eng.lang-audio/Applio-prep-HP-norm-after-uvr5.txt
```

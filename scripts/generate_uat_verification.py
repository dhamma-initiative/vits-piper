#!/usr/bin/env python3
"""Build a natural-sentence UAT vocabulary corpus and synthesize it.

The vocabulary lists contain isolated words. This tool finds each word in real
sutta prose, emits one LJSpeech-style WAV per target, and writes a 2-column
metadata file that review_corpus_server.py can open directly.

Typical use from this repository's tmp/ directory:

  python ../scripts/generate_uat_verification.py \
    --model ../model/en_gb-suttaplayer-medium.onnx \
    --config ../model/en_gb-suttaplayer-medium.onnx.json \
    --out-dir ./uat-verification-enpi

The metadata file is written as:

  OUT/metadata-uat-verification-enpi.csv
  wav_name.wav|Natural sentence containing the target term.

Each filename includes the target term, for example
EN_00042_dhamma.wav or PI_00107_sutta.wav.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import onnxruntime as ort
import soundfile as sf

PIPER_SRC = Path(os.environ.get("PIPER_SRC", "/home/ash/prj/di/piper1-gpl.0/src"))
if PIPER_SRC.exists() and str(PIPER_SRC) not in sys.path:
    sys.path.insert(0, str(PIPER_SRC))

from piper.phoneme_ids import phonemes_to_ids

REPO_ROOT = Path(__file__).resolve().parent.parent
SIBLING_ROOT = REPO_ROOT.parent
DEFAULT_TEXT_ROOT = SIBLING_ROOT / "dt.o-suttas-builder" / "build" / "text"
DEFAULT_EN_VOCAB = SIBLING_ROOT / "dt.o-suttas-builder" / "build" / "vocabulary" / "english-transliteration-freq-list.csv"
DEFAULT_PI_VOCAB = SIBLING_ROOT / "dt.o-suttas-builder" / "build" / "vocabulary" / "pali-transliteration-freq-list.csv"
DEFAULT_MODEL = REPO_ROOT / "model" / "en_gb-suttaplayer-medium.onnx"
DEFAULT_CONFIG = REPO_ROOT / "model" / "en_gb-suttaplayer-medium.onnx.json"
DEFAULT_PHONEMIZER_CONFIG = REPO_ROOT / "phoneme" / "phonemizer-config.json"
DEFAULT_EN_MAP = SIBLING_ROOT / "suttas" / "phoneme" / "pho_en[gb]-to-espeak-v1.51-ipa.json"
DEFAULT_PI_MAP = SIBLING_ROOT / "suttas" / "phoneme" / "pho_pi[si]-to-aksharamukha-2.1.0-ipa.json"
FALLBACK_EN_MAP = REPO_ROOT / "training" / "config" / DEFAULT_EN_MAP.name
FALLBACK_PI_MAP = REPO_ROOT / "training" / "config" / DEFAULT_PI_MAP.name

WORD_RE = re.compile(r"(?<![^\W\d_])[^\W\d_]+(?:['’][^\W\d_]+)*(?![^\W\d_])", re.UNICODE)
NUMBER_RE = re.compile(r"\b(\d+(?:,\d+)*)\b")
TERM_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)

ONES = [
    "",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate and synthesize natural UAT vocabulary utterances.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--text-root", default=str(DEFAULT_TEXT_ROOT), help="Root of source .txt files")
    p.add_argument("--en-vocab", default=str(DEFAULT_EN_VOCAB), help="English vocabulary CSV")
    p.add_argument("--pi-vocab", default=str(DEFAULT_PI_VOCAB), help="Pali vocabulary CSV")
    p.add_argument("--language", choices=("both", "en", "pi"), default="both")
    p.add_argument("--out-dir", default="uat-verification-enpi", help="Output directory")
    p.add_argument("--metadata", default=argparse.SUPPRESS, help="Metadata path (default: OUT/metadata-uat-verification-enpi.csv)")
    p.add_argument("--manifest", default=argparse.SUPPRESS, help="Manifest path (default: OUT/uat-verification-manifest.csv)")
    p.add_argument("--model", default=str(DEFAULT_MODEL), help="Piper ONNX model")
    p.add_argument("--config", default=str(DEFAULT_CONFIG), help="Piper .onnx.json config")
    p.add_argument("--phonemizer-config", default=str(DEFAULT_PHONEMIZER_CONFIG), help="Runtime phonemizer config")
    p.add_argument("--en-map", default=argparse.SUPPRESS, help="English IPA map (default: sibling suttas, then training/config)")
    p.add_argument("--pi-map", default=argparse.SUPPRESS, help="Pali IPA map (default: sibling suttas, then training/config)")
    p.add_argument("--start", type=int, default=0, help="First target index after selection")
    p.add_argument("--limit", type=int, default=0, help="Maximum targets; 0 means all")
    p.add_argument("--resume", action="store_true", help="Reuse valid existing WAVs")
    p.add_argument("--dry-run", action="store_true", help="Report selection only; do not write audio or metadata")
    p.add_argument("--min-words", type=int, default=5, help="Minimum words in an utterance")
    p.add_argument("--max-words", type=int, default=28, help="Maximum words in an utterance")
    p.add_argument("--max-chars", type=int, default=240, help="Maximum characters in an utterance")
    p.add_argument("--fallback", choices=("carrier", "skip"), default="carrier", help="Fallback for terms without a source sentence")
    p.add_argument("--warmup", type=int, default=2, help="Discarded model warm-up utterances")
    p.add_argument("--provider", default="CPUExecutionProvider")
    p.add_argument("--length-scale", type=float, default=None)
    p.add_argument("--noise-scale", type=float, default=None)
    p.add_argument("--noise-w", type=float, default=None)
    p.add_argument("--subtype", default="PCM_16", help="soundfile WAV subtype")
    p.add_argument("--progress-every", type=int, default=100)
    return p.parse_args()


def number_to_words(num: int) -> str:
    if num == 0:
        return "zero"

    def under_thousand(n: int) -> str:
        if n == 0:
            return ""
        if n < 20:
            return ONES[n]
        if n < 100:
            ten, rest = divmod(n, 10)
            return f"{TENS[ten]} {ONES[rest]}".strip()
        hundred, rest = divmod(n, 100)
        value = f"{ONES[hundred]} hundred"
        return f"{value} {under_thousand(rest)}".strip()

    n = abs(int(num))
    parts: list[str] = []
    for scale in (1_000_000_000, 1_000_000, 1_000):
        amount, n = divmod(n, scale)
        if amount:
            parts.append(f"{under_thousand(amount)} {'billion' if scale == 1_000_000_000 else 'million' if scale == 1_000_000 else 'thousand'}")
    if n:
        parts.append(under_thousand(n))
    return " ".join(parts).strip()


def clean_word(word: str) -> str:
    if not word:
        return ""
    return unicodedata.normalize("NFC", re.sub(r"^['’‘\"“”—–-]+|['’‘\"“”—–-]+$", "", word.strip()).lower())


def js_replacement(value: str) -> str:
    return re.sub(r"\$(\d+)", r"\\\1", value)


def compile_rules(rules: list[list[str]]) -> list[tuple[re.Pattern[str], str]]:
    compiled = []
    for rule in rules:
        find, repl = rule[0], rule[1]
        opts = rule[2] if len(rule) > 2 else "gmu"
        flags = 0
        if "i" in opts:
            flags |= re.IGNORECASE
        if "m" in opts:
            flags |= re.MULTILINE
        try:
            compiled.append((re.compile(find, flags), js_replacement(repl)))
        except re.error as exc:
            raise SystemExit(f"invalid phonemizer regex {find!r}: {exc}") from exc
    return compiled


def apply_rules(text: str, rules: list[tuple[re.Pattern[str], str]]) -> str:
    for pattern, repl in rules:
        text = pattern.sub(repl, text)
    return text


def tidy_phonemes(value: str) -> str:
    value = re.sub(r"([.,;:!?])[^\S\r\n]+(?=[.,;:!?])", r"\1", value)
    value = re.sub(r"([.,;:!?])[.,;:!?]+", r"\1", value)
    value = re.sub(r"[^\S\r\n]+([.,;:!?])", r"\1", value)
    value = re.sub(r"([.,;:!?])(?=\w)", r"\1 ", value)
    value = re.sub(r"[^\S\r\n]{2,}", " ", value)
    value = re.sub(r"^(?:[.,;:!?]|[^\S\r\n])+", "", value, flags=re.MULTILINE)
    return "\n".join(line.strip() for line in value.split("\n"))


class SuttaPhonemizer:
    def __init__(
        self,
        english: dict[str, str],
        pali: dict[str, str],
        id_map: dict[str, list[int]],
        config: dict,
    ) -> None:
        self.english = english
        self.pali = pali
        self.id_map = id_map
        self.invalid_term = config.get("invalidTerm", "ˈɪn vˈælɪd tˈɜːm")
        self.pre = compile_rules(config.get("preProcessRegExFindReplaceList", []))
        self.post = compile_rules(config.get("postProcessRegExFindReplList", []))
        self.patch = compile_rules(config.get("patchProcessRegExFindReplList", []))
        self.custom = (config.get("dictionaryResponder") or {}).get("customPhonemes") or {}

    def phonemize(self, text: str) -> tuple[str, list[str]]:
        text = unicodedata.normalize("NFC", text)
        text = apply_rules(text, self.pre).lower()
        words = {clean_word(m.group(0)) for m in WORD_RE.finditer(text)}
        words.discard("")
        numbers: dict[str, str] = {}
        for match in NUMBER_RE.finditer(text):
            replacement = number_to_words(int(match.group(0).replace(",", "")))
            numbers[match.group(0)] = replacement
            words.update(replacement.split())

        missing: list[str] = []
        dictionary: dict[str, str] = {}
        for word in sorted(words, key=len, reverse=True):
            value = self.custom.get(word) or self.english.get(word) or self.pali.get(word)
            if not value:
                missing.append(word)
                value = self.invalid_term
            dictionary[word] = value

        if numbers:
            text = NUMBER_RE.sub(lambda m: numbers[m.group(0)], text)

        terms = sorted(dictionary, key=len, reverse=True)
        if terms:
            pattern = re.compile(r"(?<![^\W\d_])(" + "|".join(map(re.escape, terms)) + r")(?![^\W\d_])", re.IGNORECASE)
            text = pattern.sub(lambda m: dictionary.get(m.group(0).lower(), m.group(0)), text)

        text = unicodedata.normalize("NFD", text)
        text = apply_rules(text, self.post)
        text = apply_rules(text, self.patch)
        text = tidy_phonemes(text)
        invalid = sorted({char for char in text if char not in self.id_map and char not in "\n"})
        return text, missing + invalid


def read_vocab(path: Path, field: str) -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        if not reader.fieldnames or field not in reader.fieldnames:
            raise SystemExit(f"{path}: missing {field!r} column")
        freq_field = "freq" if "freq" in reader.fieldnames else ""
        for row in reader:
            term = (row.get(field) or "").strip()
            if not term:
                continue
            try:
                freq = int(row.get(freq_field, "0") or "0")
            except ValueError:
                freq = 0
            rows.append((term, freq))
    return rows


def split_sentences(value: str) -> list[str]:
    value = re.sub(r"\s+", " ", value).strip()
    if not value:
        return []
    pieces = re.split(r"(?<=[.!?])\s+", value)
    return [piece.strip() for piece in pieces if piece.strip()]


def clauses(value: str, min_words: int, max_words: int) -> list[str]:
    parts = [p.strip() for p in re.split(r"(?:[;—]|,(?=\s))", value) if p.strip()]
    result = []
    for part in parts:
        words = len(TERM_RE.findall(part))
        if min_words <= words <= max_words:
            result.append(part)
    if len(parts) > 1:
        for i in range(len(parts)):
            merged = ""
            for j in range(i, min(i + 3, len(parts))):
                merged = (merged + ", " + parts[j]).strip(", ") if merged else parts[j]
                if min_words <= len(TERM_RE.findall(merged)) <= max_words:
                    result.append(merged)
    return result


def load_sources(root: Path, min_words: int, max_words: int, max_chars: int) -> list[dict]:
    sources: list[dict] = []
    seen: set[str] = set()
    for path in sorted(root.rglob("*.txt")):
        try:
            raw = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raw = path.read_text(encoding="utf-8", errors="replace")
        for paragraph in re.split(r"\n\s*\n", raw):
            for sentence in split_sentences(paragraph):
                candidates = [sentence]
                if len(TERM_RE.findall(sentence)) > max_words or len(sentence) > max_chars:
                    candidates = clauses(sentence, min_words, max_words)
                for text in candidates:
                    if not (min_words <= len(TERM_RE.findall(text)) <= max_words):
                        continue
                    if len(text) > max_chars:
                        continue
                    key = text.lower()
                    if key in seen:
                        continue
                    seen.add(key)
                    tokens = {clean_word(w) for w in TERM_RE.findall(text)}
                    tokens.discard("")
                    sources.append(
                        {
                            "text": text,
                            "tokens": tokens,
                            "source": str(path.relative_to(root)),
                            "word_count": len(TERM_RE.findall(text)),
                            "kind": "sentence" if text == sentence else "clause",
                        }
                    )
    return sources


def variants(term: str) -> set[str]:
    term = term.lower().strip()
    values = {term}
    base = re.sub(r"['’]s$", "", term)
    if base != term:
        values.add(base)
    if base.endswith("ies") and len(base) > 4:
        values.add(base[:-3] + "y")
    if base.endswith("es") and len(base) > 4:
        values.add(base[:-2])
    if base.endswith("s") and not base.endswith("ss") and len(base) > 3:
        values.add(base[:-1])
    if base.endswith("ed") and len(base) > 4:
        values.add(base[:-2])
        values.add(base[:-1])
    if base.endswith("ing") and len(base) > 5:
        values.add(base[:-3])
        values.add(base[:-3] + "e")
    if base.endswith("ly") and len(base) > 5:
        values.add(base[:-2])
    return values


def build_index(sources: list[dict]) -> dict[str, list[int]]:
    index: dict[str, list[int]] = defaultdict(list)
    for i, source in enumerate(sources):
        for word in source["tokens"]:
            index[word].append(i)
    return index


def quote_balance(text: str) -> bool:
    text = re.sub(r"(?<=\w)['’](?=\w)", "", text)
    if text.count("'") % 2:
        return False
    if text.count('"') % 2:
        return False
    if text.count("“") != text.count("”"):
        return False
    if text.count("‘") != text.count("’"):
        return False
    return True


def score_source(source: dict, term: str, variant: bool) -> float:
    text = source["text"]
    words = source["word_count"]
    score = 0.0
    score += 20.0 if not variant else 8.0
    score += 6.0 if source.get("kind") == "sentence" else 0.0
    if 8 <= words <= 20:
        score += 12.0
    elif 5 <= words < 8 or 20 < words <= 26:
        score += 5.0
    if 35 <= len(text) <= 180:
        score += 6.0
    if 180 < len(text) <= 240:
        score -= 4.0
    letters = [c for c in text if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.5:
        score -= 40.0
    if re.search(r"\b(SUTTA|NIKĀYA|NIKAYA|VAGGA|SAṀYUTTA|SAMYUTTA|AṄGUTTARA|ANGUTTARA|DĪGHA|DIGHA|MAJJHIMA)\b", text, re.IGNORECASE):
        score -= 30.0
    if "—" in text or "–" in text:
        score -= 6.0
    if text.endswith((",", ";", ":", "—")):
        score -= 5.0
    if text.startswith(("'", '"', "“", "‘", "—")):
        score -= 2.0
    if re.match(r"(?i)^(and|but|or|so|then|that|which|who|when|if|as|for|with|from|to|of)\b", text):
        score -= 3.0
    if not quote_balance(text):
        score -= 25.0
    if term.lower() in text.lower():
        score += 3.0
    return score


def choose_source(
    sources: list[dict], index: dict[str, list[int]], term: str, used: set[int]
) -> tuple[dict | None, str, int]:
    candidates: set[int] = set()
    used_variant = ""
    for value in sorted(variants(term)):
        if value in index:
            candidates.update(index[value])
            if value != term.lower():
                used_variant = value
    best_any_index = -1
    best_any_score = -math.inf
    best_new_index = -1
    best_new_score = -math.inf
    for i in sorted(candidates):
        source = sources[i]
        variant = term.lower() not in source["tokens"]
        score = score_source(source, term, variant)
        if score > best_any_score:
            best_any_index = i
            best_any_score = score
        if i not in used and score > best_new_score:
            best_new_index = i
            best_new_score = score
    if best_new_index >= 0:
        return sources[best_new_index], used_variant, best_new_index
    if best_any_index >= 0:
        return sources[best_any_index], used_variant, best_any_index
    return None, used_variant, -1


def sanitize_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if c.isascii() and (c.isalnum() or c in "-_"))
    return re.sub(r"_+", "_", value).strip("_-") or "term"


def load_map(primary: Path, fallback: Path, override: str, label: str) -> dict[str, str]:
    path = Path(override) if override else primary
    if not path.exists() and not override and fallback.exists():
        path = fallback
    if not path.exists():
        raise SystemExit(f"{label} map not found: {path}")
    print(f"{label} map: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_entries(args: argparse.Namespace, sources: list[dict], index: dict[str, list[int]]) -> list[dict]:
    groups: list[tuple[str, Path, str]] = []
    if args.language in ("both", "en"):
        groups.append(("en", Path(args.en_vocab), "english"))
    if args.language in ("both", "pi"):
        groups.append(("pi", Path(args.pi_vocab), "pali"))

    entries: list[dict] = []
    used: set[int] = set()
    for lang, path, field in groups:
        vocab = read_vocab(path, field)
        print(f"{lang.upper()} vocabulary: {len(vocab)} entries from {path}")
        for ordinal, (term, freq) in enumerate(vocab, start=1):
            source, used_variant, source_index = choose_source(sources, index, term, used)
            fallback = ""
            if source is None:
                if args.fallback == "skip":
                    continue
                text = f"The term is {term}."
                fallback = "carrier"
                source = {"text": text, "source": "", "word_count": len(TERM_RE.findall(text))}
            else:
                used.add(source_index)
            text = source["text"].replace("|", " ")
            if text and text[0].islower():
                text = text[0].upper() + text[1:]
            entries.append(
                {
                    "language": lang,
                    "term": term,
                    "freq": freq,
                    "source": source["source"],
                    "text": text,
                    "fallback": fallback,
                    "variant": used_variant,
                    "ordinal": ordinal,
                }
            )
    entries.sort(key=lambda e: (e["language"], e["ordinal"]))
    for i, entry in enumerate(entries):
        entry["index"] = i
        entry["wav"] = f"{entry['language'].upper()}_{i:05d}_{sanitize_name(entry['term'])}.wav"
    return entries


def main() -> int:
    args = parse_args()
    if args.start < 0:
        raise SystemExit("--start must be >= 0")
    if args.limit < 0:
        raise SystemExit("--limit must be >= 0")
    if args.min_words < 1 or args.max_words < args.min_words:
        raise SystemExit("invalid --min-words/--max-words")

    out_dir = Path(args.out_dir)
    metadata_path = Path(args.metadata) if getattr(args, "metadata", None) else out_dir / "metadata-uat-verification-enpi.csv"
    manifest_path = Path(args.manifest) if getattr(args, "manifest", None) else out_dir / "uat-verification-manifest.csv"
    wav_dir = out_dir / "wavs"

    print(f"text root: {args.text_root}")
    sources = load_sources(Path(args.text_root), args.min_words, args.max_words, args.max_chars)
    if not sources:
        raise SystemExit("no usable source sentences found")
    print(f"source utterances: {len(sources)}")
    index = build_index(sources)

    entries = load_entries(args, sources, index)
    selected = entries[args.start :]
    if args.limit:
        selected = selected[: args.limit]
    if not selected:
        raise SystemExit("no targets selected")
    print(f"targets: {len(selected)} selected from {len(entries)}")

    en_map = load_map(DEFAULT_EN_MAP, FALLBACK_EN_MAP, getattr(args, "en_map", None), "English IPA")
    pi_map = load_map(DEFAULT_PI_MAP, FALLBACK_PI_MAP, getattr(args, "pi_map", None), "Pali IPA")
    phon_config = json.loads(Path(args.phonemizer_config).read_text(encoding="utf-8"))
    model_config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    id_map = model_config["phoneme_id_map"]
    phonemizer = SuttaPhonemizer(en_map, pi_map, id_map, phon_config)

    prepared: list[dict] = []
    skipped: list[dict] = []
    for entry in selected:
        phonemes, missing = phonemizer.phonemize(entry["text"])
        if missing:
            skipped.append({"index": entry["index"], "term": entry["term"], "reason": ",".join(missing[:8]), "text": entry["text"]})
            continue
        entry["phonemes"] = phonemes
        entry["ids"] = len(phonemes_to_ids(list(phonemes), id_map))
        prepared.append(entry)

    if skipped:
        print(f"skipped {len(skipped)} entries with unknown words/phonemes")
        for item in skipped[:10]:
            print(f"  {item['term']}: {item['reason']}")
    if not prepared:
        raise SystemExit("no entries could be phonemized")

    counts = Counter(e["fallback"] or "source" for e in prepared)
    print("selection: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    for entry in prepared[:5]:
        print(f"  {entry['wav']} | {entry['text']}")

    manifest_fields = [
        "index",
        "language",
        "term",
        "freq",
        "wav",
        "text",
        "source",
        "fallback",
        "variant",
        "words",
        "ids",
        "duration_s",
        "phonemes",
    ]

    if args.dry_run:
        lengths = [e["ids"] for e in prepared]
        print(f"id length: min={min(lengths)} median={int(np.median(lengths))} max={max(lengths)}")
        print(f"would write {len(prepared)} WAVs and {metadata_path}")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    wav_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    sample_rate = int(model_config.get("audio", {}).get("sample_rate", 22050))
    inference = model_config.get("inference", {})
    length_scale = args.length_scale if args.length_scale is not None else float(inference.get("length_scale", 1.0))
    noise_scale = args.noise_scale if args.noise_scale is not None else float(inference.get("noise_scale", 0.667))
    noise_w = args.noise_w if args.noise_w is not None else float(inference.get("noise_w", 0.8))

    providers = [args.provider]
    if args.provider == "CUDAExecutionProvider" and "CUDAExecutionProvider" not in ort.get_available_providers():
        print("CUDA unavailable; using CPU")
        providers = ["CPUExecutionProvider"]
    session = ort.InferenceSession(args.model, providers=providers)
    input_names = {item.name for item in session.get_inputs()}
    print(f"provider: {session.get_providers()[0]}")
    print(f"inputs: {sorted(input_names)}")

    def synthesize(entry: dict) -> np.ndarray:
        ids = phonemes_to_ids(list(entry["phonemes"]), id_map)
        feed = {
            "input": np.asarray([ids], dtype=np.int64),
            "input_lengths": np.asarray([len(ids)], dtype=np.int64),
            "scales": np.asarray([noise_scale, length_scale, noise_w], dtype=np.float32),
        }
        if "sid" in input_names:
            feed["sid"] = np.asarray([int(model_config.get("default_speaker_id", 0))], dtype=np.int64)
        audio = session.run(None, feed)[0]
        return np.asarray(audio, dtype=np.float32).reshape(-1)

    for _ in range(max(0, args.warmup)):
        try:
            synthesize(prepared[0])
        except Exception as exc:
            print(f"warm-up failed: {exc}")
            break

    started = time.time()
    done = 0
    reused = 0
    failed: list[dict] = []
    with metadata_path.open("w", encoding="utf-8", newline="") as mf, manifest_path.open("w", encoding="utf-8", newline="") as ff:
        metadata_writer = csv.writer(mf, delimiter="|", lineterminator="\n")
        manifest_writer = csv.DictWriter(ff, fieldnames=manifest_fields)
        manifest_writer.writeheader()
        for entry in prepared:
            wav_path = wav_dir / entry["wav"]
            duration = 0.0
            if args.resume and wav_path.exists():
                try:
                    info = sf.info(wav_path)
                    duration = info.frames / info.samplerate
                except Exception:
                    duration = 0.0
                if duration > 0:
                    reused += 1
            if duration <= 0:
                try:
                    audio = synthesize(entry)
                except Exception as exc:
                    failed.append({"term": entry["term"], "reason": str(exc)})
                    print(f"  failed {entry['wav']}: {exc}")
                    continue
                audio = np.clip(audio, -1.0, 1.0)
                sf.write(wav_path, audio, sample_rate, subtype=args.subtype)
                duration = len(audio) / sample_rate
                done += 1
                if args.progress_every and done % args.progress_every == 0:
                    elapsed = time.time() - started
                    print(f"  {done + reused}/{len(prepared)}  {done / max(elapsed, 1e-9):.1f}/s  elapsed={elapsed / 60:.1f}m")

            metadata_writer.writerow([entry["wav"], entry["text"]])
            manifest_writer.writerow(
                {
                    "index": entry["index"],
                    "language": entry["language"],
                    "term": entry["term"],
                    "freq": entry["freq"],
                    "wav": entry["wav"],
                    "text": entry["text"],
                    "source": entry["source"],
                    "fallback": entry["fallback"],
                    "variant": entry["variant"],
                    "words": len(TERM_RE.findall(entry["text"])),
                    "ids": entry["ids"],
                    "duration_s": f"{duration:.3f}",
                    "phonemes": entry["phonemes"],
                }
            )

    print(f"wrote {done} WAVs ({reused} reused) in {(time.time() - started) / 60:.1f} min")
    print(f"metadata: {metadata_path}")
    print(f"manifest: {manifest_path}")
    if failed:
        print(f"failed: {len(failed)}")
        return 1
    if skipped:
        print(f"skipped: {len(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

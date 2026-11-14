#!/usr/bin/env python3
"""Generate the runtime phonemizer config from pinned suttas artifacts.

The generated config contains the absolute source URLs, SHA-256 digests, and
the suttas source/build versions. Rules are kept in this script so the config
can be regenerated deterministically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUTTAS_DIR = REPO_ROOT.parent / "suttas"
DEFAULT_OUTPUT = REPO_ROOT / "phoneme" / "phonemizer-config.json"
DEFAULT_BASE_URL = "https://dhamma-initiative.github.io/suttas/"
DEFAULT_MODEL_BASE_URL = ""  # relative to the endpoint base

EN_MAP_FILENAME = "pho_en[gb]-to-espeak-v1.51-ipa.json"
PI_MAP_FILENAME = "pho_pi[si]-to-aksharamukha-2.1.0-ipa.json"

PRE_PROCESS_RULES = [
    [r"[-–—]?[^\S\r\n]*&[^\S\r\n]*[-–—]?", " and "],
    ["&", " and "],
    ["(DHAMMAPADA|ITIVUTTAKA|KHUDDAKAPĀṬHA)", "$1."],
    [r"(SUTTA NIPĀTA|THERAGĀTHĀ|THERĪGĀTHĀ|UDĀNA)\s+([:\d]+)", "$1. $2."],
    [r"\s+((AṄGUTTARA|DĪGHA|MAJJHIMA|SAṀYUTTA)\s+NIKĀYA)", ". $1."],
    [r"\bblessed(\s+one)\b", "bless'ed$1", "gmiu"],
    [r"\b(in|past|their|future|previous|former|of|entire|the)\s+lives\b", "$1 lyves", "gmiu"],
]

POST_PROCESS_RULES = [
    ["=", " "],
    [r"[\u200b-\u200d\ufeff\u200e\u200f]", "", "g"],
]

PATCH_PROCESS_RULES: list[list[str]] = []


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_url(url: str) -> str:
    request = Request(url, headers={"User-Agent": "suttaplayer-phonemizer-config/1"})
    digest = hashlib.sha256()
    with urlopen(request, timeout=60) as response:
        for chunk in iter(lambda: response.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_model_version(explicit: str | None) -> str:
    if explicit:
        return explicit

    model_release = REPO_ROOT / "model" / "model-release.json"
    if model_release.exists():
        version = read_json(model_release).get("modelVersion")
        if version:
            return str(version)

    manifest_path = REPO_ROOT / "version-manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"Missing {manifest_path}; pass --model-version")

    manifest = read_json(manifest_path)
    version = manifest.get("modelVersion") or manifest.get("version")
    if not version:
        raise SystemExit(f"No modelVersion/version in {manifest_path}; pass --model-version")
    return str(version)


def build_config(
    suttas_dir: Path,
    base_url: str,
    model_version: str,
    model_dir: Path | None = None,
    model_base_url: str = DEFAULT_MODEL_BASE_URL,
    allow_missing_model: bool = False,
) -> dict:
    version_manifest_path = suttas_dir / "version-manifest.json"
    if not version_manifest_path.exists():
        raise SystemExit(f"Missing {version_manifest_path}")

    version_manifest = read_json(version_manifest_path)
    source_version = version_manifest.get("version")
    source_build_version = version_manifest.get("buildVersion")
    if not source_version:
        raise SystemExit(f"No version in {version_manifest_path}")

    base = base_url.rstrip("/") + "/"
    maps = []
    for filename in (EN_MAP_FILENAME, PI_MAP_FILENAME):
        path = suttas_dir / "phoneme" / filename
        if not path.exists():
            raise SystemExit(f"Missing phoneme map: {path}")
        maps.append(
            {
                "url": base + "phoneme/" + filename,
                "sha256": sha256_file(path),
                "sourceVersion": str(source_version),
                "sourceBuildVersion": str(source_build_version or ""),
            }
        )

    config = {
        "schemaVersion": 1,
        "modelVersion": model_version,
        "english_ipa_map": maps[0],
        "pali_ipa_map": maps[1],
        "tokenize": True,
        "strictMode": False,
        "preProcessRegExFindReplaceList": PRE_PROCESS_RULES,
        "postProcessRegExFindReplList": POST_PROCESS_RULES,
        "patchProcessRegExFindReplList": PATCH_PROCESS_RULES,
        "dictionaryResponder": {"customPhonemes": {}},
        "invalidTerm": "ˈɪn vˈælɪd tˈɜːm",
    }

    if model_dir is not None:
        release_path = model_dir / "model-release.json"
        if not release_path.exists() and not allow_missing_model:
            raise SystemExit(f"Missing {release_path}; run scripts/fetch_model_release.sh")
        if release_path.exists():
            release = read_json(release_path)
            canonical = release.get("canonical", "en_gb-suttaplayer-medium")
            base = (model_base_url.rstrip("/") + "/model/") if model_base_url else "model/"
            onnx = model_dir / f"{canonical}.onnx"
            onnx_json = model_dir / f"{canonical}.onnx.json"
            adapter = model_dir / f"{canonical}.adapter.json"
            for path in (onnx, onnx_json, adapter):
                if not path.exists() and not allow_missing_model:
                    raise SystemExit(f"Missing model artifact: {path}")
            if onnx.exists():
                config["model"] = {
                    "id": canonical,
                    "url": base + onnx.name,
                    "sha256": sha256_file(onnx),
                    "sizeBytes": onnx.stat().st_size,
                }
            if onnx_json.exists():
                config["model"]["configUrl"] = base + onnx_json.name
                config["model"]["configSha256"] = sha256_file(onnx_json)
            quant = model_dir / f"{canonical}-quant.onnx"
            quant_json = model_dir / f"{canonical}-quant.onnx.json"
            if quant.exists():
                config["modelQuant"] = {
                    "id": f"{canonical}-quant",
                    "url": base + quant.name,
                    "sha256": sha256_file(quant),
                    "sizeBytes": quant.stat().st_size,
                }
                if quant_json.exists():
                    config["modelQuant"]["configUrl"] = base + quant_json.name
                    config["modelQuant"]["configSha256"] = sha256_file(quant_json)
            if adapter.exists():
                config["modelAdapter"] = {
                    "adapterId": release.get("adapterId", "pali-en-gb-v1"),
                    "url": base + adapter.name,
                    "sha256": sha256_file(adapter),
                }
    return config


def verify_remote(config: dict) -> None:
    for key in ("model", "modelQuant"):
        if key in config and config[key].get("url"):
            dependency = config[key]
            actual = sha256_url(dependency["url"])
            if actual != dependency["sha256"]:
                raise SystemExit(f"Remote SHA-256 mismatch for {dependency['url']}: expected {dependency['sha256']}, got {actual}")
            print(f"verified {dependency['url']} ({actual})")
    if "modelAdapter" in config:
        dependency = config["modelAdapter"]
        actual = sha256_url(dependency["url"])
        if actual != dependency["sha256"]:
            raise SystemExit(f"Remote SHA-256 mismatch for {dependency['url']}: expected {dependency['sha256']}, got {actual}")
        print(f"verified {dependency['url']} ({actual})")
    for key in ("english_ipa_map", "pali_ipa_map"):
        dependency = config[key]
        actual = sha256_url(dependency["url"])
        if actual != dependency["sha256"]:
            raise SystemExit(
                f"Remote SHA-256 mismatch for {dependency['url']}: "
                f"expected {dependency['sha256']}, got {actual}"
            )
        print(f"verified {dependency['url']} ({actual})")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--suttas-dir",
        type=Path,
        default=DEFAULT_SUTTAS_DIR,
        help=f"Path to the suttas checkout (default: {DEFAULT_SUTTAS_DIR})",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Public suttas base URL (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--model-version",
        help="Model version to encode (default: version-manifest.json modelVersion)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output config path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        default=REPO_ROOT / "version-manifest.json",
        help="Endpoint version manifest path",
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=REPO_ROOT / "model",
        help="Directory holding the fetched model, config and adapter",
    )
    parser.add_argument(
        "--model-base-url",
        default=DEFAULT_MODEL_BASE_URL,
        help="Public vits-piper base URL; empty emits paths relative to the endpoint",
    )
    parser.add_argument(
        "--allow-missing-model",
        action="store_true",
        help="Generate without model/adapter fields (dictionary-only dry runs)",
    )
    parser.add_argument(
        "--check-remote",
        action="store_true",
        help="Verify the public map URLs match the generated SHA-256 digests",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = build_config(
        args.suttas_dir.resolve(),
        args.base_url,
        resolve_model_version(args.model_version),
        model_dir=args.model_dir.resolve(),
        model_base_url=args.model_base_url,
        allow_missing_model=args.allow_missing_model,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {args.output} "
        f"(model {config['modelVersion']}, "
        f"source {config['english_ipa_map']['sourceVersion']})"
    )

    if args.manifest_output:
        config["generatedAt"] = __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        manifest = {
            "version": config["modelVersion"],
            "modelVersion": config["modelVersion"],
            "corpusVersion": config["pali_ipa_map"].get("sourceBuildVersion"),
            "sourceVersion": config["english_ipa_map"].get("sourceVersion"),
            "generatedAt": config["generatedAt"],
            "adapters": {
                "model": config.get("model"),
                "quant": config.get("modelQuant"),
                "phoneme": config.get("modelAdapter"),
            },
        }
        args.manifest_output.parent.mkdir(parents=True, exist_ok=True)
        args.manifest_output.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {args.manifest_output}")

    if args.check_remote:
        verify_remote(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())

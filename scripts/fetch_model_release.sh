#!/usr/bin/env bash
# Fetch the trainer's model release into ./model/ and normalise filenames.
#
#   scripts/fetch_model_release.sh
#
# Local testing: set MODEL_SOURCE_DIR to a directory containing the three
# assets (and optionally SHA256SUMS) to skip GitHub.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$ROOT/model-release.json"
[ -f "$MANIFEST" ] || { echo "missing $MANIFEST" >&2; exit 2; }

readarray -t FIELDS < <(python3 - "$MANIFEST" <<'PY'
import json,sys
m=json.load(open(sys.argv[1]))
print(m["repository"]); print(m["tag"]); print(m["canonical"])
for k in ("onnx","config","adapter","quant"): print(m["assets"].get(k,""))
PY
)
REPO="${FIELDS[0]}"; TAG="${FIELDS[1]}"; CANON="${FIELDS[2]}"
ONNX="${FIELDS[3]}"; CONFIG="${FIELDS[4]}"; ADAPTER="${FIELDS[5]}"; QUANT="${FIELDS[6]:-}"

mkdir -p "$ROOT/model"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

if [ -n "${MODEL_SOURCE_DIR:-}" ]; then
  src="$MODEL_SOURCE_DIR"
else
  echo "downloading $TAG from $REPO"
  gh release download "$TAG" --repo "$REPO" --dir "$TMP" --clobber
  src="$TMP"
fi

for f in "$ONNX" "$CONFIG" "$ADAPTER"; do
  [ -f "$src/$f" ] || { echo "missing model asset: $src/$f" >&2; exit 2; }
done
if [ -n "$QUANT" ]; then
  [ -f "$src/$QUANT" ] || { echo "missing quant asset: $src/$QUANT" >&2; exit 2; }
fi

if [ -f "$src/SHA256SUMS" ]; then
  (cd "$src" && sha256sum -c SHA256SUMS)
else
  echo "WARN: no SHA256SUMS in model source; computing local hashes"
fi

cp "$src/$ONNX"    "$ROOT/model/$CANON.onnx"
cp "$src/$CONFIG"  "$ROOT/model/$CANON.onnx.json"
cp "$src/$ADAPTER" "$ROOT/model/$CANON.adapter.json"
if [ -n "$QUANT" ]; then
  cp "$src/$QUANT" "$ROOT/model/$CANON-quant.onnx"
  cp "$src/$CONFIG" "$ROOT/model/$CANON-quant.onnx.json"
fi

python3 - "$ROOT" "$CANON" "$TAG" "$REPO" <<'PY'
import hashlib,json,pathlib,sys
root,canon,tag,repo=sys.argv[1:]
m=json.load(open(pathlib.Path(root)/"model-release.json"))
m["resolvedTag"]=tag; m["resolvedRepository"]=repo
m["sha256"]={}
for key,suffix in (("onnx",".onnx"),("quant","-quant.onnx"),("config",".onnx.json"),("adapter",".adapter.json")):
    p=pathlib.Path(root)/"model"/f"{canon}{suffix}"
    if not p.exists(): continue
    m["sha256"][key]=hashlib.sha256(p.read_bytes()).hexdigest()
    m["sizeBytes"]=p.stat().st_size if key=="onnx" else m.get("sizeBytes")
pathlib.Path(root,"model","model-release.json").write_text(json.dumps(m,indent=2)+"\n")
print("wrote model/model-release.json")
PY
sha256sum "$ROOT/model/$CANON.onnx" "$ROOT/model/$CANON.adapter.json"

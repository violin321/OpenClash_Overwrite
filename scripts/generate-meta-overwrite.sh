#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT_DIR/Overwrite/Overwrite.conf"
DST="$ROOT_DIR/Overwrite/Overwrite-meta.conf"

[[ -f "$SRC" ]] || {
  echo "Source file not found: $SRC" >&2
  exit 1
}

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

python3 - "$SRC" "$tmp" <<'PY'
from pathlib import Path
import re
import sys

src = Path(sys.argv[1]).read_text(encoding='utf-8')
out = Path(sys.argv[2])
new, count = re.subn(r'(?m)^(CORE_TYPE\s*=\s*)Smart\s*$', r'\1Meta', src, count=1)
if count != 1:
    print('Failed to replace CORE_TYPE = Smart with CORE_TYPE = Meta exactly once', file=sys.stderr)
    sys.exit(1)
out.write_text(new, encoding='utf-8')
PY

grep -q '^CORE_TYPE = Meta$' "$tmp" || {
  echo 'Validation failed: CORE_TYPE = Meta not found in generated file' >&2
  exit 1
}
if grep -q '^CORE_TYPE = Smart$' "$tmp"; then
  echo 'Validation failed: generated file still contains CORE_TYPE = Smart' >&2
  exit 1
fi

mv "$tmp" "$DST"
echo "Generated ${DST#$ROOT_DIR/}"

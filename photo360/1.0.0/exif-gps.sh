#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: exif-gps reference.jpg target.jpg"
  exit 1
fi

ref="$1"
shift
for tgt in "$@"; do
  echo "Copying GPS from $ref -> $tgt"
  exiftool -overwrite_original -tagsfromfile "$ref" -gps:all "$tgt"
done

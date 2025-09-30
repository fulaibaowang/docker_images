#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: exif-gpano target.jpg [more.jpg ...]"
  exit 1
fi

for tgt in "$@"; do
  echo "Adding GPano tags to $tgt"
  exiftool -overwrite_original \
    -XMP-GPano:UsePanoramaViewer=True \
    -XMP-GPano:ProjectionType=equirectangular \
    -XMP-GPano:FullPanoWidthPixels=3840 \
    -XMP-GPano:FullPanoHeightPixels=1920 \
    -XMP-GPano:CroppedAreaLeftPixels=0 \
    -XMP-GPano:CroppedAreaTopPixels=0 \
    -XMP-GPano:CroppedAreaImageWidthPixels=3840 \
    -XMP-GPano:CroppedAreaImageHeightPixels=1920 \
    "$tgt"
done

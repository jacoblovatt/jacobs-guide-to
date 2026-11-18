#!/usr/bin/env bash
# Official portable Quarto; no sudo and no modification of shell startup files.
set -eu
cd "$(dirname "$0")/.."
version=$(cat .quarto-version)
case "$(uname -s)/$(uname -m)" in
  Linux/x86_64) platform=linux-amd64 ;;
  Linux/aarch64) platform=linux-arm64 ;;
  *) echo 'Use the official installer at https://quarto.org/docs/get-started/ and match .quarto-version.' >&2; exit 1 ;;
esac
if [ -x ".tools/quarto-$version/bin/quarto" ]; then
  ".tools/quarto-$version/bin/quarto" --version
  exit 0
fi
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
base="https://github.com/quarto-dev/quarto-cli/releases/download/v$version"
archive="quarto-$version-$platform.tar.gz"
curl -fL --retry 2 "$base/$archive" -o "$work/$archive"
curl -fsSL "$base/quarto-$version-checksums.txt" -o "$work/checksums.txt"
(cd "$work"; awk -v file="$archive" '$2 == file {print}' checksums.txt > selected.txt; test -s selected.txt; sha256sum -c selected.txt)
mkdir -p .tools
tar -xzf "$work/$archive" -C .tools
".tools/quarto-$version/bin/quarto" --version

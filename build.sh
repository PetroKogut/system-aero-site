#!/usr/bin/env bash
# Builds the site into dist/ — used by Cloudflare Pages and locally.
set -e
rm -rf dist && mkdir -p dist
cp -r static/. dist/
OUT_DIR=dist python3 src/generate.py
OUT_DIR=dist python3 src/locale_pl.py
echo "built $(find dist -name index.html | wc -l) pages into dist/"

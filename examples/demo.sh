#!/usr/bin/env bash
cd "$(dirname "$0")/.."
run() { printf '$ %s\n' "$*"; "$@"; printf '[exit %s]\n\n' "$?"; }
echo "# Lint a memory folder with a missing file, an orphan and a dangling [[link]]"
run python3 scripts/memory_lint.py examples/memory
echo "# Your real folder is usually ~/.claude/projects/<project>/memory"

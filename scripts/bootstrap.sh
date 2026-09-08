#!/usr/bin/env bash
# One-time setup for a fresh clone of kph-pages.
# Points git at the versioned hooks directory so the PII guard travels with the repo
# instead of living in .git/hooks, which git does not clone.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git config core.hooksPath .githooks
chmod +x .githooks/* scripts/*.sh 2>/dev/null || true
echo "hooksPath -> .githooks"
echo "PII guard active. Verify with:  git config core.hooksPath"

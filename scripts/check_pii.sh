#!/usr/bin/env bash
# check_pii.sh — refuse to let personal data reach the public gh-pages branch.
#
# kph-pages publishes from gh-pages. A commit here is publication to the open web.
# On 2026-08-05 a delegated agent put one lead's name, phone, lid and Firebase id
# into brain/LESSONS.md; it was live before being caught and redacted the same day.
# This makes that failure mechanical instead of remembered.
#
# Blocks any staged file containing:
#   - a run of 9 or more digits   (phone numbers, WhatsApp lids)
#   - a lid JID: 6+ digits immediately followed by "@lid"
#     (a bare "@lid", i.e. the column name in prose, identifies nobody and passes)
#
# Allowed through: 32-hex md5/sha digests, ISO timestamps, and run_id strings,
# which are stripped before the scan rather than whitelisted per-file.
#
# Usage:  scripts/check_pii.sh            # scan staged files (what the hook runs)
#         scripts/check_pii.sh <paths...> # scan specific files
#
# Activate the hook (not versioned by git, so every fresh clone must repeat this):
#   printf '#!/usr/bin/env bash\nexec "$(git rev-parse --show-toplevel)"/scripts/check_pii.sh\n' \
#     > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
set -uo pipefail

# macOS ships bash 3.2 — no mapfile. Use a portable read loop.
files=()
if [ "$#" -gt 0 ]; then
  files=("$@")
else
  while IFS= read -r line; do
    [ -n "$line" ] && files+=("$line")
  done < <(git diff --cached --name-only --diff-filter=ACM)
fi
[ "${#files[@]}" -eq 0 ] && exit 0

fail=0
for f in "${files[@]}"; do
  [ -f "$f" ] || continue
  case "$f" in *.png|*.jpg|*.jpeg|*.gif|*.pdf|*.woff*|*.ico) continue ;; esac

  allow="$(git rev-parse --show-toplevel 2>/dev/null)/scripts/pii_allowlist.txt"
  strip_allow='cat'
  if [ -f "$allow" ]; then
    # drop allowlisted non-personal ids (Meta ad/page/post ids) before scanning
    pat=$(grep -oE '^[0-9]{9,}' "$allow" | paste -sd'|' -)
    [ -n "$pat" ] && strip_allow="sed -E s/($pat)//g"
  fi

  hits=$(
    sed -E \
      -e 's/(data:[a-z/]+;base64,)[A-Za-z0-9+\/=]+/\\1<stripped>/g' \
      -e 's/\b[0-9a-f]{32,64}\b//g' \
      -e 's/[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:.+-]+//g' \
      -e 's/"?run_id"?[[:space:]]*[:=][[:space:]]*"[^"]*"//g' \
      "$f" 2>/dev/null | $strip_allow \
    | grep -nE '[0-9]{9,}|[0-9]{6,}@lid' | head -5
  )
  if [ -n "$hits" ]; then
    fail=1
    echo "PII CHECK FAILED: $f"
    echo "$hits" | sed 's/^/    /'
  fi
done

if [ "$fail" -ne 0 ]; then
  cat >&2 <<'MSG'

BLOCKED — a staged file looks like it contains a phone number or a WhatsApp lid.
kph-pages is PUBLIC. Move the file out of the repo; do not weaken this check.
Per-lead data belongs in _marketing_brain/data/<run_id>/ or Google Drive.
MSG
  exit 1
fi
echo "PII check passed (${#files[@]} file(s))"

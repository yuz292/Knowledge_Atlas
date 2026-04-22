#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
PROFILE="${1:-staging}"
if [[ $# -gt 0 ]]; then
  shift
fi

if [[ -f "$REPO/.smoke.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$REPO/.smoke.env"
  set +a
fi

REPORT_DIR="${REPORT_DIR:-$REPO/docs/browser_smoke_reports}"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
MD_OUT="$REPORT_DIR/${PROFILE}_${TIMESTAMP}.md"
JSON_OUT="$REPORT_DIR/${PROFILE}_${TIMESTAMP}.json"
LATEST_MD="$REPORT_DIR/latest_${PROFILE}.md"
LATEST_JSON="$REPORT_DIR/latest_${PROFILE}.json"

mkdir -p "$REPORT_DIR"

set +e
python3 "$REPO/scripts/browser_runtime_smoke.py" \
  --profile "$PROFILE" \
  --md-out "$MD_OUT" \
  --json-out "$JSON_OUT" \
  "$@"
RC=$?
set -e

if [[ -f "$MD_OUT" ]]; then
  cp "$MD_OUT" "$LATEST_MD"
fi
if [[ -f "$JSON_OUT" ]]; then
  cp "$JSON_OUT" "$LATEST_JSON"
fi

echo
echo "Browser smoke reports:"
echo "  markdown: $MD_OUT"
echo "  json:     $JSON_OUT"
echo "  latest:   $LATEST_MD"
echo "  latest:   $LATEST_JSON"

exit "$RC"

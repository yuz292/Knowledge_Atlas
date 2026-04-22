#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
PROFILE="${1:-staging}"
if [[ $# -gt 0 ]]; then
  shift
fi

if [[ -n "${PYTHON_BIN:-}" ]]; then
  PYTHON_CMD="$PYTHON_BIN"
elif [[ -x "$REPO/.venv/bin/python" ]]; then
  PYTHON_CMD="$REPO/.venv/bin/python"
else
  PYTHON_CMD="python3"
fi

if [[ -f "$REPO/.smoke.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$REPO/.smoke.env"
  set +a
fi

echo
echo "== Ruthless validation: pytest contract bundle =="
"$PYTHON_CMD" -m pytest \
  "$REPO/tests/test_site_runtime_smoke.py" \
  "$REPO/tests/test_payload_soft_rebuild_contract.py" \
  -q

echo
echo "== Ruthless validation: runtime smoke ($PROFILE) =="
bash "$REPO/scripts/run_site_runtime_smoke.sh" "$PROFILE" "$@"

echo
echo "== Ruthless validation: browser smoke ($PROFILE) =="
bash "$REPO/scripts/run_browser_runtime_smoke.sh" "$PROFILE" "$@"

echo
echo "Ruthless validation completed for profile: $PROFILE"

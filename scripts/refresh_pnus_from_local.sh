#!/usr/bin/env bash
# refresh_pnus_from_local.sh — the ONLY command the web-server SSH key is
# allowed to invoke on the instructor's Mac.
#
# Flow:
#   web server (xrlab.ucsd.edu)
#     └─ ssh -i ~/.ssh/ka_refresh_key  ka-refresh@DK_MAC  (forced-command)
#          └─ this script runs (no args accepted; stdin ignored)
#               └─ regenerates  Knowledge_Atlas/data/ka_payloads/pnus.json
#               └─ prints the fresh JSON to stdout
#
# The server captures stdout, writes it to its own pnus.json, and returns
# success to the admin browser. Nothing else can happen over this SSH key.
#
# Install: see docs/SSH_SETUP_FOR_PNU_REFRESH.md

set -euo pipefail

KA_ROOT="${HOME}/REPOS/Knowledge_Atlas"
GENERATOR="${KA_ROOT}/scripts/regenerate_pnus_json.py"
OUT_JSON="${KA_ROOT}/data/ka_payloads/pnus.json"
LOG="${HOME}/Library/Logs/ka_refresh_pnus.log"

# Log everything to a file so we can audit who pulled what, when.
{
  echo "=== $(date -u +%FT%TZ) refresh_pnus_from_local triggered ==="
  echo "Caller: ${SSH_CLIENT:-local} via ${SSH_CONNECTION:-local}"

  if [[ ! -x "$(command -v python3)" ]]; then
    echo "ERROR: python3 not on PATH" >&2
    exit 2
  fi
  if [[ ! -f "${GENERATOR}" ]]; then
    echo "ERROR: generator missing at ${GENERATOR}" >&2
    exit 3
  fi

  # Regenerate (stderr to log; stdout suppressed so only the JSON hits stdout below)
  python3 "${GENERATOR}" >&2

  if [[ ! -f "${OUT_JSON}" ]]; then
    echo "ERROR: ${OUT_JSON} did not materialise" >&2
    exit 4
  fi
  echo "OK: regenerated. Size: $(wc -c < "${OUT_JSON}") bytes"
} >> "${LOG}" 2>&1

# Emit the JSON to stdout so the caller (SSH session) receives it.
cat "${OUT_JSON}"

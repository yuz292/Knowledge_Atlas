#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
  echo "Run this as root: sudo bash $0" >&2
  exit 1
fi

DEPLOY_GROUP="${DEPLOY_GROUP:-ka-deploy}"
PRIMARY_USER="${PRIMARY_USER:-dkirsh}"
LEGACY_SERVICE_USER="${LEGACY_SERVICE_USER:-trathore}"

echo "== Preparing shared deploy control =="
echo "Deploy group:        $DEPLOY_GROUP"
echo "Primary operator:    $PRIMARY_USER"
echo "Legacy service user: $LEGACY_SERVICE_USER"
echo

groupadd -f "$DEPLOY_GROUP"
usermod -aG "$DEPLOY_GROUP" "$PRIMARY_USER"

if id "$LEGACY_SERVICE_USER" >/dev/null 2>&1; then
  usermod -aG "$DEPLOY_GROUP" "$LEGACY_SERVICE_USER"
else
  echo "Skipping legacy service user; '$LEGACY_SERVICE_USER' does not exist."
fi

echo
echo "-- resulting memberships --"
id "$PRIMARY_USER"
if id "$LEGACY_SERVICE_USER" >/dev/null 2>&1; then
  id "$LEGACY_SERVICE_USER"
fi
echo

echo "Shared deploy control prepared."

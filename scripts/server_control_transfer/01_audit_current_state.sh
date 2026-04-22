#!/usr/bin/env bash
set -euo pipefail

PRODUCTION_PATH="${PRODUCTION_PATH:-/var/www/xrlab/ka}"
STAGING_PATH="${STAGING_PATH:-/home/dkirsh/ka-staging-2026-04-20}"
SERVICE_NAME="${SERVICE_NAME:-ka-auth.service}"
PRIMARY_USER="${PRIMARY_USER:-dkirsh}"
LEGACY_SERVICE_USER="${LEGACY_SERVICE_USER:-trathore}"

echo "== Knowledge Atlas control-transfer audit =="
echo "Production path: $PRODUCTION_PATH"
echo "Staging path:    $STAGING_PATH"
echo "Service:         $SERVICE_NAME"
echo

echo "-- whoami / id --"
whoami
id
echo

echo "-- sudo rights --"
sudo -l
echo

echo "-- service status --"
sudo systemctl status "$SERVICE_NAME" --no-pager | sed -n '1,20p'
echo

echo "-- service unit --"
sudo systemctl cat "$SERVICE_NAME"
echo

echo "-- key ownership and permissions --"
sudo ls -ld "$PRODUCTION_PATH" "$PRODUCTION_PATH/data" "$STAGING_PATH" || true
echo

echo "-- sample production tree ownerships --"
sudo find "$PRODUCTION_PATH" -maxdepth 2 -printf '%M %u %g %p\n' | sort | sed -n '1,120p'
echo

echo "-- user memberships --"
id "$PRIMARY_USER"
if id "$LEGACY_SERVICE_USER" >/dev/null 2>&1; then
  id "$LEGACY_SERVICE_USER"
else
  echo "legacy service user '$LEGACY_SERVICE_USER' does not exist on this host"
fi
echo

echo "-- current auth runtime user --"
ps -eo user,pid,command | grep "[k]a_auth_server.py" || true
echo

echo "Audit complete."

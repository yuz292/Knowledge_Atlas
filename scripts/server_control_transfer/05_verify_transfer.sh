#!/usr/bin/env bash
set -euo pipefail

PRODUCTION_PATH="${PRODUCTION_PATH:-/var/www/xrlab/ka}"
STAGING_PATH="${STAGING_PATH:-/home/dkirsh/ka-staging-2026-04-20}"
SERVICE_NAME="${SERVICE_NAME:-ka-auth.service}"
PRIMARY_USER="${PRIMARY_USER:-dkirsh}"
DEPLOY_GROUP="${DEPLOY_GROUP:-ka-deploy}"

echo "== Verifying Knowledge Atlas control transfer =="
echo

echo "-- service status --"
sudo systemctl status "$SERVICE_NAME" --no-pager | sed -n '1,20p'
echo

echo "-- service override --"
sudo systemctl cat "$SERVICE_NAME"
echo

echo "-- production and staging permissions --"
ls -ld "$PRODUCTION_PATH" "$PRODUCTION_PATH/data" "$STAGING_PATH"
echo

echo "-- group membership --"
id "$PRIMARY_USER"
echo

echo "-- passwordless operational commands --"
sudo -n /usr/sbin/nginx -t
sudo -n /bin/systemctl status "$SERVICE_NAME" --no-pager | sed -n '1,8p'
echo

echo "-- production smoke --"
cd "$PRODUCTION_PATH"
bash scripts/run_site_runtime_smoke.sh production
echo

echo "Verification complete."

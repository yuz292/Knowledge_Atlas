#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
  echo "Run this as root: sudo bash $0" >&2
  exit 1
fi

DEPLOY_GROUP="${DEPLOY_GROUP:-ka-deploy}"
PRIMARY_USER="${PRIMARY_USER:-dkirsh}"
PRODUCTION_PATH="${PRODUCTION_PATH:-/var/www/xrlab/ka}"
STAGING_PATH="${STAGING_PATH:-/home/dkirsh/ka-staging-2026-04-20}"

for path in "$PRODUCTION_PATH" "$STAGING_PATH"; do
  if [[ ! -d "$path" ]]; then
    echo "Expected path does not exist: $path" >&2
    exit 1
  fi
done

echo "== Aligning Knowledge Atlas tree permissions =="
echo "Production path: $PRODUCTION_PATH"
echo "Staging path:    $STAGING_PATH"
echo "Deploy group:    $DEPLOY_GROUP"
echo

chgrp -R "$DEPLOY_GROUP" "$PRODUCTION_PATH"
chmod -R u+rwX,g+rwX,o+rX "$PRODUCTION_PATH"
find "$PRODUCTION_PATH" -type d -exec chmod g+s {} +
chmod 2775 "$PRODUCTION_PATH/data"

chown -R "$PRIMARY_USER:$DEPLOY_GROUP" "$STAGING_PATH"
chmod -R u+rwX,g+rwX,o+rX "$STAGING_PATH"
find "$STAGING_PATH" -type d -exec chmod g+s {} +
if [[ -d "$STAGING_PATH/data" ]]; then
  chmod 2775 "$STAGING_PATH/data"
fi

echo "-- key permissions after change --"
ls -ld "$PRODUCTION_PATH" "$PRODUCTION_PATH/data" "$STAGING_PATH"
echo

echo "Tree permissions aligned."

#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
  echo "Run this as root: sudo bash $0" >&2
  exit 1
fi

SERVICE_NAME="${SERVICE_NAME:-ka-auth.service}"
SERVICE_USER="${SERVICE_USER:-dkirsh}"
DEPLOY_GROUP="${DEPLOY_GROUP:-ka-deploy}"
WORKDIR="${WORKDIR:-/var/www/xrlab/ka}"
DROPIN_DIR="/etc/systemd/system/${SERVICE_NAME}.d"
DROPIN_PATH="${DROPIN_DIR}/20-ka-control-transfer.conf"

mkdir -p "$DROPIN_DIR"

cat >"$DROPIN_PATH" <<EOF
[Service]
User=$SERVICE_USER
Group=$DEPLOY_GROUP
SupplementaryGroups=$DEPLOY_GROUP
WorkingDirectory=$WORKDIR
UMask=0002
EOF

echo "Wrote $DROPIN_PATH"
echo
cat "$DROPIN_PATH"
echo

systemctl daemon-reload
systemctl restart "$SERVICE_NAME"
systemctl status "$SERVICE_NAME" --no-pager | sed -n '1,20p'

echo
echo "Auth service user switch complete."

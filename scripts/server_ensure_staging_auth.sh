#!/usr/bin/env bash
# Ensure the staging auth process is running with the expected staging paths
# and a valid SMTP configuration.

set -euo pipefail

STAGING_PATH="${STAGING_PATH:-/home/dkirsh/ka-staging-2026-04-20}"
PRODUCTION_PATH="${PRODUCTION_PATH:-/var/www/xrlab/ka}"
STAGING_AUTH_HOST="${STAGING_AUTH_HOST:-127.0.0.1}"
STAGING_AUTH_PORT="${STAGING_AUTH_PORT:-8766}"
STAGING_PUBLIC_URL="${STAGING_PUBLIC_URL:-https://xrlab.ucsd.edu/staging_KA}"
STAGING_DB_PATH="${STAGING_DB_PATH:-$STAGING_PATH/data/ka_auth.db}"
STAGING_SECRET_FILE="${STAGING_SECRET_FILE:-$STAGING_PATH/data/ka_auth_secret.txt}"
STAGING_LOG_FILE="${STAGING_LOG_FILE:-$STAGING_PATH/logs/ka-auth-staging.log}"
STAGING_PID_FILE="${STAGING_PID_FILE:-$STAGING_PATH/logs/ka-auth-staging.pid}"
PRODUCTION_PID_PATTERN="${PRODUCTION_PID_PATTERN:-$PRODUCTION_PATH/ka_auth_server.py}"

die() {
  echo "staging auth ensure failed: $*" >&2
  exit 1
}

read_env_value() {
  local pid="$1"
  local name="$2"
  python3 - "$pid" "$name" <<'PY'
import sys
from pathlib import Path

pid = sys.argv[1]
name = sys.argv[2]
env_path = Path(f"/proc/{pid}/environ")
if not env_path.exists():
    raise SystemExit(1)
raw = env_path.read_bytes().split(b"\0")
for item in raw:
    if item.startswith(name.encode() + b"="):
        print(item.split(b"=", 1)[1].decode())
        raise SystemExit(0)
raise SystemExit(1)
PY
}

resolve_smtp_var() {
  local name="$1"
  local override_name="KA_STAGING_${name#KA_}"
  local current="${!override_name:-${!name:-}}"
  if [[ -n "$current" ]]; then
    printf '%s' "$current"
    return 0
  fi

  local production_pid
  production_pid="$(pgrep -f "$PRODUCTION_PID_PATTERN" | head -n1 || true)"
  [[ -n "$production_pid" ]] || return 1
  read_env_value "$production_pid" "$name"
}

current_staging_pid() {
  if [[ -f "$STAGING_PID_FILE" ]]; then
    local pid
    pid="$(cat "$STAGING_PID_FILE" 2>/dev/null || true)"
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      printf '%s' "$pid"
      return 0
    fi
  fi
  pgrep -f "uvicorn ka_auth_server:app --host $STAGING_AUTH_HOST --port $STAGING_AUTH_PORT" | head -n1 || true
}

staging_process_is_current() {
  local pid="$1"
  [[ -n "$pid" ]] || return 1
  local public_url db_path secret_file smtp_host
  public_url="$(read_env_value "$pid" "KA_PUBLIC_SITE_URL" 2>/dev/null || true)"
  db_path="$(read_env_value "$pid" "KA_DB_PATH" 2>/dev/null || true)"
  secret_file="$(read_env_value "$pid" "KA_SECRET_FILE" 2>/dev/null || true)"
  smtp_host="$(read_env_value "$pid" "KA_SMTP_HOST" 2>/dev/null || true)"
  [[ "$public_url" == "$STAGING_PUBLIC_URL" ]] || return 1
  [[ "$db_path" == "$STAGING_DB_PATH" ]] || return 1
  [[ "$secret_file" == "$STAGING_SECRET_FILE" ]] || return 1
  [[ -n "$smtp_host" ]] || return 1
}

wait_for_health() {
  local url="http://$STAGING_AUTH_HOST:$STAGING_AUTH_PORT/health"
  for _ in $(seq 1 15); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  return 1
}

main() {
  [[ -d "$STAGING_PATH" ]] || die "staging path missing: $STAGING_PATH"
  mkdir -p "$(dirname "$STAGING_LOG_FILE")"

  local current_pid
  current_pid="$(current_staging_pid)"
  if staging_process_is_current "$current_pid"; then
    wait_for_health || die "existing staging auth process is not healthy"
    echo "staging auth already configured (pid $current_pid)"
    return 0
  fi

  local smtp_host smtp_port smtp_ssl smtp_starttls smtp_user smtp_password smtp_from
  smtp_host="$(resolve_smtp_var "KA_SMTP_HOST" || true)"
  smtp_port="$(resolve_smtp_var "KA_SMTP_PORT" || true)"
  smtp_ssl="$(resolve_smtp_var "KA_SMTP_SSL" || true)"
  smtp_starttls="$(resolve_smtp_var "KA_SMTP_STARTTLS" || true)"
  smtp_user="$(resolve_smtp_var "KA_SMTP_USER" || true)"
  smtp_password="$(resolve_smtp_var "KA_SMTP_PASSWORD" || true)"
  smtp_from="$(resolve_smtp_var "KA_SMTP_FROM" || true)"

  [[ -n "$smtp_host" ]] || die "could not resolve staging SMTP host"
  [[ -n "$smtp_port" ]] || smtp_port="25"
  [[ -n "$smtp_ssl" ]] || smtp_ssl="0"
  [[ -n "$smtp_starttls" ]] || smtp_starttls="0"
  [[ -n "$smtp_from" ]] || die "could not resolve staging SMTP from address"

  if [[ -n "$current_pid" ]]; then
    kill "$current_pid" 2>/dev/null || true
    sleep 1
  fi
  pkill -f "uvicorn ka_auth_server:app --host $STAGING_AUTH_HOST --port $STAGING_AUTH_PORT" 2>/dev/null || true

  (
    cd "$STAGING_PATH"
    env \
      KA_SECRET_FILE="$STAGING_SECRET_FILE" \
      KA_PUBLIC_SITE_URL="$STAGING_PUBLIC_URL" \
      KA_DB_PATH="$STAGING_DB_PATH" \
      KA_SMTP_HOST="$smtp_host" \
      KA_SMTP_PORT="$smtp_port" \
      KA_SMTP_SSL="$smtp_ssl" \
      KA_SMTP_STARTTLS="$smtp_starttls" \
      KA_SMTP_USER="$smtp_user" \
      KA_SMTP_PASSWORD="$smtp_password" \
      KA_SMTP_FROM="$smtp_from" \
      nohup ./.venv/bin/python -m uvicorn ka_auth_server:app \
        --host "$STAGING_AUTH_HOST" \
        --port "$STAGING_AUTH_PORT" \
        >"$STAGING_LOG_FILE" 2>&1 &
    echo $! >"$STAGING_PID_FILE"
  )

  wait_for_health || die "staging auth did not become healthy"
  echo "staging auth restarted with SMTP configuration"
}

main "$@"

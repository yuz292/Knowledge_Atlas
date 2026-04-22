#!/usr/bin/env bash
# Canonical server-side Knowledge Atlas release cycle.
#
# Intended to be run on xrlab itself. It updates the staging checkout,
# runs the staging runtime smoke, promotes staging into the production tree,
# and then runs the production runtime smoke.

set -euo pipefail

MODE="${1:-full}"
if [[ $# -gt 0 ]]; then
  shift
fi

STAGING_PATH="${STAGING_PATH:-/home/dkirsh/ka-staging-2026-04-20}"
PRODUCTION_PATH="${PRODUCTION_PATH:-/var/www/xrlab/ka}"
REMOTE_NAME="${REMOTE_NAME:-origin}"
REMOTE_BRANCH="${REMOTE_BRANCH:-master}"
RESET_EMAIL="${KA_SMOKE_RESET_EMAIL:-}"

RSYNC_EXCLUDES=(
  --exclude='.git/'
  --exclude='.venv/'
  --exclude='__pycache__/'
  --exclude='ka_config.js'
  --exclude='data/ka_auth.db'
  --exclude='data/ka_auth.db-*'
  --exclude='data/ka_auth.db-wal'
  --exclude='data/ka_auth.db-shm'
  --exclude='data/ka_auth_secret.txt'
  --exclude='docs/runtime_smoke_reports/'
)

BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
RESET="\033[0m"

step=0
step_header() { step=$((step + 1)); printf "\n${BOLD}[Step %d]${RESET} %s\n" "$step" "$1"; }
ok()   { printf "  ${GREEN}✓${RESET} %s\n" "$1"; }
warn() { printf "  ${YELLOW}⚠${RESET} %s\n" "$1"; }
die()  { printf "  ${RED}✗${RESET} %s\n" "$1"; exit 1; }

usage() {
  cat <<'EOF'
Usage:
  bash scripts/server_release_cycle.sh full
  bash scripts/server_release_cycle.sh staging
  bash scripts/server_release_cycle.sh promote
  bash scripts/server_release_cycle.sh production-smoke

Modes:
  full              staging pull -> staging smoke -> promote -> production smoke
  staging           staging pull -> staging smoke
  promote           promote staging tree into production (no smoke)
  production-smoke  production smoke only

Environment overrides:
  STAGING_PATH
  PRODUCTION_PATH
  REMOTE_NAME
  REMOTE_BRANCH
  KA_SMOKE_RESET_EMAIL
EOF
}

ensure_path() {
  local label="$1"
  local path="$2"
  [[ -d "$path" ]] || die "$label path missing: $path"
}

pull_staging() {
  step_header "Update staging checkout"
  ensure_path "staging" "$STAGING_PATH"
  git -C "$STAGING_PATH" pull --rebase --autostash "$REMOTE_NAME" "$REMOTE_BRANCH"
  ok "staging updated to $(git -C "$STAGING_PATH" rev-parse --short HEAD)"
}

smoke_staging() {
  step_header "Run staging runtime smoke"
  ensure_path "staging" "$STAGING_PATH"
  (
    cd "$STAGING_PATH"
    bash scripts/server_ensure_staging_auth.sh
    bash scripts/run_site_runtime_smoke.sh staging --fail-on-skip
  )
  ok "staging runtime smoke passed"
}

promote_to_production() {
  step_header "Promote staging tree into production"
  ensure_path "staging" "$STAGING_PATH"
  ensure_path "production" "$PRODUCTION_PATH"
  rsync -a "${RSYNC_EXCLUDES[@]}" "$STAGING_PATH/" "$PRODUCTION_PATH/"
  if [[ -d "$PRODUCTION_PATH/data" ]]; then
    chmod 2775 "$PRODUCTION_PATH/data"
    chgrp 'domain users' "$PRODUCTION_PATH/data" || warn "could not set production data group to domain users"
    ok "production data directory permissions restored"
  else
    warn "production data directory missing after promotion"
  fi
  ok "production tree refreshed from staging"
}

smoke_production() {
  step_header "Run production runtime smoke"
  ensure_path "production" "$PRODUCTION_PATH"
  if [[ -n "$RESET_EMAIL" ]]; then
    (
      cd "$PRODUCTION_PATH"
      KA_SMOKE_RESET_EMAIL="$RESET_EMAIL" bash scripts/run_site_runtime_smoke.sh production
    )
  else
    (
      cd "$PRODUCTION_PATH"
      bash scripts/run_site_runtime_smoke.sh production
    )
  fi
  ok "production runtime smoke passed"
}

case "$MODE" in
  -h|--help|help)
    usage
    exit 0
    ;;
  staging)
    pull_staging
    smoke_staging
    ;;
  promote)
    promote_to_production
    ;;
  production-smoke)
    smoke_production
    ;;
  full)
    pull_staging
    smoke_staging
    promote_to_production
    smoke_production
    ;;
  *)
    usage
    die "unknown mode: $MODE"
    ;;
esac

printf "\n${BOLD}${GREEN}Release cycle step(s) completed.${RESET}\n"

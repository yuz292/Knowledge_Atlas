#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bootstrap_full_system_from_handoff.sh --repo-root /path/to/REPOS --bundle-dir /path/to/handoff [--with-af-full] [--python python3.12]

What it does:
  1. Unpacks the required runtime bundle into the repo root.
  2. Optionally unpacks the larger Article Finder full-data bundle.
  3. Creates/refreshes the Python virtual environments for AE, AF, and KA.
  4. Installs Python dependencies.
  5. Runs smoke tests for AF, AE, and KA.

Assumptions:
  - The four repos are already cloned under the repo root:
      Knowledge_Atlas
      Article_Eater_PostQuinean_v1_recovery
      Article_Finder_v3_2_3
      Designing_Experiments
  - The handoff directory contains:
      ka_ae_af_runtime_bundle_2026-03-26.zip
      article_finder_full_data_bundle_2026-03-26.zip   (optional)
EOF
}

log() {
  printf '[handoff-bootstrap] %s\n' "$*"
}

require_dir() {
  if [[ ! -d "$1" ]]; then
    printf 'Missing required directory: %s\n' "$1" >&2
    exit 1
  fi
}

REPO_ROOT=""
BUNDLE_DIR=""
PYTHON_BIN="python3.12"
WITH_AF_FULL="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-root)
      REPO_ROOT="${2:-}"
      shift 2
      ;;
    --bundle-dir)
      BUNDLE_DIR="${2:-}"
      shift 2
      ;;
    --python)
      PYTHON_BIN="${2:-}"
      shift 2
      ;;
    --with-af-full)
      WITH_AF_FULL="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$REPO_ROOT" || -z "$BUNDLE_DIR" ]]; then
  usage
  exit 1
fi

require_dir "$REPO_ROOT"
require_dir "$BUNDLE_DIR"

KA_REPO="$REPO_ROOT/Knowledge_Atlas"
AE_REPO="$REPO_ROOT/Article_Eater_PostQuinean_v1_recovery"
AF_REPO="$REPO_ROOT/Article_Finder_v3_2_3"
DE_REPO="$REPO_ROOT/Designing_Experiments"

for repo in "$KA_REPO" "$AE_REPO" "$AF_REPO" "$DE_REPO"; do
  require_dir "$repo"
done

RUNTIME_ZIP="$BUNDLE_DIR/ka_ae_af_runtime_bundle_2026-03-26.zip"
AF_FULL_ZIP="$BUNDLE_DIR/article_finder_full_data_bundle_2026-03-26.zip"

if [[ ! -f "$RUNTIME_ZIP" ]]; then
  printf 'Missing runtime bundle: %s\n' "$RUNTIME_ZIP" >&2
  exit 1
fi

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  printf 'Python interpreter not found: %s\n' "$PYTHON_BIN" >&2
  exit 1
fi

if ! command -v unzip >/dev/null 2>&1; then
  printf 'unzip is required but not installed.\n' >&2
  exit 1
fi

log "Unpacking runtime bundle into $REPO_ROOT"
(
  cd "$REPO_ROOT"
  unzip -oq "$RUNTIME_ZIP"
)

if [[ "$WITH_AF_FULL" == "1" ]]; then
  if [[ ! -f "$AF_FULL_ZIP" ]]; then
    printf 'Requested --with-af-full but missing bundle: %s\n' "$AF_FULL_ZIP" >&2
    exit 1
  fi
  log "Unpacking full Article Finder data bundle into $REPO_ROOT"
  (
    cd "$REPO_ROOT"
    unzip -oq "$AF_FULL_ZIP"
  )
fi

log "Bootstrapping Article Eater environment"
(
  cd "$AE_REPO"
  "$PYTHON_BIN" -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip setuptools wheel
  pip install -r requirements.txt
)

log "Bootstrapping Article Finder environment"
(
  cd "$AF_REPO"
  "$PYTHON_BIN" -m venv venv
  source venv/bin/activate
  python -m pip install --upgrade pip setuptools wheel
  pip install -e .
  pip install -r requirements.txt
)

log "Bootstrapping Knowledge Atlas helper environment"
(
  cd "$KA_REPO"
  "$PYTHON_BIN" -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip setuptools wheel
)

log "Running smoke tests"

log "AF: cli stats"
(
  cd "$AF_REPO"
  source venv/bin/activate
  python cli/main.py stats
)

log "AE: py_compile deep_stat_candidate_aggregator.py"
(
  cd "$AE_REPO"
  source .venv/bin/activate
  python3 -m py_compile src/services/deep_stat_candidate_aggregator.py
)

log "AE: build_deep_stat_adjudication_batch.py"
(
  cd "$AE_REPO"
  source .venv/bin/activate
  python3 scripts/build_deep_stat_adjudication_batch.py
)

log "KA: build_ka_adapter_payloads.py"
(
  cd "$KA_REPO"
  source .venv/bin/activate
  python3 scripts/build_ka_adapter_payloads.py
)

cat <<EOF

Bootstrap complete.

Next useful commands:

  cd "$KA_REPO"
  python3 -m http.server 8080

Open:
  http://localhost:8080/ka_home.html

If this machine is intended to run Mathpix:
  cd "$AE_REPO"
  source .venv/bin/activate
  python3 scripts/run_mathpix_priority_batch.py --limit 5 --bands critical high
EOF

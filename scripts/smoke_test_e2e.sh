#!/usr/bin/env bash
# End-to-end smoke test for the Knowledge Atlas class-state stack.
#
# Exercises (in order, short-circuiting on first failure):
#
#   1. Migration applies cleanly (idempotent)
#   2. Seed populates class_offerings, deliverables, enrollments
#   3. Classifier DB is reachable at the expected cross-repo path
#   4. FastAPI backend starts, /health returns ok
#   5. /api/admin/class/grading returns 15-student payload
#   6. ai_grader.py queue builds briefings without error
#   7. rag_harvest.py --dry-run emits stub payloads for all services
#   8. rag_classify_check.py joins harvest with classifier DB
#   9. export_egrades.py --dry-run produces the preview table
#  10. site_validator.py reports zero errors
#
# Usage
# -----
#   bash scripts/smoke_test_e2e.sh              # Uses a throwaway DB at /tmp/
#   bash scripts/smoke_test_e2e.sh --real-db    # Touches data/ka_auth.db
#
# Exit codes: 0 = all pass; 1 = a stage failed (the failing stage is
# printed in bold red before exit).

set -u
set -o pipefail

# ─── Paths + config ───────────────────────────────────────────────
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

REAL_DB=0
if [[ "${1:-}" == "--real-db" ]]; then
  REAL_DB=1
fi

if [[ "$REAL_DB" -eq 1 ]]; then
  TEST_DB="$REPO/data/ka_auth.db"
else
  TEST_DB="/tmp/ka_smoke_$(date +%s).db"
  cp "$REPO/data/ka_auth.db" "$TEST_DB"
fi

export KA_AUTH_DB="$TEST_DB"
export KA_ADMIN_ALLOW_OPEN=1        # bypass token for the test
BACKEND_PORT=8099
BACKEND_LOG="/tmp/ka_smoke_backend_$(date +%s).log"

# ─── Colour helpers ───────────────────────────────────────────────
BOLD="\033[1m"; GREEN="\033[32m"; RED="\033[31m"; YELLOW="\033[33m"; RESET="\033[0m"
step=0
pass() { step=$((step+1)); printf " ${GREEN}✓${RESET} [%02d] %s\n" "$step" "$1"; }
fail() { step=$((step+1)); printf " ${BOLD}${RED}✗${RESET} [%02d] ${BOLD}%s${RESET}\n" "$step" "$1"; shift; printf "      %s\n" "$@"; cleanup; exit 1; }
warn() { printf "      ${YELLOW}note:${RESET} %s\n" "$@"; }

# ─── Cleanup ──────────────────────────────────────────────────────
cleanup() {
  if [[ -n "${BACKEND_PID:-}" ]]; then
    kill "$BACKEND_PID" 2>/dev/null || true
    wait "$BACKEND_PID" 2>/dev/null || true
  fi
  if [[ "$REAL_DB" -eq 0 && -f "$TEST_DB" ]]; then
    rm -f "$TEST_DB"
  fi
}
trap cleanup EXIT

# ─── Banner ───────────────────────────────────────────────────────
printf "\n${BOLD}KA end-to-end smoke test${RESET}\n"
printf "repo:  %s\n" "$REPO"
printf "db:    %s %s\n" "$TEST_DB" "$([[ $REAL_DB -eq 1 ]] && echo '(REAL)' || echo '(throwaway)')"
printf "port:  %s\n\n" "$BACKEND_PORT"

# ─── Stage 1: migration ───────────────────────────────────────────
if python3 -c "
import sqlite3
con = sqlite3.connect('$TEST_DB')
con.executescript(open('scripts/migrations/2026-04-17_class_state.sql').read())
con.close()
" 2>/dev/null; then
  pass "migration applies cleanly"
else
  fail "migration script failed" "scripts/migrations/2026-04-17_class_state.sql"
fi

# ─── Stage 2: seed ────────────────────────────────────────────────
if python3 scripts/seed_class_state.py --db "$TEST_DB" >/dev/null 2>&1; then
  pass "seed populates offerings/deliverables/enrollments"
else
  fail "seed_class_state.py failed"
fi

# Verify counts
OFFERINGS=$(python3 -c "import sqlite3; print(sqlite3.connect('$TEST_DB').cursor().execute('SELECT COUNT(*) FROM class_offerings').fetchone()[0])")
DELIVS=$(python3 -c "import sqlite3; print(sqlite3.connect('$TEST_DB').cursor().execute(\"SELECT COUNT(*) FROM deliverables WHERE offering_id='cogs160sp26'\").fetchone()[0])")
ENROLLS=$(python3 -c "import sqlite3; print(sqlite3.connect('$TEST_DB').cursor().execute(\"SELECT COUNT(*) FROM enrollments WHERE offering_id='cogs160sp26'\").fetchone()[0])")
if [[ "$OFFERINGS" -ge 1 && "$DELIVS" -ge 30 && "$ENROLLS" -ge 15 ]]; then
  pass "seeded data counts OK (offerings=$OFFERINGS, deliverables=$DELIVS, enrollments=$ENROLLS)"
else
  fail "seeded data counts unexpected" "offerings=$OFFERINGS deliverables=$DELIVS enrollments=$ENROLLS"
fi

# ─── Stage 3: classifier DB reachable ────────────────────────────
CLASS_DB_DEFAULT="/sessions/brave-great-tesla/mnt/REPOS/Article_Eater_PostQuinean_v1_recovery/data/pipeline_registry_unified.db"
CLASS_DB="${KA_UNIFIED_REGISTRY_DB:-$CLASS_DB_DEFAULT}"
if [[ -f "$CLASS_DB" ]]; then
  N_PAPERS=$(python3 -c "import sqlite3; print(sqlite3.connect('$CLASS_DB').cursor().execute('SELECT COUNT(*) FROM papers').fetchone()[0])" 2>/dev/null || echo 0)
  if [[ "$N_PAPERS" -ge 500 ]]; then
    pass "classifier DB reachable with $N_PAPERS papers"
  else
    fail "classifier DB has too few papers ($N_PAPERS)" "expected >= 500"
  fi
else
  fail "classifier DB not found at $CLASS_DB" "set KA_UNIFIED_REGISTRY_DB to override"
fi

# ─── Stage 4: backend boots, /health returns ─────────────────────
# Kill anything already on the port
lsof -ti:$BACKEND_PORT 2>/dev/null | xargs -r kill -9 2>/dev/null || true
python3 -m uvicorn scripts.ka_class_api:app --port $BACKEND_PORT --log-level error >"$BACKEND_LOG" 2>&1 &
BACKEND_PID=$!
# Wait up to 10s for the backend to be ready
for i in $(seq 1 20); do
  if curl -sf "http://127.0.0.1:$BACKEND_PORT/api/admin/class/health" >/dev/null 2>&1; then
    break
  fi
  sleep 0.5
done
if ! curl -sf "http://127.0.0.1:$BACKEND_PORT/api/admin/class/health" >/dev/null; then
  warn "backend log tail:"
  tail -20 "$BACKEND_LOG" | sed 's/^/        /'
  fail "backend did not come up on port $BACKEND_PORT"
fi
pass "backend /health responds"

# ─── Stage 5: /grading endpoint returns the expected payload ─────
GRADING_JSON=$(curl -sf "http://127.0.0.1:$BACKEND_PORT/api/admin/class/grading" || true)
if [[ -z "$GRADING_JSON" ]]; then
  fail "/grading endpoint returned empty"
fi
N_STUDENTS=$(echo "$GRADING_JSON" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('students',[])))")
if [[ "$N_STUDENTS" -ge 15 ]]; then
  pass "/grading returns $N_STUDENTS students"
else
  fail "/grading returned too few students ($N_STUDENTS)" "expected >= 15"
fi

# ─── Stage 6: ai_grader queue ─────────────────────────────────────
# Use a scratch grading dir so the test doesn't pollute the real one
SCRATCH_GRADING="/tmp/ka_smoke_grading_$(date +%s)"
mkdir -p "$SCRATCH_GRADING"
# ai_grader uses 160sp/grading/ directly; stash and restore
if [[ -d 160sp/grading ]]; then mv 160sp/grading 160sp/grading.bak.smoke; fi
if python3 scripts/ai_grader.py queue --student s01 --deliverable A0 >/dev/null 2>&1; then
  N_BRIEFINGS=$(find 160sp/grading/queue -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$N_BRIEFINGS" -ge 1 ]]; then
    pass "ai_grader queue built $N_BRIEFINGS briefing(s)"
  else
    fail "ai_grader queue produced no briefing files"
  fi
else
  fail "scripts/ai_grader.py queue failed"
fi
# Clean
rm -rf 160sp/grading
if [[ -d 160sp/grading.bak.smoke ]]; then mv 160sp/grading.bak.smoke 160sp/grading; fi

# ─── Stage 7: rag_harvest dry-run ─────────────────────────────────
SCRATCH_TRACKS="/tmp/ka_smoke_tracks_$(date +%s)"
if [[ -d 160sp/tracks ]]; then mv 160sp/tracks 160sp/tracks.bak.smoke; fi
if python3 scripts/rag_harvest.py --student smoke --query "test query" --dry-run >/dev/null 2>&1; then
  N_HARVESTS=$(find 160sp/tracks/t2/smoke/T2.d.2/harvest -name normalised.json 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$N_HARVESTS" -ge 1 ]]; then
    pass "rag_harvest dry-run produced $N_HARVESTS service payload(s)"
  else
    fail "rag_harvest produced no normalised.json files"
  fi
else
  fail "scripts/rag_harvest.py --dry-run failed"
fi

# ─── Stage 8: rag_classify_check joins harvest + DB ──────────────
if python3 scripts/rag_classify_check.py --student smoke >/dev/null 2>&1; then
  if [[ -f 160sp/tracks/t2/smoke/T2.d.2/classifier_check.csv ]]; then
    N_ROWS=$(tail -n +2 160sp/tracks/t2/smoke/T2.d.2/classifier_check.csv | wc -l | tr -d ' ')
    pass "rag_classify_check wrote CSV with $N_ROWS row(s)"
  else
    fail "rag_classify_check did not produce classifier_check.csv"
  fi
else
  fail "scripts/rag_classify_check.py failed"
fi
# Clean up tracks dir
rm -rf 160sp/tracks
if [[ -d 160sp/tracks.bak.smoke ]]; then mv 160sp/tracks.bak.smoke 160sp/tracks; fi

# ─── Stage 9: export_egrades dry-run ─────────────────────────────
if python3 scripts/export_egrades.py --offering cogs160sp26 --dry-run >/dev/null 2>&1; then
  pass "export_egrades.py --dry-run produces preview"
else
  fail "scripts/export_egrades.py --dry-run failed"
fi

# ─── Stage 10: site validator ─────────────────────────────────────
VALIDATOR_OUT=$(python3 scripts/site_validator.py 2>&1 | tail -5)
N_ERRORS=$(echo "$VALIDATOR_OUT" | grep -oE "'error': [0-9]+" | grep -oE "[0-9]+" | head -1)
if [[ "${N_ERRORS:-1}" == "0" ]]; then
  N_WARNS=$(echo "$VALIDATOR_OUT" | grep -oE "'warn': [0-9]+" | grep -oE "[0-9]+" | head -1)
  pass "site validator: 0 errors, $N_WARNS warns"
else
  fail "site validator reports $N_ERRORS error(s)" "$VALIDATOR_OUT"
fi

# ─── Done ─────────────────────────────────────────────────────────
printf "\n${BOLD}${GREEN}all %d stages passed${RESET}\n\n" "$step"
exit 0

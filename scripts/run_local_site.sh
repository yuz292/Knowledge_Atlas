#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  Knowledge Atlas — Local Development Server
#  Mirrors the production site at xrlab.ucsd.edu/ka/
# ═══════════════════════════════════════════════════════════════
#
#  Usage:
#    bash scripts/run_local_site.sh            # default: port 8765
#    bash scripts/run_local_site.sh 9000       # custom port
#
#  This serves:
#    - All static HTML/JS/CSS pages (same as nginx on production)
#    - The FastAPI auth + article API endpoints
#    - From the repo root, so all relative links work
#
#  Open in browser:   http://localhost:8765/ka_home.html
#  API docs:          http://localhost:8765/docs
#  Health check:      http://localhost:8765/health
# ═══════════════════════════════════════════════════════════════

set -e
cd "$(dirname "$0")/.."
PORT="${1:-8765}"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Knowledge Atlas — Local Development Server"
echo "═══════════════════════════════════════════════════════════"
echo ""

# ── Check Python ──
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Install via Homebrew: brew install python"
    exit 1
fi

# ── Check dependencies ──
MISSING=()
for pkg in fastapi uvicorn jose passlib; do
    python3 -c "import $pkg" 2>/dev/null || MISSING+=("$pkg")
done
if [ ${#MISSING[@]} -gt 0 ]; then
    echo "Installing missing Python packages..."
    pip3 install fastapi uvicorn "python-jose[cryptography]" "passlib[bcrypt]" \
        python-multipart aiofiles "pydantic[email]" --break-system-packages -q
    echo "Done."
fi

# ── Ensure data directory ──
mkdir -p data/storage data/ka_payloads

# ── Database: use production snapshot if no working DB exists ──
if [ ! -f data/ka_auth.db ]; then
    if [ -f data/ka_auth.server_2026-04-12.db ]; then
        echo "Copying production database snapshot → data/ka_auth.db"
        cp data/ka_auth.server_2026-04-12.db data/ka_auth.db
    else
        echo "No database found. Server will create a fresh one with seed data."
    fi
fi

# ── JWT secret ──
if [ ! -f data/ka_auth_secret.txt ]; then
    python3 -c "import secrets; print(secrets.token_hex(48))" > data/ka_auth_secret.txt
    echo "Generated JWT secret."
fi

# ── Kill any existing server on this port ──
lsof -ti :$PORT 2>/dev/null | xargs kill -9 2>/dev/null || true

echo ""
echo "  Site:     http://localhost:$PORT/ka_home.html"
echo "  Course:   http://localhost:$PORT/160sp/ka_schedule.html"
echo "  Upload:   http://localhost:$PORT/160sp/collect-articles-upload.html"
echo "  Tracks:   http://localhost:$PORT/160sp/ka_track_signup.html"
echo "  Login:    http://localhost:$PORT/ka_login.html"
echo "  API docs: http://localhost:$PORT/docs"
echo ""
echo "  Test credentials: dkirsh@ucsd.edu / <KA_BOOTSTRAP_INSTRUCTOR_PASSWORD>"
echo ""
echo "  Press Ctrl+C to stop."
echo "═══════════════════════════════════════════════════════════"
echo ""

# ── Launch ──
python3 -m uvicorn ka_auth_server:app --host 127.0.0.1 --port $PORT --reload

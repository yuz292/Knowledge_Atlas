#!/bin/bash
# ============================================================
# START LOCAL KA DEV SERVER
# ============================================================
# Serves all HTML pages AND the FastAPI backend on one port.
#
# After starting:
#   Home page:    http://localhost:8765/ka_home.html
#   User home:    http://localhost:8765/ka_user_home.html
#   Student page: http://localhost:8765/ka_home_student.html
#   160sp pages:  http://localhost:8765/160sp/collect-articles-upload.html
#   API docs:     http://localhost:8765/docs
#   Health:       http://localhost:8765/health
#
# Instructor login:
#   Email:    dkirsh@ucsd.edu
#   Password: value of KA_BOOTSTRAP_INSTRUCTOR_PASSWORD
#
# The server auto-reloads when you edit files.
# ============================================================

cd "$HOME/REPOS/Knowledge_Atlas" || { echo "ERROR: repo not found"; exit 1; }

# Check dependencies
echo "Checking Python dependencies..."
python3 -c "import fastapi, uvicorn, jose, passlib" 2>/dev/null
if [ $? -ne 0 ]; then
  echo ""
  echo "Missing dependencies. Installing..."
  pip3 install --break-system-packages fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart pdfplumber PyPDF2
  echo ""
fi

echo "Starting Knowledge Atlas local server..."
echo ""
python3 ka_auth_server.py

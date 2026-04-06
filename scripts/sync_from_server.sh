#!/bin/bash
# Pull server versions of modified files for diffing
# Run this on your Mac terminal

DEST="$HOME/REPOS/Knowledge_Atlas/server_snapshot"
mkdir -p "$DEST"

echo "=== Pulling server files for merge ==="

# The two files that exist on BOTH server and local (with different changes)
sftp dkirsh@xrlab.ucsd.edu <<'SFTP'
cd /var/www/html/ka
lcd /Users/davidusa/REPOS/Knowledge_Atlas/server_snapshot
get ka_home.html
get ka_user_home.html
get ka_auth_server.py
get ka_article_endpoints.py
bye
SFTP

echo ""
echo "=== Server files saved to $DEST ==="
echo "Files downloaded:"
ls -la "$DEST"
echo ""
echo "Now go back to Cowork — I'll diff and merge."

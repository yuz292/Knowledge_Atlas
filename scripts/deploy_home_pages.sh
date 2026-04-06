#!/bin/bash
# Deploy user-type home pages and updated files to xrlab.ucsd.edu
# Run this on your Mac terminal from ~/REPOS/Knowledge_Atlas/
#
# What this uploads:
#   6 NEW pages:  ka_home_{student,contributor,instructor,practitioner,researcher,theory}.html
#   2 MODIFIED:   ka_home.html (added MODE_HOME_PAGES routing)
#                 ka_user_home.html (added ROLE_HOME_PAGES banner + link)
#   1 DOC:        docs/USER_TYPE_HOME_PAGES_AND_JOURNEY_ARCHITECTURE_2026-04-03.md

cd "$HOME/REPOS/Knowledge_Atlas" || { echo "ERROR: repo not found"; exit 1; }

echo "=== Deploying to xrlab.ucsd.edu ==="
echo "Files to upload:"
echo "  NEW:  ka_home_student.html (1,097 lines)"
echo "  NEW:  ka_home_contributor.html (737 lines)"
echo "  NEW:  ka_home_instructor.html (1,044 lines)"
echo "  NEW:  ka_home_practitioner.html (784 lines)"
echo "  NEW:  ka_home_researcher.html (1,313 lines)"
echo "  NEW:  ka_home_theory.html (1,600 lines)"
echo "  MOD:  ka_home.html (+44 lines: MODE_HOME_PAGES routing)"
echo "  MOD:  ka_user_home.html (+32 lines: ROLE_HOME_PAGES banner)"
echo ""
read -p "Proceed? [y/N] " confirm
[[ "$confirm" =~ ^[Yy] ]] || { echo "Aborted."; exit 0; }

sftp dkirsh@xrlab.ucsd.edu <<'SFTP'
cd /var/www/html/ka
put ka_home_student.html
put ka_home_contributor.html
put ka_home_instructor.html
put ka_home_practitioner.html
put ka_home_researcher.html
put ka_home_theory.html
put ka_home.html
put ka_user_home.html
bye
SFTP

echo ""
echo "=== Upload complete ==="
echo "Verify at: https://xrlab.ucsd.edu/ka/ka_home.html"
echo "  Student:     https://xrlab.ucsd.edu/ka/ka_home_student.html"
echo "  Contributor:  https://xrlab.ucsd.edu/ka/ka_home_contributor.html"
echo "  Instructor:   https://xrlab.ucsd.edu/ka/ka_home_instructor.html"
echo "  Practitioner: https://xrlab.ucsd.edu/ka/ka_home_practitioner.html"
echo "  Researcher:   https://xrlab.ucsd.edu/ka/ka_home_researcher.html"
echo "  Theory:       https://xrlab.ucsd.edu/ka/ka_home_theory.html"

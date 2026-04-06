#!/bin/bash
# ============================================================
# PULL FULL WEBSITE FROM xrlab.ucsd.edu INTO server_snapshot/
# ============================================================
# Run this on your Mac terminal from ~/REPOS/Knowledge_Atlas/
#
# What it does:
#   1. Creates server_snapshot/ directory (clean)
#   2. Downloads ALL web-facing files from the server
#   3. Preserves directory structure (160sp/, Designing_Experiments/, data/)
#   4. Skips __pycache__ and .pyc files
#
# After this runs, Cowork can diff server_snapshot/ vs local files
# and build a canonical merged version.
# ============================================================

set -e

REPO="$HOME/REPOS/Knowledge_Atlas"
DEST="$REPO/server_snapshot"

# Start fresh
if [ -d "$DEST" ]; then
  echo "⚠  server_snapshot/ already exists. Backing up to server_snapshot_prev/"
  rm -rf "$DEST"_prev
  mv "$DEST" "$DEST"_prev
fi
mkdir -p "$DEST"
mkdir -p "$DEST/160sp"
mkdir -p "$DEST/Designing_Experiments"
mkdir -p "$DEST/data"

echo "============================================"
echo "  Downloading full KA website from server"
echo "============================================"
echo ""

# ── OPTION A: rsync (fastest, if ssh works) ──────────────────
# Uncomment this block and comment out the sftp block below
# if rsync over ssh works for you:
#
# rsync -avz --exclude='__pycache__' --exclude='*.pyc' \
#   --exclude='.git' --exclude='node_modules' \
#   dkirsh@xrlab.ucsd.edu:/var/www/html/ka/ "$DEST/"
# echo "Done via rsync."
# exit 0

# ── OPTION B: sftp (works everywhere) ────────────────────────
echo "Connecting via sftp..."
echo "(If the server path is different from /var/www/html/ka,"
echo " edit the 'cd' line below.)"
echo ""

sftp dkirsh@xrlab.ucsd.edu <<'SFTP_COMMANDS'

# Navigate to the KA web root on the server
cd /var/www/html/ka

# Set local destination
lcd server_snapshot

# ── Root HTML pages ──
get ka_home.html
get ka_user_home.html
get ka_login.html
get ka_register.html
get ka_forgot_password.html
get ka_reset_password.html
get ka_topics.html
get ka_topic_hierarchy.html
get ka_evidence.html
get ka_gaps.html
get ka_warrants.html
get ka_articles.html
get ka_article_search.html
get ka_article_propose.html
get ka_annotations.html
get ka_argumentation.html
get ka_interpretation.html
get ka_contribute.html
get ka_datacapture.html
get ka_tagger.html
get ka_my_work.html
get ka_workflow_hub.html
get ka_hypothesis_builder.html
get ka_question_maker.html
get ka_sensors.html
get ka_neuro_perspective.html
get ka_neuro_grounding_demo.html
get ka_explain_system.html
get ka_ai_methodology.html
get ka_ai_system_failures.html
get ka_demo.html
get ka_demo_v04.html
get ka_sitemap.html
get ka_instructor_review.html
get fall160_schedule.html
get SITEMAP_HIERARCHICAL.html

# ── Python backend ──
get ka_auth_server.py
get ka_article_endpoints.py

# ── Any new pages we don't know about ──
# (sftp doesn't support wildcards well, but try)
# If this fails, it's fine — we got the known files above

# ── 160sp/ course pages ──
lcd 160sp
cd 160sp
get collect-articles-upload.html
get ka_student_setup.html
get ka_collect_articles.html
get ka_article_finder_assignment.html
get ka_google_search_guide.html
get ka_gui_assignment.html
get ka_tag_assignment.html
get ka_vr_assignment.html
get ka_dashboard.html
get ka_approve.html
get ka_schedule.html
get ka_tracks.html
get ka_track_signup.html
get ka_track1_tagging.html
get ka_track2_pipeline.html
get ka_track3_vr.html
get ka_track4_ux.html
get ka_thursday_tasks.html
get instructor_prep.html
get week1_agenda.html
get week2_agenda.html
get week2_exercises.html
get week3_agenda.html
get week4_agenda.html
get week5_agenda.html
get week6_agenda.html
get week7_agenda.html
get week8_agenda.html
get article_finder_assignment_v1_archive.html
# Try to get any A0-related pages David may have added
get a0-question-home.html
get a0-home.html
get a0-assignment.html
get student-home.html
get index.html
cd ..
lcd ..

# ── Designing_Experiments/ ──
lcd Designing_Experiments
cd Designing_Experiments
get cogs160_spring_2026_site.html
get knowledge_navigator.html
get experiment_wizard.html
get hypothesis_builder.html
get bn_navigator.html
get en_navigator.html
get course_pilot.html
get measurement_instruments.html
get methods_taxonomy.html
get sensor_catalogue.html
get system_inventory.html
get theory_and_experiment_design.html
cd ..
lcd ..

# ── Data files (JSON payloads, not the SQLite DB) ──
lcd data
cd data
get -r ka_payloads
cd ..
lcd ..

bye
SFTP_COMMANDS

echo ""
echo "============================================"
echo "  Download complete!"
echo "============================================"
echo ""
echo "Files saved to: $DEST/"
echo ""
echo "Quick inventory:"
echo "  Root HTML:  $(ls "$DEST"/*.html 2>/dev/null | wc -l | tr -d ' ') files"
echo "  Python:     $(ls "$DEST"/*.py 2>/dev/null | wc -l | tr -d ' ') files"
echo "  160sp/:     $(ls "$DEST"/160sp/*.html 2>/dev/null | wc -l | tr -d ' ') files"
echo "  DE/:        $(ls "$DEST"/Designing_Experiments/*.html 2>/dev/null | wc -l | tr -d ' ') files"
echo ""
echo "Next: Go back to Cowork. I'll diff everything and build canonical versions."

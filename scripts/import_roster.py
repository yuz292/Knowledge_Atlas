#!/usr/bin/env python3
"""
Import the real class roster into data/ka_auth.db.

Reads a UCSD Registrar-format CSV and populates the users + enrollments
tables for a given offering. Idempotent: existing users are looked up
by email; existing enrollments for the same (user, offering) are left
alone. New rows are inserted.

Expected CSV shape
------------------
The Registrar's instructor-of-record CSV export has these columns (as
of the 2025–26 format; DK to confirm if the format has changed):

    PID, FirstName, LastName, Email, Level, Section, Track (optional)

Only PID, FirstName, LastName, and Email are strictly required. The
Track column is optional; if present, it's one of {T1, T2, T3, T4}
(or their lowercase equivalents) and is mapped into enrollments.track.

If the Registrar's export is missing the Track column, import_roster
puts every student into a 'pending' track status and prints a list of
students the instructor needs to assign tracks to manually at the
Week-3 planning meeting.

Usage
-----
    # Dry-run: show what would be inserted, don't touch DB
    python3 scripts/import_roster.py --csv ~/Downloads/roster.csv --dry-run

    # Apply to default DB (data/ka_auth.db)
    python3 scripts/import_roster.py --csv ~/Downloads/roster.csv

    # Custom offering or DB
    python3 scripts/import_roster.py \
        --csv ~/Downloads/roster.csv \
        --offering cogs160sp26 \
        --db /tmp/ka_auth_test.db

    # Force-update: re-apply even if enrollments already exist
    # (updates track column if CSV has new track assignment)
    python3 scripts/import_roster.py --csv ~/Downloads/roster.csv --update-tracks

Safety
------
- Runs inside a single transaction; rollback on any error.
- Never overwrites an existing user's password hash or email.
- Logs every insert/update to audit_log_class with actor = the calling
  instructor's user_id (resolved via --instructor-email, default
  dkirsh@ucsd.edu).

Relationship to seed_class_state.py
-----------------------------------
seed_class_state.py populates the demo roster (Aisha Rahman, Ben
Choi, …). This script populates the real roster. Typical sequence:

    1. First-time setup:
         python3 scripts/migrations/apply_2026-04-17_class_state.sql  (or equivalent)
         python3 scripts/seed_class_state.py   # writes offering + deliverables
    2. When the real roster arrives:
         python3 scripts/import_roster.py --csv <registrar_export.csv>
         # This adds the real students alongside (or replacing, at
         # DK's discretion) the demo students. Pass --drop-demo to
         # flip the demo enrollments to status='dropped'.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sqlite3
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO / "data" / "ka_auth.db"

# Same user_id convention as scripts/seed_class_state.py
def _user_id_for(email: str) -> str:
    h = hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()[:16]
    return f"u_{h}"


TRACK_MAP = {
    "t1": "t1", "track1": "t1", "track 1": "t1", "1": "t1",
    "t2": "t2", "track2": "t2", "track 2": "t2", "2": "t2",
    "t3": "t3", "track3": "t3", "track 3": "t3", "3": "t3",
    "t4": "t4", "track4": "t4", "track 4": "t4", "4": "t4",
}


def normalise_track(raw: str | None) -> str | None:
    if not raw:
        return None
    return TRACK_MAP.get(raw.strip().lower())


def detect_columns(header: list[str]) -> dict[str, str]:
    """Map canonical column names to whatever the CSV actually uses."""
    hl = [h.lower().strip() for h in header]
    mapping = {}
    for canon, aliases in [
        ("email",      ["email", "emailaddress", "email address", "e-mail", "preferredemail"]),
        ("first_name", ["firstname", "first name", "first", "givenname"]),
        ("last_name",  ["lastname", "last name", "last", "surname", "familyname"]),
        ("pid",        ["pid", "studentid", "student id", "ucsdid", "ucsd id", "id"]),
        ("track",      ["track", "assignedtrack", "assigned track"]),
        ("section",    ["section", "sectioncode", "section code"]),
        ("level",      ["level", "grade", "class", "classlevel"]),
    ]:
        for alias in aliases:
            if alias in hl:
                mapping[canon] = header[hl.index(alias)]
                break
    return mapping


def read_csv(csv_path: Path) -> tuple[dict, list[dict]]:
    """Return (column-mapping, list-of-rows-keyed-by-canonical-names)."""
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        col_map = detect_columns(header)
        required = {"email", "first_name", "last_name"}
        missing = required - set(col_map.keys())
        if missing:
            sys.exit(f"error: CSV is missing required columns: {missing}. "
                     f"Detected columns: {list(col_map.keys())}. "
                     f"Header was: {header}")
        rows = []
        for row in reader:
            if not row or not any(row):
                continue
            rd = dict(zip(header, row))
            out = {canon: (rd.get(col) or "").strip() for canon, col in col_map.items()}
            if not out.get("email"):
                continue
            rows.append(out)
        return col_map, rows


def ensure_user(c: sqlite3.Cursor, first: str, last: str, email: str, pid: str = "") -> tuple[str, bool]:
    """Look up user by email; insert if absent. Returns (user_id, was_created)."""
    row = c.execute(
        "SELECT user_id FROM users WHERE LOWER(email) = LOWER(?)", (email,)).fetchone()
    if row:
        return row[0], False
    cols_available = [r[1] for r in c.execute("PRAGMA table_info(users)").fetchall()]
    values = {
        "user_id": _user_id_for(email),
        "email": email,
        "first_name": first,
        "last_name": last,
    }
    if "password_hash" in cols_available:
        values["password_hash"] = "pending_dk_set"
    if "status" in cols_available:
        values["status"] = "pending"
    if "role" in cols_available:
        values["role"] = "student"
    if "institution" in cols_available:
        values["institution"] = "UC San Diego"
    if "created_at" in cols_available:
        values["created_at"] = date.today().isoformat()
    # PID might go in a 'ucsd_pid' or similar column if it exists, else skip
    for pid_col in ("ucsd_pid", "pid", "student_id"):
        if pid_col in cols_available and pid:
            values[pid_col] = pid
            break
    present = [k for k in values if k in cols_available]
    placeholders = ",".join("?" for _ in present)
    cols_sql = ",".join(present)
    c.execute(f"INSERT INTO users ({cols_sql}) VALUES ({placeholders})",
              tuple(values[k] for k in present))
    return values["user_id"], True


def ensure_enrollment(c: sqlite3.Cursor, user_id: str, offering_id: str,
                     track: str | None, update_tracks: bool) -> tuple[str, bool]:
    """Insert or (if --update-tracks) refresh the enrollment row. Returns (action, changed)."""
    row = c.execute(
        "SELECT enrollment_id, track FROM enrollments WHERE user_id = ? AND offering_id = ?",
        (user_id, offering_id)).fetchone()
    if row is None:
        c.execute(
            """INSERT INTO enrollments
               (user_id, offering_id, role, track, status)
               VALUES (?, ?, 'student', ?, ?)""",
            (user_id, offering_id, track, "pending" if not track else "active"))
        return ("inserted", True)
    existing_track = row[1]
    if update_tracks and track and track != existing_track:
        c.execute("UPDATE enrollments SET track = ? WHERE enrollment_id = ?",
                  (track, row[0]))
        return (f"track:{existing_track}->{track}", True)
    return ("skip-existing", False)


def drop_demo_enrollments(c: sqlite3.Cursor, offering_id: str) -> int:
    """Flip demo student enrollments to 'dropped' so they stop counting."""
    # Demo emails all end with @ucsd.edu and were created by seed_class_state.
    # Identify them by the fact that their user_id starts with u_ and was
    # created with password_hash='pending_dk_set' (the seed's marker) —
    # but real imports also set pending_dk_set, so we can't distinguish
    # at that level. Safer: mark demo users by their exact email list.
    demo_emails = {
        "arahman@ucsd.edu", "bchoi@ucsd.edu", "cmendoza@ucsd.edu",
        "doneill@ucsd.edu", "epetrov@ucsd.edu", "falhassan@ucsd.edu",
        "gnakamura@ucsd.edu", "htanaka@ucsd.edu", "isantos@ucsd.edu",
        "jpark@ucsd.edu", "kvolkov@ucsd.edu", "lmccarthy@ucsd.edu",
        "mjohnson@ucsd.edu", "npatel@ucsd.edu", "osullivan@ucsd.edu",
    }
    placeholders = ",".join("?" for _ in demo_emails)
    rows = c.execute(
        f"""UPDATE enrollments
            SET status = 'dropped'
            WHERE offering_id = ?
              AND user_id IN (SELECT user_id FROM users WHERE email IN ({placeholders}))
              AND status = 'active'""",
        (offering_id, *demo_emails)).rowcount
    return rows


def import_roster(csv_path: Path, offering_id: str, db_path: Path,
                 dry_run: bool, update_tracks: bool, drop_demo: bool,
                 instructor_email: str) -> None:
    if not csv_path.exists():
        sys.exit(f"error: CSV not found: {csv_path}")
    if not db_path.exists():
        sys.exit(f"error: DB not found: {db_path}. "
                 "Apply scripts/migrations/2026-04-17_class_state.sql first.")

    col_map, rows = read_csv(csv_path)
    print(f"Reading {csv_path}")
    print(f"  detected columns: {col_map}")
    print(f"  {len(rows)} data rows")
    print()

    con = sqlite3.connect(str(db_path))
    con.execute("PRAGMA foreign_keys = ON")
    c = con.cursor()

    # Verify migration applied
    need = {"class_offerings", "enrollments", "users"}
    have = {r[0] for r in c.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    missing = need - have
    if missing:
        sys.exit(f"error: DB missing tables {missing}. "
                 "Apply the class-state migration first.")
    if not c.execute(
            "SELECT 1 FROM class_offerings WHERE offering_id = ?",
            (offering_id,)).fetchone():
        sys.exit(f"error: offering_id {offering_id!r} not in class_offerings. "
                 "Run seed_class_state.py first.")

    # Resolve instructor user_id for audit log
    instr = c.execute(
        "SELECT user_id FROM users WHERE LOWER(email) = LOWER(?)",
        (instructor_email,)).fetchone()
    instructor_uid = instr[0] if instr else None

    # Import
    n_new_users = 0
    n_new_enrolls = 0
    n_updated = 0
    n_skipped = 0
    unassigned_tracks: list[str] = []

    for row in rows:
        email = row["email"]
        first = row.get("first_name", "")
        last = row.get("last_name", "")
        pid = row.get("pid", "")
        track = normalise_track(row.get("track"))
        if not track:
            unassigned_tracks.append(f"{last}, {first} <{email}>")
        try:
            uid, user_created = ensure_user(c, first, last, email, pid)
            action, changed = ensure_enrollment(
                c, uid, offering_id, track, update_tracks)
            if user_created:
                n_new_users += 1
            if action == "inserted":
                n_new_enrolls += 1
            elif action.startswith("track:"):
                n_updated += 1
            else:
                n_skipped += 1
        except sqlite3.Error as e:
            print(f"  error on row {email}: {e}")
            con.rollback()
            sys.exit(1)

    if drop_demo:
        dropped = drop_demo_enrollments(c, offering_id)
        print(f"Demo students dropped: {dropped}")

    # Audit log entry
    try:
        c.execute(
            """INSERT INTO audit_log_class
               (offering_id, actor_user_id, event_type, target, detail)
               VALUES (?, ?, 'roster.import', 'all',
                 'csv=' || ? || ' new_users=' || ? || ' new_enrolls=' || ? ||
                 ' updated=' || ? || ' skipped=' || ? || ' unassigned_tracks=' || ?)""",
            (offering_id, instructor_uid, str(csv_path),
             n_new_users, n_new_enrolls, n_updated, n_skipped,
             len(unassigned_tracks)))
    except sqlite3.OperationalError:
        pass  # audit_log_class not present on older schemas

    print()
    print(f"Summary:")
    print(f"  new users created:       {n_new_users}")
    print(f"  new enrollments:         {n_new_enrolls}")
    print(f"  track updates:           {n_updated}")
    print(f"  unchanged / skipped:     {n_skipped}")
    if unassigned_tracks:
        print()
        print(f"⚠  {len(unassigned_tracks)} students have NO track assignment "
              "(CSV had no track column or track value was blank/unrecognised):")
        for s in unassigned_tracks[:10]:
            print(f"    {s}")
        if len(unassigned_tracks) > 10:
            print(f"    ... and {len(unassigned_tracks) - 10} more")
        print("  Assign these at the Week-3 planning meeting, or re-run with "
              "--csv pointing at an updated CSV and --update-tracks.")

    if dry_run:
        con.rollback()
        print()
        print("DRY RUN — transaction rolled back.")
    else:
        con.commit()
        print()
        print(f"Committed to {db_path}.")
    con.close()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", type=Path, required=True,
                    help="Registrar CSV path")
    ap.add_argument("--offering", default="cogs160sp26",
                    help="Offering id (default cogs160sp26)")
    ap.add_argument("--db", type=Path, default=DEFAULT_DB,
                    help="SQLite DB path (default data/ka_auth.db)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Roll back the transaction instead of committing")
    ap.add_argument("--update-tracks", action="store_true",
                    help="Overwrite enrollment.track if CSV has a new value")
    ap.add_argument("--drop-demo", action="store_true",
                    help="Flip the 15 seed-demo enrollments to status='dropped'")
    ap.add_argument("--instructor-email", default="dkirsh@ucsd.edu",
                    help="Instructor email for audit log attribution")
    args = ap.parse_args()
    import_roster(args.csv, args.offering, args.db, args.dry_run,
                  args.update_tracks, args.drop_demo, args.instructor_email)


if __name__ == "__main__":
    main()

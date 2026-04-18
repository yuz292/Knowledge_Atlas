#!/usr/bin/env python3
"""
migrate_to_canonical_nav.py — retrofit pages to the canonical navbar pattern.

What it does, page by page:
  1. Add  <script src="ka_canonical_navbar.js" defer></script>  if missing.
     (Uses the right relative path: ../ka_canonical_navbar.js for pages
      nested inside 160sp/, or plain ka_canonical_navbar.js otherwise.)
  2. Add  data-ka-regime="160sp"  (or "global") to <body> if missing.
     (Regime inferred from URL path: under 160sp/ → 160sp; else global.)
  3. Add  <div id="ka-navbar-slot"></div>  and
          <div id="ka-breadcrumb-slot"></div>
     immediately inside <body> if missing.
  4. Does NOT touch existing inline <nav> elements — those are left
     for manual removal because styling-removal is page-specific.
     The canonical navbar will render into its slot above the inline
     one; both will be visible until someone removes the inline. The
     validator will still flag NAV005, but NAV001 + NAV002 clear.

Safe: idempotent, non-destructive, leaves the rest of the file alone.
Run from the Knowledge_Atlas repo root:

    python3 scripts/migrate_to_canonical_nav.py            # dry run
    python3 scripts/migrate_to_canonical_nav.py --apply    # write

Exit 0 always; prints per-file diff summary.
"""

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
KA_ROOT = SCRIPT_DIR.parent

SCRIPT_TAG_RX   = re.compile(r'<script[^>]+ka_canonical_navbar\.js', re.I)
BODY_RX         = re.compile(r'(<body\b)([^>]*)(>)', re.I | re.S)
REGIME_RX       = re.compile(r'data-ka-regime\s*=', re.I)
NAV_SLOT_RX     = re.compile(r'id=["\']ka-navbar-slot["\']', re.I)
CRUMB_SLOT_RX   = re.compile(r'id=["\']ka-breadcrumb-slot["\']', re.I)
HEAD_END_RX     = re.compile(r'</head>', re.I)
BODY_OPEN_RX    = re.compile(r'<body\b[^>]*>', re.I)


def infer_regime(rel_path: str) -> str:
    return "160sp" if "/160sp/" in rel_path.replace("\\", "/") or rel_path.startswith("160sp/") else "global"


def script_path_for(rel_path: str) -> str:
    depth = rel_path.replace("\\", "/").count("/")
    if depth >= 1:
        return "../" * depth + "ka_canonical_navbar.js"
    return "ka_canonical_navbar.js"


def user_type_script_path_for(rel_path: str) -> str:
    depth = rel_path.replace("\\", "/").count("/")
    if depth >= 1:
        return "../" * depth + "ka_user_type.js"
    return "ka_user_type.js"


def migrate(path: Path, rel_path: str, apply: bool) -> tuple[list[str], str | None]:
    """Return (list of changes, new_text or None if no changes)."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"READ FAILURE: {e}"], None

    changes: list[str] = []
    new_text = text

    # (1) Script tag
    if not SCRIPT_TAG_RX.search(new_text):
        src = script_path_for(rel_path)
        src_ut = user_type_script_path_for(rel_path)
        tag = (f'<script src="{src}" defer></script>\n'
               f'<script src="{src_ut}" defer></script>\n')
        # Insert right before </head>
        m = HEAD_END_RX.search(new_text)
        if m:
            new_text = new_text[:m.start()] + tag + new_text[m.start():]
            changes.append(f"added canonical nav script ({src})")
        else:
            changes.append("WARN: no </head> found; skipping script add")

    # (2) data-ka-regime on <body>
    if not REGIME_RX.search(new_text):
        regime = infer_regime(rel_path)
        m = BODY_RX.search(new_text)
        if m:
            new_body = f'{m.group(1)}{m.group(2)} data-ka-regime="{regime}"{m.group(3)}'
            new_text = new_text[:m.start()] + new_body + new_text[m.end():]
            changes.append(f'added data-ka-regime="{regime}"')

    # (3) Slot divs
    if not NAV_SLOT_RX.search(new_text):
        m = BODY_OPEN_RX.search(new_text)
        if m:
            slot = ('\n<div id="ka-navbar-slot"></div>\n'
                    '<div id="ka-breadcrumb-slot"></div>\n')
            insert = m.end()
            new_text = new_text[:insert] + slot + new_text[insert:]
            changes.append("added #ka-navbar-slot + #ka-breadcrumb-slot")
    elif not CRUMB_SLOT_RX.search(new_text):
        # Has nav slot but missing breadcrumb slot — insert the breadcrumb
        m = NAV_SLOT_RX.search(new_text)
        if m:
            # Find the end of the line containing the nav slot
            nav_end = new_text.find("</div>", m.end())
            if nav_end != -1:
                insert = nav_end + len("</div>")
                new_text = (new_text[:insert]
                           + '\n<div id="ka-breadcrumb-slot"></div>'
                           + new_text[insert:])
                changes.append("added #ka-breadcrumb-slot")

    if not changes:
        return [], None

    if apply and new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return changes, new_text


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="Write changes to disk (default is dry-run)")
    ap.add_argument("--pattern", default="160sp/**/*.html",
                    help="Glob relative to root (default: 160sp/**/*.html)")
    ap.add_argument("--skip", nargs="*",
                    default=["ka_live_snapshot", "__pycache__", "archive"],
                    help="Directory names to skip")
    args = ap.parse_args()

    total_changed = 0
    total_ok = 0
    total_err = 0
    for path in sorted(KA_ROOT.glob(args.pattern)):
        parts = set(path.relative_to(KA_ROOT).parts)
        if parts & set(args.skip):
            continue
        rel = path.relative_to(KA_ROOT).as_posix()
        changes, _ = migrate(path, rel, apply=args.apply)
        if not changes:
            total_ok += 1
            continue
        if any("FAILURE" in c for c in changes):
            total_err += 1
            print(f"\033[31mERR \033[0m  {rel}: {'; '.join(changes)}")
            continue
        total_changed += 1
        action = "APPLIED" if args.apply else "WOULD APPLY"
        print(f"\033[33m{action:10s}\033[0m {rel}")
        for c in changes:
            print(f"             · {c}")

    print()
    print(f"{'Applied' if args.apply else 'Would apply'}: {total_changed}")
    print(f"Already OK: {total_ok}")
    print(f"Errors: {total_err}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

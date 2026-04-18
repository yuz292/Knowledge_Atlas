#!/usr/bin/env python3
"""
hide_inline_navs.py — second-pass migration that hides inline global
navs on pages that already have the canonical navbar.

Motivation: after migrate_to_canonical_nav.py adds the canonical script
and slot divs, pages that still carry inline <nav> elements render TWO
navigation bars. This script adds style="display:none" to inline navs
matching known-offending class patterns so only the canonical shows.

It leaves in-page / sidebar / tabs navs alone — only the global nav
patterns (top-nav, topnav, global-nav, classbar, ka-nav, header-nav)
are hidden. If a page's inline nav is doing something specific that
must stay visible, add its class name to the SKIP_CLASSES list.

Run from repo root:
    python3 scripts/hide_inline_navs.py            # dry run
    python3 scripts/hide_inline_navs.py --apply    # write
"""

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
KA_ROOT = SCRIPT_DIR.parent

# Classes that identify a GLOBAL site-level nav (hide these)
GLOBAL_NAV_CLASSES = {
    "top-nav", "topnav", "global-nav", "classbar", "ka-nav",
    "header-nav", "site-nav", "main-nav"
}

# Classes that are in-page navigation (leave alone)
SKIP_CLASSES = {
    "subnav", "sidenav", "sidebar-nav", "tabs", "week-nav",
    "workflow-nav", "nav-links", "navlinks", "ka-tabs", "crumb",
    "breadcrumb"
}


def process(path: Path, apply: bool) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"READ FAILURE: {e}"]

    # Only touch pages that HAVE the canonical nav script (otherwise
    # hiding the inline would leave them navigationless)
    if "ka_canonical_navbar.js" not in text:
        return []

    changes = []
    new_text = text

    # Find every <nav class="..."> and decide
    def replace_nav(m):
        full = m.group(0)
        classes = m.group(1).split()
        first = classes[0] if classes else ""
        if first in SKIP_CLASSES:
            return full
        if first not in GLOBAL_NAV_CLASSES:
            return full
        # Already has display:none?
        if 'display:none' in full or 'display: none' in full:
            return full
        # Add inline style
        if 'style="' in full:
            full2 = re.sub(r'style="', 'style="display:none;', full, count=1)
        elif "style='" in full:
            full2 = re.sub(r"style='", "style='display:none;", full, count=1)
        else:
            # Insert style="display:none" before closing >
            full2 = full[:-1] + ' style="display:none"' + full[-1]
        changes.append(f'hid <nav class="{first}">')
        return full2

    new_text = re.sub(
        r'<nav\b[^>]*class\s*=\s*["\']([^"\']+)["\'][^>]*>',
        replace_nav, new_text, flags=re.I)

    if apply and new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return changes


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--skip-dirs", nargs="*",
                    default=["ka_live_snapshot", "__pycache__", "archive",
                             "node_modules", ".git"])
    args = ap.parse_args()

    total_changed = 0
    total_ok = 0
    for path in sorted(KA_ROOT.rglob("*.html")):
        parts = set(path.relative_to(KA_ROOT).parts)
        if parts & set(args.skip_dirs):
            continue
        changes = process(path, args.apply)
        if not changes:
            total_ok += 1
            continue
        total_changed += 1
        action = "APPLIED" if args.apply else "WOULD APPLY"
        rel = path.relative_to(KA_ROOT).as_posix()
        print(f"\033[33m{action:10s}\033[0m {rel}")
        for c in changes:
            print(f"             · {c}")

    print()
    print(f"{'Applied' if args.apply else 'Would apply'}: {total_changed}")
    print(f"Unchanged: {total_ok}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

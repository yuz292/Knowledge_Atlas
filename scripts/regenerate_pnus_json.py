#!/usr/bin/env python3
"""
regenerate_pnus_json.py — build data/ka_payloads/pnus.json from the canonical
mechanism-profiles index that lives in the Article_Eater_PostQuinean_v1_recovery
repo.

Source of truth: the `_index.md` file shipped with the `pnu-generator` skill.
This script parses that index into a JSON manifest the `ka_neural.html` page
consumes at load time.

Run locally:
    python3 scripts/regenerate_pnus_json.py

Run with a custom source (for CI or cross-repo integration):
    python3 scripts/regenerate_pnus_json.py \\
      --source /path/to/mechanism_profiles/_index.md \\
      --profiles-dir /path/to/mechanism_profiles \\
      --out data/ka_payloads/pnus.json

Exit codes: 0 on success, 1 on parse/IO error.
"""

import argparse
import json
import os
import re
import sys
import datetime
from pathlib import Path


# Default locations assume the two repos are siblings under ~/REPOS/
SCRIPT_DIR = Path(__file__).resolve().parent
KA_ROOT    = SCRIPT_DIR.parent                   # Knowledge_Atlas/
REPOS_ROOT = KA_ROOT.parent                      # REPOS/
DEFAULT_SOURCE = (REPOS_ROOT /
    "Article_Eater_PostQuinean_v1_recovery" /
    "skills/pnu-generator/references/mechanism_profiles/_index.md")
DEFAULT_PROFILES_DIR = DEFAULT_SOURCE.parent
DEFAULT_OUT = KA_ROOT / "data/ka_payloads/pnus.json"


# ─── Parsing helpers ──────────────────────────────────────────────────

# "## Predictive Processing (PP)"  → id "PP", name "Predictive Processing"
# "## Cross-Framework Mechanisms"  → id "CROSS", name "Cross-Framework Mechanisms"
FRAMEWORK_HEADING = re.compile(r"^##\s+([^\(]+?)(?:\s*\(([A-Z]+)\))?\s*$")

# A markdown table row (with 5 or 6 pipe-separated cells).
TABLE_ROW = re.compile(r"^\s*\|(.+)\|\s*$")

# Separator row (| --- | --- |)
TABLE_SEPARATOR = re.compile(r"^\s*\|\s*-+[\-\s\|]*$")


def _cells(row_line: str) -> list[str]:
    inner = row_line.strip().strip("|")
    return [c.strip() for c in inner.split("|")]


def parse_index(source: Path) -> dict:
    """Parse the mechanism_profiles/_index.md file into a structured dict."""
    if not source.exists():
        raise FileNotFoundError(f"PNU index not found at {source}")

    text = source.read_text(encoding="utf-8")
    lines = text.splitlines()

    frameworks: list[dict] = []
    cross_framework: list[dict] = []
    construct_lookup: list[dict] = []

    current_framework: dict | None = None
    in_construct_lookup = False
    table_header: list[str] | None = None
    rows_since_separator: list[list[str]] = []

    def flush_table():
        """Attach the last-parsed table to wherever it belongs."""
        nonlocal table_header
        if not table_header or not rows_since_separator:
            table_header = None
            rows_since_separator.clear()
            return
        hdr = [c.lower() for c in table_header]
        for row in rows_since_separator:
            if len(row) < 2:
                continue
            # Construct-lookup table: Construct | Primary Mechanisms | Secondary
            if "construct" in hdr[0] and in_construct_lookup:
                primary = [m.strip() for m in re.split(r",\s*", row[1]) if m.strip()]
                secondary = ([m.strip() for m in re.split(r",\s*", row[2]) if m.strip()]
                             if len(row) > 2 else [])
                construct_lookup.append({
                    "construct": row[0],
                    "primary": primary,
                    "secondary": secondary,
                })
                continue
            # Cross-framework table: ID | Name | File | Frameworks | Maturity | Temporal
            if current_framework is None and "framework" in " ".join(hdr):
                cross_framework.append({
                    "id": row[0],
                    "name": row[1],
                    "file": row[2] if len(row) > 2 else "",
                    "frameworks": [f.strip() for f in re.split(r",\s*", row[3]) if f.strip()]
                                 if len(row) > 3 else [],
                    "maturity": row[4] if len(row) > 4 else "",
                    "temporal": row[5] if len(row) > 5 else "",
                })
                continue
            # Framework-specific table: ID | Name | File | Maturity | Temporal
            if current_framework is not None:
                current_framework["mechanisms"].append({
                    "id": row[0],
                    "name": row[1],
                    "file": row[2] if len(row) > 2 else "",
                    "maturity": row[3] if len(row) > 3 else "",
                    "temporal": row[4] if len(row) > 4 else "",
                })
        table_header = None
        rows_since_separator.clear()

    for raw in lines:
        line = raw.rstrip("\n")

        # Section heading
        m = FRAMEWORK_HEADING.match(line)
        if m:
            flush_table()
            heading_name = m.group(1).strip()
            heading_code = m.group(2) or ""
            # Treat certain well-known headings as meta-sections rather than frameworks
            if heading_name.startswith("Cross-Framework"):
                current_framework = None
                in_construct_lookup = False
                continue
            if heading_name.startswith("Quick Lookup"):
                current_framework = None
                in_construct_lookup = True
                continue
            # Regular framework heading
            current_framework = {
                "id": heading_code or heading_name.split()[0].upper(),
                "name": heading_name,
                "mechanisms": [],
            }
            frameworks.append(current_framework)
            in_construct_lookup = False
            continue

        # Table separator (| --- | --- |) — after this, rows are data rows
        if TABLE_SEPARATOR.match(line):
            # Everything buffered above was the header row
            if rows_since_separator:
                table_header = rows_since_separator[-1]
                rows_since_separator.clear()
            continue

        # Table row (data or header)
        if TABLE_ROW.match(line):
            rows_since_separator.append(_cells(line))
            continue

        # Anything else — blank line or prose. Treat as end-of-table marker.
        if rows_since_separator or table_header:
            flush_table()

    flush_table()  # trailing table at EOF

    return {
        "frameworks": frameworks,
        "cross_framework": cross_framework,
        "construct_lookup": construct_lookup,
    }


def enrich_with_wordcounts(parsed: dict, profiles_dir: Path) -> dict:
    """Add word_count and exists flags to every mechanism row."""
    def add(mech: dict):
        f = mech.get("file", "")
        if not f:
            mech["exists"] = False
            mech["word_count"] = 0
            return
        p = profiles_dir / f
        if not p.exists():
            mech["exists"] = False
            mech["word_count"] = 0
            return
        try:
            words = len(p.read_text(encoding="utf-8").split())
        except Exception:
            words = 0
        mech["exists"] = True
        mech["word_count"] = words

    for fw in parsed["frameworks"]:
        for m in fw["mechanisms"]:
            add(m)
    for m in parsed["cross_framework"]:
        add(m)
    return parsed


def summarise(parsed: dict) -> dict:
    total = sum(len(fw["mechanisms"]) for fw in parsed["frameworks"]) + len(parsed["cross_framework"])
    # Readiness bucketing (useful for an admin "what needs writing" view)
    def bucket(word_count: int) -> str:
        if word_count == 0:           return "missing"
        if word_count < 300:          return "stub"
        if word_count < 600:          return "brief"
        return "full"
    buckets = {"missing": 0, "stub": 0, "brief": 0, "full": 0}
    for fw in parsed["frameworks"]:
        for m in fw["mechanisms"]:
            buckets[bucket(m.get("word_count", 0))] += 1
    for m in parsed["cross_framework"]:
        buckets[bucket(m.get("word_count", 0))] += 1

    return {
        "total": total,
        "framework_count": len(parsed["frameworks"]),
        "cross_framework_count": len(parsed["cross_framework"]),
        "construct_count": len(parsed["construct_lookup"]),
        "readiness": buckets,
    }


def build_manifest(source: Path, profiles_dir: Path) -> dict:
    parsed = parse_index(source)
    parsed = enrich_with_wordcounts(parsed, profiles_dir)
    manifest = {
        "schema_version": 1,
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
                            .replace(microsecond=0).isoformat(),
        "source": {
            "repo": "Article_Eater_PostQuinean_v1_recovery",
            "path": str(source),
            "profiles_dir": str(profiles_dir),
            "mtime": datetime.datetime.fromtimestamp(source.stat().st_mtime,
                        tz=datetime.timezone.utc).replace(microsecond=0).isoformat(),
        },
        "summary": summarise(parsed),
        "frameworks": parsed["frameworks"],
        "cross_framework": parsed["cross_framework"],
        "construct_lookup": parsed["construct_lookup"],
    }
    return manifest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE,
                    help="Path to the mechanism_profiles/_index.md file.")
    ap.add_argument("--profiles-dir", type=Path, default=None,
                    help="Directory containing the profile .md files (default: same dir as --source).")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT,
                    help="Output path for pnus.json.")
    ap.add_argument("--pretty", action="store_true", default=True,
                    help="Pretty-print JSON (default: on).")
    ap.add_argument("--compact", dest="pretty", action="store_false",
                    help="Compact JSON (no pretty-printing).")
    args = ap.parse_args()

    profiles_dir = args.profiles_dir or args.source.parent

    try:
        manifest = build_manifest(args.source, profiles_dir)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(manifest, indent=2 if args.pretty else None, ensure_ascii=False),
        encoding="utf-8"
    )
    s = manifest["summary"]
    print(f"Wrote {args.out}")
    print(f"  {s['framework_count']} frameworks, "
          f"{s['total']} mechanisms "
          f"({s['cross_framework_count']} cross-framework)")
    print(f"  readiness: full={s['readiness']['full']} "
          f"brief={s['readiness']['brief']} "
          f"stub={s['readiness']['stub']} "
          f"missing={s['readiness']['missing']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

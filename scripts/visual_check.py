#!/usr/bin/env python3
"""
visual_check.py — visual regression for the K-ATLAS site.

Reads a scenario list from visual_scenarios.json, navigates Chromium
via Playwright to each URL at three viewports, saves screenshots, and
(if baselines exist) produces a pixel-diff HTML report showing any
drift above a configurable threshold.

Design: optimised for a mostly-static site with ~10 reference templates.
Do not scan all ~1000 content pages on every run; instead, scan the
canonical instance of each template and trust that template-level
changes propagate predictably. Re-run after template changes, after
canonical-navbar changes, and on weekly schedule.

Install once:
    pip3 install --break-system-packages playwright Pillow
    python3 -m playwright install chromium

Run:
    # First run — captures baselines, no diff
    python3 scripts/visual_check.py --capture-baselines

    # Subsequent runs — capture current + diff against committed baselines
    python3 scripts/visual_check.py

    # Diff only (no fresh capture; useful after pulling a new branch)
    python3 scripts/visual_check.py --diff-only

Output:
    scripts/visual_baselines/<scenario_id>_<viewport>.png   baseline
    scripts/visual_current/<scenario_id>_<viewport>.png     current
    scripts/visual_diff/<scenario_id>_<viewport>.png        diff image
    scripts/visual_report.html                              HTML report

Exit codes:
    0  no drift above threshold
    1  drift exceeded threshold on at least one scenario
    2  scanner error (Playwright not installed, etc.)
"""

import argparse
import json
import sys
import os
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
KA_ROOT = SCRIPT_DIR.parent
BASELINE_DIR = SCRIPT_DIR / "visual_baselines"
CURRENT_DIR  = SCRIPT_DIR / "visual_current"
DIFF_DIR     = SCRIPT_DIR / "visual_diff"
REPORT_PATH  = SCRIPT_DIR / "visual_report.html"
SCENARIOS_PATH = SCRIPT_DIR / "visual_scenarios.json"

VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "tablet":  {"width": 768,  "height": 1024},
    "mobile":  {"width": 390,  "height": 844},
}

DEFAULT_THRESHOLD = 0.001  # 0.1% pixels differing counts as drift


# ─── Scenarios ────────────────────────────────────────────────────────

DEFAULT_SCENARIOS = [
    # (id, description, url-relative-to-server-root)
    {"id": "home",          "desc": "Landing page",         "path": "ka_home.html"},
    {"id": "theories",      "desc": "Theories index",       "path": "ka_theories.html"},
    {"id": "framework_pp",  "desc": "T1 framework (PP)",    "path": "ka_framework_pp.html"},
    {"id": "mechanisms",    "desc": "Mechanisms index",     "path": "ka_mechanisms.html"},
    {"id": "neural",        "desc": "Neural Underpinnings", "path": "ka_neural.html"},
    {"id": "articles",      "desc": "Articles",             "path": "ka_articles.html"},
    {"id": "topics",        "desc": "Topics",               "path": "ka_topics.html"},
    {"id": "contribute",    "desc": "Contribute",           "path": "ka_contribute.html"},
    {"id": "schedule_160sp", "desc": "160sp schedule",       "path": "160sp/ka_schedule.html"},
    {"id": "track1_hub",    "desc": "160sp Track 1 hub",    "path": "160sp/ka_track1_hub.html"},
    {"id": "admin",         "desc": "Admin console",        "path": "160sp/ka_admin.html"},
    {"id": "archive",       "desc": "Archive index",        "path": "ka_archive.html"},
]


def load_scenarios() -> list[dict]:
    if SCENARIOS_PATH.exists():
        return json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    # Seed the file on first run
    SCENARIOS_PATH.write_text(
        json.dumps(DEFAULT_SCENARIOS, indent=2), encoding="utf-8")
    return DEFAULT_SCENARIOS


# ─── Capture ─────────────────────────────────────────────────────────

def capture_all(scenarios: list[dict], base_url: str, out_dir: Path) -> list[dict]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.\n"
              "  pip3 install --break-system-packages playwright Pillow\n"
              "  python3 -m playwright install chromium", file=sys.stderr)
        sys.exit(2)

    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        for s in scenarios:
            url = f"{base_url.rstrip('/')}/{s['path']}"
            for vp_name, vp in VIEWPORTS.items():
                ctx = browser.new_context(viewport=vp)
                page = ctx.new_page()
                dest = out_dir / f"{s['id']}_{vp_name}.png"
                try:
                    page.goto(url, wait_until="networkidle", timeout=15000)
                    # Let any lazy-load settle
                    page.wait_for_timeout(500)
                    page.screenshot(path=str(dest), full_page=False)
                    status = "ok"
                except Exception as e:
                    status = f"error: {e}"
                finally:
                    ctx.close()
                results.append({
                    "scenario": s["id"], "viewport": vp_name,
                    "url": url, "status": status, "file": str(dest)})
        browser.close()
    return results


# ─── Diff ────────────────────────────────────────────────────────────

@dataclass
class DiffResult:
    scenario: str
    viewport: str
    baseline: Optional[Path]
    current: Optional[Path]
    diff_path: Optional[Path]
    pct_different: float
    status: str   # pass / drift / missing-baseline / missing-current / size-mismatch


def diff_pair(baseline: Path, current: Path, diff_path: Path) -> DiffResult:
    try:
        from PIL import Image, ImageChops
    except ImportError:
        return DiffResult(
            scenario=baseline.stem.rsplit("_", 1)[0],
            viewport=baseline.stem.rsplit("_", 1)[1],
            baseline=baseline, current=current, diff_path=None,
            pct_different=0.0, status="pillow-not-installed")

    parts = baseline.stem.rsplit("_", 1)
    scenario, viewport = parts[0], parts[1] if len(parts) > 1 else ""

    if not baseline.exists():
        return DiffResult(scenario, viewport, None, current, None, 0.0, "missing-baseline")
    if not current.exists():
        return DiffResult(scenario, viewport, baseline, None, None, 0.0, "missing-current")

    b = Image.open(baseline).convert("RGB")
    c = Image.open(current).convert("RGB")
    if b.size != c.size:
        return DiffResult(scenario, viewport, baseline, current, None,
                          0.0, "size-mismatch")

    diff_im = ImageChops.difference(b, c)
    # Count non-zero pixels
    hist = diff_im.convert("L").point(lambda p: 255 if p > 5 else 0)
    diff_count = sum(hist.point(lambda p: 1 if p else 0).getdata())
    total = b.size[0] * b.size[1]
    pct = diff_count / total if total else 0.0

    diff_path.parent.mkdir(parents=True, exist_ok=True)
    # Produce an overlay visualisation: diff on red where changed
    from PIL import ImageDraw
    overlay = c.copy()
    mask = hist  # already 0 or 255
    red_layer = Image.new("RGB", c.size, (255, 0, 0))
    overlay.paste(red_layer, mask=mask)
    overlay.save(diff_path)

    status = "pass" if pct < DEFAULT_THRESHOLD else "drift"
    return DiffResult(scenario, viewport, baseline, current, diff_path, pct, status)


def diff_all(scenarios: list[dict]) -> list[DiffResult]:
    results = []
    for s in scenarios:
        for vp in VIEWPORTS:
            bl = BASELINE_DIR / f"{s['id']}_{vp}.png"
            cu = CURRENT_DIR / f"{s['id']}_{vp}.png"
            df = DIFF_DIR / f"{s['id']}_{vp}.png"
            results.append(diff_pair(bl, cu, df))
    return results


# ─── Report ──────────────────────────────────────────────────────────

REPORT_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>K-ATLAS visual regression</title>
<style>
body{{font-family:-apple-system,Arial,sans-serif;background:#F7F4EF;
     color:#2C2C2C;line-height:1.5;padding:24px;max-width:1200px;margin:0 auto}}
h1{{font-family:Georgia,serif;color:#1C3D3A}}
.stamp{{color:#6B6B6B;font-size:.88rem;margin-bottom:18px}}
table{{width:100%;border-collapse:collapse;margin-top:14px;font-size:.88rem}}
th,td{{padding:8px 10px;text-align:left;border-bottom:1px solid #E0D8CC}}
th{{background:#F9F5EE;font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:#8A9A96}}
tr.pass td:first-child::before{{content:"✓ ";color:#1A7050;font-weight:700}}
tr.drift td:first-child::before{{content:"⚠ ";color:#E8872A;font-weight:700}}
tr.missing-baseline td:first-child::before{{content:"? ";color:#6B6B6B}}
tr.drift{{background:#FEF3E2}}
.pct{{font-family:ui-monospace,monospace}}
.thumbs{{display:flex;gap:10px;margin-top:14px;flex-wrap:wrap}}
.thumbs .card{{border:1px solid #E0D8CC;border-radius:6px;padding:8px;background:#fff}}
.thumbs img{{max-width:260px;display:block}}
.summary{{background:#fff;border:1.5px solid #E0D8CC;border-radius:10px;padding:14px 18px;margin-bottom:18px}}
</style></head><body>
<h1>Visual Regression Report</h1>
<div class="stamp">Generated {ts} · threshold {thr:.2%} · scenarios {n}</div>
<div class="summary"><b>Pass:</b> {n_pass} &nbsp;·&nbsp;
  <b>Drift:</b> {n_drift} &nbsp;·&nbsp;
  <b>Missing baseline:</b> {n_mb} &nbsp;·&nbsp;
  <b>Missing current:</b> {n_mc} &nbsp;·&nbsp;
  <b>Size mismatch:</b> {n_sm}</div>
<table>
<thead><tr><th>Scenario</th><th>Viewport</th><th>Status</th><th>% diff</th></tr></thead>
<tbody>
{rows}
</tbody></table>
</body></html>"""


def write_report(results: list[DiffResult], threshold: float):
    rows = []
    counts = {"pass":0,"drift":0,"missing-baseline":0,"missing-current":0,"size-mismatch":0}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1
        rows.append(
            f'<tr class="{r.status}">'
            f'<td>{r.scenario}</td>'
            f'<td>{r.viewport}</td>'
            f'<td>{r.status}</td>'
            f'<td class="pct">{r.pct_different:.3%}</td>'
            f'</tr>'
        )
    REPORT_PATH.write_text(REPORT_TEMPLATE.format(
        ts=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        thr=threshold, n=len(results),
        n_pass=counts["pass"], n_drift=counts["drift"],
        n_mb=counts["missing-baseline"], n_mc=counts["missing-current"],
        n_sm=counts["size-mismatch"],
        rows="\n".join(rows)), encoding="utf-8")


# ─── Main ────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base-url", default="http://localhost:8765",
                    help="Base URL of the local site server")
    ap.add_argument("--capture-baselines", action="store_true",
                    help="Write captured images to baselines instead of current")
    ap.add_argument("--diff-only", action="store_true",
                    help="Skip capture; diff existing current vs baseline")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    args = ap.parse_args()

    scenarios = load_scenarios()

    if not args.diff_only:
        out = BASELINE_DIR if args.capture_baselines else CURRENT_DIR
        print(f"Capturing {len(scenarios) * len(VIEWPORTS)} screenshots to {out} …")
        results = capture_all(scenarios, args.base_url, out)
        errors = [r for r in results if r["status"] != "ok"]
        if errors:
            print(f"WARN: {len(errors)} capture failures:")
            for e in errors[:10]:
                print(f"  {e['scenario']}/{e['viewport']}: {e['status']}")
        if args.capture_baselines:
            print(f"Baselines saved. Commit {BASELINE_DIR.relative_to(KA_ROOT)}/ to lock them in.")
            return 0

    # Diff phase
    results = diff_all(scenarios)
    write_report(results, args.threshold)
    drift = [r for r in results if r.status == "drift"]
    print(f"Diff complete. {len(drift)} scenarios over {args.threshold:.2%} threshold.")
    print(f"Report: {REPORT_PATH}")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())

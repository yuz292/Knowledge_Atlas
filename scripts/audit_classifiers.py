#!/usr/bin/env python3
"""
End-to-end audit of the Track-2 article and topic classifiers.

Answers three questions before we build T2.d.2 on top of these
classifiers:

  1. Are the classifiers producing any output at all, and for what
     fraction of the corpus?
  2. Does classification_confidence have a reasonable distribution
     (not all 1.0, not all 0.5) — a cheap sanity signal?
  3. On a hand-sampleable subset, does the predicted topic look
     plausible given the paper title?

The audit is read-only against the authoritative DB at
Article_Eater_PostQuinean_v1_recovery/data/pipeline_registry_unified.db.

Usage
-----
    python3 scripts/audit_classifiers.py
    python3 scripts/audit_classifiers.py --sample 30 --csv audit.csv

No LLM calls; just SQL + descriptive statistics + a hand-sample CSV
the instructor can eyeball.
"""
from __future__ import annotations

import argparse
import csv
import os
import random
import sqlite3
import sys
from collections import Counter
from pathlib import Path

# Default path to the cross-repo unified registry. This is the DB our
# T2 rubrics + ai_grader briefings reference. Overridable via env var
# so production deploys (where AE and KA live at different mount
# points) can set it once.
DEFAULT_DB = os.environ.get(
    "KA_UNIFIED_REGISTRY_DB",
    "/sessions/brave-great-tesla/mnt/REPOS/"
    "Article_Eater_PostQuinean_v1_recovery/data/pipeline_registry_unified.db",
)


def fmt_pct(numer: int, denom: int) -> str:
    if not denom:
        return "—"
    return f"{numer:>5d}/{denom:<5d} ({100*numer/denom:>5.1f}%)"


def audit(db_path: str, sample_size: int, csv_out: Path | None) -> None:
    if not Path(db_path).exists():
        print(f"error: DB not found at {db_path}", file=sys.stderr)
        sys.exit(1)

    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    c = con.cursor()

    # ─── 1. Corpus size + classifier coverage ────────────────────
    print(f"=== Classifier audit — {Path(db_path).name} ===\n")
    total = c.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
    print(f"Corpus size: {total} papers\n")

    coverage_queries = {
        "Has topic_category":
            "SELECT COUNT(*) FROM papers WHERE topic_category IS NOT NULL AND topic_category != ''",
        "Has topic_subcategory":
            "SELECT COUNT(*) FROM papers WHERE topic_subcategory IS NOT NULL AND topic_subcategory != ''",
        "Has classification_confidence":
            "SELECT COUNT(*) FROM papers WHERE classification_confidence IS NOT NULL",
        "Has primary_topic_candidate":
            "SELECT COUNT(*) FROM papers WHERE primary_topic_candidate IS NOT NULL AND primary_topic_candidate != ''",
        "Has pnu_status not null":
            "SELECT COUNT(*) FROM papers WHERE pnu_status IS NOT NULL AND pnu_status != ''",
        "Has canonical_classifications row":
            """SELECT COUNT(DISTINCT p.paper_id) FROM papers p
               JOIN canonical_classifications cc ON cc.paper_id = p.paper_id""",
        "n_tag_assignments > 0":
            "SELECT COUNT(*) FROM papers WHERE n_tag_assignments > 0",
    }
    print("Coverage:")
    for label, q in coverage_queries.items():
        n = c.execute(q).fetchone()[0]
        print(f"  {label:<42} {fmt_pct(n, total)}")
    print()

    # ─── 2. classification_confidence distribution ───────────────
    print("classification_confidence distribution:")
    rows = c.execute(
        "SELECT classification_confidence FROM papers "
        "WHERE classification_confidence IS NOT NULL").fetchall()
    # classification_confidence is TEXT in this schema — coerce, drop
    # any entries that don't parse to a 0-1 float
    confs = []
    non_numeric = Counter()
    for r in rows:
        try:
            v = float(r[0])
            if 0.0 <= v <= 1.0:
                confs.append(v)
            else:
                non_numeric[f"out-of-range:{r[0]}"] += 1
        except (TypeError, ValueError):
            non_numeric[str(r[0])[:20]] += 1
    if non_numeric:
        print(f"  (note: {sum(non_numeric.values())} non-numeric / "
              f"out-of-range confidence values; top: {dict(non_numeric.most_common(5))})")
    if confs:
        bins = [0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.001]
        bin_labels = [f"[{bins[i]:.2f}, {bins[i+1]:.2f})" for i in range(len(bins)-1)]
        counts = [0] * (len(bins) - 1)
        for v in confs:
            for i in range(len(bins) - 1):
                if bins[i] <= v < bins[i+1]:
                    counts[i] += 1
                    break
        for label, n in zip(bin_labels, counts):
            bar = "█" * min(50, n // max(1, max(counts) // 50))
            print(f"  {label:<16} {n:>5d}  {bar}")
        print(f"  mean: {sum(confs)/len(confs):.3f}, "
              f"min: {min(confs):.3f}, max: {max(confs):.3f}")
    else:
        print("  (no confidence values — classifier not producing numeric output)")
    print()

    # ─── 3. Top topic categories ─────────────────────────────────
    print("Top topic_category (unique values):")
    topic_rows = c.execute("""
        SELECT topic_category, COUNT(*) AS n
        FROM papers
        WHERE topic_category IS NOT NULL AND topic_category != ''
        GROUP BY topic_category
        ORDER BY n DESC
    """).fetchall()
    for r in topic_rows[:25]:
        print(f"  {r[0][:60]:<62} {r[1]:>4d}")
    if len(topic_rows) > 25:
        print(f"  ... and {len(topic_rows) - 25} more distinct categories")
    print(f"  total distinct topic_category values: {len(topic_rows)}")
    print()
    n_distinct_topics = len(topic_rows)

    # ─── 3b. canonical_primary_topic (the richer classifier surface) ─
    print("Top canonical_primary_topic (canonical_classifications table):")
    cc_topic_rows = c.execute("""
        SELECT canonical_primary_topic, COUNT(*) AS n
        FROM canonical_classifications
        WHERE canonical_primary_topic IS NOT NULL AND canonical_primary_topic != ''
        GROUP BY canonical_primary_topic
        ORDER BY n DESC
    """).fetchall()
    for r in cc_topic_rows[:25]:
        print(f"  {r[0][:60]:<62} {r[1]:>4d}")
    if len(cc_topic_rows) > 25:
        print(f"  ... and {len(cc_topic_rows) - 25} more distinct canonical topics")
    print(f"  total distinct canonical_primary_topic values: {len(cc_topic_rows)}")
    print()

    # ─── 3c. canonical_article_type + triage ──────────────────────
    print("canonical_article_type distribution:")
    for r in c.execute("""
        SELECT canonical_article_type, COUNT(*) AS n
        FROM canonical_classifications
        WHERE canonical_article_type IS NOT NULL AND canonical_article_type != ''
        GROUP BY canonical_article_type
        ORDER BY n DESC LIMIT 15
    """).fetchall():
        print(f"  {r[0][:60]:<62} {r[1]:>4d}")
    print()

    print("canonical_triage_decision distribution:")
    for r in c.execute("""
        SELECT canonical_triage_decision, COUNT(*) AS n
        FROM canonical_classifications
        WHERE canonical_triage_decision IS NOT NULL AND canonical_triage_decision != ''
        GROUP BY canonical_triage_decision
        ORDER BY n DESC LIMIT 15
    """).fetchall():
        print(f"  {r[0][:60]:<62} {r[1]:>4d}")
    print()

    print(f"has_classifier_conflict: "
          f"{c.execute('SELECT COUNT(*) FROM canonical_classifications WHERE has_classifier_conflict = 1').fetchone()[0]} "
          f"of {c.execute('SELECT COUNT(*) FROM canonical_classifications').fetchone()[0]} papers")
    print()

    # ─── 4. canonical_classifications (cross-table) ───────────────
    print("canonical_classifications — per-paper classification rows:")
    try:
        total_cc = c.execute("SELECT COUNT(*) FROM canonical_classifications").fetchone()[0]
        distinct_papers = c.execute(
            "SELECT COUNT(DISTINCT paper_id) FROM canonical_classifications").fetchone()[0]
        print(f"  total rows: {total_cc}")
        print(f"  papers with >=1 classification: {distinct_papers} "
              f"({100*distinct_papers/total:.1f}% of corpus)")
        cc_cols = [r[1] for r in c.execute("PRAGMA table_info(canonical_classifications)").fetchall()]
        print(f"  columns: {cc_cols}")
    except sqlite3.OperationalError as e:
        print(f"  (no canonical_classifications table: {e})")
    print()

    # ─── 5. Hand-sample for instructor eyeballing ────────────────
    print(f"Hand-sample of {sample_size} papers (random):")
    rows = c.execute("""
        SELECT paper_id, title, topic_category, topic_subcategory,
               primary_topic_candidate, classification_confidence,
               pnu_status, n_tag_assignments
        FROM papers
        WHERE topic_category IS NOT NULL AND topic_category != ''
        ORDER BY RANDOM()
        LIMIT ?
    """, (sample_size,)).fetchall()

    if csv_out:
        with csv_out.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["paper_id", "title", "topic_category",
                        "topic_subcategory", "primary_topic_candidate",
                        "classification_confidence", "pnu_status",
                        "n_tag_assignments", "instructor_agrees?"])
            for r in rows:
                w.writerow([*r, ""])
        print(f"  wrote {len(rows)} rows to {csv_out} "
              "(fill 'instructor_agrees?' column by eye, then import)")
    else:
        for r in rows[:10]:
            title = (r["title"] or "")[:68]
            topic = (r["topic_category"] or "")[:38]
            conf  = f"{r['classification_confidence']:.2f}" if r["classification_confidence"] is not None else "—"
            print(f"  [{conf}] {topic:<40} {title}")
        if len(rows) > 10:
            print(f"  ... ({len(rows) - 10} more in sample; pass --csv to export all)")
    print()

    # ─── 6. Verdict (structural, not content) ─────────────────────
    print("Structural verdict:")
    signals = {
        "corpus size > 500": total > 500,
        "topic_category populated for > 40% of corpus":
            c.execute("SELECT COUNT(*) FROM papers WHERE topic_category IS NOT NULL AND topic_category != ''").fetchone()[0] > total * 0.4,
        "classification_confidence varies (not flat)":
            len(set(round(v, 1) for v in confs)) > 3 if confs else False,
        "canonical_classifications covers 100% of corpus":
            c.execute("SELECT COUNT(DISTINCT paper_id) FROM canonical_classifications").fetchone()[0] >= total,
        "canonical_primary_topic has >= 10 distinct values":
            len(cc_topic_rows) >= 10,
        "papers.topic_category has >= 10 distinct values":
            n_distinct_topics >= 10,
    }
    all_pass = True
    for label, ok in signals.items():
        mark = "✓" if ok else "✗"
        print(f"  {mark} {label}")
        if not ok:
            all_pass = False
    print()
    if all_pass:
        print("→ Classifier structure is sound. T2.d.2's check-side is viable.")
        print("  Next step: instructor hand-reviews a 20-paper sample to")
        print("  assess prediction quality, not just structure.")
    else:
        print("→ Structural gaps flagged above. Two possible responses:")
        print("  (a) Narrow T2.d.2's 'topic classifier' to the surface")
        print("      that IS populated (canonical_classifications richer")
        print("      columns + papers.topic_category for its 9-value modality).")
        print("  (b) Defer T2.d.2 until primary_topic_candidate and a finer")
        print("      topic taxonomy are filled in.")

    con.close()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=DEFAULT_DB,
                    help="Path to pipeline_registry_unified.db "
                         "(default: env KA_UNIFIED_REGISTRY_DB or the "
                         "AE recovery repo sibling path)")
    ap.add_argument("--sample", type=int, default=15,
                    help="Hand-sample size (default 15)")
    ap.add_argument("--csv", type=Path,
                    help="Write the full sample to this CSV file for "
                         "instructor review")
    args = ap.parse_args()
    audit(args.db, args.sample, args.csv)


if __name__ == "__main__":
    main()

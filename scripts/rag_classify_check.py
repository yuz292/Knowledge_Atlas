#!/usr/bin/env python3
"""
RAG harvest × our classifier — disagreement report builder.

Reads the per-service normalised harvest JSON files produced by
scripts/rag_harvest.py for one student, and for every unique paper
across all services builds one row in classifier_check.csv. Each row
records what the RAG services said about the paper and what our
classifiers (in pipeline_registry_unified.db) say about the same paper.

The output CSV is the input to the student's disagreement_report.md
writeup (see 160sp/rubrics/t2/T2.d.2_rag_audit.md §3 for the
deliverable spec).

Usage
-----
    # Build classifier_check.csv for one student
    python3 scripts/rag_classify_check.py --student s03

    # Custom paths (testing or non-default DB)
    python3 scripts/rag_classify_check.py --student s03 \\
        --db /path/to/pipeline_registry_unified.db \\
        --out /tmp/check.csv

Disagreement flags
------------------
For each paper, the script computes an `agreement_flag` with one of:
  - agree                 : services and our classifier agree on type AND topic
  - service_disagreement  : services contradict each other (one says yes, one no)
  - our_disagreement      : services agree, but our classifier disagrees
  - unknown_to_us         : paper not in our DB; nothing to compare against
  - mixed                 : everything else
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TRACKS = REPO / "160sp" / "tracks" / "t2"
DEFAULT_DB = os.environ.get(
    "KA_UNIFIED_REGISTRY_DB",
    "/sessions/brave-great-tesla/mnt/REPOS/"
    "Article_Eater_PostQuinean_v1_recovery/data/pipeline_registry_unified.db",
)


def load_harvest(student_id: str) -> dict:
    """Return {service_id: harvest_dict} for one student."""
    harvest_dir = TRACKS / student_id / "T2.d.2" / "harvest"
    if not harvest_dir.exists():
        sys.exit(f"error: no harvest directory at {harvest_dir}. "
                 "Run scripts/rag_harvest.py first.")
    out = {}
    for sub in harvest_dir.iterdir():
        if not sub.is_dir():
            continue
        norm = sub / "normalised.json"
        if not norm.exists():
            continue
        out[sub.name] = json.loads(norm.read_text())
    if not out:
        sys.exit(f"error: no normalised.json files found under {harvest_dir}")
    return out


def index_papers_by_doi(harvests: dict) -> dict:
    """Cross-service index: doi -> list of (service_id, paper_dict)."""
    by_doi = defaultdict(list)
    for service_id, payload in harvests.items():
        for paper in payload.get("papers", []):
            doi = paper.get("doi")
            if doi:
                by_doi[doi.lower().strip()].append((service_id, paper))
    return dict(by_doi)


def lookup_our_classification(con: sqlite3.Connection, doi: str) -> dict | None:
    """Look up a paper by DOI in pipeline_registry_unified.db.

    Returns a dict with our classifier's verdict, or None if the paper
    is not in our corpus.
    """
    c = con.cursor()
    row = c.execute("""
        SELECT p.paper_id, p.title, p.topic_category, p.topic_subcategory,
               p.classification_confidence,
               cc.canonical_article_type, cc.canonical_primary_topic,
               cc.canonical_article_type_confidence,
               cc.canonical_question_best_verdict,
               cc.canonical_triage_decision
        FROM papers p
        LEFT JOIN canonical_classifications cc ON cc.paper_id = p.paper_id
        WHERE LOWER(TRIM(p.doi)) = ?
        LIMIT 1
    """, (doi.lower().strip(),)).fetchone()
    if not row:
        return None
    cols = ["paper_id", "title", "topic_category", "topic_subcategory",
            "classification_confidence", "canonical_article_type",
            "canonical_primary_topic", "canonical_article_type_confidence",
            "canonical_question_best_verdict", "canonical_triage_decision"]
    return dict(zip(cols, row))


def compute_agreement_flag(service_calls: list, our: dict | None) -> str:
    """Compare RAG-service relevance verdicts with our classifier."""
    if our is None:
        return "unknown_to_us"

    verdicts = [c[1].get("service_claimed_verdict") for c in service_calls]
    relevances = [c[1].get("service_claimed_relevance") for c in service_calls
                  if c[1].get("service_claimed_relevance") is not None]

    distinct_verdicts = {v for v in verdicts if v}
    services_agree = len(distinct_verdicts) <= 1

    has_our_topic = bool(our.get("topic_category"))
    has_our_type = bool(our.get("canonical_article_type"))

    if not services_agree:
        return "service_disagreement"

    if not (has_our_topic or has_our_type):
        return "no_our_classification"

    if relevances and max(relevances) >= 0.7 and has_our_topic:
        return "agree"

    if relevances and max(relevances) < 0.4 and has_our_topic:
        return "our_disagreement"

    return "mixed"


def build_csv(student_id: str, db_path: str, out: Path) -> None:
    if not Path(db_path).exists():
        sys.exit(f"error: classifier DB not found at {db_path}")
    harvests = load_harvest(student_id)
    by_doi = index_papers_by_doi(harvests)
    con = sqlite3.connect(db_path)

    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "doi", "title", "services_returning_it",
        "service_claimed_relevance", "service_claimed_verdict",
        "our_paper_id", "our_topic_category", "our_topic_subcategory",
        "our_canonical_article_type", "our_canonical_primary_topic",
        "our_classification_confidence",
        "agreement_flag",
    ]
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()

        n_total = 0
        n_known = 0
        n_unknown = 0
        for doi, calls in sorted(by_doi.items()):
            n_total += 1
            our = lookup_our_classification(con, doi)
            if our:
                n_known += 1
            else:
                n_unknown += 1
            services = ",".join(sorted({c[0] for c in calls}))
            relevances = json.dumps({c[0]: c[1].get("service_claimed_relevance")
                                     for c in calls})
            verdicts = json.dumps({c[0]: c[1].get("service_claimed_verdict")
                                   for c in calls})
            title = calls[0][1].get("title", "")
            row = {
                "doi": doi,
                "title": title,
                "services_returning_it": services,
                "service_claimed_relevance": relevances,
                "service_claimed_verdict": verdicts,
                "our_paper_id": our["paper_id"] if our else "",
                "our_topic_category": (our or {}).get("topic_category", ""),
                "our_topic_subcategory": (our or {}).get("topic_subcategory", ""),
                "our_canonical_article_type": (our or {}).get("canonical_article_type", ""),
                "our_canonical_primary_topic": (our or {}).get("canonical_primary_topic", ""),
                "our_classification_confidence": (our or {}).get("classification_confidence", ""),
                "agreement_flag": compute_agreement_flag(calls, our),
            }
            w.writerow(row)

    con.close()
    print(f"wrote {n_total} papers to {out}")
    print(f"  known to our classifier:    {n_known}")
    print(f"  unknown to our classifier:  {n_unknown}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--student", "-s", required=True,
                    help="Student id (e.g. s03)")
    ap.add_argument("--db", default=DEFAULT_DB,
                    help="pipeline_registry_unified.db path "
                         "(default: env KA_UNIFIED_REGISTRY_DB)")
    ap.add_argument("--out", type=Path,
                    help="Output CSV path "
                         "(default: 160sp/tracks/t2/{student}/T2.d.2/classifier_check.csv)")
    args = ap.parse_args()
    out = args.out or (TRACKS / args.student / "T2.d.2" / "classifier_check.csv")
    build_csv(args.student, args.db, out)


if __name__ == "__main__":
    main()

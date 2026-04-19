#!/usr/bin/env python3
"""
RAG harvest orchestrator for T2.d.2.

Sends a single structured query to every AI research-assistant service
listed in data/rag_services.yaml and writes each service's normalised
response to 160sp/tracks/t2/{student_id}/T2.d.2/harvest/{service_id}/.

Pluggable service adapters
--------------------------
Each service has a Python adapter module under scripts/rag_adapters/
with a single top-level function:

    harvest(query: str, service_config: dict) -> dict

that returns a dict matching the normalised schema documented at the
bottom of data/rag_services.yaml. The orchestrator is agnostic to
individual service APIs; adapters encapsulate per-service quirks
(authentication, rate-limiting, response-shape normalisation).

Interim "manual" adapters
-------------------------
Services without a usable API (ChatGPT Deep Research, Gemini Deep
Research as of April 2026) use `access: "manual"` in rag_services.yaml.
For those, this script does not attempt to call the service; instead
it emits a harvest/{service_id}/INSTRUCTIONS.md file explaining what
the student must paste in. Once the student saves the response, the
adapter's `normalise_manual(...)` function converts the pasted text
into the common schema.

Secrets handling
----------------
API keys and tokens live in environment variables following the
pattern KA_RAG_{SERVICE_ID}_API_KEY (uppercase). Adapters read them;
no key is ever written to disk. If an adapter cannot find its key, it
skips the service and prints a clear diagnostic.

Usage
-----
    # Harvest for one student, one query
    python3 scripts/rag_harvest.py \\
        --student s03 \\
        --query "daylight effects on cognitive performance in offices" \\
        --services elicit,consensus,scispace

    # Dry-run (show what would be called; do not hit any service)
    python3 scripts/rag_harvest.py --student s03 --query "..." --dry-run

    # Harvest for all services listed in rag_services.yaml
    python3 scripts/rag_harvest.py --student s03 --query "..."

Status
------
This is a SKELETON orchestrator. The individual service adapters are
stubs — each returns a synthetic payload matching the normalised
schema so downstream tooling (scripts/rag_classify_check.py) can be
developed and tested without live API credentials. The adapters
become real when DK confirms the service list and provides
credentials; each adapter is 50–150 lines once fleshed out.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    raise SystemExit(
        "PyYAML not installed. Run: pip3 install --break-system-packages pyyaml"
    )

REPO = Path(__file__).resolve().parent.parent
SERVICES_YAML = REPO / "data" / "rag_services.yaml"
TRACKS = REPO / "160sp" / "tracks" / "t2"
ADAPTERS_DIR = REPO / "scripts" / "rag_adapters"


# ─── Service config ───────────────────────────────────────────────
def load_services(filter_ids: list[str] | None = None) -> list[dict]:
    if not SERVICES_YAML.exists():
        sys.exit(f"error: {SERVICES_YAML} not found — fill in the services manifest first.")
    data = yaml.safe_load(SERVICES_YAML.read_text())
    services = data.get("services", [])
    if filter_ids:
        services = [s for s in services if s["id"] in filter_ids]
    return services


# ─── Adapter loader ───────────────────────────────────────────────
def load_adapter(adapter_name: str):
    """Import scripts.rag_adapters.{adapter_name} on demand."""
    try:
        return importlib.import_module(f"scripts.rag_adapters.{adapter_name}")
    except ModuleNotFoundError:
        return None


def stub_harvest(query: str, service: dict) -> dict:
    """Synthetic payload used when no real adapter is present.

    Returns a valid normalised-schema dict with a small placeholder
    papers list so downstream tooling can be developed without live
    credentials. The stub records enough metadata that a reviewer
    can see the harvest was a stub, not a real call.
    """
    return {
        "service_id": service["id"],
        "service_name": service.get("name", service["id"]),
        "query": query,
        "harvested_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "synthesis": (
            f"[STUB — real adapter not yet wired for {service['id']}] "
            f"In production, this is where {service['name']}'s synthesised "
            "answer goes. Harvest this manually or wire the adapter once "
            "credentials are configured."
        ),
        "papers": [
            {
                "doi": f"10.STUB/{service['id']}-001",
                "title": f"[Stub paper 1 for {service['name']}]",
                "authors": ["Stub, A.", "Placeholder, B."],
                "year": 2024,
                "abstract": "This is a stub abstract. Replace with a real harvest.",
                "service_claimed_relevance": 0.90,
                "service_claimed_verdict": None,
                "service_evidence_snippet": None,
                "source_url": None,
            },
        ],
        "raw_response_path": None,
        "is_stub": True,
    }


def harvest_service(query: str, service: dict, dry_run: bool) -> dict:
    """Run one service's adapter against a query. Returns normalised dict."""
    adapter_name = service.get("adapter")
    if not adapter_name:
        return stub_harvest(query, service) | {"error": "no adapter declared"}

    access = service.get("access", "api")
    if access == "manual":
        # Manual services emit instructions rather than calling an API.
        return {
            "service_id": service["id"],
            "service_name": service.get("name", service["id"]),
            "query": query,
            "harvested_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "access": "manual",
            "papers": [],
            "instructions": (
                f"Paste `{query}` into {service['name']}; copy the "
                "response into response.md in this directory; then run "
                f"`python3 scripts/rag_harvest.py --normalise {service['id']}` "
                "to run the manual-normalisation pass."
            ),
            "is_stub": False,
        }

    if dry_run:
        return {
            **stub_harvest(query, service),
            "dry_run": True,
            "note": f"Would call {adapter_name}.harvest(...) with access={access}",
        }

    adapter = load_adapter(adapter_name)
    if adapter is None:
        return stub_harvest(query, service) | {
            "error": f"adapter module scripts/rag_adapters/{adapter_name}.py not found",
        }
    if not hasattr(adapter, "harvest"):
        return stub_harvest(query, service) | {
            "error": f"{adapter_name} has no harvest() function",
        }
    try:
        return adapter.harvest(query, service)
    except Exception as e:
        return stub_harvest(query, service) | {
            "error": f"{adapter_name}.harvest raised: {type(e).__name__}: {e}",
        }


# ─── Orchestrator ─────────────────────────────────────────────────
def run_harvest(student_id: str, query: str,
                service_filter: list[str] | None,
                dry_run: bool) -> dict:
    services = load_services(service_filter)
    if not services:
        sys.exit("error: no services to run (check filter + rag_services.yaml)")

    out_dir = TRACKS / student_id / "T2.d.2" / "harvest"
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "student_id": student_id,
        "query": query,
        "harvested_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "dry_run": dry_run,
        "services": [],
    }

    for svc in services:
        print(f"  [{svc['id']:<24}] ", end="", flush=True)
        result = harvest_service(query, svc, dry_run)
        svc_dir = out_dir / svc["id"]
        svc_dir.mkdir(exist_ok=True)
        (svc_dir / "normalised.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False))
        papers_count = len(result.get("papers", []))
        status = "STUB " if result.get("is_stub") else ""
        status += "MANUAL " if result.get("access") == "manual" else ""
        status += f"ERROR ({result.get('error', '')}) " if result.get("error") else ""
        print(f"{status or 'ok'} · {papers_count} papers")
        summary["services"].append({
            "id": svc["id"],
            "name": svc.get("name"),
            "papers": papers_count,
            "status": status.strip() or "ok",
            "path": str(svc_dir.relative_to(REPO) / "normalised.json"),
        })

    summary_path = out_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


# ─── CLI ──────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--student", "-s", required=True,
                    help="Student id (e.g. s03)")
    ap.add_argument("--query", "-q", required=True,
                    help="The structured query to send to every service")
    ap.add_argument("--services", default="",
                    help="Comma-separated service ids to limit to "
                         "(e.g. 'elicit,consensus'); default = all")
    ap.add_argument("--dry-run", action="store_true",
                    help="Don't hit any service; emit stub payloads only")
    args = ap.parse_args()

    filters = [s.strip() for s in args.services.split(",") if s.strip()] or None
    summary = run_harvest(args.student, args.query, filters, args.dry_run)
    print()
    print(f"wrote {len(summary['services'])} service payloads to "
          f"{TRACKS / args.student / 'T2.d.2' / 'harvest'}")


if __name__ == "__main__":
    main()

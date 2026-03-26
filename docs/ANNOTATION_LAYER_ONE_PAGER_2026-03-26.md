# Annotation Layer

## What it is
The annotation layer is the review overlay for Knowledge Atlas. It stores calibration notes, sensitivity flags, replication markers, dispute notes, and related guidance that helps a human reviewer understand what still needs attention.

## How we make it
Inputs:
- regenerated annotation products from Article Eater
- belief-level notes emitted by annotation services or repair scripts

Current live artifacts:
- `Article_Eater_PostQuinean_v1_recovery/data/rebuild/annotations_regenerated.json`

Bridge into KA:
- `Knowledge_Atlas/scripts/build_ka_adapter_payloads.py`
- `Knowledge_Atlas/data/ka_payloads/annotations.json`
- `Knowledge_Atlas/ka_annotations.html`

## What it does for us
- lets contributors and reviewers see warnings without opening backend files
- distinguishes a belief that is merely present from one that has caveats attached
- creates a place for incremental review work to accumulate visibly

## What it does for QA
- flags which beliefs are sensitive to network changes
- records replication or surprise status in a machine-readable way
- gives us a compact review surface that can later seed ML training for QA judgments
- helps prevent silent promotion of weak or unstable beliefs

## Current limitation
The current annotation payload is a derived overlay, not the full annotation inventory. It is useful now, but still partial.

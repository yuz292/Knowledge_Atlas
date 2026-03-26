# Argumentation Layer

## What it is
The argumentation layer is the part of Knowledge Atlas that represents support, contestation, and debate structure rather than just listing articles or findings. It sits above the evidence rows and asks how claims relate to each other.

## How we make it
Inputs:
- rebuilt paper and claim records from Article Eater
- theory assignments and paper-level grouping
- claim-level argument graph products

Current live artifacts:
- `Article_Eater_PostQuinean_v1_recovery/data/rebuild/argumentation_graph_v5.json`
- `Article_Eater_PostQuinean_v1_recovery/data/rebuild/claim_argument_graph_v1.json`

Bridge into KA:
- `Knowledge_Atlas/scripts/build_ka_adapter_payloads.py`
- `Knowledge_Atlas/data/ka_payloads/argumentation.json`
- `Knowledge_Atlas/ka_argumentation.html`

## What it does for us
- shows where the field clusters into debates
- exposes support structure instead of hiding it behind article cards
- makes it possible to inspect whether a claim is isolated, supported, or weakly contested
- gives theory/mechanism users a real graph surface to browse

## What it does for QA
- reveals thin stance coverage and other missing graph semantics
- makes contestation gaps visible instead of letting them masquerade as certainty
- provides a place to inspect whether support edges are too generic or too weak
- creates a target surface for later HITL review of warrants and defeat structure

## Current limitation
The graph is live, but explicit stance and contestation typing are still sparse. That is a real maturity limit, not a UI problem.

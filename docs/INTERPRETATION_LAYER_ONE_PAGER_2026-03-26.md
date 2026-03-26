# Interpretation Layer

## What it is
The interpretation layer is where Knowledge Atlas turns evidence and graph structure into research priorities. It tracks boundary beliefs, validation completeness, and frontier questions with high value of information.

## How we make it
Inputs:
- interpretation-space phase 4 outputs from Article Eater
- frontier-prioritization results
- validation completeness scores
- boundary map outputs

Current live artifacts:
- `Article_Eater_PostQuinean_v1_recovery/data/interpretation_space/phase4/phase4_summary.json`
- `Article_Eater_PostQuinean_v1_recovery/data/interpretation_space/phase4/prioritized_frontier_questions.json`
- `Article_Eater_PostQuinean_v1_recovery/data/interpretation_space/phase4/validation_completeness.json`
- `Article_Eater_PostQuinean_v1_recovery/data/interpretation_space/phase4/boundary_map.json`

Bridge into KA:
- `Knowledge_Atlas/scripts/build_ka_adapter_payloads.py`
- `Knowledge_Atlas/data/ka_payloads/interpretation.json`
- `Knowledge_Atlas/ka_interpretation.html`

## What it does for us
- shows which beliefs still sit at the active boundary of the field
- surfaces which questions would most reduce uncertainty
- separates evidence accumulation from interpretation and prioritization
- gives theory/mechanism exploration a practical planning surface

## What it does for QA
- makes incomplete validation visible
- shows whether the system is overclaiming closure where scope is still weak
- gives us a principled way to rank what needs more evidence next
- supports classroom explanation of why "what we know" and "what to do next" are different layers

## Current limitation
The interpretation outputs are live, but they still depend on upstream extraction and graph maturity. Better extraction improves this layer directly.

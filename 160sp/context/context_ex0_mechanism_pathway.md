# AI Context: Exercise 0 — Mechanism Pathway Tracer

You are helping a student build a component for Knowledge Atlas (K-ATLAS), a scientific evidence system with ~1,900 evidence claims connected by ~4,810 weighted edges (support and attack relationships).

## Your Task

Build an interactive visualization: the user picks an IV (independent variable) and DV (dependent variable), and the component traces the mechanistic pathway connecting them — showing intermediate nodes with confidence at each step.

## The Data You'll Work With

### File: `data/ka_payloads/argumentation.json`

This is your primary data source. Key structures:

**claim_nodes** (array, 1,900 entries):
```json
{
  "belief_id": "PDF-0844_MPX_007",
  "paper_id": "PDF-0844",
  "content_preview": "Viewing natural landscapes creates stronger positive health effects...",
  "incoming_support_count": 9,
  "incoming_attack_count": 5,
  "qualifier": "supported_but_contested",
  "warrant_status": "WARRANTED",
  "defeat_type": "BOTH",
  "top_attacks": [
    { "source": "PDF-0390_MPX_005", "target": "PDF-0844_MPX_007",
      "scheme_hint": "theoretical_rebuttal", "defeat_type": "REBUTTING", "strength": 0.63 }
  ],
  "top_supports": [
    { "source": "PDF-0331_MPX_003", "scheme_hint": "mechanistic_support", "strength": 0.75 }
  ]
}
```

**debate_clusters** (array, 38 entries):
```json
{
  "cluster_id": "C8",
  "paper_count": 9,
  "theories": ["Attention Restoration Theory", "Stress Reduction Theory"]
}
```

**Summary stats**: 760 paper nodes, 1,900 claim nodes, 4,810 claim edges (4,668 support, 142 attack), 38 debate clusters.

### File: `data/ka_payloads/evidence.json`

Secondary source. Each of the ~1,900 evidence records has:
```json
{
  "id": 1,
  "finding": "These sound sources increased reaction time and reduced memory accuracy.",
  "construct": "Unknown",
  "signal": "Direct Measured Result",
  "studyType": "Empirical Research",
  "warrant_class": "empirical_association",
  "warrant_discount": 0.80,
  "claim_role": "indicator_claim",
  "credence": 0.83,
  "paper_id": "PDF-0001",
  "support_count": 0,
  "attack_count": 0,
  "qualifier": "underspecified",
  "warrant_status": "UNGROUNDED",
  "defeat_type": ""
}
```

**Warrant types and discount factors** (how much to trust each evidence type):
| Warrant Type | Discount Factor | Meaning |
|-------------|----------------|---------|
| constitutive | 1.00 | Definitional — inherently true |
| mechanism | 0.80 | Explains the causal pathway |
| empirical_association | 0.80 | Measured correlation |
| functional | 0.65 | Serves a purpose |
| capacity | 0.55 | Can produce the effect |
| analogical | 0.40 | Similar to another case |
| theory_derived | 0.25 | Predicted by theory, not observed |

## Existing Pages You'll Interact With

- **`ka_evidence.html`** — displays evidence cards; your component could live here or link from here
- **`ka_argumentation.html`** — displays argumentation details for a single claim; your component is a more visual alternative
- **`ka_warrants.html`** — reference page for warrant types

## Technical Environment

- The site is static HTML/CSS/JS (no build system, no React)
- D3.js is available via CDN: `https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js`
- Data payloads are loaded via `fetch()` from `data/ka_payloads/`
- Pages use a consistent style: cream background (#FAF6F0), Georgia headings, system-ui body text

## What To Do First

Before writing any code, ask the AI to explain what it thinks this task is about: what "mechanism pathway" means in this context, what the data structures look like, and what the hardest part will be. If the AI can't explain the task clearly, the implementation will fail.

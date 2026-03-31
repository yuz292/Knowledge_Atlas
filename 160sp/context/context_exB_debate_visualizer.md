# AI Context: Exercise B — Debate Cluster Visualizer

You are helping a student build a component for Knowledge Atlas (K-ATLAS), a scientific evidence system that tracks disagreements between competing theories.

## Your Task

Build an interactive visualization of one scientific debate. The system has 38 debate clusters — real scientific disagreements with claims on opposing sides connected by support and attack edges. Your component renders one cluster as a visual argument map.

## The Data You'll Work With

### File: `data/ka_payloads/argumentation.json`

**debate_clusters** (array, 38 entries):
```json
{
  "cluster_id": "C8",
  "paper_count": 9,
  "theory_count": 2,
  "papers": ["PDF-0285", "PDF-0355", "PDF-0537", ...],
  "theories": ["Attention Restoration Theory", "Stress Reduction Theory"]
}
```

**claim_nodes** (array, 1,900 entries) — the claims involved in debates:
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
    {
      "source": "PDF-0390_MPX_005",
      "target": "PDF-0844_MPX_007",
      "source_preview": "In the first two papers the focus was on...",
      "scheme_hint": "theoretical_rebuttal",
      "defeat_type": "REBUTTING",
      "strength": 0.63,
      "critical_question_hints": [
        "Does the proposed theoretical challenge explain the full target effect?",
        "Are there stronger alternative explanations still live?"
      ]
    }
  ],
  "top_supports": [
    { "source": "PDF-0331_MPX_003", "scheme_hint": "mechanistic_support", "strength": 0.75 }
  ]
}
```

**Key edge types you'll encounter:**

| scheme_hint | What It Means |
|------------|---------------|
| `mechanistic_support` | One claim explains the mechanism behind another |
| `empirical_support` | One claim provides measured evidence for another |
| `theoretical_rebuttal` | One claim challenges the theory behind another (REBUTTING defeat) |
| `methodological_undercut` | One claim questions the method, not the conclusion (UNDERCUTTING defeat) |

**Summary stats**: 1,900 claim nodes, 4,668 support edges, 142 attack edges, 38 debate clusters.

**Important**: The debate_clusters array gives you cluster membership (which papers and theories are in each debate), but the actual edges are in the claim_nodes' `top_attacks` and `top_supports` arrays. You'll need to cross-reference: find claim_nodes whose paper_id matches a cluster's papers list, then render their support/attack edges.

## Existing Pages

- **`ka_argumentation.html`** (~63 KB) — shows argumentation details for a single claim. Your component offers a cluster-level view instead.
- **`ka_evidence.html`** — evidence cards. A debate visualizer could link from here.

## Technical Environment

- Static HTML/CSS/JS (no build system)
- D3.js available via CDN: `https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js`
- Data loaded via `fetch('data/ka_payloads/argumentation.json')`
- Site style: cream background (#FAF6F0), Georgia headings, system-ui body text

## What To Do First

Before writing any code, ask the AI to explain what it thinks this task is about: what a "debate cluster" is in scientific argumentation, the difference between rebutting and undercutting defeat, and how to connect the debate_clusters data to the claim_nodes data. If the AI can't explain the task clearly, the implementation will fail.

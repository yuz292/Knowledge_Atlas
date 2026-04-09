# AI Context: Exercise C — Warrant Strength Calculator

You are helping a student build a component for Knowledge Atlas (K-ATLAS), a scientific evidence system with ~1,900 evidence claims, each with credibility metadata.

## Your Task

Build a function that takes one evidence claim and computes a transparent trust score from its components — then displays the calculation step by step, like a receipt showing exactly how each factor contributed. The point is not to produce a number (credence already does that) but to make the reasoning *visible*.

## The Data You'll Work With

### File: `data/ka_payloads/evidence.json`

Each evidence record has these fields (all inputs to your calculator):

```json
{
  "id": 1,
  "finding": "These sound sources increased reaction time...",
  "warrant_class": "empirical_association",
  "warrant_discount": 0.80,
  "credence": 0.83,
  "studyType": "Empirical Research",
  "signal": "Direct Measured Result",
  "claim_role": "indicator_claim",
  "support_count": 0,
  "attack_count": 0,
  "qualifier": "underspecified",
  "warrant_status": "UNGROUNDED",
  "defeat_type": ""
}
```

**The factors your calculator must combine:**

| Factor | Field | Range | What It Captures |
|--------|-------|-------|-----------------|
| Warrant strength | `warrant_discount` | 0.25–1.0 | How strong is this *type* of evidence? |
| Replication | `support_count` | 0–20+ | How many independent claims back this up? |
| Contestation | `attack_count` | 0–10+ | How many claims contradict it? |
| Study rigor | `studyType` | 4 values | Empirical Research > Review > Theoretical > Other |
| Signal directness | `signal` | 4 values | Direct Measured Result > Author Stated Conclusion > Discussion Level > Inferred |
| Defeat status | `defeat_type` | 4 values | Empty (no defeat) < undercutting < rebutting < BOTH |
| Overall status | `warrant_status` | 2 values | WARRANTED vs. UNGROUNDED |
| Stability | `qualifier` | 3 values | stable > supported_but_contested > underspecified |

**Warrant taxonomy** (the discount factors are central to this exercise):
| Warrant Type | Discount | Why |
|-------------|----------|-----|
| constitutive | 1.00 | Definitional truth — category membership |
| mechanism | 0.80 | Causal pathway identified |
| empirical_association | 0.80 | Measured statistical relationship |
| functional | 0.65 | Functional role established |
| capacity | 0.55 | Capability demonstrated |
| analogical | 0.40 | Argument by analogy |
| theory_derived | 0.25 | Deduced from theory, not measured |

## The Design Challenge

The `credence` field already gives a number. Your job is to *decompose* that number into visible factors. The output should look like a receipt:

```
Trust Score: 0.68
─────────────────────────────
  Warrant type (mechanism):        0.80  ← causal pathway evidence
  Replication (3 supporting):     +0.12  ← multiple independent confirmations
  Contestation (1 attack):        −0.08  ← one rebutting defeat recorded
  Study type (Empirical):         +0.05  ← controlled measurement
  Signal (Direct Measured):       +0.03  ← not inferred or speculative
  Defeat adjustment (rebutting):  −0.04  ← direct contradiction exists
─────────────────────────────
  Computed trust:                  0.68
```

Your panel (Step 1 of the method) will argue about the right formula. The key question is: should factors combine multiplicatively (like conditional probabilities) or additively (like weighted scoring)?

## Existing Pages

- **`ka_evidence.html`** — where evidence cards live. Your calculator's output could appear as a panel within each card.
- **`ka_warrants.html`** — reference page explaining warrant types.

## Technical Environment

- Static HTML/CSS/JS (no build system)
- **Data is loaded via fetch() using the full URL:**
  - `fetch('https://xrlab.ucsd.edu/ka/data/ka_payloads/evidence.json')`
- Site style: cream background (#FAF6F0), Georgia headings, system-ui body text
- Your output is a JavaScript function + an HTML renderer
- **Data loading strategy — choose one:**
  1. **Fetch from server** (works in AI preview environments and when running a local server): `fetch('https://xrlab.ucsd.edu/ka/data/ka_payloads/evidence.json')`
  2. **Embed sample data inline** (works everywhere, no server needed): Ask the AI to create a `const SAMPLE_DATA = [...]` variable with 20–30 representative records based on the schema above, then use that for development and testing. This avoids all cross-origin issues.
  3. **Local files** (if you downloaded the JSON): `fetch('data/ka_payloads/evidence.json')` — requires running `python3 -m http.server` in the parent directory

## What To Do First

Before writing any code, ask the AI to explain what it thinks this task is about: what "warrant discount" means, why the formula matters, and what would make a trust calculation misleading. If the AI can't explain the task clearly, the implementation will fail.

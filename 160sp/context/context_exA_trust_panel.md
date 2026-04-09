# AI Context: Exercise A — "Why Trust This?" Evidence Panel

You are helping a student build a component for Knowledge Atlas (K-ATLAS), a scientific evidence system with ~1,900 evidence claims, each tagged with credibility metadata.

## Your Task

Build a UI panel that appears next to any evidence claim and answers two questions: "Why should I trust this claim?" and "What could be wrong with it?" The panel must assemble a readable trust judgment from the data fields — not just display raw numbers.

## The Data You'll Work With

### File: `data/ka_payloads/evidence.json`

Each of the ~1,900 evidence records has these fields (all relevant to trust):

```json
{
  "id": 1,
  "finding": "These sound sources increased reaction time and reduced memory accuracy.",
  "construct": "Unknown",
  "signal": "Direct Measured Result",
  "studyType": "Empirical Research",
  "warrant": "Empirical Association",
  "warrant_class": "empirical_association",
  "warrant_discount": 0.80,
  "claim_role": "indicator_claim",
  "credence": 0.83,
  "citation": "The Influence of Indoor Acoustic Environments on...",
  "paper_id": "PDF-0001",
  "support_count": 0,
  "attack_count": 0,
  "qualifier": "underspecified",
  "warrant_status": "UNGROUNDED",
  "defeat_type": ""
}
```

**What each field means for trust:**

| Field | What It Tells You | Trust Implication |
|-------|------------------|-------------------|
| `credence` | Overall confidence (0–1) | Higher = more trusted, but this is the number you're *explaining*, not just showing |
| `warrant_class` | Type of evidence | Some types are inherently stronger (mechanism: 0.80) than others (analogical: 0.40) |
| `warrant_discount` | How much to trust this type (0.25–1.0) | Direct multiplier on credibility |
| `support_count` | How many claims back this one | More support = more resilient |
| `attack_count` | How many claims contradict it | Attacks reduce trust, especially if unresolved |
| `warrant_status` | WARRANTED or UNGROUNDED | UNGROUNDED means it lacks sufficient backing |
| `defeat_type` | rebutting / undercutting / BOTH / empty | Rebutting = directly contradicted; undercutting = evidence undermined |
| `qualifier` | stable / supported_but_contested / underspecified | Shows how settled the claim is |
| `studyType` | Empirical Research / Review Article / etc. | Some study types are more rigorous |
| `signal` | Direct Measured Result / Discussion Level Interpretation / etc. | How directly the claim was extracted from data |

**Warrant types and discount factors:**
| Warrant Type | Discount | Strength |
|-------------|----------|----------|
| constitutive | 1.00 | Definitional — inherently true |
| mechanism | 0.80 | Causal pathway explanation |
| empirical_association | 0.80 | Measured correlation |
| functional | 0.65 | Serves a purpose |
| capacity | 0.55 | Can produce the effect |
| analogical | 0.40 | Similar to another case |
| theory_derived | 0.25 | Predicted, not observed |

## Existing Page You'll Modify

- **`ka_evidence.html`** (~79 KB) — This is where evidence cards are displayed. Your trust panel will appear alongside or within these cards.
- The page loads evidence.json via `fetch('https://xrlab.ucsd.edu/ka/data/ka_payloads/evidence.json')` and renders cards dynamically.

## Technical Environment

- Static HTML/CSS/JS (no build system)
- **Data is loaded via fetch() using the full URL:**
  - `fetch('https://xrlab.ucsd.edu/ka/data/ka_payloads/evidence.json')`
- Pages use: cream background (#FAF6F0), Georgia headings, system-ui body text
- Evidence cards are rendered client-side from JSON
- Your component should work as a standalone HTML file that loads evidence.json, or as a panel injectable into ka_evidence.html
- **Data loading strategy — choose one:**
  1. **Fetch from server** (works in AI preview environments and when running a local server): `fetch('https://xrlab.ucsd.edu/ka/data/ka_payloads/evidence.json')`
  2. **Embed sample data inline** (works everywhere, no server needed): Ask the AI to create a `const SAMPLE_DATA = [...]` variable with 20–30 representative records based on the schema above, then use that for development and testing. This avoids all cross-origin issues.
  3. **Local files** (if you downloaded the JSON): `fetch('data/ka_payloads/evidence.json')` — requires running `python3 -m http.server` in the parent directory

## What To Do First

Before writing any code, ask the AI to explain what it thinks this task is about: what "trust" means in the context of scientific evidence, what the difference is between warrant_discount and credence, and why showing raw numbers is insufficient. If the AI can't explain the task clearly, the implementation will fail.

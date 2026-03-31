# AI Context: Exercise D — Evidence Search Filter

You are helping a student build a component for Knowledge Atlas (K-ATLAS), a scientific evidence system with ~1,900 evidence claims that currently have no search or filter interface.

## Your Task

Build a search and filter bar for the Evidence Explorer page. A user should be able to say "show me only mechanism claims about lighting with credence above 0.6 that haven't been defeated" and get a filtered list. The filter fields already exist in the data — but no UI exposes them.

## The Data You'll Work With

### File: `data/ka_payloads/evidence.json`

~1,900 evidence records. Each has these filterable fields:

```json
{
  "id": 1,
  "finding": "These sound sources increased reaction time and reduced memory accuracy.",
  "construct": "Unknown",
  "signal": "Direct Measured Result",
  "studyType": "Empirical Research",
  "warrant_class": "empirical_association",
  "warrant_discount": 0.80,
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

**Filter-relevant fields and their values:**

| Field | Type | Possible Values | What It Filters |
|-------|------|----------------|----------------|
| `warrant_class` | enum (7) | constitutive, mechanism, empirical_association, functional, capacity, analogical, theory_derived | Type of evidence |
| `credence` | float | 0.0–1.0 | Confidence level |
| `construct` | text | ~200 unique values (Lighting, Biophilia, Acoustics, Spatial, Color, Thermal, etc.) | Topic/domain |
| `qualifier` | enum (3) | stable, supported_but_contested, underspecified | How settled |
| `warrant_status` | enum (2) | WARRANTED, UNGROUNDED | Is it still standing? |
| `studyType` | enum (4) | Empirical Research, Review Article, Theoretical Paper, Policy/Opinion | Research type |
| `signal` | enum (4) | Direct Measured Result, Author Stated Conclusion, Discussion Level Interpretation, Inferred From Context | How directly extracted |
| `support_count` | int | 0–20+ | Number of supporting claims |
| `attack_count` | int | 0–10+ | Number of attacking claims |
| `finding` | text | Free text | Keyword search in claim text |

**Distribution notes** (so you know what to expect):
- ~65% of claims are empirical_association
- ~20% are mechanism
- ~45% are UNGROUNDED (no support edges)
- ~7% have attack_count > 0
- credence ranges from 0.15 to 0.95, median ~0.55

## Existing Page You'll Modify

- **`ka_evidence.html`** (~79 KB) — This is the Evidence Explorer. It currently shows all ~1,900 claims in a scrollable list with no filtering. Your filter bar sits at the top of this page and narrows what's displayed.
- The page loads `data/ka_payloads/evidence.json` via `fetch()` and renders cards dynamically.

## Technical Environment

- Static HTML/CSS/JS (no build system, no React)
- Data loaded via `fetch('data/ka_payloads/evidence.json')`
- Site style: cream background (#FAF6F0), Georgia headings, system-ui body text, cards with 1px #D8D0C5 borders and 10px border-radius
- Your filter should work client-side — all 1,900 records are loaded into memory

## Design Considerations

A filter bar with 10 dropdowns is overwhelming. Your panel (Step 1) will argue about which filters should be visible by default and which should be in an "Advanced" toggle. Think about:
- A practitioner (architect) wants: construct + credence range + warrant_status
- A philosopher wants: warrant_class + qualifier + defeat_type
- Both want: keyword search in the finding text

## What To Do First

Before writing any code, ask the AI to explain what it thinks this task is about: what the difference is between warrant_class and warrant_status, why a user would filter by qualifier, and what makes a search filter misleading (e.g., hiding the number of filtered-out results). If the AI can't explain the task clearly, the implementation will fail.

# Week 2: AI-Directed Programming Exercises

**COGS 160 · Spring 2026 · Week 2**

These are real engineering tasks on the Knowledge Atlas codebase. Each exercise uses Prof Kirsh's seven-step AI-directed development method. You are not expected to know the domain — the panel supplies the domain knowledge. Your job is to run the method correctly and produce working code.

---

## How Week 2 Works

**Tuesday (Day 3):** Prof Kirsh demos Exercise 0 live — the full seven-step cycle on a real task, start to finish. You watch the method in action: convene panel, write spec, implement with AI, verify, iterate when it fails.

**Thursday (Day 4):** You do one exercise yourself (assigned by team). Same method, different task. Submit: all prompts (including failures), the AI's output at each step, verification results, and a two-paragraph reflection.

---

## The Seven-Step Method (Quick Reference)

| Step | What You Do | What It Produces |
|------|------------|-----------------|
| 1. **Convene Panel** | Ask the AI to simulate 2–3 domain experts who argue about what the component should do | A list of requirements you wouldn't have thought of |
| 2. **Write Spec** | Define inputs, outputs, success conditions, edge cases | A testable contract |
| 3. **Define Acceptance Tests** | Write 3–5 concrete test cases before any code | Verification criteria |
| 4. **Implement** | Have the AI build it against the spec | Working code |
| 5. **Verify** | Run acceptance tests; check output against real data | Pass/fail on each test |
| 6. **Diagnose Failures** | When (not if) something fails, figure out why — was the spec wrong, or the implementation? | A correction |
| 7. **Iterate** | Fix and re-verify until all acceptance tests pass | Finished component |

**The rule:** You must complete steps 1–3 before touching step 4. If you skip the panel and spec, the AI will produce plausible-looking code that fails in ways you can't diagnose. That's Failure Mode #1 from the method lecture.

---

## Step 0: Initialize Your AI (Do This Before Everything Else)

Each exercise has a **context file** — a document that tells the AI what part of the Knowledge Atlas codebase this task involves, what the data looks like, and where the relevant files are. Without this, the AI is flying blind and will hallucinate data structures.

**The procedure:**

1. **Find your context file.** They are in `160sp/context/`:
   - Exercise 0 (Demo): `context_ex0_mechanism_pathway.md`
   - Exercise A: `context_exA_trust_panel.md`
   - Exercise B: `context_exB_debate_visualizer.md`
   - Exercise C: `context_exC_warrant_calculator.md`
   - Exercise D: `context_exD_search_filter.md`

2. **Paste the entire context file into your AI chat as the first message.** This is not optional. The context file contains the actual JSON schemas, field names, file paths, and data distributions your AI needs. Without it, the AI will guess — and guess wrong.

3. **Then ask the AI to explain the task back to you.** Say something like:
   > "Before we start building, explain what you think this task is about. What are the key data structures? What's the hardest part? What could go wrong?"

   If the AI's explanation doesn't match the context file, correct it before proceeding. An AI that misunderstands the data model will produce code that looks right but crashes on real data.

4. **Only then move to Step 1 (Convene Panel).**

**Why this matters:** The AI is your collaborator, not a vending machine. If you don't initialize it with the right context, every subsequent step — the panel discussion, the spec, the implementation — will be built on a misunderstanding. This is Failure Mode #2: correct method, wrong mental model.

---

## Exercise 0: Mechanism Pathway Tracer (DEMO — Prof Kirsh does this one)

**Track:** Theory/Mechanism (Track 4)
**Time:** ~40 minutes live
**Context file:** `160sp/context/context_ex0_mechanism_pathway.md`
**What it builds:** An interactive visualization — click an IV→DV pair (e.g., "natural light → task performance") and see the mechanistic pathway traced through intermediate nodes with confidence at each step.

### The Problem

Knowledge Atlas has ~1,900 evidence claims and ~4,810 edges connecting them (4,668 support edges, 142 attack edges). Among these, 34 are explicitly tagged as `mechanism_claim` — they describe *how* one thing causes another, not just *that* it does. But there's no way to visualize the chain. A researcher asking "how does natural light affect performance?" has to manually click through dozens of evidence cards. We need a component that traces the pathway automatically and shows confidence at each step.

### Step 1 — Convene Panel

**Prompt to AI:**

> You are running a design panel for a mechanism pathway visualization component. The panelists are:
>
> - **Judea Pearl** (causal inference): What makes a mechanism chain valid vs. merely plausible?
> - **Edward Tufte** (information design): How should confidence be encoded visually without clutter?
> - **A cognitive science graduate student** (target user): What would actually help me understand the pathway?
>
> The component takes an IV (independent variable) and DV (dependent variable) and displays the mechanistic chain connecting them, with confidence ratings per step. The data source is `argumentation.json` which has ~1,900 claim nodes with typed support/attack edges and strength scores (0–1).
>
> Each panelist: state your top 3 requirements for this component and one thing that would make it misleading or useless.

### Step 2 — Write Spec

After the panel argues, extract a spec. Example of what it should look like:

```
COMPONENT: MechanismPathwayTracer
INPUT: iv_term (string), dv_term (string)
OUTPUT: SVG/HTML showing directed graph from IV to DV

DATA SOURCE: argumentation.json
  - claim nodes with belief_id, content_preview, warrant_status
  - edges with source, target, scheme_hint, strength (0-1), defeat_type

REQUIREMENTS:
1. Find all mechanism_claim nodes whose content matches IV and DV terms
2. Trace shortest path from IV-related to DV-related claims via support edges
3. Display each intermediate node with: claim text (truncated), confidence, warrant type
4. Color edges by strength: green (>0.7), amber (0.4-0.7), red (<0.4)
5. Show attack edges as dashed red lines with defeat_type label
6. If no path exists, display "No mechanism chain found" with the closest partial path

EDGE CASES:
- Multiple paths exist → show the highest-confidence path, note alternatives
- Circular references → detect and break cycles
- IV or DV not found in data → suggest closest matches
```

### Step 3 — Define Acceptance Tests

```
TEST 1: Input "natural light", "task performance"
  EXPECT: A directed graph with ≥2 intermediate nodes
  VERIFY: Each node's content_preview mentions a plausible mechanism step

TEST 2: Input "noise", "stress"
  EXPECT: A pathway through at least one mechanism_claim
  VERIFY: Edge strengths match argumentation.json values exactly

TEST 3: Input "unicorns", "happiness"
  EXPECT: "No mechanism chain found" message
  VERIFY: No graph rendered, no crash

TEST 4: Visual verification
  EXPECT: High-strength edges visibly different from low-strength edges
  VERIFY: Screenshot comparison — can you tell which path is more confident?
```

### Steps 4–7 — Implementation, Verification, Iteration

This is where the live demo happens. The audience watches:
- The AI builds the D3.js visualization
- Prof Kirsh runs the acceptance tests
- Something fails (it always does — maybe the path-finding misses an intermediate node, or the color scale is wrong)
- The diagnosis: was the spec insufficient, or did the AI misinterpret it?
- The fix and re-verification

**What students should notice:** The spec did most of the intellectual work. The AI wrote the code in minutes. The debugging required going back to the spec, not staring at code.

---

## Exercise A: "Why Trust This?" Evidence Panel

**Track:** QA/Trust (Track 5)
**Assigned to:** Teams 1–2
**Time:** ~60–80 minutes
**Context file:** `160sp/context/context_exA_trust_panel.md`
**What it builds:** A UI panel that appears next to any evidence claim and answers: "Why should I trust this claim? What could be wrong with it?"

### The Problem

Every evidence card in `ka_evidence.html` shows a credence score (0–1) and a warrant type. But a student looking at "credence: 0.68, warrant: empirical_association" has no idea whether to trust it. Is 0.68 good? Is empirical association strong or weak evidence? How many studies support it? Has anything contradicted it? The numbers are there in the data but not assembled into a readable trust judgment.

### Your Data

From `evidence.json`, each claim has:

| Field | What it tells you | Example |
|-------|------------------|---------|
| `credence` | Overall confidence (0–1) | 0.68 |
| `warrant_class` | Type of evidence | empirical_association |
| `warrant_discount` | How much to trust this type (1.0 = best, 0.25 = weakest) | 0.80 |
| `support_count` | How many other claims back this one up | 3 |
| `attack_count` | How many other claims contradict it | 1 |
| `warrant_status` | Is it still standing? | WARRANTED / UNGROUNDED |
| `defeat_type` | If attacked, how? | rebutting / undercutting |
| `qualifier` | Stability | stable / supported_but_contested / underspecified |
| `studyType` | What kind of research | Empirical Research / Review Article |
| `signal` | How was the claim extracted? | Direct Measured Result / Discussion Level Interpretation |

### Step 1 — Convene Panel

**Prompt to AI:**

> You are running a design panel for a "Why Trust This?" evidence panel. The panelists are:
>
> - **Deborah Mayo** (philosophy of science, severe testing): When is evidence actually strong vs. merely present?
> - **A first-year graduate student** (target user): What would help me decide whether to cite this claim in my thesis?
> - **Ben Shneiderman** (information visualization): How do you present trust information without overwhelming the user?
>
> The panel will appear alongside evidence cards. It must answer two questions: "Why trust this?" and "What could be wrong?" using only the fields available in the data (listed above).
>
> Each panelist: state your top 3 requirements and one design mistake that would make the panel misleading.

### Step 2 — Write Spec

Your panel discussion will surface requirements. Turn them into a spec:

```
COMPONENT: TrustPanel
INPUT: One evidence claim object (from evidence.json)
OUTPUT: HTML panel with two sections

SECTION 1: "Why trust this?"
  - Trust tier (compute from the data fields — your panel will argue about how)
  - Plain-English sentence summarizing the evidence basis
  - Visual indicator of warrant strength (not just the number)

SECTION 2: "What could be wrong?"
  - List of specific vulnerabilities (e.g., "only 1 supporting study", "undercutting defeat recorded")
  - If attack_count > 0, show what the attack is about
  - If qualifier is "underspecified", flag this prominently

REQUIREMENTS:
  [Fill in from your panel discussion]

EDGE CASES:
  [Fill in — what happens with a claim that has no support AND no attacks?]
```

### Step 3 — Define Acceptance Tests

Write at least 4 tests. Here are two starters — you must add two more:

```
TEST 1: Claim with credence=0.83, support_count=5, attack_count=0, warrant_class=mechanism
  EXPECT: High trust tier, "What could be wrong?" section should still show something
  (Mayo would say: absence of attacks is not the same as severe testing)

TEST 2: Claim with credence=0.35, support_count=1, attack_count=2, qualifier=supported_but_contested
  EXPECT: Low trust tier with specific warnings about the attacks
  VERIFY: Panel doesn't just show red — it explains WHY the trust is low

TEST 3: [You write this — pick a real claim from evidence.json]

TEST 4: [You write this — an edge case]
```

### Steps 4–7: Implement, Verify, Iterate

Run the method. Submit everything.

---

## Exercise B: Debate Cluster Visualizer

**Track:** Theory/Mechanism (Track 4)
**Assigned to:** Teams 3–4
**Time:** ~60–80 minutes
**Context file:** `160sp/context/context_exB_debate_visualizer.md`
**What it builds:** A visual map of a scientific debate — two competing theories, the claims that support each, and the attack edges between them.

### The Problem

`argumentation.json` contains 38 debate clusters. Each cluster represents a real scientific disagreement — e.g., Attention Restoration Theory vs. Stress Reduction Theory, with 9 papers and multiple claims on each side with support/attack edges. This is extraordinary data, but there's no way to see it. A researcher has to read JSON to find out that claim X attacks claim Y with strength 0.63 via a "theoretical rebuttal." We need a component that renders one debate cluster as a visual argument map.

### Your Data

From `argumentation.json`, each debate cluster has:

```javascript
{
  "cluster_id": "C6",
  "paper_count": 9,
  "theories": ["Attention Restoration Theory", "Stress Reduction Theory"],
  // claim nodes with:
  "belief_id": "PDF-0844_MPX_007",
  "content_preview": "Viewing natural landscapes creates stronger positive health effects...",
  "incoming_support_count": 9,
  "incoming_attack_count": 5,
  "qualifier": "supported_but_contested",
  "top_attacks": [
    { "source": "PDF-0390_MPX_005", "scheme_hint": "theoretical_rebuttal",
      "defeat_type": "REBUTTING", "strength": 0.63 }
  ],
  "top_supports": [
    { "source": "PDF-0331_MPX_003", "scheme_hint": "mechanistic_support", "strength": 0.75 }
  ]
}
```

### Step 1 — Convene Panel

**Prompt to AI:**

> You are running a design panel for a scientific debate visualizer. The panelists are:
>
> - **Stephen Toulmin** (argumentation theory): What makes an argument map truthful vs. decorative?
> - **Mike Bostock** (D3.js creator): What graph layout makes support/attack structure readable at 20–50 nodes?
> - **An undergraduate who has never seen an argument map** (target user): What would help me understand which side is winning and why?
>
> The component renders one debate cluster: two competing theories, the claims on each side, and the support/attack edges between them. Data includes edge strength (0–1), defeat type (rebutting/undercutting), and scheme hints (mechanistic_support, theoretical_rebuttal, methodological_undercut).
>
> Each panelist: state your top 3 requirements and one thing that would make the visualization misleading.

### Step 2 — Write Spec

```
COMPONENT: DebateClusterMap
INPUT: cluster_id (string, e.g. "C6")
OUTPUT: Interactive SVG showing the debate structure

REQUIREMENTS:
1. Two-column layout: Theory A claims on left, Theory B claims on right
2. Support edges within a theory shown as [your panel's recommendation]
3. Attack edges between theories shown as [your panel's recommendation]
4. Edge thickness or color encodes strength (0-1)
5. Clicking a node shows: full claim text, paper citation, warrant status
6. Overall "balance" indicator: which theory has more surviving (undefeated) support?

EDGE CASES:
  [Fill in from panel — what if one side has 15 claims and the other has 2?]
```

### Step 3 — Acceptance Tests, then Steps 4–7

[Same structure as Exercise A — write 4 tests, implement, verify, iterate]

---

## Exercise C: Warrant Strength Calculator

**Track:** QA/Trust (Track 5)
**Assigned to:** Teams 5–6
**Time:** ~60–80 minutes
**Context file:** `160sp/context/context_exC_warrant_calculator.md`
**What it builds:** A function that takes a claim and computes a transparent trust score by combining warrant discount, support/attack ratio, study type, and signal quality — then displays the calculation step by step so a user can see exactly why the score is what it is.

### The Problem

The `credence` field in evidence.json is a single number (e.g., 0.68). Nobody knows how it was computed. The underlying components exist — warrant_discount (0.25–1.0), support_count, attack_count, studyType, signal — but they aren't combined transparently. We need a function that recomputes trust from first principles and shows its work, like a math proof where every step is visible.

### Your Data

Same as Exercise A, but here you're computing, not displaying.

### Step 1 — Convene Panel

**Prompt to AI:**

> You are running a design panel for a transparent trust score calculator. The panelists are:
>
> - **Wolfgang Spohn** (ranking theory): How should warrant discount and support/attack counts combine mathematically? What's the right aggregation — multiplicative, additive, or something else?
> - **Susan Haack** (foundherentism): When is a claim well-grounded vs. merely coherent? What's the difference and how should the score reflect it?
> - **A data scientist** (implementation perspective): What's the simplest formula that captures the key distinctions without overfitting to noise?
>
> The calculator takes one evidence claim object and produces a trust score (0–1) with a step-by-step breakdown showing exactly how each factor contributed. The available fields are: warrant_discount, support_count, attack_count, studyType, signal, warrant_status, defeat_type, qualifier.
>
> Each panelist: propose a formula, justify it, and identify when it would give a misleading result.

### Step 2 — Write Spec

```
COMPONENT: TransparentTrustCalculator
INPUT: One evidence claim object
OUTPUT: {
  trust_score: number (0-1),
  breakdown: [
    { factor: "warrant_type", value: 0.80, explanation: "Empirical association: moderate discount" },
    { factor: "replication", value: ..., explanation: "..." },
    { factor: "contestation", value: ..., explanation: "..." },
    ...
  ],
  html: rendered HTML showing the calculation like a receipt
}

REQUIREMENTS:
1. Every factor must have a plain-English explanation
2. The breakdown must multiply/combine to produce the final score (no hidden steps)
3. The HTML output shows the calculation as a vertical "receipt" — factor, contribution, running total
4. If a claim is UNGROUNDED, the receipt must show WHY (which factor drove it to zero)

EDGE CASES:
  [What if support_count=0 and attack_count=0? What does "no evidence either way" mean for trust?]
```

### Step 3–7 — Tests, Implement, Verify, Iterate

---

## Exercise D: Evidence Search Filter

**Track:** Evidence Explorer (Track 1)
**Assigned to:** Teams 7–8
**Time:** ~60–80 minutes
**Context file:** `160sp/context/context_exD_search_filter.md`
**What it builds:** A search/filter bar for the Evidence Explorer that lets users narrow 1,900 claims by domain, warrant type, credence range, and whether the claim is contested.

### The Problem

`ka_evidence.html` currently shows all ~1,900 claims in a scrollable list. There's no way to say "show me only mechanism claims about lighting with credence above 0.6 that haven't been defeated." The data fields for filtering exist — `warrant_class`, `credence`, `construct`, `qualifier`, `warrant_status` — but no UI exposes them.

### Step 1 — Convene Panel

**Prompt to AI:**

> You are running a design panel for a search and filter bar on the Evidence Explorer page. The panelists are:
>
> - **Jakob Nielsen** (usability): What are the most common filtering mistakes in search interfaces? Which filters should be visible by default vs. hidden in "advanced"?
> - **A practitioner (architect)** trying to answer: "What does the evidence say about biophilic design and stress reduction?" They need to find relevant claims quickly and assess their quality.
> - **A philosophy of science student** trying to find: "All contested claims with undercutting defeaters." They need precise epistemic filtering.
>
> The data has ~1,900 claims. Available filter fields: warrant_class (7 types), credence (0-1), construct (text), qualifier (3 values), warrant_status (2 values), studyType (4 values), signal (4 values), support_count and attack_count (integers).
>
> Each panelist: which 3 filters matter most for your use case? What filter would be misleading or useless?

### Step 2 — Write Spec

[Same structure — define the component, its inputs/outputs, requirements, edge cases]

### Step 3–7 — Tests, Implement, Verify, Iterate

---

## What You Submit

For each exercise, upload a single document containing:

1. **Your panel transcript** — the full AI conversation from Step 1
2. **Your spec** — the document from Step 2 (including acceptance tests from Step 3)
3. **All prompts** — everything you sent to the AI during implementation, including failures
4. **The AI's output** — code, errors, corrections
5. **Verification results** — which tests passed, which failed, what you did about failures
6. **Two-paragraph reflection:**
   - Paragraph 1: Where did the panel surface a requirement you wouldn't have thought of?
   - Paragraph 2: Where did the AI produce something that looked right but failed a test? How did you diagnose it?

---

## Grading Rubric

| Component | Weight | What we're looking for |
|-----------|--------|----------------------|
| Panel quality | 25% | Did you get a real argument between panelists, or just a list of features? |
| Spec completeness | 25% | Are inputs, outputs, edge cases, and success conditions all defined before implementation? |
| Verification rigor | 25% | Did you actually run the tests? Did you catch failures? Did you fix them? |
| Reflection honesty | 25% | Did you identify a real surprise and a real failure, or did you write generic praise? |

**Note:** We do not grade on whether the final code is perfect. We grade on whether you followed the method. A component that fails one test but has a clear diagnosis of why is worth more than a component that "works" but was never tested.

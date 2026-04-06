# Knowledge Atlas: User-Type Home Pages and Journey Architecture

**Date**: 2026-04-03
**Author**: David Kirsh / Claude
**Status**: Design Sketch — for review before implementation

---

## 1. Current State: What Exists Now

The site currently has a single public home page (`ka_home.html`) with a mode-pill switcher that adapts the primary CTA and nav order based on 6 user types. After login, all users land on `ka_user_home.html`, which shows role-specific workflow cards. This is flat: everyone enters through the same funnel, and the differentiation is limited to which workflow cards appear. There is no distinct intellectual framing per user type — no governing question, no curated "Of Potential Interest" sidebar, no topic checklist, no customized orientation.

### Current Journey Counts per User Type

| User Type | Defined Workflows | Mapped Journeys | Complete | Broken |
|-----------|------------------|-----------------|----------|--------|
| Student Explorer | 2 | 3 | 1 | 2 |
| Researcher | 4 | 2 | 0 | 2 |
| Contributor | 3 | 2 | 0 | 2 |
| Instructor | 1 | 2 | 1 | 1 |
| Practitioner | 3 | 0 | 0 | 0 |
| Theory Explorer | 2 | 0 | 0 | 0 |

**The practitioner and theory explorer have no implemented journeys at all** — they exist only as mode-pill labels and workflow definitions in `ka_workflows.js`.

---

## 2. The Six User Types: Governing Questions and Primary Concerns

### 2.1 STUDENT EXPLORER

**Governing Question**: *What does the evidence actually say about how environments affect people, and where are the gaps in what we know?*

**Primary Concerns** (documented in workflows, audit, and site copy):
- Orientation: "Where do I even start? What does this system contain?"
- Literacy: "How do I read evidence claims critically rather than accepting them?"
- Navigation: "How does the topic hierarchy work? What's a research front?"
- Quality: "Which findings are robust and which are tentative?"
- Purpose: "What am I supposed to do with this knowledge? What's A0?"

**Journey Choices**: 3 current (first-time entry, explore topics, hypothesis building), should expand to 4 with "course assignment" as primary directed journey.

---

### 2.2 RESEARCHER

**Governing Question**: *What does the cumulative evidence say about my hypothesis, and where are the genuine targets of opportunity for new work?*

**Primary Concerns**:
- Hypothesis testing: "Does the evidence support or challenge my theoretical prediction?"
- Gaps and contradictions: "Where are the holes? Where do studies conflict?"
- Mechanism: "What neural, cognitive, or behavioral mechanisms explain these effects?"
- Population specificity: "For whom does this hold? Where are the cultural/demographic boundaries?"
- Methodological quality: "How strong is this evidence? What are the warrant types?"
- VOI (Value of Information): "What experiment would most reduce uncertainty in this domain?"

**Journey Choices**: 4 defined workflows (hypothesis-test, lit-synthesis, evidence-pipeline, deep-dive), but the entry points are poorly differentiated. The researcher needs a home page that immediately surfaces the key intellectual affordances: neural underpinnings, population differences, theoretical diversity, and VOI maps.

---

### 2.3 CONTRIBUTOR

**Governing Question**: *How do I find, validate, and submit articles that the Atlas can actually use — and how does my contribution fit into the larger system?*

**Primary Concerns**:
- Track clarity: "Which of the 4 tracks am I on, and what exactly am I supposed to deliver?"
- Article pipeline: "How do I find experimental articles, upload them, and know they're accepted?"
- Quality gates: "What makes an article 'good enough' for the corpus?"
- Progress: "How many articles have I submitted? How many count?"
- Integration: "How does my tagged claim connect to the broader web of belief?"

**Journey Choices**: 2 mapped journeys (propose-and-submit, course track), but the course track journey is broken at 2 steps. The contributor home page should center the production workflow and surface their track assignment prominently.

---

### 2.4 INSTRUCTOR

**Governing Question**: *Are students on track, is the pipeline producing valid contributions, and where do I need to intervene?*

**Primary Concerns**:
- Enrollment health: "Who's registered? Who hasn't started?"
- Submission flow: "Are articles coming in? Are they experimental? Are they on-topic?"
- Track management: "How are the 4 tracks performing? Any bottlenecks?"
- Quality assurance: "Which submissions need review? Which have been auto-classified incorrectly?"
- Course logistics: "Schedule, prep checklist, student communications"

**Journey Choices**: 2 mapped (review-approve, manage-setup), but setup journey is broken. The instructor home page should be a dashboard with submission metrics, pending reviews, and enrollment status.

---

### 2.5 PRACTITIONER

**Governing Question**: *What does the science say I should actually do when designing this space for these people?*

**Primary Concerns**:
- Actionability: "Give me specific, usable guidance — not theory abstractions"
- Context specificity: "This is a hospital waiting room / classroom / office — what matters here?"
- Confidence: "How confident should I be in this recommendation?"
- Trade-offs: "If I optimize for attention restoration, what do I sacrifice in wayfinding?"
- Communication: "How do I justify this design choice to a client with evidence?"

**Journey Choices**: 3 defined workflows (design-decision, client-brief, deep-dive) but none implemented. The practitioner home page should present topics organized by **space type** and **design decision** rather than by academic taxonomy.

---

### 2.6 THEORY / MECHANISM EXPLORER

**Governing Question**: *How do the competing theoretical accounts explain these effects, and what experiment would distinguish between them?*

**Primary Concerns**:
- Theory comparison: "Attention Restoration Theory vs. Stress Recovery Theory — what separates them empirically?"
- Mechanism chains: "What is the neural pathway from environmental stimulus to behavioral outcome?"
- Critical tests: "What experiment would genuinely differentiate these accounts?"
- Underdetermination: "Are multiple theories equally consistent with the data?"
- Formal structure: "How does the warrant system represent theoretical commitments?"

**Journey Choices**: 2 defined workflows (mechanism-trace, hypothesis-test) but none implemented. The theory explorer home page should foreground the 10 neural frameworks, theory comparison matrices, and mechanism chain visualizations.

---

## 3. Proposed Architecture: Distinct Home Pages

### 3.1 Design Principle

When a user selects their type (from the public home page, from the mode switcher, or from their profile), they arrive at a **type-specific home page** that:

1. States the **governing question** prominently in the hero
2. Shows a **topic checklist** (checkboxes for 19 research fronts, organized by domain family)
3. Presents **"Of Potential Interest" cards** — curated examples of the kind of content this user type cares about
4. Offers **2–4 journey entry points** as distinct CTAs, each framed as a question
5. Includes a **"What's New" feed** filtered by relevance to this user type

### 3.2 Common Elements Across All Type Home Pages

**Topic Checklist Panel** (sidebar or top):
- 19 research fronts grouped into 5 domain families:
  - **Nature & Biophilia** (7 fronts): Stress Response, Restoration, Wellbeing (3 variants), Mechanism, Biophilic Design
  - **Luminous Environment** (4 fronts): Circadian × Wellbeing, Circadian × Physiology, Circadian × Cognition, Circadian × Mechanism
  - **Acoustic Environment** (3 fronts): Soundscape Perception, Physiological Response, Mechanism
  - **Spatial Form** (3 fronts): Neuroaesthetics, Spatial Navigation, Stress Physiology
  - **Material & Surface** (1 front): Biophilic × Physiology
- Users check topics they're interested in; the rest of the page adapts
- Checked topics persist across sessions (localStorage)

**"Of Potential Interest" Card Types**:
- **Topic Card**: Name, article count, what's new, sub-topic breakdown
- **VOI Card**: High-value-of-information question, current uncertainty, potential impact
- **Neural Card**: Mechanism chain summary, relevant frameworks, grounding score
- **Theory Card**: Competing accounts, evidence balance, critical test needed
- **Article Card**: Recent experimental finding, warrant type, confidence level
- **Gap Card**: Under-studied intersection, potential contribution opportunity

---

## 4. Type-Specific Home Page Designs

### 4.1 STUDENT EXPLORER HOME — `ka_home_student.html`

**Hero**: *"What does the evidence actually say about how environments affect people?"*
**Subtitle**: Start by exploring what's known, what's tentative, and what's genuinely unknown.

**Section 1: Your Orientation Checklist**
- ☐ Read the AI Methodology guide (required)
- ☐ Browse 3 "Did You Know" findings
- ☐ Open the Topic Hierarchy and identify 2 topics that interest you
- ☐ Complete A0 (upload 10 experimental articles)

**Section 2: "Of Potential Interest" Cards** (4 cards):
- **Did You Know** card: A rotating surprising finding with "Why this matters" annotation
- **Topic Spotlight** card: One well-studied topic with article count and key claim
- **Gap Alert** card: An under-studied area where student contributions would have high impact
- **New This Week** card: Recently added articles or claims

**Section 3: Journey Choices** (framed as questions):

| Journey | Question | CTA |
|---------|----------|-----|
| First Questions | "What does Atlas know, and how does it know it?" | Explore the Atlas → |
| A0 Assignment | "Can I find 10 experimental articles on my assigned topic?" | Start A0 → |
| Hypothesis Building | "Can I turn a finding into a testable question?" | Build a Hypothesis → |
| Deep Dive | "How deep does the evidence go on one claim?" | Follow One Claim → |

---

### 4.2 RESEARCHER HOME — `ka_home_researcher.html`

**Hero**: *"Test your hypotheses against the evidence the field has actually produced."*
**Subtitle**: Neural underpinnings, population boundaries, theoretical diversity, and targets of opportunity.

**Section 1: Topic Checklist** (with checkboxes) — selecting topics filters everything below

**Section 2: "Of Potential Interest" Cards** (6 cards, filtered by checked topics):
- **Neural Underpinnings** card: Top mechanism chain for checked topics. E.g., "Nature exposure → amygdala downregulation → cortisol reduction: 3 supporting studies, CCI = 0.72"
- **Population & Cultural Differences** card: Known moderators — "Light-cognition effects studied in 4 countries; age moderation reported in 2 studies; no data on neurodivergent populations"
- **Relevant Theories** card: Competing accounts for the checked topic. "ART vs. SRT: 12 studies consistent with both; 3 studies discriminate"
- **Targets of Opportunity** card: Highest-VOI questions. "VOI = 0.83: Does circadian disruption moderate the nature–stress restoration pathway?"
- **VOI Map** card: Visual heat map of information value across the checked topic cluster
- **Recent Experimental Findings** card: 3 newest experimental articles in checked topics

**Section 3: Journey Choices** (framed as questions):

| Journey | Question | CTA |
|---------|----------|-----|
| Hypothesis Test | "Does the evidence support my prediction?" | Test a Hypothesis → |
| Literature Synthesis | "What's the state of evidence in this domain?" | Map the Evidence → |
| Evidence Pipeline | "Can I contribute a validated article to the corpus?" | Submit Evidence → |
| Deep Dive | "How does one claim survive scrutiny?" | Trace a Claim → |

**Section 4: Quick Access**
- Article Search (filtered to checked topics)
- Evidence Browser
- Warrant Inspector
- Neuro Perspective

---

### 4.3 CONTRIBUTOR HOME — `ka_home_contributor.html`

**Hero**: *"Build the evidence base one verified claim at a time."*
**Subtitle**: Your track, your progress, your next task.

**Section 1: My Track & Progress** (personalized):
- Current track assignment (Track 1–4) with progress bar
- Articles submitted / target (e.g., "7/10 experimental articles accepted")
- Next deliverable with deadline
- Quick link: Upload Articles →

**Section 2: Topic Checklist** — relevant to assigned question

**Section 3: "Of Potential Interest" Cards** (4 cards):
- **My Question** card: Assigned research question, current article count, gaps remaining
- **High-Impact Contributions Needed** card: Topics where the corpus is thinnest
- **Recent Accepts** card: Articles recently accepted into the corpus (models of what "good" looks like)
- **Track Peers** card: What others on your track have submitted (anonymized counts)

**Section 4: Journey Choices**:

| Journey | Question | CTA |
|---------|----------|-----|
| Upload Articles | "Do I have 10 experimental articles ready?" | Upload Now → |
| Find Articles | "Where do I find good experimental papers?" | Search Literature → |
| Tag Claims | "Can I identify and tag the key claims in an article?" | Start Tagging → |
| Understand Quality | "What makes an article good enough for Atlas?" | Read Evidence Standards → |

---

### 4.4 INSTRUCTOR HOME — `ka_home_instructor.html`

**Hero**: *"Are students on track, and is the pipeline producing valid contributions?"*
**Subtitle**: Enrollment, submissions, track health, and intervention points.

**Section 1: Dashboard Metrics** (real-time):
- Total registered / approved / active students
- Articles submitted this week / total
- Classification breakdown (experimental / review / theory / unknown)
- Pending reviews count

**Section 2: "Of Potential Interest" Cards** (4 cards):
- **Needs Review** card: Articles awaiting instructor classification review, sorted by submission date
- **Student Alerts** card: Students who haven't submitted in >7 days, or whose submissions are mostly non-experimental
- **Track Health** card: Per-track submission rates and bottlenecks
- **Schedule** card: This week's milestones and upcoming deadlines

**Section 3: Journey Choices**:

| Journey | Question | CTA |
|---------|----------|-----|
| Review Submissions | "Which articles need my attention?" | Open Review Queue → |
| Student Progress | "Who's behind, and why?" | View Student Dashboard → |
| Course Setup | "Is everything configured for this week?" | Check Setup → |
| Onboarding | "Are new registrations processed?" | Manage Registrations → |

---

### 4.5 PRACTITIONER HOME — `ka_home_practitioner.html`

**Hero**: *"Evidence-grounded design requires knowing what the science actually shows."*
**Subtitle**: From space type to specific recommendation, with confidence levels.

**Section 1: Topic Checklist** — organized by **space type** rather than academic taxonomy:
- ☐ Office / Workplace
- ☐ Healthcare / Hospital
- ☐ Educational / Classroom
- ☐ Residential / Home
- ☐ Public / Civic
- ☐ Retail / Commercial
- ☐ Outdoor / Landscape

**Section 2: "Of Potential Interest" Cards** (5 cards):
- **Design Decision** card: "Choosing between daylight strategies for an open-plan office? Here's what the circadian evidence says." Confidence level, caveats, specific recommendation.
- **Trade-Off Alert** card: "Maximizing acoustic privacy may reduce biophilic exposure. Evidence on the trade-off: 4 studies, moderate confidence."
- **Client-Ready Evidence** card: A pre-formatted evidence summary suitable for a client presentation. Topic, claim, confidence, source count.
- **Space Type Spotlight** card: Evidence summary for the checked space type — what factors matter most, ranked by effect size.
- **Practice Note** card: A short, actionable design guideline derived from the evidence. "For attention restoration in waiting rooms: minimum 15% visible greenery, natural light from east or south, ambient noise below 45 dB."

**Section 3: Journey Choices**:

| Journey | Question | CTA |
|---------|----------|-----|
| Design Decision | "What does the evidence say about this specific choice?" | Evaluate a Decision → |
| Client Brief | "How do I justify this design to a client?" | Build Evidence Cards → |
| Deep Dive | "How strong is the evidence behind this recommendation?" | Trace the Evidence → |

---

### 4.6 THEORY EXPLORER HOME — `ka_home_theory.html`

**Hero**: *"Understand mechanism, not only outcome."*
**Subtitle**: Competing theories, neural pathways, critical tests, and warrant structure.

**Section 1: Topic Checklist** — with theory overlay:
- Each topic shows which theories apply (ART, SRT, PP, SN, etc.)
- Checking a topic highlights relevant mechanism chains

**Section 2: "Of Potential Interest" Cards** (6 cards):
- **Neural Frameworks** card: The 10 Tier-1 frameworks (PP, SN, DP, DT, NM, IC, MS, EC, CB, MSI) with article counts and grounding scores
- **Theory Comparison** card: "ART vs. SRT on nature restoration: evidence balance, discriminating predictions, and the experiment that would settle it"
- **Mechanism Chain** card: Visual chain from environmental feature → neural substrate → cognitive effect → behavioral outcome. E.g., "Daylight → ipRGC → SCN → cortisol rhythm → sustained attention"
- **Critical Test** card: "The highest-priority experiment that would discriminate between competing accounts in this domain"
- **Warrant Structure** card: How the 7 warrant types (constitutive through theory-derived) distribute across checked topics
- **Underdetermination Alert** card: Cases where multiple theories are equally consistent with the data — the intellectually honest "we don't know yet"

**Section 3: Journey Choices**:

| Journey | Question | CTA |
|---------|----------|-----|
| Mechanism Trace | "What's the neural pathway from stimulus to outcome?" | Trace a Mechanism → |
| Hypothesis Test | "Does the evidence favor this theory over its rival?" | Test a Theory → |
| Deep Dive | "How does one claim survive scrutiny at the mechanism level?" | Inspect One Claim → |

---

## 5. The Journey Question: What Is the Right Sequence for a Research Question?

When a user arrives with a question — whether it's a student exploring a topic, a researcher testing a hypothesis, or a practitioner looking for design guidance — the journey should follow a consistent but role-adapted sequence.

### 5.1 The Universal Journey Template

Every research question generates a journey through these stages:

**Stage 1: ORIENT** — "What do we know about this?"
- Topic page with article counts, sub-topic breakdown, what's new
- "Of Potential Interest" cards: related topics, adjacent findings, key researchers
- **Follow-on page**: Dynamically generated list of relevant articles

**Stage 2: INSPECT** — "How strong is this evidence?"
- Evidence browser filtered to the question's topic
- Warrant types visible per claim
- Confidence levels and replication status
- "Of Potential Interest" cards: VOI opportunities, gaps, conflicting findings

**Stage 3: EXPLAIN** — "Why does this happen?"
- Neural underpinning panel (mechanism chains, grounding scores)
- Theory comparison (which accounts are consistent, which discriminate)
- "Of Potential Interest" cards: related mechanisms, analogous pathways, critical tests

**Stage 4: EVALUATE** — "How much should I trust this?"
- Argumentation structure (support/attack clusters)
- Annotation layer (replication notes, calibration flags)
- Interpretation layer (active-boundary beliefs, honest uncertainty)
- "Of Potential Interest" cards: open questions, areas of genuine disagreement

**Stage 5: ACT** — "What should I do with this?"
- *Researcher*: Write a research question, identify the highest-VOI experiment
- *Student*: Complete assignment, submit articles
- *Practitioner*: Generate design guidance, build client-ready evidence cards
- *Theory Explorer*: Identify the critical test, map the mechanism frontier

### 5.2 "Of Potential Interest" Cards on Follow-On Pages

Every page after the type-specific home page should include an "Of Potential Interest" sidebar or footer section. The cards shown depend on (a) the user type, (b) the checked topics, and (c) the current page context.

**Card selection logic**:

| Current Page | Card Types Shown |
|-------------|-----------------|
| Topic page | Related topics, VOI, Neural underpinnings, Recent articles |
| Evidence page | Warrant breakdown, Conflicting findings, Replication status, Theory relevance |
| Article list | Similar articles, Gap alerts, Methodology notes, Mechanism connections |
| Neuro perspective | Theory comparison, Critical tests, Population differences, Related mechanisms |
| Warrant inspector | Theory links, Evidence density per warrant type, Underdetermination cases |

### 5.3 Dynamically Generated Article Pages

When a user clicks through from a topic or interest card, the next page should be a **dynamically generated article list** filtered by:
- Topic (from checked topics or clicked topic card)
- Article type (experimental, review, theory — user can filter)
- Recency (newest first, with date indicators)
- Relevance score (if available from the pipeline)

Each article entry shows: title, authors, year, article type badge, abstract snippet, warrant types used, and whether it has a mechanism chain annotation.

---

## 6. Implementation Priority

### Phase 1 (Immediate — This Sprint)
1. Create `ka_home_student.html` — the most active user group
2. Create `ka_home_researcher.html` — the most intellectually demanding
3. Wire the mode-pill selection to redirect to type-specific home pages instead of adapting a single page

### Phase 2 (Next Sprint)
4. Create `ka_home_contributor.html` — personalized with track/progress
5. Create `ka_home_instructor.html` — dashboard-centric
6. Implement "Of Potential Interest" card component (reusable across all pages)

### Phase 3 (Following Sprint)
7. Create `ka_home_practitioner.html` — space-type oriented
8. Create `ka_home_theory.html` — mechanism and theory focused
9. Implement dynamic article list generation from topic selection
10. Add topic checklist persistence and cross-page filtering

---

## 7. Summary Table

| User Type | Governing Question | Home Page | Journey Count | Card Types |
|-----------|-------------------|-----------|---------------|------------|
| Student Explorer | What does the evidence say, and where are the gaps? | `ka_home_student.html` | 4 | Did You Know, Topic, Gap, New |
| Researcher | Does the evidence support my hypothesis? | `ka_home_researcher.html` | 4 | Neural, Population, Theory, VOI, Map, Recent |
| Contributor | How do I submit articles the Atlas can use? | `ka_home_contributor.html` | 4 | My Question, High-Impact, Recent Accepts, Peers |
| Instructor | Are students on track and producing valid work? | `ka_home_instructor.html` | 4 | Needs Review, Alerts, Track Health, Schedule |
| Practitioner | What should I do when designing this space? | `ka_home_practitioner.html` | 3 | Decision, Trade-Off, Client-Ready, Space, Practice |
| Theory Explorer | How do competing theories explain these effects? | `ka_home_theory.html` | 3 | Frameworks, Comparison, Chain, Critical Test, Warrant, Underdetermination |

---

## Appendix A: The 19 Research Fronts (Current Corpus)

**Nature & Biophilia** (7 fronts):
1. Nature & Biophilia × Stress Response (Attention)
2. Nature & Biophilia × Restoration / Recovery (Attention)
3. Nature & Biophilia × Stress Response (Biophilia)
4. Nature & Biophilia × Stress Response (Biophilic)
5. Nature & Biophilia × Wellbeing (Evidence-Based)
6. Nature & Biophilia × Mechanism / Pathway (Biophilia)
7. Nature & Biophilia × Wellbeing (Biophilic)

**Luminous Environment** (4 fronts):
8. Luminous Environment × Wellbeing (Circadian)
9. Luminous Environment × Physiological Response (Circadian)
10. Luminous Environment × Cognitive Performance (Circadian)
11. Luminous Environment × Mechanism / Pathway (Circadian)

**Acoustic Environment** (3 fronts):
12. Acoustic Environment × Soundscape Perception (Soundscape)
13. Acoustic Environment × Physiological Response (Soundscape)
14. Acoustic Environment × Mechanism / Pathway (Soundscape)

**Spatial Form** (3 fronts):
15. Spatial Form × Aesthetic Preference (Neuroaesthetics)
16. Spatial Form × Spatial Navigation (Spatial)
17. Spatial Form × Physiological Response (Stress)

**Material & Surface** (1 front):
18. Material & Surface × Physiological Response (Biophilic)

**Cross-cutting**:
19. Nature & Biophilia × Wellbeing (Biophilia) [overlaps with front 6]

## Appendix B: The 10 Tier-1 Neural Frameworks

| Code | Framework | Core Mechanism |
|------|-----------|---------------|
| PP | Predictive Processing | Surprise minimization, prediction error |
| SN | Salience Network | Attentional capture, threat detection |
| DP | Dopaminergic Pathways | Reward, motivation, exploratory behavior |
| DT | Default Mode / Task-Positive Toggle | Mind-wandering vs. focused attention |
| NM | Neuromodulation | Serotonin, norepinephrine, cortisol regulation |
| IC | Interoceptive–Cortical Coupling | Body-state awareness, embodied cognition |
| MS | Multisensory Integration | Cross-modal binding, environmental coherence |
| EC | Entorhinal–Hippocampal Complex | Spatial memory, place cells, cognitive maps |
| CB | Cerebellar Timing | Motor prediction, temporal processing |
| MSI | Mirror System / Social Cognition | Imitation, social affordance detection |

## Appendix C: The 7 Bridge Warrant Types

| Type | Default d | Epistemic Role |
|------|----------|---------------|
| Constitutive | 1.00 | Definitional identity |
| Mechanism | 0.80 | Causal pathway evidence |
| Empirical Association | 0.80 | Statistical regularity |
| Functional | 0.65 | Role/capacity argument |
| Capacity | 0.55 | Potential-based inference |
| Analogical | 0.40 | Cross-domain similarity |
| Theory-Derived | 0.25 | Theoretical prediction only |

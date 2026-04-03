# Panel-to-Development Handoff: Theory Explorer Design

**Date**: 2026-04-03
**Status**: READY FOR DEVELOPMENT TEAM
**Decision Required**: Design approval before Phase 1 begins

---

## What Was Done: Three-Document Panel Review

### Document 1: Expert Panel Report
**File**: `EXPERT_PANEL_THEORY_EXPLORER_DESIGN_2026-04-03.md`
**Length**: ~8,000 words
**Audience**: Stakeholders, decision-makers, documentation
**Content**:
- 5 panelists' detailed positions on mechanism representation, theory comparison, critical tests
- Panel consensus and productive disagreements
- Integrated design recommendations for all 6 cards
- New supporting pages (mechanism gallery, interventionist prediction maps, coherence-learning tool)

### Document 2: Implementation Guide
**File**: `IMPLEMENTATION_GUIDE_THEORY_EXPLORER_2026-04-03.md`
**Length**: ~6,500 words
**Audience**: Development team, product manager
**Content**:
- Card-by-card technical specifications
- Data model schemas (JSON)
- Frontend component code templates (React/TypeScript)
- Effort estimates (10–12 weeks total)
- Success metrics, risk mitigation, next steps

### Document 3: Quick Reference
**File**: `PANEL_SUMMARY_QUICK_REFERENCE_2026-04-03.md`
**Length**: ~1,500 words
**Audience**: Team quick reference, content creators
**Content**:
- One-paragraph summaries of each panelist
- Visual tables (what each card should contain)
- Checklists for content creators
- Key references and implementation questions

---

## What Changed From Original Proposal

### Original Design (6 Cards)
```
1. Neural Frameworks
2. Theory Comparison
3. Mechanism Chain
4. Critical Test
5. Warrant Structure
6. Underdetermination Alert
```

### Issues Identified (Panel)
1. **Theory Comparison**: Purely qualitative; no way to rank underdetermined theories
2. **Mechanism Chain**: Linear chain conflates ontological levels; omits activities
3. **Critical Test**: "High-priority" ≠ "critical"; lacks theory-specific targeting

### What Panel Added

#### To Theory Comparison
- **Entity-activity pairs** (Machamer): specify what each entity *does*
- **Mechanistic level column** (Craver): mark which level each theory explains
- **Coherence scores** (Thagard): quantitative ranking when evidence ties
- **Explanatory scope matrix** (Darden): which domains each theory addresses
- **Interventionist predictions** (Woodward): opposite predictions under intervention

#### To Mechanism Chain
- **Multi-level pyramid** (Craver): behavioral → circuit → synaptic → molecular
- **Schema-gap notation** (Darden): color-coded by empirical support (green/yellow/red/gray)
- **Activity specifications** (Machamer): not just entities, but what they do
- **Empirical support table** (Darden): # papers, confidence, key references per level
- **Interventionist properties** (Woodward): what interventions test/break the mechanism?

#### To Critical Test
- **Mechanistic level targeting** (Craver): specifies which level each test addresses
- **Causal bottleneck** (Craver + Woodward): what specific mechanism is being tested?
- **Theory-specific predictions** (all panelists): opposite predictions for each theory
- **Discrimination index** (Darden): quantitative measure of test's discriminatory power (0.0–1.0)
- **Coherence impact** (Thagard): how much would outcome change theory coherence landscape?
- **Interventionist specificity** (Woodward): how targeted is the intervention?

#### New Supporting Pages
- **Mechanism Schema Gallery**: how-possibly vs. how-actually schemas side-by-side
- **Interventionist Prediction Maps**: for each theory, what interventions test its predictions?
- **Coherence-Learning Tool**: interactive exploration of how evidence updates coherence

---

## Key Design Decisions From Panel

### Decision 1: Multi-Level Mechanism Representation
**Panel Position**: All five panelists agreed.
**Rationale**: Mechanisms exist at multiple ontological levels (behavioral, circuit, synaptic, molecular). Theories operating at different levels are complementary, not competing. Linear chains hide this.
**Implementation**: Replace single chains with pyramid diagrams showing all levels with explicit color-coded empirical support.

### Decision 2: Coherence-Based Theory Ranking
**Panel Position**: Thagard's framework; supported by Darden, Craver.
**Rationale**: When theories tie on observational evidence, use ECHO-style coherence (breadth, depth, background fit, simplicity) to rank them. This is principled and transparent.
**Implementation**: Compute and display coherence scores with formula breakdown; explain why one theory is favored.

### Decision 3: Interventionist Testing for Discrimination
**Panel Position**: Woodward's framework; supported by Darden, Craver.
**Rationale**: Theories that appear observationally equivalent often make *different* predictions under intervention. This reveals the true causal structure.
**Implementation**: For every theory pair, specify the intervention that would distinguish them; rank critical tests by discrimination index.

### Decision 4: Explicit Schema Gaps
**Panel Position**: Darden's framework; supported by all panelists.
**Rationale**: Science advances by refining incomplete schemas. Pretending mechanisms are finished misleads users about the state of knowledge.
**Implementation**: Color-code mechanism steps (green=confirmed, yellow=tentative, red=gap, gray=untested); distinguish how-possibly from how-actually schemas.

### Decision 5: Activities, Not Just Entities
**Panel Position**: Machamer's framework; supported by Craver.
**Rationale**: Entities (amygdala, dopamine) do nothing by themselves. Activities (encode, inhibit, gate) are where causation happens. Specify activities explicitly.
**Implementation**: Always pair entities with activities (e.g., "Amygdala **encodes** threat"); build activity lexicon.

---

## Effort & Timeline Breakdown

### Phase 1: Foundation (Weeks 1–2)
**Tasks**:
- [ ] Update Neural Frameworks card (add domain count, gallery links)
- [ ] Design UI components (pyramid, coherence scores, color-coded status)
- [ ] Build data infrastructure

**Deliverable**: Prototype of multi-level pyramid visualization

---

### Phase 2: Core Cards (Weeks 3–8)
**Tasks**:
- [ ] Implement Theory Comparison card with all new fields
- [ ] Implement Mechanism Chain card with pyramid, gaps, activities
- [ ] Build coherence scoring backend
- [ ] Populate data for 3–5 test phenomena

**Deliverable**: Working theory comparison + mechanism chain; manual testing with domain experts

---

### Phase 3: Advanced Cards (Weeks 9–12)
**Tasks**:
- [ ] Implement Critical Test card with discrimination index + coherence impact
- [ ] Implement Underdetermination Alert card (revised)
- [ ] Populate critical test specifications with domain experts
- [ ] Full QA and refinement

**Deliverable**: Complete 6-card system; ready for soft launch

---

### Phase 4: Content & Launch (Weeks 12+)
**Tasks**:
- [ ] Populate mechanism chain for all 19 research fronts
- [ ] Populate critical tests for all underdetermined cases
- [ ] Expert panel review of populated data
- [ ] User testing with cognitive scientists
- [ ] Iterate and deploy

**Deliverable**: Live theory explorer with complete content

---

## Resource Requirements

### Development Team
- **1 Senior Frontend Engineer**: Multi-level visualizations, component design (full-time, 10–12 weeks)
- **1 Backend Engineer**: Coherence scoring, data models, API (full-time, 8–10 weeks)
- **1 Product Manager**: Requirements, testing, stakeholder coordination (part-time)
- **1 QA Engineer**: Component testing, cross-browser, accessibility (part-time)

### Content & Domain Experts
- **2–3 Cognitive Neuroscientists**: Populate mechanism chains, critical tests
- **1–2 Philosophy of Science Experts**: Validate coherence calculations, theory-level specs
- **1 Science Communicator**: User testing, documentation

### Timeline
- **Parallel tracks**: Frontend design (weeks 1–2) while backend scaffolding (weeks 1–2)
- **Critical path**: Coherence scoring implementation (must complete by week 5 for Critical Test card)
- **Content bottleneck**: Expert time (typically available 10–15 hrs/week); plan accordingly

---

## What Stays the Same

### Neural Frameworks Card
- Minor updates only
- Structure and content largely unchanged
- Add two fields: domain_count, mechanism_gallery_url

### Warrant Structure Card
- **Zero changes** — epistemologically sound as-is
- Continue using as before

### Overall UX Journey
- OIIEA (Orient → Inspect → Explain → Evaluate → Act) framework preserved
- Home page structure preserved
- Navigation between cards intuitive (Theory Comp → Mechanism → Critical Test)

---

## What's New

### Data Models
- Theory now includes: entities_and_activities, mechanistic_level, coherence_score breakdown, interventionist_predictions
- Mechanism now includes: multi-level structure, schema_status per level, empirical_support per level, schema_gaps
- Critical test now includes: mechanistic_level, causal_bottleneck, discrimination_index, coherence_impact

### UI Components
- Multi-level pyramid (interactive SVG)
- Coherence subscores with weights visualization
- Schema-gap color legend
- Expandable detail panels (coherence breakdown, scope matrix, interventionist properties)
- Discrimination index badge
- Feasibility timeline widget

### Backend Calculations
- ECHO-style coherence scoring (weighted sum of breadth, depth, background fit, simplicity)
- Discrimination index computation (difference in predicted probabilities across theories)
- Coherence impact calculation (change in coherence scores if test outcome observed)

---

## Decision Points Before Development

### 1. Coherence Formula Sign-Off
**Question**: Is the proposed ECHO-style formula (breadth × 0.3 + depth × 0.3 + background_fit × 0.2 + simplicity × 0.2) acceptable?

**Who Decides**: David Kirsh + at least one panelist (recommend Thagard)

**Timeline**: Week 0 (before Phase 1)

---

### 2. Schema-Gap Color Scheme
**Question**: Are the proposed colors (green/yellow/red/gray) accessible and appropriate?

**Who Decides**: Accessibility reviewer + content team

**Timeline**: Week 0–1

---

### 3. Content Population Strategy
**Question**: Which phenomena should be fully populated first (for testing)? Suggest top 3 from 19 research fronts.

**Who Decides**: David Kirsh + content team

**Timeline**: Week 1

---

### 4. Critical Test Sourcing
**Question**: Will domain experts (panelists + Atlas team) directly author critical test specs, or should development team draft them for expert review?

**Who Decides**: David Kirsh + proposed content lead

**Timeline**: Week 4 (before Phase 3)

---

### 5. Supporting Pages Priority
**Question**: Should Mechanism Schema Gallery, Interventionist Prediction Maps, and Coherence-Learning Tool launch simultaneously with main cards, or be deferred to v2.2?

**Options**:
- A: Launch all together (Phase 4, weeks 12+)
- B: Defer supporting pages to v2.2; focus on 6-card system
- C: Launch mechanism gallery only in v2.1; defer others to v2.2

**Recommendation**: Option C (mechanism gallery is most critical for helping users understand knowledge state)

**Who Decides**: David Kirsh + product manager

**Timeline**: Week 6 (when Phase 2 nearing completion)

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Coherence formula is oversimplified; experts dispute weighting | Medium | Medium | Get sign-off from Thagard before development; allow tuning in code |
| Content population takes longer than expected | High | High | Start with 3 test phenomena; scale gradually; hire expert writer early |
| Multi-level pyramid visualization is hard to render across browsers | Low | Medium | Design once, test across Chrome/Safari/Firefox early; use standard SVG |
| Discrimination index calculations prove ambiguous in practice | Medium | Medium | Have panelists validate calculations on 2–3 test cases before rollout |
| Users confused by too many detail panels; disclosure overload | Medium | Low | User testing in Phase 4; simplify panels if needed |

---

## Success Criteria (For Phase 1–3 Completion)

### Code Quality
- [ ] All React components tested (unit + integration)
- [ ] Data models validated against actual content
- [ ] Accessibility audit passed (WCAG 2.1 AA)
- [ ] Performance: Mechanism pyramid renders in <500ms

### Content Quality
- [ ] Mechanism chains for test phenomena have all 4 levels populated
- [ ] Schema gaps marked and explained (0 unmarked gaps)
- [ ] Critical tests have discrimination indices validated by domain experts
- [ ] Coherence scores manually reviewed by panelist

### User Research
- [ ] 5+ cognitive scientists can navigate between cards intuitively
- [ ] Users report understanding why theories compete vs. complement
- [ ] Users report understanding which experiments would resolve underdetermination
- [ ] 80%+ of users find schema-gap notation helpful (survey)

---

## Documentation Deliverables

### For Development Team
- Detailed component specifications (API, props, styling)
- Data model documentation with example JSON
- Deployment checklist

### For Content Team
- Mechanism description template (YAML/JSON)
- Theory comparison template
- Critical test specification template
- Coherence scoring guide (how to verify calculations)

### For Users
- "How to read a mechanism schema" tutorial
- "Understanding coherence scores" explainer
- "Designing a critical test" interactive guide

---

## Next Steps (Immediate, Week 0)

1. **Decision Checkpoint**: Review this document + the three panel reports. Confirm:
   - [ ] Design direction approved
   - [ ] 5 key design decisions endorsed
   - [ ] Effort/timeline realistic for available capacity
   - [ ] Content/domain expert resources committed

2. **Design Kickoff**: If approved:
   - [ ] Design team reads implementation guide in detail
   - [ ] Schedule 1-hour sync with panelists (recommend Craver + Woodward for technical questions)
   - [ ] Create Figma mockups of multi-level pyramid + theory comparison table
   - [ ] Identify 3 test phenomena for Phase 2 content population

3. **Governance Setup**:
   - [ ] Assign development lead + content lead
   - [ ] Create weekly sync schedule (dev + David + domain experts)
   - [ ] Set up TASKS.md (already in repo; update with this project tasks)
   - [ ] Establish code review process for panel-sensitive components

4. **Content Preparation**:
   - [ ] Recruit 2–3 domain experts for content population
   - [ ] Schedule intro call to explain new data models
   - [ ] Prepare first batch of phenomena for expert mapping

---

## Open Questions For Panel

1. **Craver**: Do you see any problems with the multi-level pyramid structure as described? Should we add relata (connections) explicitly in the diagram?

2. **Machamer**: Is the entity-activity pair notation sufficient, or should we also represent causal vs. constitutive relations within each level?

3. **Darden**: Are there cases where a theory should be labeled "how-possibly" at the circuit level but "how-actually" at the behavioral level? How should the color scheme handle mixed status?

4. **Thagard**: The coherence formula weights breadth and depth equally (0.3 each). Does this match ECHO practice, or should we adjust?

5. **Woodward**: For critical tests, should we distinguish between "interventions that discriminate theories" vs. "interventions that test a single theory's predictions"? Or are these the same thing?

---

## References

### Panel Report
- **File**: `EXPERT_PANEL_THEORY_EXPLORER_DESIGN_2026-04-03.md` (full positions, synthesis, bibliography)

### Implementation Guide
- **File**: `IMPLEMENTATION_GUIDE_THEORY_EXPLORER_2026-04-03.md` (data models, component code, effort/timeline)

### Quick Reference
- **File**: `PANEL_SUMMARY_QUICK_REFERENCE_2026-04-03.md` (one-pagers, checklists, success criteria)

### Related Docs (Existing in Atlas Repo)
- `AG_THEORY_AND_MECHANISM_REVIEW_2026-03-24.md` (prior theory/mechanism work review)
- `THEORY_GUIDES_ARCHITECTURE_2026-03-24.md` (existing theory architecture)
- `TASKS.md` (main project task list)

---

**Status**: READY FOR STAKEHOLDER REVIEW
**Decision Needed**: Approve design direction, estimate feasibility, commit resources
**Timeline to Go/No-Go**: End of week 0 (April 3–4, 2026)

# AI Context Files — COGS 160 Manifest

**Created**: 2026-03-30
**Location**: `/sessions/keen-busy-turing/mnt/REPOS/Knowledge_Atlas/160sp/context/`

## Overview

Five files have been created to provide AI assistants with precise domain knowledge for each COGS 160 track. Each context file is a standalone markdown document that students can load into their AI sessions before assigning work.

## Files

### 1. context_image_tagger.md
**Track**: Image Tagger (Track 1)
**Size**: 8.2 KB
**Purpose**: Teach AI how to link environmental photographs to psychological constructs in K-ATLAS evidence base

**Key sections**:
- What K-ATLAS is (2 paragraphs explaining credence structure and Evidence Network)
- The Evidence Network model: Claims, Edges, Warrants
- The 7 warrant types with calibrated d values (CONSTITUTIVE 1.0 through THEORY-DERIVED 0.25)
- Image tagging in K-ATLAS (linking CNFA tags to psychological constructs)
- CNFA framework (environmental variables → psychological mechanisms → behavioral outcomes)
- Data model for image tag records (image_id, construct, evidence_item_id, confidence, tagger_id, timestamp)
- Acceptance criteria (reference to real evidence, justified confidence, no hallucinated constructs, measurement validity, traceability)

### 2. context_article_finder.md
**Track**: Article Finder (Track 2)
**Size**: 7.6 KB
**Purpose**: Teach AI how to find and add papers to K-ATLAS corpus while avoiding duplicates and ensuring relevance

**Key sections**:
- What K-ATLAS is (2 paragraphs with emphasis on credence propagation)
- The corpus: scale (~760 papers, ~1,900 evidence items, 11 topic clusters)
- What "relevance" means (paper must address specific environmental variable, population, outcome measure)
- Question format in K-ATLAS (structured queries with embedded components)
- Data model for articles (doi, title, authors, year, journal, abstract, pdf_path, relevance_score, assigned_question_id, optional fields)
- The deduplication problem (same paper found through multiple search paths)
- Acceptance criteria (unique DOI, accessible PDF, justified relevance, no hallucinated citations, metadata accuracy, question mapping specificity)

### 3. context_vr_production.md
**Track**: VR Production (Track 3)
**Size**: 9.5 KB
**Purpose**: Teach AI how to design VR environments that instantiate and test K-ATLAS evidence relationships

**Key sections**:
- What K-ATLAS is (2 paragraphs emphasizing translation of evidence to actionable design)
- How evidence items describe environment-behavior relationships (Feature → Mechanism → Outcome)
- What a VR environment must demonstrate (environmental variable instantiation, mechanism visualization, outcome measurability, credence transparency)
- Warrant system and confidence structure (table of 7 warrant types with d values and design application)
- Data model for VR scene specifications (scene_id, target_evidence_items, environmental_variables, behavioral_outcomes, measurement_points, credence_levels, platform, fidelity_level)
- Platform flexibility (Unreal Engine 5, A-Frame, Unity, custom WebGL with tradeoffs)
- Acceptance criteria (evidence instantiation, mechanism visibility, measurement integrity, credence-appropriate design, boundary condition documentation, scene reusability)

### 4. context_gui_evaluation.md
**Track**: GUI Evaluation (Track 4)
**Size**: 12 KB
**Purpose**: Teach AI how to evaluate K-ATLAS interface usability across six user modes

**Key sections**:
- What K-ATLAS is (2 paragraphs emphasizing transparent epistemic structure and navigation)
- Current site structure (K-ATLAS root pages, COGS 160 pages, data payloads)
- The six user modes (student_explorer, researcher, contributor, instructor, practitioner, theory_mechanism_explorer) with goals and key pages
- What usability evaluation means (task success, not aesthetics; specific friction points, not vague impressions)
- Examples of usability problems (mode ambiguity, navigation inconsistency, search-to-answer gap, boundary condition invisibility)
- Current known UI problems (6 specific issues documented)
- Data model for evaluation records (page_url, user_mode, task_attempted, success, time_to_complete, friction_points, suggested_fix, tester_id, timestamp)
- Acceptance criteria (cover all primary user flows, friction reproducible, fixes specific, tested with actual users or detailed simulation, explicit success criteria, addresses known problems)

### 5. index.html
**Purpose**: Navigation hub and entry point for all context files

**Features**:
- Styled with K-ATLAS color scheme (navy, teal, amber, cream, gold)
- Navigation bar linking to schedule, tracks, and dashboard
- Hero section explaining the purpose of context files
- Intro box with usage instructions
- Four cards (one per track) with brief descriptions and download links
- Footer navigation linking back to schedule and Week 2 agenda
- Responsive design (works on mobile and desktop)

## Usage

Students follow this workflow:

1. Visit `/160sp/context/index.html` from the K-ATLAS site
2. Click the card corresponding to their assigned track
3. Download or copy the context file (.md)
4. Load the file into their AI session before writing task prompts
5. The AI now has precise domain knowledge (K-ATLAS structure, warrant types, data models, acceptance criteria)

## Content Philosophy

Each context file follows this principle: **only include what the AI needs to produce correct output for that track.**

No filler. No pedagogical asides. No "learn about K-ATLAS in general." Instead:
- K-ATLAS structure is explained only in the context relevant to that track's work
- Domain knowledge is specific (e.g., the 7 warrant types with d values, not abstract epistemology)
- Data models are explicit (image tag records need these exact fields)
- Acceptance criteria are operationalized and measurable
- Examples use the same constructs and evidence items that appear in the actual K-ATLAS instance

This ensures that when an AI loads a context file, it can immediately produce work at the standard expected for COGS 160.

## Integration Points

These context files integrate with existing COGS 160 materials:

- **ka_thursday_tasks.html**: The seven exploratory tasks that introduce each track
- **ka_tag_assignment.html**: Track 1 (Image Tagger) detailed assignment
- **ka_article_finder_assignment.html**: Track 2 (Article Finder) detailed assignment
- **ka_vr_assignment.html**: Track 3 (VR Production) detailed assignment
- **ka_gui_assignment.html**: Track 4 (GUI Evaluation) detailed assignment
- **ka_schedule.html**: Course timeline; links to context directory

## Quality Assurance

Each context file has been verified for:
- ✓ Accuracy against ka_explain_system.html (K-ATLAS system architecture)
- ✓ Accuracy against ka_thursday_tasks.html (track definitions and workflows)
- ✓ Consistency of domain terminology (credence, warrant type, evidence item, construct, etc.)
- ✓ Data model completeness (all required fields specified)
- ✓ Acceptance criteria specificity (measurable and enforceable)
- ✓ No redundancy across files (each file covers its track only)

## Files and Artifacts Summary

| File | Type | Size | Status |
|------|------|------|--------|
| context_image_tagger.md | Markdown | 8.2 KB | ✓ Complete |
| context_article_finder.md | Markdown | 7.6 KB | ✓ Complete |
| context_vr_production.md | Markdown | 9.5 KB | ✓ Complete |
| context_gui_evaluation.md | Markdown | 12 KB | ✓ Complete |
| context_ex0_mechanism_pathway.md | Markdown | ~4 KB | ✓ Complete |
| context_exA_trust_panel.md | Markdown | ~5 KB | ✓ Complete |
| context_exB_debate_visualizer.md | Markdown | ~4 KB | ✓ Complete |
| context_exC_warrant_calculator.md | Markdown | ~5 KB | ✓ Complete |
| context_exD_search_filter.md | Markdown | ~5 KB | ✓ Complete |
| index.html | HTML | 9.9 KB | ✓ Complete |
| MANIFEST.md | Markdown | This file | ✓ Complete |

### Week 2 Programming Exercise Context Files (NEW — 2026-03-30)

Five additional context files were created for the Week 2 AI-directed programming exercises. These are more focused than the track context files: each targets one specific coding task, includes the exact JSON schemas the student will need, and ends with the instruction to ask the AI to explain the task before starting.

- **context_ex0_mechanism_pathway.md** — Demo exercise: D3.js mechanism pathway tracer using argumentation.json
- **context_exA_trust_panel.md** — Exercise A: "Why Trust This?" panel using evidence.json trust fields
- **context_exB_debate_visualizer.md** — Exercise B: debate cluster argument map using argumentation.json
- **context_exC_warrant_calculator.md** — Exercise C: transparent trust score calculator with receipt-style display
- **context_exD_search_filter.md** — Exercise D: filter bar for 1,900 evidence claims

**Total deliverable**: 10 context files + 1 index page + 1 manifest
**Total size**: ~79 KB
**Location**: `/sessions/keen-busy-turing/mnt/REPOS/Knowledge_Atlas/160sp/context/`

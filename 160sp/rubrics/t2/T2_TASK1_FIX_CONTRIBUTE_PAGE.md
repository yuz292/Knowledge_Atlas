# Track 2 · Task 1: Fix the Contribute Page

**Track:** Article Finder  
**What's wrong:** The contribute page accepts PDFs but does nothing with them — no classification, no storage, no feedback.  
**Your job:** Fix it so that submitted papers are classified, stored correctly, and the user sees what happened.

---

## What This Assignment Teaches

You will use AI to fix a broken page. But the point is not the fix — AI writes the code. The point is:

- Can you **diagnose** what's broken by asking your AI the right questions?
- Can you **spec** the fix precisely enough that AI builds the right thing?
- Can you **verify** that the AI's fix actually works — and catch the cases where it silently doesn't?

---

## Setup: Clone the Repositories

You need four repositories. All are at [github.com/dkirsh](https://github.com/dkirsh):

```bash
# 1. The Knowledge Atlas site (contains the contribute page you'll fix)
git clone https://github.com/dkirsh/Knowledge_Atlas.git

# 2. The Article Finder pipeline (the discovery half of the system)
git clone https://github.com/dkirsh/Article_Finder.git

# 3. The Article Eater extraction engine (the processing half)
git clone https://github.com/dkirsh/Article_Eater.git

# 4. The shared classifier module (the ID function you'll wire in)
git clone https://github.com/dkirsh/atlas_shared.git
cd atlas_shared && pip install -e . && cd ..
```

Verify `atlas_shared` installed correctly:
```bash
python3 -c "from atlas_shared.classifier_system import AdaptiveClassifierSubsystem; print('OK')"
```

---

## Phase 1: Diagnose — What's Broken?

You need to understand two programs before you can connect them.

### 1A. Ask your AI to explain the contribute page

Open `Knowledge_Atlas/ka_contribute_public.html`. Give the full source to your AI and ask:

> *"Walk me through exactly what happens when a user drops a PDF and clicks 'Send suggestion.' For each step, tell me: what function runs, what data is created, and where it goes. Then tell me everything that is MISSING that a working version would need."*

Then ask:

> *"Draw a box-and-arrow diagram showing the data flow. Label every missing component."*

**Your deliverable:** A boxology diagram and a short "Current State" paragraph describing what the page does and does not do.

### 1B. Ask your AI to explain the classifier

Open `atlas_shared/src/atlas_shared/classifier_system.py`. Give it to your AI and ask:

> *"This is the classifier for the Knowledge Atlas. Explain two things:*
> 1. *How does it decide what TYPE of article a PDF is? (empirical, review, theoretical, etc.)*
> 2. *How does it decide what TOPIC a paper belongs to? (daylight + cognition, ceiling height + creativity, etc.)*
> 
> *For each, tell me the class name, the method, and what data it looks at. Then draw a box-and-arrow diagram showing what happens inside `classify()`."*

**Your deliverable:** A boxology diagram of the classifier's internal steps.

### 1C. Identify the gap

Now you have two diagrams: what the contribute page does, and what the classifier does. The gap between them is your assignment.

> *Ask your AI: "Given these two programs, what would I need to build to connect them? Be specific — what endpoint, what data transformations, what storage?"*

> *Also ask: "Are there any existing files in the Knowledge Atlas repo that already handle article submission? Search for files with 'article' or 'submit' in their names."*

This second question is critical. Your AI should find existing infrastructure. Ask it to explain what's already built and what's missing.

**Your deliverable:** A one-paragraph gap statement: "The contribute page currently does X. The classifier can do Y. The existing backend already does Z. To complete the integration, we need W."

---

## Phase 2: Spec — Write the Contract

Write a contract called **"Classifier Integration Contract"** that specifies exactly what the fixed version should do. Your contract must include:

- **Inputs:** What the user provides (PDF, citation, or both)
- **Processing:** What the backend does with it (build evidence, call classifier)
- **Outputs on the page:** What the user sees in a results section — for each paper:
  - Whether it was **accepted**, **edge case**, or **rejected**
  - What type of article it is
  - What topic(s) it matches
  - Confidence score
- **Storage rules:**
  - Accepted papers: stored (PDF + database entry)
  - Edge-case papers: stored but flagged as edge cases
  - Rejected papers: shown in results but NOT stored
- **Success conditions:** At least 3 specific test cases with expected outcomes

### Ask your AI about storage

You need to know where PDFs go and where database entries go. Ask:

> *"In the Knowledge Atlas project, where are article PDFs stored? There's a lifecycle database — what tables does it have, and what should a new paper's entry look like when it first arrives? Show me the schema."*

> *"The pipeline has defined stages. What is the first stage a newly contributed paper should be at? What status should it have?"*

Do not accept the AI's answer at face value. Open the database yourself and check:

```bash
sqlite3 Knowledge_Atlas/160sp/pipeline_lifecycle_full.db ".schema papers"
sqlite3 Knowledge_Atlas/160sp/pipeline_lifecycle_full.db ".schema lifecycle_events"
sqlite3 Knowledge_Atlas/160sp/pipeline_lifecycle_full.db "SELECT stage_name, stage_order FROM stage_definitions ORDER BY stage_order;"
```

**Your deliverable:** The completed contract with storage paths and database column values filled in.

---

## Phase 3: Fix — Delegate to Your AI

Give your AI:
1. Your contract
2. The source of `ka_contribute_public.html`
3. The source of `classifier_system.py`
4. Any existing backend files your AI found in Phase 1C

Ask it to build:
1. A backend endpoint that receives the form submission and runs the classifier
2. A results section on the contribute page that shows classification results
3. Storage logic for accepted and edge-case papers

### Questions you must ask your AI to verify the fix

After your AI produces code, do NOT just run it. Ask these questions first:

> *"Show me exactly where in your code the PDF file gets saved to disk. What path does it use? What happens if that directory doesn't exist?"*

> *"Show me the line where you call `AdaptiveClassifierSubsystem.classify()`. What are you passing in as the `evidence_like` argument? Walk me through which fields of ClassificationEvidence get populated from the user's submission."*

> *"Show me where you write to the database. Which table? What values go in each column? What happens if the paper_id already exists?"*

> *"What happens when the classifier returns `next_action = 'need_abstract_or_keywords'`? Does your code handle that case, or does it silently ignore it?"*

> *"How do you distinguish an accepted paper from an edge case in storage? Show me the exact field or flag."*

> *"If I submit 5 PDFs in one session, does the results section show all 5? Or does each new submission overwrite the previous result?"*

If the AI can't answer any of these clearly, the fix is incomplete. Push back.

**Your deliverable:** The working code, plus a log of which verification questions revealed problems and how you fixed them.

---

## Phase 4: Prove — Run the Tests

### Prepare test papers

Get at least 4 PDFs:
1. A known on-topic empirical paper (e.g., one already in the Atlas)
2. A clearly off-topic paper (e.g., a machine learning paper)
3. An edge case (e.g., an architectural theory paper with no empirical data)
4. A citation-only submission (no PDF)

### Run each test and record

| Test | Input | Expected verdict | Actual verdict | Expected type | Actual type | Stored? | DB entry? | PASS? |
|------|-------|-----------------|----------------|---------------|-------------|---------|-----------|-------|
| 1 | On-topic PDF | accept | | empirical | | yes | yes | |
| 2 | Off-topic PDF | reject | | — | | no | no | |
| 3 | Edge-case PDF | edge_case | | theoretical | | yes (flagged) | yes | |
| 4 | Citation only | varies | | varies | | — | — | |

### Verify storage

For every paper that should be stored, check:

```bash
# Does the PDF file exist?
ls -la <expected_path>

# Does the database entry exist?
sqlite3 pipeline_lifecycle_full.db \
  "SELECT paper_id, article_type, current_stage, current_status FROM papers WHERE paper_id='<id>';"

# Is there a lifecycle event?
sqlite3 pipeline_lifecycle_full.db \
  "SELECT stage_name, status, agent FROM lifecycle_events WHERE paper_id='<id>';"

# Is the edge case distinguishable from the accepted paper?
sqlite3 pipeline_lifecycle_full.db \
  "SELECT paper_id, current_status FROM papers ORDER BY created_at DESC LIMIT 5;"
```

### When something fails — diagnose

For each failure, determine: **Is the spec wrong, or is the AI's implementation wrong?**

- If the classifier produces the wrong verdict → the spec may be right but the constitutions may not cover the topic. That's a classifier issue, not your bug.
- If the classifier produces the right verdict but the page doesn't show it → the AI's code has a rendering bug. That IS your bug.
- If the PDF is stored but the database entry is missing → the AI's code has a storage bug. That IS your bug.

**Your deliverable:** The completed validation matrix, plus a diagnosis note for any failures explaining whether it was a spec bug or an implementation bug.

---

## What You Submit

| Item | What it is |
|------|-----------|
| **Boxology diagrams** (Phase 1) | Two diagrams: the contribute page data flow, and the classifier's internal steps |
| **Gap statement** (Phase 1) | One paragraph: what exists, what the classifier does, what's missing |
| **Classifier Integration Contract** (Phase 2) | Your spec with inputs, outputs, storage, and success conditions |
| **Working code** (Phase 3) | The fixed contribute page, endpoint, and storage logic |
| **Verification log** (Phase 3) | Which questions you asked your AI, which revealed problems, how you fixed them |
| **Validation matrix** (Phase 4) | Test results for all 4+ test cases |
| **Storage proof** (Phase 4) | Terminal output showing the PDF exists and the DB entries are correct |
| **Diagnosis notes** (Phase 4) | For any failures: spec bug or implementation bug? |

---

## Files You Must Submit

Your submission must include a **file manifest** listing every file you changed or created, with a one-line description. The instructor will diff your repo against the upstream to verify.

Expected files (your list may differ, but these are the minimum):

| File | Change Type | What It Does |
|------|------------|-------------|
| `ka_contribute_public.html` | Modified | Form now posts to a real endpoint; results section added below the form |
| Backend endpoint file (e.g., added to `ka_article_endpoints.py` or a new file) | Modified or New | Receives form submission, runs `atlas_shared` classifier, returns JSON result |
| `data/storage/` or `data/pnu_articles/` | New files | Stored PDFs for accepted and edge-case papers |
| Database (e.g., `data/ka_auth.db` or `pipeline_lifecycle_full.db`) | Modified | New rows for submitted papers |

**How to generate your manifest:**
```bash
cd Knowledge_Atlas
git diff --name-only HEAD    # shows files you changed
git status --short           # shows new files
```

Include the output of both commands in your submission.

---

## Grading

| Criterion | What we check |
|-----------|--------------|
| **Diagnosis** | Your boxology diagrams are accurate, your gap statement is correct |
| **Spec quality** | Your contract is complete, specific, and testable |
| **Verification questions** | You asked probing questions that caught real problems in the AI's code |
| **Validation** | At least 3 of 4 test papers produce correct results and storage |
| **Diagnosis of failures** | You correctly identified whether failures were spec bugs or implementation bugs |
| **File manifest** | Your manifest is complete and matches your actual changes |

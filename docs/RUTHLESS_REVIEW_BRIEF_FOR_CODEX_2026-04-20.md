# Ruthless review brief — Codex, pre-staging-push (2026-04-20 revision)

*Date*: 2026-04-20
*Supersedes*: `docs/RUTHLESS_REVIEW_BRIEF_FOR_CODEX_2026-04-19.md`
*Requested by*: DK
*Executor*: Codex (GPT-5.x)
*Target*: the tip of the `master` branch of `Knowledge_Atlas` at the moment you run this review
*Expected output*: either a clean signal (no fixes needed) or one or more commits that close the gaps, followed by a status note at `docs/RUTHLESS_REVIEW_STATUS_2026-04-20.md`
*Companion doc*: `docs/STAGING_DEPLOYMENT_PLAN_2026-04-19.md` (Phase 2)

---

## Why this exists and what's new since the 2026-04-19 brief

The first brief went out yesterday. Since then two further waves of work have landed on CW's branch and are awaiting this review before they are committed and pushed:

1. **Track 4 deliverable pages (wave 1)** — eight scaffolded pages at `160sp/ka_t4_{a|b|b2|c|d|e|f|g}_*.html` plus one shared stylesheet `160sp/ka_t4_page.css`, plus edits to `160sp/ka_track4_hub.html`. Each page uses a six-section pattern (Goal · What you'll do · Files · Naive-approach counter-example · Verification · Workspace · Next step) and a workspace form that saves drafts to `localStorage` under `ka.t4{letter}_draft`.

2. **Complicated-surface journey pages (wave 2)** — twelve spec-and-critique pages at the repo root as `ka_journey_{slug}.html` for `en, bn, interpretation, argumentation, qa, mechanism, theory, gaps, evidence, fronts, ontology, topic_inspector`, plus an index `ka_journeys.html`, shared stylesheet `ka_journey_page.css`, shared sibling-nav helper `ka_journey_surface.js`, and the generator script `scripts/gen_journey_pages.py`. Each page follows a six-section pattern (What it displays · Who needs it and why · Why it's hard · Naive solution · Per-role critique · Data files) and writes critique drafts to `localStorage` under `ka.critique.{slug}` via `ka_journey_surface.js`. Plus a linked-from edit to `160sp/ka_t4_a_heuristic_audit.html` that points students at the journey pages as optional audit targets.

Together these twenty-seven files introduce three new interaction patterns (sibling-nav row, status pill, per-role critique form) and twelve new `localStorage` namespaces. They must be checked for the usual hazards (broken links, inconsistent siblings, colliding storage keys, persona-vocabulary drift) before the staging push.

The **nine original probes** from the 2026-04-19 brief are still in force; run them first. The **two new probes** (10 and 11) below are specific to the new surface area.

---

## The original nine probes (condensed; see yesterday's brief for full text)

### Probe 1 — Broken links
Walk every `href="..."` in every HTML file. Verify local targets exist and anchors resolve. **New for today**: the T4 deliverable pages reference `rubrics/t4/{deliverable}.md` and `rubrics/t4/*_template.*` files; confirm these exist in the rubric directory, or flag each missing file in the status note for DK to populate. The journey pages use `<a>` tags for file-list display without `href` (intentional — those are identifiers, not live links). Treat those as fine.
*Expected count*: ≤ 5.

### Probe 2 — Unauthenticated admin paths
Same as yesterday. No new admin surfaces introduced today, but verify yesterday's `ka_admin.html` "wrong door" callout still renders and still gates.
*Expected count*: 0–3.

### Probe 3 — Persona-awareness regressions
Same as yesterday. **New for today**: the twelve journey pages' "Who needs this, and why" sections use the canonical five-role vocabulary (`public_visitor`, `160_student`, `researcher`, `practitioner`, `admin`). Confirm each journey page's role list spans all five roles in the same order, and each list item makes an honest claim (either "this user is served because X" or "this user is not a target, route to Y" — not a generic "could help anyone").
*Expected count*: ≤ 3.

### Probe 4 — Copy contradictions
Same as yesterday, with **two additions**:

- The T4 deliverable pages declare point values in their header `.t4-meta` blocks: T4.a=12, T4.b=5, T4.b.2=10, T4.c=15, T4.d=5, T4.e=13, T4.f=10, T4.g=5 → 75 points total. Verify the Region 3.5 card on `160sp/ka_track4_hub.html` agrees with each of the eight pages, and that their sum is exactly 75 (the Track 4 project block).
- The status pills on journey pages take one of four values (`naive`, `prototype`, `shipped`, `absent`). Verify that the pill class on each page matches the index page `ka_journeys.html` and that the explanation paragraph on the index (describing what each label means) lists exactly those four values.

*Expected count*: ≤ 5.

### Probe 5 — Validator warnings above threshold
Run `python3 scripts/site_validator.py`. New pages should not introduce errors; warnings are acceptable if they are the existing `LNK001` template-placeholder class. SEC001 on any new page blocks the deploy.
*Expected count*: 0 errors; 0–3 SEC001 issues worth investigating.

### Probe 6 — Mobile breakage
Run yesterday's checklist plus the new pages:
- one T4 deliverable page (`160sp/ka_t4_a_heuristic_audit.html`) — check the `.t4-workspace` form fields stack cleanly
- `ka_journeys.html` — the `.layer-grid` should reflow to one column
- one journey page (`ka_journey_en.html`) — check that the `.j-siblings` row wraps rather than overflowing and that the critique form's textareas resize

*Expected count*: 0–5 minor polishing items.

### Probe 7 — Dead code
Same as yesterday.
*Expected count*: 5–15 items, mostly retainable.

### Probe 8 — Payload staleness
Same as yesterday. **Important caveat for today**: the twelve journey pages' "Data files and endpoints" sections reference payload files and API endpoints that in many cases **do not yet exist** (they are marked `<span class="file-type missing">missing</span>`). This is intentional — those sections are specifications, not live fetches. Verify that none of the journey pages actually try to `fetch()` a non-existent payload file at load time; a `fetch()` that silently 404s is a different hazard from a documented missing file.
*Expected count*: 0–2 real issues.

### Probe 9 — Security leaks
Same as yesterday. The generator script `scripts/gen_journey_pages.py` is pure-Python content-embedding with no secrets; verify as routine.
*Expected count*: 0.

---

## Probe 10 — Track 4 deliverable-page consistency (new)

The eight T4 deliverable pages are a sibling set and must behave as one. Please verify:

### 10a. Siblings row is identical across the eight pages

Every one of `160sp/ka_t4_{a,b,b2,c,d,e,f,g}_*.html` has a `<div class="t4-siblings">` block with the same eight `<a>` tags in the same order (`T4.a · T4.b · T4.b.2 · T4.c · T4.d · T4.e · T4.f · T4.g`), and exactly one of them carries `class="current"`, matching the page it is on. One missing or misordered sibling, or two pages marking themselves current, is a bug.

### 10b. localStorage key namespace is disjoint

Each T4 page's workspace form saves to a key under the pattern `ka.t4{letter}_draft`. Verify:

- `T4.a` → `ka.t4a_draft`
- `T4.b` → `ka.t4b_draft` (keyed by role when per-role)
- `T4.b.2` → `ka.t4b2_matrix` (and not `ka.t4b2_draft`, because the b.2 workspace stores a matrix, not a single draft)
- `T4.c` → `ka.t4c_draft`
- `T4.d` → `ka.t4d_draft`
- `T4.e` → `ka.t4e_draft`
- `T4.f` → `ka.t4f_draft`
- `T4.g` → `ka.t4g_draft`

No two pages should write to the same key; no page should read from a key it does not own.

### 10c. Rubric links resolve or are flagged

Every page's `.rubric-link` (top of header) and every `<li>` in the Files &amp; pages section that has `class="file-type">RUBRIC<` points to a path under `rubrics/t4/`. If any of those target files does not exist in the repo, do NOT treat it as Probe-1 breakage; instead list it in the status note under a section `§ T4 rubric files still to author` — these are known to be stubs until the track-lead deliverable lands.

### 10d. Naive-approach blocks are functionally distinct

Each T4 page's `.t4-naive` block demonstrates a different failure mode appropriate to its deliverable: T4.a's is a subjective finding, T4.c's is a moderator-led pilot log, T4.d's is a severity backlog with no evidence column, T4.e's is a non-reproduction report that blames the world, T4.f's is an aesthetic-preference redesign, T4.g's is a self-celebratory report. Spot-check three pages to confirm the naive examples are not cut-and-pasted from each other; generic "this is bad because it's not specific" counter-examples are a failure mode.

### 10e. The hub link-out and T4.a link-in both resolve

The new Region 3.5 in `160sp/ka_track4_hub.html` links to all eight T4 pages. Verify each link resolves. The T4.a page now has an "Ambitious add-on" callout pointing at `../ka_journeys.html`. Verify that link resolves.

*Expected count*: 0–3 consistency issues.

---

## Probe 11 — Journey-page consistency (new)

The twelve journey pages are generated from a single Python script but shipped as twelve separate HTML files. Please verify:

### 11a. Siblings rows match the canonical slug list

`ka_journey_surface.js` defines a `SIBLINGS` constant listing twelve slugs in the canonical order (`en, bn, interpretation, argumentation, qa, mechanism, theory, gaps, evidence, fronts, ontology, topic_inspector`). On every one of the twelve `ka_journey_*.html` pages, the `<div class="j-siblings" id="j-siblings-slot">` element should be injected at load time by `renderJourneySiblings(slug)` where `slug` matches the page filename's middle segment (`ka_journey_{slug}.html`). Verify that:

- every page calls `renderJourneySiblings('{correct_slug}')` with the slug matching its filename;
- the script tag for `ka_journey_surface.js` is present in every page's `<head>`;
- at most one sibling-link carries `class="current"` — namely the one matching the current page.

### 11b. Critique-form localStorage namespace is disjoint

Each journey page writes critique drafts under `ka.critique.{slug}` via `saveCritique('{slug}')`. Verify the slug parameter on every page's `saveCritique` and `restoreCritique` calls matches its filename. Two pages writing to the same key would cross-contaminate drafts.

### 11c. The index page statuses match the pages

`ka_journeys.html` ascribes a status label (`naive`, `prototype`, `shipped`, `absent`) to each of the twelve pages. The same page under its own `.status-pill` class must carry the same label. If the index says "prototype" and the page says "naive", that is a consistency failure.

### 11d. No live fetch to missing payloads

Confirm (by grep) that none of the twelve journey pages actually fetches any of the files listed in its "Data files and endpoints" section at load time. The intent is that those sections are specifications; the page is static. If any page has a `fetch('data/ka_payloads/...')` that targets a not-yet-existing payload, it will 404 silently and should be either removed, wrapped in a try/catch, or converted into an explicit "not yet wired" notice.

### 11e. Role list cardinality

Every journey page's `.role-list` has exactly five `<li>` entries corresponding to the five canonical roles. The critique form block below it has exactly five `.role-crit` children with ids `crit_public_visitor`, `crit_160_student`, `crit_researcher`, `crit_practitioner`, `crit_admin`. A mismatch between the "Who needs it" list and the critique form is a design bug: if a page declares a role not a target user, the critique form should still invite that user to say so, not hide them.

### 11f. The generator script does not crash when regenerated

Run `python3 scripts/gen_journey_pages.py` from the repo root and confirm it exits 0. The output is deterministic; a diff against `git diff ka_journey_*.html` after regeneration should be empty if nothing in the script's `PAGES` list has drifted relative to the committed HTML.

*Expected count*: 0–3 consistency issues, mostly in 11c (status-label drift) and 11e (role-list drift).

---

## How to land the fixes

Same process as yesterday. Each fix is its own commit on `master`, attributed to Codex:

```
git add <files>
git -c user.name="Codex" -c user.email="codex@openai.com" \
    commit --author="Codex <codex@openai.com>" \
    -m "Ruthless-review fix (2026-04-20): <one-line subject>" \
    -m "<paragraph explaining what the bug was and what the fix does; \
        reference the probe number>"
```

Batch related fixes into one commit where they affect the same surface (e.g. one commit for "Probe 10: T4 sibling-row consistency"); don't fragment into one-per-file commits.

When all eleven probes are clean, write `docs/RUTHLESS_REVIEW_STATUS_2026-04-20.md` with:

- Probe-by-probe finding count (including the new 10 and 11)
- Commits landed (hashes + subjects)
- Any DK-decision items that remain open (rubric authorship stubs, payload-wiring priorities, missing-service blockers)
- Verdict: **CLEAN** / **CLEANED** (with N fixes) / **BLOCKED** (with reason)

Then DK executes Phase 3 of `docs/STAGING_DEPLOYMENT_PLAN_2026-04-19.md`.

---

## What this review is not

Unchanged from the 2026-04-19 brief:

- It is not a design review of the T4 deliverable structure itself — the six-section pattern (Goal · Steps · Files · Naive · Verification · Workspace) is settled; its contents may need revision, but that is a DK-scope decision, not a Codex fix.
- It is not a content review of the twelve journey pages' "Why it's hard" sections or "Who needs it" framings — those are the strategic-thinking payload DK wants in place, and domain disagreements belong in the panel process, not in this review.
- It is not a full accessibility audit of the new interaction patterns (sibling row, critique form). Flag severity-1 gaps (missing labels, no focus indicators, unreachable tabstops) as routine; a full WCAG-AA sweep is separate work.

---

## If you find something the brief doesn't anticipate

As yesterday: add it as a twelfth (or further) probe section in the status note and either fix it or flag it. The eleven probes are experience-driven, not a closed set; the twenty-seven new files introduce three new interaction patterns and it is plausible that one of them has a failure mode neither DK nor I anticipated. If you find one, call it Probe 12 and describe it clearly enough that the next review run can use it.

---

## Appendix — the twenty-seven files this review covers

For ease of scoping:

**Track 4 deliverable pages (`160sp/`)**
- `ka_t4_a_heuristic_audit.html` *(modified today — T4.a add-on callout added)*
- `ka_t4_b_scenarios.html`
- `ka_t4_b2_variant_evaluation.html`
- `ka_t4_c_usability_pilot.html`
- `ka_t4_d_severity_backlog.html`
- `ka_t4_e_reproducibility.html`
- `ka_t4_f_redesign.html`
- `ka_t4_g_final_report.html`
- `ka_t4_page.css`
- `ka_track4_hub.html` *(modified — Region 3.5 added)*

**Complicated-surface journey pages (repo root)**
- `ka_journeys.html` *(index)*
- `ka_journey_page.css`
- `ka_journey_surface.js`
- `ka_journey_en.html`
- `ka_journey_bn.html`
- `ka_journey_interpretation.html`
- `ka_journey_argumentation.html`
- `ka_journey_qa.html`
- `ka_journey_mechanism.html`
- `ka_journey_theory.html`
- `ka_journey_gaps.html`
- `ka_journey_evidence.html`
- `ka_journey_fronts.html`
- `ka_journey_ontology.html`
- `ka_journey_topic_inspector.html`
- `scripts/gen_journey_pages.py` *(tooling, not a user-facing page)*

Twenty-seven items in total (fifteen new HTML, two new CSS, one new JS, one new Python, two modified HTML, six new HTML under `160sp/`).

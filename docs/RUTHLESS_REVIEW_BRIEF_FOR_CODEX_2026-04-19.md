# Ruthless review brief — Codex, pre-staging-push

*Date*: 2026-04-19
*Requested by*: DK
*Executor*: Codex (GPT-5.x)
*Target*: the tip of the `master` branch of `Knowledge_Atlas` at the moment you run this review
*Expected output*: either a clean signal (no fixes needed) or one or more commits that close the gaps, followed by a status note at `docs/RUTHLESS_REVIEW_STATUS_2026-04-19.md`
*Companion doc*: `docs/STAGING_DEPLOYMENT_PLAN_2026-04-19.md` (Phase 2)

---

## Why this exists

DK wants a ruthless final review *before* the repo is pushed to GitHub and deployed to the staging server on xrlab. CW has landed substantial new work (class-state backend, AI-grading system, five topic-page variants, per-persona variants, classifier audit, strategic panels doc) across ~ 30 commits in the last two weeks. Before the whole tree ships to staging, a second AI worker with a critical eye should probe for the nine most-likely failure modes this kind of rapid iteration produces.

The spirit is the *ruthless prompt* methodology from COGS 160: after a first-pass implementation, a second AI is given a structured critique prompt that specifically hunts for flaws rather than politely reviewing. The goal is to find real problems before they ship, not to produce a nice-looking review document.

---

## Your nine probes

For each probe: identify specific failing files or lines, quote the problematic content, and either fix it with a commit or — if the fix needs a judgement call — flag it in the status note for DK.

### Probe 1 — Broken links

Walk every `href="..."` in every HTML file under the repo root and under `160sp/`. For each link target that is a local path (not `http://` or `https://`), confirm the target file exists and the anchor (if any) exists within it. The site validator already catches static `data-*` references; your job is to catch the rest, including:

- relative links to files that were renamed in recent commits (e.g. the old `data/pnu_articles/PDF-XXXX_pnu.html` links that I already repaired in `ka_topics.html` — verify none remain).
- anchor links to `#sections` that no longer exist on the target page.
- Links to files in sibling repos (`../Article_Eater_PostQuinean_v1_recovery/...`) that would break on the server — the server only has the `Knowledge_Atlas` repo, not its siblings.

Expected finding count: ≤ 5. Report zero if the tree is clean.

### Probe 2 — Unauthenticated admin paths

Open every page under `160sp/` plus the global `ka_admin*.html` pages (if any). Confirm that each page that renders data or controls that belong only to instructors has a client-side auth gate that fires before the data is visible. The pattern on `ka_admin.html` is the gold standard (`isAdmin()` check → `showAuthGate()` or `hideAuthGate()`). Pages to audit in particular:

- `160sp/ka_admin.html` — the gate exists; verify the new "wrong door" callout (added today) renders correctly.
- `160sp/ka_dashboard.html` — if it exists, does it gate?
- `160sp/ka_approve.html` — approval dashboard; should gate.
- Any `160sp/ka_*` page whose title or content implies maintainer-side data.

If any admin-side page lacks a gate, either add the gate using the existing pattern or flag the page for explicit DK decision (some maintainer-only pages may be intentionally public for documentation reasons).

Expected finding count: 0–3.

### Probe 3 — Persona-awareness regressions

Walk the per-persona variant pages (`ka_topics_public_view.html`, `ka_topics_student_view.html`, `ka_contribute_public.html`) and the role router on `ka_home.html`. Confirm:

- Each variant's top-level copy is calibrated to its persona (no maintainer jargon leaking through, no references to internal terminology like "EN", "warrant type", "crosswalk row" without glossary).
- The role router on `ka_home.html` points the right persona at the right variant (Researcher → `ka_topics_public_view.html`, Contributor → `ka_contribute_public.html`, 160 Student → `160sp/ka_student_setup.html`).
- The variants link back up the hierarchy sensibly (public variant has a "wait, I'm a maintainer" escape hatch; student variant has a "switch to public view" escape hatch).

Compare against the audit at `docs/USABILITY_AUDIT_USER_TYPES_2026-04-19.md` — any top-ten finding not yet addressed is a candidate for a commit.

Expected finding count: ≤ 3.

### Probe 4 — Copy contradictions

Across pages, look for two places that say different things about the same fact:

- Grading point allocation: 5 A0 + 5 A1 + 75 track + 15 F160 = 100. Any page that cites a different allocation is wrong.
- Number of tracks: 4 (T1 image tagging, T2 article finder, T3 VR, T4 UX research). Any page that lists a different count is wrong.
- Number of crosswalk rows: 102 (from Codex's build). Any page that cites a different number is stale.
- T1 frameworks: 11 (PP, SN, DP, DT, NM, IC, MS, EC, CB, MSI, IE_DPT). T1.5 theories: 13.
- Start / end of the Spring sprint: 2026-04-06 to 2026-06-15.

Any drift from these anchors is a finding.

Expected finding count: ≤ 5.

### Probe 5 — Validator warnings above threshold

Run `python3 scripts/site_validator.py` from the repo root. The current state is 0 errors, 176 warns. If any warning is LNK001 on a file that is NOT a template placeholder, investigate. If any SEC001 warning points at a page that reads from localStorage *before* the admin gate has fired, that's a real issue worth fixing. Cosmetic LNK001 warnings (the `${...}` placeholders) can be ignored.

Hard rule: errors > 0 blocks the deploy. Warnings in the SEC001 category that point at unauthenticated reads of sensitive state block the deploy too.

Expected finding count: 0 errors; 0–3 SEC001 issues worth investigating.

### Probe 6 — Mobile breakage

Open each of the following pages in a simulated 390 × 844 viewport (Chrome DevTools mobile emulation, iPhone 15 preset):

- `ka_home.html`
- `ka_topics_public_view.html`
- `ka_topic_heatmap_view.html` (expected to scroll horizontally; that's OK for a dense matrix)
- `ka_topic_dashboard_view.html` (three-col layout should collapse to stacked)
- `ka_article_view.html?id=PDF-0007`
- `ka_contribute_public.html`
- `ka_theories.html`
- One `ka_framework_*.html` page
- `160sp/ka_student_setup.html`

For each, confirm: no horizontal scroll on the main content, text is legible at default zoom, touch targets ≥ 44 px where they exist. Exempt: `ka_admin.html` (desktop-only), dense inspector pages that explicitly document horizontal scroll.

Expected finding count: 0–5 minor polishing items.

### Probe 7 — Dead code

Look for HTML, CSS, and JS that is no longer referenced by any reachable page. Don't remove it yet (some of it may be retained intentionally as design templates); flag it in the status note for DK decision.

Specific candidates:

- `ka_article.html` (794-line, hardcoded to PDF-0011) — superseded by `ka_article_view.html`.
- `ka_demo.html`, `ka_demo_v04.html` — demo pages; still useful?
- `ka_evidence.html`, `ka_gaps.html` — redirect stubs; are they still linked anywhere?
- Scripts referenced in HTML that no longer exist.

Expected finding count: 5–15 dead-code items, most retainable.

### Probe 8 — Payload staleness

Walk the `data/ka_payloads/*.json` files and verify that the HTML pages reading from them handle the current schema, not a schema that was in place at the time the page was written. Particular files:

- `data/ka_payloads/articles.json` — consumed by `ka_topics.html` and `ka_article_view.html`.
- `data/ka_payloads/topic_crosswalk.json` — consumed by the five variant pages.
- `data/ka_payloads/topic_hierarchy.json` — consumed by theories and topic views.
- `data/ka_payloads/topics.json` — consumed by `ka_topics.html`.

If a field used by a page has been renamed or removed in the current payload, that's a real bug. Spot-check three representative (page, payload) pairs.

Expected finding count: 0–2.

### Probe 9 — Security leaks

The Cowork sandbox has no production credentials, but the tree may contain accidentally committed secrets. Grep for:

- `token`, `api_key`, `password`, `secret`, `bearer` in uncommented lines of code and config.
- Hard-coded email addresses that aren't DK's public ones.
- UCSD PIDs or student identifiers that aren't the synthetic demo set (`A00000001`–`A00000015`).
- `.env` files, `.pem` files, `id_rsa`-shaped files that shouldn't be in a public repo.

The `.gitignore` already excludes `data/ka_auth.db` and `.env`; verify no other DB or credential file slips through.

Expected finding count: 0. Anything found here blocks the deploy outright.

---

## How to land the fixes

Each fix is its own commit on `master`, attributed to Codex:

```
git add <files>
git -c user.name="Codex" -c user.email="codex@openai.com" \
    commit --author="Codex <codex@openai.com>" \
    -m "Ruthless-review fix: <one-line subject>" \
    -m "<paragraph explaining what the bug was and what the fix does; \
        reference the probe number>"
```

Batch related fixes into one commit; don't make 20 one-liners.

When all probes are clean, write `docs/RUTHLESS_REVIEW_STATUS_2026-04-19.md` with:

- Probe-by-probe finding count
- Commits landed (hashes + subjects)
- Any DK-decision items that remain open
- Verdict: CLEAN / CLEANED (with N fixes) / BLOCKED (with reason)

Then DK executes Phase 3 of `docs/STAGING_DEPLOYMENT_PLAN_2026-04-19.md`.

---

## What this review is not

- It is not a design review. The strategic design decisions (which variant is canonical, what the panel plan should be) are DK decisions and are settled by the panels in `docs/COMPLICATED_PAGES_JOURNEYS_AND_PANELS_2026-04-19.md`.
- It is not a content review of the T1 framework pages or T1.5 theory pages; those carry "Working draft · expert review in progress" banners and go through their own domain panels.
- It is not a full accessibility audit. Where severity-1 accessibility gaps are obvious (missing alt text on an image, a form field with no label), flag them; a full WCAG-AA audit is separate work.

---

## If you find something the brief doesn't anticipate

If your walk surfaces a failure mode not covered by the nine probes (e.g., a performance issue that would make a page unusable on the server's CPU budget), add it as a tenth probe section in the status note and fix it. The nine probes are prior experience, not a closed set.

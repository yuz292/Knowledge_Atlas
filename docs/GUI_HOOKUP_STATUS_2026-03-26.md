# GUI Hookup Status — 2026-03-26

## Bottom line

The website is no longer mostly mockup. The core Atlas pages and the three epistemic layers are payload-backed and live. The remaining weakness is not shell/navigation; it is workflow persistence.

## What is fully or meaningfully hooked up

These pages load generated JSON payloads from `data/ka_payloads` and render live rebuild-derived content:

- `ka_topics.html`
- `ka_evidence.html`
- `ka_gaps.html`
- `ka_articles.html`
- `ka_article_search.html`
- `ka_dashboard.html`
- `ka_argumentation.html`
- `ka_annotations.html`
- `ka_interpretation.html`

## Layer data actually present

Current layer payloads are non-empty and can drive page content:

- Argumentation layer:
  - `12` debate clusters
  - `263` paper nodes
  - `5335` claim nodes
  - `75858` claim edges
- Annotation layer:
  - `61` active annotations
  - `57` touched beliefs
  - `6` annotation types
- Interpretation layer:
  - `3` high-VOI frontier questions
  - `9` medium-VOI frontier questions
  - `20` validation beliefs
  - average completeness `0.591`

## New workflow hookup in this pass

A shared workflow-state adapter now exists:

- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_workflow_store.js`

Pages now reading shared contributor/admin state through that adapter instead of each inventing separate localStorage handling:

- `ka_login.html`
- `ka_register.html`
- `ka_article_propose.html`
- `ka_articles.html`
- `ka_dashboard.html`
- `ka_approve.html`

Most important visible improvement:

- `ka_approve.html` now renders its pending/approved/rejected/roster views from shared registration state instead of fixed demo applicants.

## Should more of the GUI use a database?

Yes, but only for workflow state.

A database is justified for:

- accounts/auth
- registrations and approval decisions
- contributor assignments
- intake submissions
- saved hypotheses and track progress

A database is not necessary for the read-mostly scientific display layers right now. For those, generated JSON payloads are a good bridge because:

- rebuild artifacts are batch-produced
- the site needs walkthrough realism before a full web backend exists
- payloads keep the scientific surfaces deterministic and inspectable

So the correct split is:

- scientific corpus/layer pages: payload-backed is fine for now
- contributor/admin workflow: should move to a real DB-backed service next

## What still remains only partially real

These areas still rely on prototype-style persistence or staged logic:

- login/register auth semantics
- contributor assignment claiming
- durable multi-user course state
- instructor settings/configuration
- article proposal / approval as true multi-user queue writes

## What the user can expect right now

A walkthrough should now work for:

- topic browsing
- evidence browsing
- gap browsing
- article browsing and article-to-layer drilldown
- argumentation / annotation / interpretation inspection
- contributor dashboard review
- article intake review
- instructor approval queue review

The user should not yet expect:

- real multi-user synchronization
- a production auth backend
- durable shared workflow state across machines without exporting/importing local state

## Current surfaced corpus quality

Current `json_status` summary for the `250` KA-visible papers:

- titles good: `224`
- abstracts good: `69`
- abstracts provisional: `33`
- abstracts missing: `148`
- DOI good: `69`
- sample_n accepted: `25`
- p_value accepted: `13`
- effect_size accepted: `6`
- main_conclusion accepted: `93`

So the GUI is now meaningfully driven by imperfect data, which is the right state for site walkthrough and QA.

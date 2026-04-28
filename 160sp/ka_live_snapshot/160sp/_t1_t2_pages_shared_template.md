# Shared Template & Conventions for the New Track Pages

*This file is internal documentation for the eight new HTML pages I'm authoring (t1_intro, t1_task1, t1_task2, t1_task3, t2_intro, t2_task1, t2_task2, t2_task3). It captures the shared HTML skeleton, the side-nav pattern, the GitHub-submission block, and the colour/typography conventions, so each page is consistent. Not student-facing.*

---

## Page skeleton (every new page uses this structure)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{TRACK} — {PAGE} · COGS 160</title>
  <link rel="stylesheet" href="_track_pages_shared.css"> <!-- see below -->
</head>
<body>

  <!-- 1. TOP FIXED NAV (matches the rest of 160sp) -->
  <nav class="top-nav">
    <a class="wordmark" href="../ka_home.html">Knowledge Atlas</a>
    <div class="nav-center">
      <a href="../ka_topics.html">Explore</a>
      <a href="../ka_evidence.html">Evidence</a>
      <a href="../ka_gaps.html">Gaps</a>
      <a href="../ka_article_search.html">Articles</a>
      <a href="../ka_contribute.html">Contribute</a>
      <a href="ka_student_setup.html">Course</a>
      <a href="ka_schedule.html">160 Syllabus</a>
      <a href="ka_tracks.html" class="active">Tracks</a>
    </div>
    <div class="nav-right"><span class="mode-pill">STUDENT</span></div>
  </nav>

  <!-- 2. BREADCRUMB -->
  <div class="breadcrumb">
    <a href="ka_tracks.html">All Tracks</a> /
    <a href="{TRACK_INTRO}.html">{TRACK NAME}</a> /
    <span>{PAGE NAME}</span>
  </div>

  <!-- 3. PAGE LAYOUT: side-nav + content -->
  <div class="page-grid">

    <!-- 3a. SIDE NAV (intro + 3 tasks; current page highlighted) -->
    <aside class="side-nav">
      <div class="side-nav-title">{TRACK NAME}</div>
      <a href="{TRACK}_intro.html" class="{active|''}">Track Overview</a>
      <a href="{TRACK}_task1.html" class="{active|''}">Task 1: {short title}</a>
      <a href="{TRACK}_task2.html" class="{active|''}">Task 2: {short title}</a>
      <a href="{TRACK}_task3.html" class="{active|''}">Task 3: {short title}</a>
      <div class="side-nav-divider"></div>
      <a href="ka_tracks.html" class="side-nav-back">← All Tracks</a>
    </aside>

    <!-- 3b. MAIN CONTENT -->
    <main class="content">
      <!-- Hero -->
      <header class="hero">
        <div class="hero-track">{TRACK NAME}</div>
        <h1>{Page title}</h1>
        <p class="hero-sub">{One-sentence summary of what this page covers}</p>
      </header>

      <!-- Body — varies per page (sections, code blocks, tables, AI prompts, etc.) -->
      {... per-page content ...}

      <!-- GITHUB SUBMISSION SECTION (every task page; abridged on intro page) -->
      <section class="github-submission">
        <h2 id="submission">How to submit this task on GitHub</h2>
        {... see Section "GitHub Submission Block" below ...}
      </section>

    </main>
  </div>

  <!-- 4a. WITHIN-TRACK NAV (prev / next; only on task pages, not intros) -->
  <nav class="track-footer-nav" aria-label="Within-track navigation">
    <a href="{prev page}.html" class="prev">← {prev page name}</a>
    <a href="{next page}.html" class="next">{next page name} →</a>
  </nav>

  <!-- 4b. SITE FOOTER (every page; lets users escape back to global / portal / sitemap) -->
  <footer class="site-footer">
    <div class="site-footer-inner">
      <div class="site-footer-col">
        <div class="site-footer-title">Knowledge Atlas</div>
        <a href="../ka_home.html">Global home</a>
        <a href="../ka_sitemap.html">Site map</a>
      </div>
      <div class="site-footer-col">
        <div class="site-footer-title">COGS 160 SP</div>
        <a href="ka_tracks.html">Tracks portal</a>
        <a href="ka_student_setup.html">Course setup</a>
        <a href="ka_schedule.html">Syllabus</a>
      </div>
      <div class="site-footer-col">
        <div class="site-footer-title">This track</div>
        <a href="{TRACK_INTRO}.html">Track overview</a>
        <a href="#submission">Submit on GitHub</a>
      </div>
      <div class="site-footer-meta">
        COGS 160 Spring 2026 · Prof. David Kirsh, UCSD Cognitive Science.
        Page maintained as part of the Knowledge Atlas project.
      </div>
    </div>
  </footer>

</body>
</html>
```

### Logo / wordmark — must always link to global home

Every page's top-nav `.wordmark` element MUST be a clickable link to `../ka_home.html` (the Knowledge Atlas global home). This is the user's escape hatch from any track page back to the top-level site. The pattern:

```html
<a class="wordmark" href="../ka_home.html" aria-label="Knowledge Atlas — global home">
  Knowledge Atlas
</a>
```

This applies regardless of which portal the user is in — 160 SP students who land on `t1_task2.html` need to see the wordmark and know that clicking it returns them to the *global* Atlas home, not the COGS 160 hub. The COGS 160 hub link lives separately in the top nav (`Course` → `ka_student_setup.html`) and in the footer ("Tracks portal" → `ka_tracks.html`).

### Site footer CSS

```css
.site-footer {
  background: var(--navy); color: #b8d8d4;
  margin-top: 80px; padding: 32px 24px 24px;
  border-top: 4px solid var(--teal);
}
.site-footer-inner {
  max-width: 1120px; margin: 0 auto;
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 32px; padding-bottom: 22px;
}
.site-footer-col { display: flex; flex-direction: column; gap: 6px; }
.site-footer-title {
  font-family: Georgia, serif; font-size: 0.86rem;
  color: var(--teal-lt); margin-bottom: 4px;
  letter-spacing: 0.04em;
}
.site-footer a {
  color: #b8d8d4; text-decoration: none; font-size: 0.84rem;
  padding: 2px 0;
}
.site-footer a:hover { color: var(--white); text-decoration: underline; }
.site-footer-meta {
  grid-column: 1 / -1;
  border-top: 1px solid rgba(255,255,255,0.08);
  padding-top: 16px; font-size: 0.76rem; color: #8aa8a4;
  text-align: center;
}
@media (max-width: 700px) {
  .site-footer-inner { grid-template-columns: 1fr; gap: 20px; }
}
```

### Sitemap — what to do

Two sitemaps already exist in `ka_live_snapshot/`:

- **`ka_sitemap.html`** (54K) — the user-facing sitemap with the standard global nav. Footer links should point here.
- **`SITEMAP_HIERARCHICAL.html`** (35K) — a developer-oriented tree view; not for the student footer.

After my work, both sitemaps will need a small append to add the new pages (`t1_intro.html`, `t1_task1.html`, `t1_task2.html`, `t1_task3.html`, `t2_intro.html`, `t2_task1.html`, `t2_task2.html`, `t2_task3.html`) under their respective track sections. This is a separate small task; for now, the footer link points to the existing sitemap and a follow-up commit appends the new entries.

---

## Side-nav design

A **left-rail sidebar** sits next to the main content on screens ≥ 900px wide; on narrower screens it collapses to a horizontal pill bar above the content. The active page is highlighted with the teal accent colour. The list:

- *Track Overview* (the intro page) — always first
- *Task 1: …*
- *Task 2: …*
- *Task 3: …*
- horizontal divider
- *← All Tracks* (back-link to `ka_tracks.html`)

CSS for the side-nav:

```css
.page-grid {
  max-width: 1200px;
  margin: 80px auto 100px;
  padding: 0 28px;
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 36px;
}
.side-nav {
  position: sticky; top: 80px; align-self: start;
  background: var(--white); border: 1px solid var(--border);
  border-radius: 8px; padding: 18px 16px;
  font-size: 0.85rem;
}
.side-nav-title {
  font-family: Georgia, serif; font-size: 0.8rem;
  color: var(--muted); text-transform: uppercase;
  letter-spacing: 0.08em; margin-bottom: 12px;
}
.side-nav a {
  display: block; padding: 8px 10px; color: var(--ink);
  text-decoration: none; border-radius: 4px; margin-bottom: 4px;
}
.side-nav a:hover { background: var(--teal-bg); color: var(--teal); }
.side-nav a.active {
  background: var(--teal-bg); color: var(--teal);
  font-weight: 600; border-left: 3px solid var(--teal);
}
.side-nav-divider {
  height: 1px; background: var(--border); margin: 12px 0;
}
.side-nav-back {
  font-size: 0.78rem; color: var(--muted) !important;
}
@media (max-width: 900px) {
  .page-grid { grid-template-columns: 1fr; }
  .side-nav {
    position: static;
    display: flex; flex-wrap: wrap; gap: 6px;
    padding: 10px 14px;
  }
  .side-nav-title, .side-nav-divider, .side-nav-back { display: none; }
  .side-nav a {
    display: inline-block; margin-bottom: 0;
    font-size: 0.78rem; padding: 5px 10px;
    border: 1px solid var(--border);
  }
}
```

---

## Colour palette and typography (inherited from existing 160sp pages)

```css
:root {
  --navy: #1C3D3A;
  --teal: #2A7868;
  --teal-lt: #5AC8AA;
  --teal-bg: #E6F5F0;
  --amber: #E8872A;
  --amber-lt: #FFF3E0;
  --amber-dk: #9a5010;
  --cream: #F7F4EF;
  --ink: #2C2C2C;
  --muted: #6B6B6B;
  --border: #D8D0C5;
  --white: #FFFFFF;
  --rose: #A84F6B;
  --rose-lt: #F8EBF0;
  --blue: #3A6EA8;
  --blue-lt: #EBF2F8;
}
body { font-family: Arial, sans-serif; background: var(--cream); color: var(--ink); }
h1, h2, h3, .hero h1, .section-title { font-family: Georgia, serif; }
code, pre { font-family: SFMono-Regular, Menlo, Consolas, monospace; }
```

---

## Callout / box conventions

- `.callout-teal` — informational
- `.callout-amber` — caution / requirement
- `.callout-blue` — context
- `.callout-rose` — warning / "do not"
- `.ai-box` (light purple `#F0EBF8`) — AI prompt students copy verbatim, italic Georgia serif
- `.code-block` — bash / Python / SQL code, dark teal background `#1a2a28`, mono font, overflow-x auto

---

## GitHub Submission Block

The reusable submission block, embedded on each task page (per-task variant) and abridged on the intro page (lifecycle summary).

### Per-task variant (one block per task page)

```html
<section class="github-submission">
  <h2 id="submission">Submit Task {N} on GitHub</h2>

  <p>Each track has one branch per student, named <code>track{N}/your-name</code>
  (lowercase, hyphenated — e.g., <code>track1/jane-doe</code>). All three tasks in
  a track live on this single branch. You'll open one Pull Request per completed
  task so the instructor can review tasks independently.</p>

  <h3>One-time setup (do once at the start of the track)</h3>
  <pre><code class="lang-bash"># 1. Fork the relevant repo on GitHub (use the Fork button on the repo page)
#    For Track {N}, fork: {LIST OF REPOS THIS TASK NEEDS}

# 2. Clone your fork to your machine
git clone git@github.com:&lt;YOUR-USERNAME&gt;/{REPO}.git
cd {REPO}

# 3. Add the upstream remote so you can pull instructor updates
git remote add upstream git@github.com:dkirsh/{REPO}.git

# 4. Create your track branch, off the latest main
git fetch upstream
git checkout -b track{N}/&lt;your-name&gt; upstream/main
</code></pre>

  <h3>Working on Task {N}</h3>
  <pre><code class="lang-bash"># Make sure you're on your track branch
git checkout track{N}/&lt;your-name&gt;

# Commit early and often as you work — small, reviewable commits
git add &lt;files-you-changed&gt;
git commit -m "task{N}: short description of what this commit does"

# Push to your fork at the end of each work session
git push origin track{N}/&lt;your-name&gt;
</code></pre>

  <h3>Submitting Task {N} for review</h3>
  <p>When Task {N} is complete and all the deliverables on this page are checked off:</p>

  <ol>
    <li>Make sure your latest work is pushed: <code>git push origin track{N}/&lt;your-name&gt;</code></li>
    <li>On GitHub, open a Pull Request from <code>&lt;YOUR-USERNAME&gt;:track{N}/&lt;your-name&gt;</code> to <code>dkirsh:main</code></li>
    <li>Title the PR: <code>Track {N} · Task {N}: &lt;short title&gt; — &lt;your name&gt;</code></li>
    <li>In the PR body, paste your <strong>file manifest</strong> (run <code>git diff --name-only upstream/main</code>) and a one-paragraph summary of what you built and what you tested.</li>
    <li>Add the label <code>track{N}-task{N}-review</code> and tag the instructor (<code>@dkirsh</code>).</li>
    <li>Leave the PR open. <strong>Do not merge.</strong> The instructor will review and either merge, request changes, or comment for follow-up.</li>
  </ol>

  <p>When you start Task {N+1}, keep working on the same <code>track{N}/&lt;your-name&gt;</code>
  branch — additional commits will appear in your existing PR <em>only until you open the
  Task {N+1} PR</em>, at which point the new task gets its own PR off the same branch (use
  GitHub's "compare" feature with the previous task's merge commit as the base).</p>

  <h3>If you get stuck</h3>
  <ul>
    <li><strong>Merge conflict:</strong> <code>git fetch upstream &amp;&amp; git rebase upstream/main</code>, resolve conflicts, then <code>git push --force-with-lease</code>.</li>
    <li><strong>Forgot to commit before switching machines:</strong> <code>git stash</code> on the old machine, push, then <code>git stash pop</code> after pulling on the new machine.</li>
    <li><strong>Unsure if the instructor has reviewed:</strong> the PR page on GitHub shows review state. Don't email; let the PR system carry the conversation.</li>
  </ul>
</section>
```

### Intro-page variant (one block on each intro page, summarising the lifecycle)

```html
<section class="github-submission">
  <h2 id="submission">How submission works for Track {N}</h2>

  <p>Track {N} uses a single git branch per student — <code>track{N}/your-name</code>
  — across all {N_TASKS} tasks. Each completed task is submitted as its own Pull
  Request to the instructor. The full mechanics are on each task page; here's the
  lifecycle in one paragraph:</p>

  <ol>
    <li><strong>Once at the start of the track:</strong> fork the track's repos, clone, set the upstream remote, create <code>track{N}/your-name</code> off <code>upstream/main</code>.</li>
    <li><strong>Continuously while working:</strong> commit small, push at the end of each session.</li>
    <li><strong>At the end of each task:</strong> open a Pull Request from your branch to <code>dkirsh:main</code>, title it <code>Track {N} · Task {N}: ... — your name</code>, paste your file manifest, tag <code>@dkirsh</code>, do not merge.</li>
    <li><strong>Across tasks:</strong> keep using the same branch; additional task PRs are opened against the previous task's merge commit.</li>
  </ol>

  <p>The detailed commands and the per-task PR title format are on each task page
  under "Submit Task {N} on GitHub."</p>
</section>
```

---

## "New pages first" — change to ka_tracks.html

The existing track landing page lists `ka_track1_tagging.html`, `ka_track2_pipeline.html`, `ka_track3_vr.html`, `ka_track4_ux.html`. After this work, the page reorders to:

1. **NEW (recommended):** Track 1 Image Tagger → `t1_intro.html`
2. **NEW (recommended):** Track 2 Article Finder → `t2_intro.html`
3. Track 3 VR → `ka_track3_vr.html` (unchanged for now; will be migrated to `t3_intro.html` when its source markdown is supplied)
4. Track 4 UX → `ka_track4_ux.html` (same; pending source)
5. *Legacy assignment pages (kept for reference):* `ka_track1_tagging.html`, `ka_track2_pipeline.html`, `ka_article_finder_assignment.html`, etc., listed under a "Legacy / archive" subsection at the bottom.

---

*End of internal template document.*

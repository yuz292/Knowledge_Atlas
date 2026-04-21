/*  ka_journey_surface.js — shared helpers for ka_journey_{name}.html
    pages. Provides three surfaces:
      1. renderJourneySidebar(slug)   left-hand sub-navigation with six
                                      collapsible group cards (twisties).
      2. renderJourneySiblings(slug)  secondary horizontal cross-link row.
      3. saveCritique / restoreCritique for the per-role critique drafts.

    Do NOT confuse with ka_journey_nav.js, which renders the user-type
    journey sidebar on other site pages. This script is specific to
    the complicated-surface meta pages.

    Bug-fix pass 2026-04-20 PM (ruthless-review P0s + P1s):
      P0-2 — duplicate class attr on side-index anchor fixed.
      P0-3 — sidebar total count computed dynamically from GROUPS.
      P0-4 — aria-expanded now tracks actual visible state.
      P1-7 — current group's head gets a tinted background + bold weight.
      P1-9 — "Collapse all" affordance added; on __index__ only the
             first and AF groups auto-open by default.
      P1-10 — Layer F label shortened to "Evidence density and gaps".
*/

(function () {
  // ── Six card groups. The final one (AF) is flagged with accent:"af"
  //    so the sidebar renders it with an amber palette.
  const GROUPS = [
    {
      label: "Belief & causal networks",
      slugs: [
        { slug: "en", title: "Epistemic Network (Web of Belief)", status: "naive" },
        { slug: "bn", title: "Bayesian Network viewer", status: "naive" },
      ],
    },
    {
      label: "Interpretation, argument, QA",
      slugs: [
        { slug: "interpretation", title: "Interpretation layer", status: "naive" },
        { slug: "argumentation", title: "Argumentation layer", status: "absent" },
        { slug: "qa", title: "Question-answering layer", status: "prototype" },
      ],
    },
    {
      label: "Causal pathways and frameworks",
      slugs: [
        { slug: "mechanism", title: "Mechanism layer", status: "naive" },
        { slug: "theory", title: "Theory deep-dive", status: "prototype" },
      ],
    },
    {
      // P1-10: previously "Where the evidence is dense — or absent" —
      // too opaque at a glance; shortened so the sidebar reads clean.
      label: "Evidence density and gaps",
      slugs: [
        { slug: "gaps", title: "Gaps in the evidence base", status: "naive" },
        { slug: "evidence", title: "Evidence-landscape map", status: "prototype" },
        { slug: "fronts", title: "Research fronts", status: "absent" },
      ],
    },
    {
      label: "What is in the database",
      slugs: [
        { slug: "ontology", title: "Ontology inspector", status: "prototype" },
        { slug: "topic_inspector", title: "Topic inspector", status: "naive" },
      ],
    },
    // Article Finder problems — amber, distinguished by accent:"af"
    {
      label: "Article Finder problems",
      accent: "af",
      slugs: [
        { slug: "af_references", title: "AF-1 · Articles referred to in corpus", status: "absent" },
        { slug: "af_roi",        title: "AF-2 · ROI-based candidate generator", status: "absent" },
        { slug: "af_neuro",      title: "AF-3 · Plausible Neural Underpinnings", status: "absent" },
      ],
    },
  ];

  // Flattened list for the siblings row.
  const SIBLINGS = GROUPS.flatMap(g =>
    g.slugs.map(s => ({ slug: s.slug, label: s.title.split(" ")[0], full: s.title }))
  );

  // ── Sub-navigation sidebar renderer ───────────────────────────────
  window.renderJourneySidebar = function (currentSlug) {
    const mount = document.getElementById("j-sidebar-slot");
    if (!mount) return;

    // Which group contains the current slug?
    const activeGroupIdx = GROUPS.findIndex(g => g.slugs.some(s => s.slug === currentSlug));

    // P1-9: on the index page, auto-open only the first and the AF groups.
    // On any other page, open the group containing the current slug.
    const afIdx = GROUPS.findIndex(g => g.accent === "af");
    const autoOpenOnIndex = new Set([0, afIdx].filter(i => i >= 0));

    // P0-3: compute total count dynamically so it cannot drift.
    const totalSurfaces = GROUPS.reduce((n, g) => n + g.slugs.length, 0);

    // P0-2: single class attribute on the index anchor.
    const indexActive = currentSlug === "__index__";
    const parts = [
      `<div class="side-label">Complicated surfaces</div>`,
      `<a class="side-index${indexActive ? " current" : ""}" href="ka_journeys.html">` +
        `↺ Index · all ${totalSurfaces} surfaces</a>`,
      // P1-9: collapse-all affordance
      `<button type="button" class="side-toggle-all" aria-label="Collapse all groups">` +
        `Collapse all</button>`,
    ];

    GROUPS.forEach((g, gi) => {
      // P0-4: a single isOpen variable drives BOTH the visual class and
      // the ARIA attribute, so screen readers announce the true state.
      const isOpen = gi === activeGroupIdx
                  || (indexActive && autoOpenOnIndex.has(gi));
      const openCls = isOpen ? " open" : "";
      const accentCls = g.accent ? ` side-accent-${g.accent}` : "";
      // P1-7: mark the group that contains the current page so CSS can
      // give its header a tinted background + bold weight.
      const currentCls = gi === activeGroupIdx ? " side-group-current" : "";
      parts.push(`<div class="side-group${openCls}${accentCls}${currentCls}" data-group-idx="${gi}">`);
      parts.push(
        `<button type="button" class="side-head" aria-expanded="${isOpen}">` +
          `<span class="twisty">▶</span>` +
          `<span>${g.label}</span>` +
        `</button>`
      );
      parts.push(`<div class="side-body">`);
      g.slugs.forEach(s => {
        const current = s.slug === currentSlug ? " current" : "";
        parts.push(
          `<a href="ka_journey_${s.slug}.html" class="${current.trim()}">` +
            `${s.title}` +
            `<span class="side-status ${s.status}">${s.status}</span>` +
          `</a>`
        );
      });
      parts.push(`</div>`);
      parts.push(`</div>`);
    });

    mount.innerHTML = parts.join("\n");

    // Wire twisty click-to-toggle with aria-expanded in sync.
    mount.querySelectorAll(".side-group > button.side-head").forEach(btn => {
      btn.addEventListener("click", () => {
        const g = btn.parentElement;
        const nowOpen = g.classList.toggle("open");
        btn.setAttribute("aria-expanded", nowOpen);
      });
    });

    // Wire collapse-all.
    const toggleAll = mount.querySelector(".side-toggle-all");
    if (toggleAll) {
      toggleAll.addEventListener("click", () => {
        const anyOpen = mount.querySelector(".side-group.open");
        const target = !anyOpen; // if everything is closed, open all; else close all
        mount.querySelectorAll(".side-group").forEach(g => {
          g.classList.toggle("open", target);
          const head = g.querySelector("button.side-head");
          if (head) head.setAttribute("aria-expanded", target);
        });
        toggleAll.textContent = target ? "Collapse all" : "Expand all";
      });
    }
  };

  // ── Secondary horizontal sibling row ──────────────────────────────
  window.renderJourneySiblings = function (currentSlug) {
    const mount = document.getElementById("j-siblings-slot");
    if (!mount) return;
    const parts = [`<span class="sb-label">Cross-jump</span>`];
    parts.push(`<a href="ka_journeys.html" title="Index">↺ index</a>`);
    SIBLINGS.forEach(s => {
      const cls = s.slug === currentSlug ? "current" : "";
      parts.push(
        `<a href="ka_journey_${s.slug}.html" class="${cls}" title="${s.full}">${s.label}</a>`
      );
    });
    mount.innerHTML = parts.join("");
  };

  // ── Per-role critique drafts (localStorage-backed) ────────────────
  window.saveCritique = function (pageKey) {
    const roles = ["public_visitor", "160_student", "researcher", "practitioner", "admin"];
    const data = {};
    roles.forEach(r => {
      const ta = document.getElementById("crit_" + r);
      if (ta) data[r] = ta.value;
    });
    try { localStorage.setItem("ka.critique." + pageKey, JSON.stringify(data)); } catch (e) {}
    const s = document.getElementById("j-crit-status");
    if (s) {
      s.classList.add("show");
      setTimeout(() => s.classList.remove("show"), 2500);
    }
  };

  window.restoreCritique = function (pageKey) {
    try {
      const raw = localStorage.getItem("ka.critique." + pageKey);
      if (!raw) return;
      const data = JSON.parse(raw);
      Object.keys(data || {}).forEach(r => {
        const ta = document.getElementById("crit_" + r);
        if (ta) ta.value = data[r] || "";
      });
    } catch (e) {}
  };
})();

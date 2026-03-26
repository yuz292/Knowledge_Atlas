/**
 * ka_about_page.js
 * Knowledge Atlas — About This Page anchor section
 *
 * Injects an always-visible "About this page" footer section and a small
 * floating "About" link that anchors to it. Does NOT require login.
 * Complements ka_page_function.js (the login-gated deep-dive overlay).
 *
 * Usage: include <script src="ka_about_page.js"></script> in every KA page,
 * with window.KA_ABOUT_PAGE defined before or after the script tag.
 *
 * window.KA_ABOUT_PAGE = {
 *   pageId:    'ka_sensors',              // filename sans extension
 *   objective: 'One-sentence statement of what this page does.',
 *   users:     'Students at the operationalization stage; researchers selecting instruments',
 *   uses: [
 *     'Browse 27 physiological, neural, and behavioural measures',
 *     'Map a construct to a measurable signal before writing a hypothesis',
 *     'Check practical constraints (lab vs. field, cost tier)'
 *   ]
 * };
 *
 * The injected #about-this-page section sits at the very bottom of <body>,
 * below all page content, so it can be linked with href="#about-this-page".
 * A floating "About this page" badge is fixed to the bottom-right (above the
 * existing version-badge, if present) and scrolls to the section on click.
 */

(function () {
  'use strict';

  /* ── Styles ─────────────────────────────────────────────────────────── */
  const CSS = `
    /* Floating trigger link */
    #ka-about-trigger {
      position: fixed; bottom: 52px; right: 24px; z-index: 9000;
      background: rgba(28,61,58,0.82); color: #A8C8BF;
      font-family: Arial, sans-serif; font-size: 0.67rem; font-weight: 700;
      letter-spacing: 0.1em; text-transform: uppercase;
      padding: 4px 11px; border-radius: 10px; cursor: pointer;
      border: none; text-decoration: none;
      transition: background 0.15s, color 0.15s;
      display: inline-block;
      user-select: none;
    }
    #ka-about-trigger:hover { background: #1C3D3A; color: #F5A623; }

    /* About section ── injected before </body> */
    #about-this-page {
      background: #F0EDE7;
      border-top: 2px solid #D4CDC4;
      font-family: Arial, sans-serif;
      padding: 40px 32px 48px;
      margin-top: 0;
      scroll-margin-top: 72px; /* offset for fixed nav */
    }

    .ka-about-inner {
      max-width: 820px;
      margin: 0 auto;
    }

    .ka-about-eyebrow {
      font-size: 0.65rem; font-weight: 700; letter-spacing: 0.14em;
      text-transform: uppercase; color: #9A8A78; margin-bottom: 14px;
      display: flex; align-items: center; gap: 8px;
    }
    .ka-about-eyebrow::before {
      content: ""; display: inline-block;
      width: 20px; height: 2px; background: #C4B8A8; border-radius: 1px;
    }

    .ka-about-objective {
      font-family: Georgia, serif;
      font-size: 1.05rem;
      color: #1C3D3A;
      line-height: 1.6;
      margin-bottom: 24px;
      font-weight: 400;
    }

    .ka-about-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }
    @media (max-width: 640px) {
      .ka-about-grid { grid-template-columns: 1fr; }
    }

    .ka-about-card {
      background: #fff;
      border: 1px solid #DDD6CD;
      border-radius: 8px;
      padding: 18px 20px;
    }

    .ka-about-card-label {
      font-size: 0.65rem; font-weight: 700; letter-spacing: 0.12em;
      text-transform: uppercase; color: #B0A090;
      margin-bottom: 10px;
    }

    .ka-about-card-text {
      font-size: 0.88rem; color: #3A3228; line-height: 1.6;
    }

    .ka-about-uses-list {
      list-style: none; padding: 0; margin: 0;
    }
    .ka-about-uses-list li {
      font-size: 0.86rem; color: #3A3228; line-height: 1.55;
      padding: 5px 0 5px 18px; position: relative;
      border-bottom: 1px solid #EEE9E3;
    }
    .ka-about-uses-list li:last-child { border-bottom: none; }
    .ka-about-uses-list li::before {
      content: "→"; position: absolute; left: 0;
      color: #E8872A; font-size: 0.78rem; top: 6px;
    }

    .ka-about-footer-row {
      margin-top: 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
    }
    .ka-about-page-id {
      font-size: 0.72rem; color: #B0A090; font-family: monospace;
      letter-spacing: 0.04em;
    }
    .ka-about-fn-link {
      font-size: 0.72rem; color: #E8872A; cursor: pointer;
      text-decoration: none; background: none; border: none;
      font-family: Arial, sans-serif; display: none; /* shown when logged in */
    }
    .ka-about-fn-link:hover { text-decoration: underline; }
  `;

  /* ── Build the section ──────────────────────────────────────────────── */
  function buildSection(spec) {
    const usesHtml = Array.isArray(spec.uses) && spec.uses.length
      ? `<ul class="ka-about-uses-list">${spec.uses.map(u => `<li>${u}</li>`).join('')}</ul>`
      : `<p class="ka-about-card-text">${spec.uses || '—'}</p>`;
    const resourcesHtml = Array.isArray(spec.resources) && spec.resources.length
      ? `<div class="ka-about-card" style="margin-top:20px;">
          <div class="ka-about-card-label">Related docs and routes</div>
          <ul class="ka-about-uses-list">${spec.resources.map(function (row) {
            return `<li><a href="${row.href}" style="color:#1C3D3A; font-weight:700; text-decoration:none;">${row.label}</a></li>`;
          }).join('')}</ul>
        </div>`
      : '';

    const section = document.createElement('section');
    section.id = 'about-this-page';
    section.innerHTML = `
      <div class="ka-about-inner">
        <div class="ka-about-eyebrow">About this page</div>
        <p class="ka-about-objective">${spec.objective || 'No objective defined for this page.'}</p>
        <div class="ka-about-grid">
          <div class="ka-about-card">
            <div class="ka-about-card-label">Primary users</div>
            <div class="ka-about-card-text">${spec.users || '—'}</div>
          </div>
          <div class="ka-about-card">
            <div class="ka-about-card-label">Primary uses</div>
            ${usesHtml}
          </div>
        </div>
        ${resourcesHtml}
        <div class="ka-about-footer-row">
          <span class="ka-about-page-id">${spec.pageId || ''}</span>
          <button class="ka-about-fn-link" id="ka-about-fn-open"
            title="Open the full page function specification (GUI track evaluators)">
            ⊙ Full function spec →
          </button>
        </div>
      </div>
    `;
    return section;
  }

  /* ── Build the floating trigger button ─────────────────────────────── */
  function buildTrigger() {
    const a = document.createElement('a');
    a.id = 'ka-about-trigger';
    a.href = '#about-this-page';
    a.textContent = '⊕ About this page';
    a.title = 'What this page is for, who it serves, and how to use it';
    // Smooth scroll on click
    a.addEventListener('click', function (e) {
      const sec = document.getElementById('about-this-page');
      if (sec) {
        e.preventDefault();
        sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
    return a;
  }

  /* ── Wire the "Full function spec" link inside the about section ────── */
  function wireSpecLink() {
    const link = document.getElementById('ka-about-fn-open');
    if (!link) return;
    const isLoggedIn = localStorage.getItem('ka_logged_in') === '1' ||
                       sessionStorage.getItem('ka_logged_in') === '1' ||
                       new URLSearchParams(window.location.search).get('fnspec') === '1';
    if (isLoggedIn) {
      link.style.display = 'inline';
      link.addEventListener('click', function () {
        // Open the ka_page_function panel if it exists on this page
        const btn = document.getElementById('ka-fn-btn');
        if (btn) { btn.click(); }
      });
    }
    // Also listen for login events during the same session
    window.addEventListener('storage', function (e) {
      if (e.key === 'ka_logged_in') {
        link.style.display = e.newValue === '1' ? 'inline' : 'none';
      }
    });
  }

  /* ── Inject styles ──────────────────────────────────────────────────── */
  function injectStyles() {
    const el = document.createElement('style');
    el.textContent = CSS;
    document.head.appendChild(el);
  }

  /* ── Main init ──────────────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', function () {
    const spec = window.KA_ABOUT_PAGE;
    if (!spec) return; // page hasn't defined a spec — skip silently

    injectStyles();

    // Append the about section at the very end of body
    const section = buildSection(spec);
    document.body.appendChild(section);

    // Floating trigger badge
    const trigger = buildTrigger();
    document.body.appendChild(trigger);

    // Wire the "full function spec" link (visible only when logged in)
    wireSpecLink();
  });

})();

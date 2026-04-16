/*
 * ka_canonical_navbar.js
 *
 * Injects the canonical five-item K-ATLAS content navbar into any page
 * that exposes a <div id="ka-navbar-slot"></div>. Pages that set
 *   <body data-ka-active="topics">           (or articles|theories|mechanisms|neural|home)
 * get the active link highlighted.
 *
 * The injector also:
 *   - wires the Log-In pill / user pill from localStorage (ka_current_user),
 *   - wires an optional breadcrumb via <div id="ka-breadcrumb-slot">
 *     with data-ka-crumbs='[["Label","href"], ...]' on <body>.
 *
 * Load ORDER on each page:
 *   <link rel="stylesheet" href="ka_atlas_shell.css">
 *   ...
 *   <body data-ka-active="topics">
 *   <div id="ka-navbar-slot"></div>
 *   ...
 *   <script src="ka_canonical_navbar.js" defer></script>
 *
 * Author: CW, 2026-04-15
 */
(function () {
  'use strict';

  // Five canonical content destinations, in order.
  var NAV_ITEMS = [
    { key: 'articles',    href: 'ka_articles.html',    label: 'Articles' },
    { key: 'topics',      href: 'ka_topics.html',      label: 'Topics' },
    { key: 'theories',    href: 'ka_theories.html',    label: 'Theories' },
    { key: 'mechanisms',  href: 'ka_mechanisms.html',  label: 'Mechanisms' },
    { key: 'neural',      href: 'ka_neuro_perspective.html', label: 'Neural Underpinnings' }
  ];

  // SVG wordmark reused across the site.
  var WORDMARK_SVG =
    '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true">' +
      '<circle cx="16" cy="16" r="3.5" fill="#F5A623"/>' +
      '<circle cx="16" cy="5"  r="2.5" fill="#A8C8BF"/>' +
      '<circle cx="27" cy="22" r="2.5" fill="#A8C8BF"/>' +
      '<circle cx="5"  cy="22" r="2.5" fill="#A8C8BF"/>' +
      '<line x1="16" y1="7.5" x2="16" y2="12.5" stroke="#F5A623" stroke-width="1.5" stroke-opacity="0.9"/>' +
      '<line x1="24.8" y1="20.2" x2="19.0" y2="17.3" stroke="#F5A623" stroke-width="1.5" stroke-opacity="0.9"/>' +
      '<line x1="7.2" y1="20.2" x2="13.0" y2="17.3" stroke="#F5A623" stroke-width="1.5" stroke-opacity="0.9"/>' +
    '</svg>';

  function isIn160sp() {
    return location.pathname.indexOf('/160sp/') !== -1;
  }

  function basePrefix() {
    // Pages in /160sp/ need to ../ back up to the root for canonical hrefs.
    return isIn160sp() ? '../' : '';
  }

  // Portal pages: their logo links to global home.
  // All other pages within a user-type section: logo links to that section's portal.
  var PORTAL_PAGES = [
    'ka_schedule.html',           // 160sp portal
    'ka_home_student.html',       // student portal
    'ka_home_student_new.html',   // new-student portal
    'ka_home_instructor.html',    // instructor portal
    'ka_home_researcher.html',    // researcher portal
    'ka_home_practitioner.html',  // practitioner portal
    'ka_home_contributor.html',   // contributor portal
    'ka_home_theory.html'         // theory portal
  ];

  function logoHref() {
    var path = location.pathname;
    var page = path.split('/').pop() || '';

    // If this IS a portal page, logo goes to global home.
    for (var i = 0; i < PORTAL_PAGES.length; i++) {
      if (page === PORTAL_PAGES[i]) {
        return basePrefix() + 'ka_home.html';
      }
    }
    // If inside 160sp section, logo goes to the 160sp portal.
    if (isIn160sp()) {
      return 'ka_schedule.html';
    }
    // Otherwise (root-level pages), logo goes to global home.
    return 'ka_home.html';
  }

  function readUser() {
    try {
      var raw = localStorage.getItem('ka_current_user');
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }

  function buildNav(activeKey) {
    var prefix = basePrefix();
    var html =
      '<a class="ka-skip" href="#ka-main">Skip to main content</a>' +
      '<nav class="ka-topnav" aria-label="Primary">' +
        '<div class="ka-nav-left">' +
          '<a class="ka-wordmark" href="' + logoHref() + '">' +
            WORDMARK_SVG +
            '<span class="ka-wordmark-text">' +
              '<span class="ka-wordmark-top">Knowledge</span>' +
              '<span class="ka-wordmark-bottom">At<span>las</span></span>' +
            '</span>' +
          '</a>' +
          '<ul>';
    NAV_ITEMS.forEach(function (it) {
      var cls = (activeKey === it.key) ? ' class="active"' : '';
      html += '<li><a href="' + prefix + it.href + '"' + cls + '>' + it.label + '</a></li>';
    });
    html += '</ul></div>' +
      '<div class="ka-nav-right" id="ka-nav-right"></div>' +
      '</nav>';
    return html;
  }

  function renderUserArea() {
    var holder = document.getElementById('ka-nav-right');
    if (!holder) return;
    var prefix = basePrefix();
    var user = readUser();
    if (user && (user.first_name || user.email)) {
      var name = user.first_name || (user.email || '').split('@')[0];
      var roleLabel = (user.role || 'student').toUpperCase();
      holder.innerHTML =
        '<span class="ka-user-pill" title="Role">' + roleLabel + '</span>' +
        '<a class="ka-login-link" href="' + prefix + '160sp/ka_student_profile.html">' +
        name + '</a>';
    } else {
      holder.innerHTML =
        '<a class="ka-login-link" href="' + prefix + 'ka_login.html">Log in</a>';
    }
  }

  function renderBreadcrumb() {
    var slot = document.getElementById('ka-breadcrumb-slot');
    if (!slot) return;
    var raw = document.body.getAttribute('data-ka-crumbs');
    if (!raw) { slot.style.display = 'none'; return; }
    var crumbs;
    try { crumbs = JSON.parse(raw); } catch (e) { slot.style.display = 'none'; return; }
    if (!Array.isArray(crumbs) || crumbs.length === 0) { slot.style.display = 'none'; return; }
    var parts = crumbs.map(function (c, i) {
      var label = c[0] || '';
      var href  = c[1] || '';
      var last  = (i === crumbs.length - 1);
      if (last || !href) {
        return '<span>' + label + '</span>';
      }
      return '<a href="' + href + '">' + label + '</a>';
    });
    slot.className = 'ka-breadcrumb';
    slot.innerHTML = parts.join('<span class="sep">›</span>');
  }

  function init() {
    var slot = document.getElementById('ka-navbar-slot');
    if (!slot) return;  // page opted out
    var active = document.body.getAttribute('data-ka-active') || '';
    slot.outerHTML = buildNav(active);
    renderUserArea();
    renderBreadcrumb();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose for pages that need to re-render after login events.
  window.KA_CANONICAL_NAV = { render: init, renderUserArea: renderUserArea };
})();

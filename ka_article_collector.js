/**
 * ka_article_collector.js  —  ATLAS Article Collector Component
 * ---------------------------------------------------------------
 * A persistent, floating article basket that lets users "shoot"
 * articles into a collection as they move through workflows and
 * browse the site.  Data is persisted to localStorage.  If the
 * JWT auth server is running the basket is tagged with the user's
 * ID so it can be synced server-side in future.
 *
 * Public API (window.KA_COLLECTOR):
 *   .init()                 — render and attach the widget
 *   .add(article)           — add { title, url, doi?, notes? }
 *   .remove(id)             — remove by generated id
 *   .clear()                — empty the basket
 *   .getAll()               — return array of collected articles
 *   .count()                — number in basket
 *   .openPanel()            — expand the collector panel
 *   .onAdd(fn)              — register callback when article added
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'ka_article_basket';
  const callbacks = { add: [] };

  /* ── Storage helpers ─────────────────────────────────────────────────── */

  function load() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }
    catch (e) { return []; }
  }

  function save(articles) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(articles)); }
    catch (e) { /* storage full — silently ignore */ }
  }

  function makeId() {
    return 'art_' + Date.now() + '_' + Math.random().toString(36).slice(2, 7);
  }

  /* ── Core API ────────────────────────────────────────────────────────── */

  function add(article) {
    const articles = load();
    // Deduplicate by URL or DOI
    const exists = articles.some(function (a) {
      return (article.url && a.url === article.url) ||
             (article.doi && a.doi === article.doi);
    });
    if (exists) {
      flashWidget('Already in basket');
      return null;
    }
    const entry = Object.assign({}, article, {
      id: makeId(),
      addedAt: new Date().toISOString()
    });
    articles.unshift(entry);
    save(articles);
    renderList();
    updateBadge();
    flashWidget('Added to basket ✓');
    animatePulse();
    callbacks.add.forEach(function (fn) { fn(entry); });
    return entry;
  }

  function remove(id) {
    const articles = load().filter(function (a) { return a.id !== id; });
    save(articles);
    renderList();
    updateBadge();
  }

  function clear() {
    save([]);
    renderList();
    updateBadge();
  }

  function getAll() { return load(); }

  function count() { return load().length; }

  /* ── DOM Rendering ───────────────────────────────────────────────────── */

  let panelOpen = false;
  let widgetEl = null;
  let flashTimeout = null;

  function buildWidget() {
    const el = document.createElement('div');
    el.id = 'ka-collector-widget';
    el.innerHTML = `
      <div id="ka-col-toggle" title="Article Collector" role="button" aria-label="Open article collector">
        <span id="ka-col-icon">📚</span>
        <span id="ka-col-badge" style="display:none">0</span>
      </div>
      <div id="ka-col-panel" style="display:none" aria-live="polite">
        <div id="ka-col-header">
          <div id="ka-col-title">📚 Article Collector</div>
          <div id="ka-col-header-actions">
            <button id="ka-col-copy" title="Copy all as citations">⎘ Copy</button>
            <button id="ka-col-clear" title="Clear basket">✕ Clear</button>
            <button id="ka-col-close" title="Close">╲╱</button>
          </div>
        </div>
        <div id="ka-col-add-bar">
          <input id="ka-col-url-input" type="url" placeholder="Paste article URL or DOI…" />
          <button id="ka-col-add-btn">+ Add</button>
        </div>
        <div id="ka-col-flash" style="display:none"></div>
        <div id="ka-col-list-wrap">
          <div id="ka-col-empty" class="ka-col-empty-state">
            <div style="font-size:2rem;margin-bottom:8px">📭</div>
            <div>No articles yet.</div>
            <div style="margin-top:4px;font-size:.82rem;color:#9ca3af">Use the + Add button or click<br>"Save to Collector" on any evidence card.</div>
          </div>
          <ul id="ka-col-list"></ul>
        </div>
        <div id="ka-col-footer">
          <span id="ka-col-count-label">0 articles collected</span>
          <a id="ka-col-submit-link" href="ka_article_propose.html" style="display:none">Submit to ATLAS →</a>
        </div>
      </div>
    `;

    // Styles
    const style = document.createElement('style');
    style.textContent = `
      #ka-collector-widget {
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 9000;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 14px;
      }
      #ka-col-toggle {
        width: 52px;
        height: 52px;
        border-radius: 50%;
        background: #1a56a4;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 16px rgba(26,86,164,.45);
        transition: transform .15s, box-shadow .15s;
        position: relative;
        font-size: 1.4rem;
        user-select: none;
      }
      #ka-col-toggle:hover { transform: scale(1.08); box-shadow: 0 6px 20px rgba(26,86,164,.55); }
      #ka-col-toggle.pulse { animation: ka-pulse .4s ease-out; }
      @keyframes ka-pulse {
        0%   { transform: scale(1); }
        40%  { transform: scale(1.18); }
        100% { transform: scale(1); }
      }
      #ka-col-badge {
        position: absolute;
        top: -4px; right: -4px;
        background: #e53e3e;
        color: #fff;
        border-radius: 50%;
        min-width: 20px; height: 20px;
        font-size: .7rem; font-weight: 700;
        display: flex; align-items: center; justify-content: center;
        padding: 0 4px;
        box-shadow: 0 1px 4px rgba(0,0,0,.2);
      }
      #ka-col-panel {
        position: absolute;
        bottom: 62px;
        right: 0;
        width: 340px;
        max-height: 520px;
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 8px 40px rgba(0,0,0,.18);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        border: 1.5px solid #e5e7eb;
      }
      #ka-col-header {
        background: #1a56a4;
        color: #fff;
        padding: 12px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-shrink: 0;
      }
      #ka-col-title { font-weight: 700; font-size: .95rem; }
      #ka-col-header-actions { display: flex; gap: 6px; }
      #ka-col-header-actions button {
        background: rgba(255,255,255,.15);
        border: none; color: #fff;
        border-radius: 5px;
        padding: 3px 8px;
        cursor: pointer;
        font-size: .78rem;
        transition: background .15s;
      }
      #ka-col-header-actions button:hover { background: rgba(255,255,255,.28); }
      #ka-col-add-bar {
        display: flex;
        gap: 6px;
        padding: 10px 12px;
        border-bottom: 1px solid #f0f0f0;
        flex-shrink: 0;
      }
      #ka-col-url-input {
        flex: 1; border: 1.5px solid #d1d5db;
        border-radius: 6px; padding: 6px 10px;
        font-size: .85rem; outline: none;
      }
      #ka-col-url-input:focus { border-color: #1a56a4; }
      #ka-col-add-btn {
        background: #1a56a4; color: #fff;
        border: none; border-radius: 6px;
        padding: 6px 12px; cursor: pointer;
        font-size: .85rem; font-weight: 600;
        white-space: nowrap;
        transition: background .15s;
      }
      #ka-col-add-btn:hover { background: #154899; }
      #ka-col-flash {
        padding: 6px 14px;
        font-size: .82rem;
        background: #d1fae5;
        color: #065f46;
        flex-shrink: 0;
        border-bottom: 1px solid #a7f3d0;
      }
      #ka-col-list-wrap {
        flex: 1; overflow-y: auto;
        padding: 6px 0;
      }
      .ka-col-empty-state {
        padding: 24px 20px;
        text-align: center;
        color: #6b7280;
        font-size: .88rem;
      }
      #ka-col-list { list-style: none; margin: 0; padding: 0 10px; }
      .ka-col-item {
        display: flex; align-items: flex-start; gap: 8px;
        padding: 8px 4px;
        border-bottom: 1px solid #f3f4f6;
      }
      .ka-col-item:last-child { border-bottom: none; }
      .ka-col-item-text { flex: 1; min-width: 0; }
      .ka-col-item-title {
        font-size: .85rem; font-weight: 600; color: #1f2937;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      }
      .ka-col-item-meta { font-size: .75rem; color: #6b7280; margin-top: 2px; }
      .ka-col-item-remove {
        background: none; border: none;
        color: #9ca3af; cursor: pointer;
        font-size: 1rem; padding: 0 2px;
        line-height: 1;
        flex-shrink: 0;
        transition: color .15s;
      }
      .ka-col-item-remove:hover { color: #e53e3e; }
      #ka-col-footer {
        padding: 10px 14px;
        border-top: 1px solid #f0f0f0;
        display: flex; align-items: center;
        justify-content: space-between;
        flex-shrink: 0;
        background: #f9fafb;
        font-size: .82rem; color: #6b7280;
      }
      #ka-col-submit-link {
        font-size: .82rem; color: #1a56a4;
        font-weight: 600; text-decoration: none;
      }
      #ka-col-submit-link:hover { text-decoration: underline; }
      @media (max-width: 520px) {
        #ka-col-panel { width: calc(100vw - 32px); right: 0; }
      }
    `;
    document.head.appendChild(style);
    document.body.appendChild(el);

    // Event listeners
    el.querySelector('#ka-col-toggle').addEventListener('click', togglePanel);
    el.querySelector('#ka-col-close').addEventListener('click', closePanel);
    el.querySelector('#ka-col-clear').addEventListener('click', function () {
      if (confirm('Clear all collected articles?')) clear();
    });
    el.querySelector('#ka-col-copy').addEventListener('click', copyAllCitations);
    el.querySelector('#ka-col-add-btn').addEventListener('click', addFromInput);
    el.querySelector('#ka-col-url-input').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') addFromInput();
    });

    widgetEl = el;
    renderList();
    updateBadge();
  }

  function togglePanel() {
    panelOpen ? closePanel() : openPanel();
  }

  function openPanel() {
    panelOpen = true;
    widgetEl.querySelector('#ka-col-panel').style.display = 'flex';
  }

  function closePanel() {
    panelOpen = false;
    widgetEl.querySelector('#ka-col-panel').style.display = 'none';
  }

  function flashWidget(msg) {
    if (!widgetEl) return;
    const flash = widgetEl.querySelector('#ka-col-flash');
    flash.textContent = msg;
    flash.style.display = 'block';
    clearTimeout(flashTimeout);
    flashTimeout = setTimeout(function () { flash.style.display = 'none'; }, 2500);
  }

  function animatePulse() {
    if (!widgetEl) return;
    const toggle = widgetEl.querySelector('#ka-col-toggle');
    toggle.classList.remove('pulse');
    void toggle.offsetWidth; // reflow
    toggle.classList.add('pulse');
  }

  function updateBadge() {
    if (!widgetEl) return;
    const n = count();
    const badge = widgetEl.querySelector('#ka-col-badge');
    badge.textContent = n;
    badge.style.display = n > 0 ? 'flex' : 'none';
    const countLabel = widgetEl.querySelector('#ka-col-count-label');
    countLabel.textContent = n + (n === 1 ? ' article collected' : ' articles collected');
    const submitLink = widgetEl.querySelector('#ka-col-submit-link');
    submitLink.style.display = n > 0 ? 'inline' : 'none';
  }

  function renderList() {
    if (!widgetEl) return;
    const articles = load();
    const list = widgetEl.querySelector('#ka-col-list');
    const empty = widgetEl.querySelector('#ka-col-empty');
    if (articles.length === 0) {
      list.innerHTML = '';
      empty.style.display = 'block';
      return;
    }
    empty.style.display = 'none';
    list.innerHTML = articles.map(function (a) {
      const safeTitle = (a.title || 'Untitled article').replace(/</g, '&lt;');
      const meta = a.doi ? 'DOI: ' + a.doi : (a.url ? 'URL saved' : 'No link');
      return '<li class="ka-col-item">' +
        '<div class="ka-col-item-text">' +
          '<div class="ka-col-item-title" title="' + safeTitle + '">' + safeTitle + '</div>' +
          '<div class="ka-col-item-meta">' + meta + '</div>' +
        '</div>' +
        '<button class="ka-col-item-remove" data-id="' + a.id + '" title="Remove">✕</button>' +
      '</li>';
    }).join('');
    list.querySelectorAll('.ka-col-item-remove').forEach(function (btn) {
      btn.addEventListener('click', function () { remove(btn.dataset.id); });
    });
  }

  function addFromInput() {
    if (!widgetEl) return;
    const input = widgetEl.querySelector('#ka-col-url-input');
    const raw = input.value.trim();
    if (!raw) return;
    const isDoi = raw.startsWith('10.') || raw.startsWith('doi:');
    const entry = isDoi
      ? { title: 'Article (DOI: ' + raw + ')', doi: raw.replace(/^doi:/, '') }
      : { title: 'Article from ' + raw.replace(/^https?:\/\//, '').split('/')[0], url: raw };
    add(entry);
    input.value = '';
  }

  function copyAllCitations() {
    const articles = load();
    if (!articles.length) { flashWidget('Nothing to copy'); return; }
    const text = articles.map(function (a, i) {
      return (i + 1) + '. ' + (a.title || 'Untitled') +
        (a.doi ? ' — DOI: ' + a.doi : '') +
        (a.url && !a.doi ? ' — ' + a.url : '');
    }).join('\n');
    navigator.clipboard.writeText(text).then(function () {
      flashWidget('Copied ' + articles.length + ' citation(s) to clipboard');
    }).catch(function () {
      flashWidget('Could not copy — check browser permissions');
    });
  }

  /* ── Page-level "Save to Collector" button wiring ────────────────────── */
  // Call window.KA_COLLECTOR.wireButtons() after page content is loaded.
  // Looks for elements with data-collect-title and data-collect-url attributes.

  function wireButtons() {
    document.querySelectorAll('[data-collect-title]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        add({
          title: btn.dataset.collectTitle || btn.textContent,
          url:   btn.dataset.collectUrl || '',
          doi:   btn.dataset.collectDoi || '',
          notes: btn.dataset.collectNotes || ''
        });
        if (!panelOpen) openPanel();
      });
    });
  }

  /* ── Init ────────────────────────────────────────────────────────────── */

  function init(opts) {
    if (widgetEl) return; // already initialised
    opts = opts || {};
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () {
        buildWidget();
        if (opts.wireOnInit !== false) wireButtons();
      });
    } else {
      buildWidget();
      if (opts.wireOnInit !== false) wireButtons();
    }
  }

  /* ── Public API ──────────────────────────────────────────────────────── */

  window.KA_COLLECTOR = {
    init:        init,
    add:         add,
    remove:      remove,
    clear:       clear,
    getAll:      getAll,
    count:       count,
    openPanel:   openPanel,
    closePanel:  closePanel,
    wireButtons: wireButtons,
    onAdd: function (fn) { callbacks.add.push(fn); }
  };

})();

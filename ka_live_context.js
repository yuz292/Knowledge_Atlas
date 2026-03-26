(function () {
  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function findAnchor() {
    return (
      document.querySelector('.page-header') ||
      document.querySelector('.stage-header') ||
      document.querySelector('.main-content') ||
      document.querySelector('.main-area') ||
      document.querySelector('.page-wrap') ||
      document.querySelector('main') ||
      document.body
    );
  }

  function injectStyles() {
    if (document.getElementById('ka-live-context-styles')) return;
    const style = document.createElement('style');
    style.id = 'ka-live-context-styles';
    style.textContent = `
      .ka-live-context {
        background: #FFFFFF;
        border: 1px solid #D8D0C5;
        border-left: 4px solid #2A7868;
        border-radius: 10px;
        padding: 16px 18px;
        margin: 0 0 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
      }
      .ka-live-context.warn { border-left-color: #E8872A; }
      .ka-live-context-head {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        align-items: baseline;
        margin-bottom: 10px;
      }
      .ka-live-context-title {
        font: 700 12px/1.2 Arial, sans-serif;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #1C3D3A;
      }
      .ka-live-context-status {
        font: 700 11px/1.2 Arial, sans-serif;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #2A7868;
      }
      .ka-live-context.warn .ka-live-context-status { color: #C05A1F; }
      .ka-live-context-copy {
        font: 15px/1.6 Georgia, serif;
        color: #3C3C3C;
        margin: 0 0 12px;
      }
      .ka-live-context-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 10px;
      }
      .ka-live-context-stat {
        background: #F7F4EF;
        border-radius: 8px;
        padding: 10px 12px;
      }
      .ka-live-context-stat strong {
        display: block;
        font: 700 18px/1.2 Arial, sans-serif;
        color: #1C3D3A;
      }
      .ka-live-context-stat span {
        display: block;
        margin-top: 2px;
        font: 11px/1.35 Arial, sans-serif;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #6B6B6B;
      }
    `;
    document.head.appendChild(style);
  }

  function buildCopy(config, data) {
    const summaries = {
      hypothesis_builder:
        'This workflow is connected to live corpus counts so the student can see the scale of available evidence, but the saved hypothesis path is still prototype-level rather than a real backend record.',
      tagger:
        'This contributor surface is structurally live but still depends on local/demo assignment state rather than a real batch-assignment backend.',
      tag_assignment:
        'This assignment surface is now anchored to live corpus counts, but claiming and persistence remain workflow placeholders rather than a true task database.',
      sensors:
        'This catalogue is reference-grade and now shows live corpus context, but instrument-to-paper grounding is still incomplete because the extraction layer is still improving instrument coverage.',
      auth:
        'This authentication/setup surface is wired into the shared shell, but account state is still local prototype state rather than a real persistent identity system.'
    };
    return config.copy || summaries[config.surface] || 'This page is connected to the current Atlas payloads, but parts of the workflow remain prototype-level and should not be mistaken for a full production backend.';
  }

  async function loadStats() {
    const adapter = window.KA_DATA_ADAPTER;
    if (!adapter || typeof adapter.loadPayload !== 'function') return null;
    const [topics, articles, evidence, status] = await Promise.all([
      adapter.loadPayload('topics'),
      adapter.loadPayload('articles'),
      adapter.loadPayload('evidence'),
      adapter.loadPayload('json_status')
    ]);
    const summary = (status && status.summary) || {};
    return {
      topicCount: Array.isArray(topics && topics.topics) ? topics.topics.length : 0,
      articleCount: Array.isArray(articles && articles.articles) ? articles.articles.length : 0,
      evidenceCount: Array.isArray(evidence && evidence.evidence) ? evidence.evidence.length : 0,
      abstractGood: Number(summary.abstract_good || 0),
      doiGood: Number(summary.doi_good || 0),
      subjectCountGood: Number(summary.subject_count_good || 0)
    };
  }

  async function render(config) {
    injectStyles();
    const stats = await loadStats();
    if (!stats) return;

    const card = el('section', 'ka-live-context' + (config.warn ? ' warn' : ''));
    const head = el('div', 'ka-live-context-head');
    head.appendChild(el('div', 'ka-live-context-title', config.title || 'Live Context'));
    head.appendChild(el('div', 'ka-live-context-status', config.status || 'Partial implementation'));
    card.appendChild(head);
    card.appendChild(el('p', 'ka-live-context-copy', buildCopy(config, stats)));

    const grid = el('div', 'ka-live-context-grid');
    const statRows = [
      ['Topics', stats.topicCount],
      ['Articles', stats.articleCount],
      ['Evidence rows', stats.evidenceCount],
      ['Abstracts good', stats.abstractGood],
      ['DOIs good', stats.doiGood],
      ['Subject counts good', stats.subjectCountGood]
    ];
    for (const [label, value] of statRows) {
      const box = el('div', 'ka-live-context-stat');
      box.appendChild(el('strong', '', String(value)));
      box.appendChild(el('span', '', label));
      grid.appendChild(box);
    }
    card.appendChild(grid);

    const anchor = findAnchor();
    if (anchor.classList && (anchor.classList.contains('page-header') || anchor.classList.contains('stage-header'))) {
      anchor.insertAdjacentElement('afterend', card);
      return;
    }
    anchor.prepend(card);
  }

  document.addEventListener('DOMContentLoaded', function () {
    const config = window.KA_LIVE_CONTEXT_CONFIG;
    if (!config) return;
    render(config).catch(function (err) {
      console.warn('KA live context failed', err);
    });
  });
})();

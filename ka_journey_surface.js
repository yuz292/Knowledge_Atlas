/*  ka_journey_surface.js — shared helpers for the ka_journey_{name}.html
    pages (the "complicated surface" specs). Each page calls
    renderJourneySiblings(slug) to inject the cross-link row, and uses
    saveCritique(pageKey) / restoreCritique(pageKey) to persist per-role
    critique drafts to localStorage.

    NOTE: do NOT confuse with ka_journey_nav.js, which renders the
    user-type journey sidebar on other pages of the site. These two
    scripts are independent; this one is specific to the complicated-
    surface meta pages.
*/

(function(){
  const SIBLINGS = [
    {slug: 'en',                label: 'EN',          full: 'Epistemic Network'},
    {slug: 'bn',                label: 'BN',          full: 'Bayesian Network'},
    {slug: 'interpretation',    label: 'Interp.',     full: 'Interpretation'},
    {slug: 'argumentation',     label: 'Arg.',        full: 'Argumentation'},
    {slug: 'qa',                label: 'QA',          full: 'Question-answering'},
    {slug: 'mechanism',         label: 'Mech.',       full: 'Mechanism'},
    {slug: 'theory',            label: 'Theory',      full: 'Theory'},
    {slug: 'gaps',              label: 'Gaps',        full: 'Gaps'},
    {slug: 'evidence',          label: 'Evidence',    full: 'Evidence landscape'},
    {slug: 'fronts',            label: 'Fronts',      full: 'Research fronts'},
    {slug: 'ontology',          label: 'Ontology',    full: 'Ontology inspector'},
    {slug: 'topic_inspector',   label: 'Topic insp.', full: 'Topic inspector'},
  ];

  window.renderJourneySiblings = function(currentSlug) {
    const mount = document.getElementById('j-siblings-slot');
    if (!mount) return;
    const parts = [`<span class="sb-label">Complicated surfaces</span>`];
    parts.push(`<a href="ka_journeys.html" title="Index">↺ index</a>`);
    SIBLINGS.forEach(s => {
      const cls = s.slug === currentSlug ? 'current' : '';
      parts.push(`<a href="ka_journey_${s.slug}.html" class="${cls}" title="${s.full}">${s.label}</a>`);
    });
    mount.innerHTML = parts.join('');
  };

  window.saveCritique = function(pageKey) {
    const roles = ['public_visitor','160_student','researcher','practitioner','admin'];
    const data = {};
    roles.forEach(r => {
      const ta = document.getElementById('crit_' + r);
      if (ta) data[r] = ta.value;
    });
    try { localStorage.setItem('ka.critique.' + pageKey, JSON.stringify(data)); } catch(e) {}
    const s = document.getElementById('j-crit-status');
    if (s) { s.classList.add('show'); setTimeout(() => s.classList.remove('show'), 2500); }
  };

  window.restoreCritique = function(pageKey) {
    try {
      const raw = localStorage.getItem('ka.critique.' + pageKey);
      if (!raw) return;
      const data = JSON.parse(raw);
      Object.keys(data || {}).forEach(r => {
        const ta = document.getElementById('crit_' + r);
        if (ta) ta.value = data[r] || '';
      });
    } catch(e){}
  };
})();

(function () {
  function text(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value == null ? '' : String(value);
  }

  function href(id, value) {
    const el = document.getElementById(id);
    if (el) el.href = value || '#';
  }

  function html(id, value) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = value || '';
  }

  function statGrid(rows) {
    return rows.map(function (row) {
      return '<div class="layer-stat"><strong>' + row.value + '</strong><span>' + row.label + '</span></div>';
    }).join('');
  }

  function cardList(rows, renderer) {
    if (!rows || !rows.length) {
      return '<div class="layer-empty">No live rows were available in the current payload.</div>';
    }
    return rows.map(renderer).join('');
  }

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderArgumentation(payload) {
    const summary = payload.summary || {};
    html('layer-stats', statGrid([
      { label: 'Paper nodes', value: summary.paper_node_count || 0 },
      { label: 'Claim nodes', value: summary.claim_node_count || 0 },
      { label: 'Claim edges', value: summary.claim_edge_count || 0 },
      { label: 'Debate clusters', value: summary.cluster_count || 0 },
      { label: 'Claims surfaced', value: summary.total_claims || 0 },
      { label: 'Unique theories', value: summary.unique_theories || 0 }
    ]));
    const coverage = payload.coverage_report || {};
    html('layer-summary-copy', [
      'The argumentation layer is the conflict-and-support surface that sits above the article corpus. ',
      'It currently spans ' + (summary.paper_node_count || 0) + ' paper-level nodes and ' + (summary.claim_node_count || 0) + ' claim-level nodes. ',
      'Stance coverage is still thin at ' + Math.round(Number(coverage.stance_coverage_rate || 0) * 10000) / 100 + '%, which is a real QA gap rather than something to hide.'
    ].join(''));
    html('layer-primary-list', cardList(payload.debate_clusters || [], function (row) {
      return '<article class="layer-card">'
        + '<div class="layer-card-head"><h3>' + esc(row.cluster_id) + '</h3><span>' + esc(row.paper_count) + ' papers</span></div>'
        + '<p>This cluster currently groups ' + esc(row.paper_count) + ' papers around ' + esc(row.theory_count) + ' theory anchors.</p>'
        + '<p><strong>Theories:</strong> ' + esc((row.theories || []).join(', ') || 'None surfaced') + '</p>'
        + '<p><strong>Sample papers:</strong> ' + esc((row.papers || []).join(', ')) + '</p>'
        + '</article>';
    }));
    html('layer-secondary-list', cardList(payload.claim_nodes || [], function (row) {
      return '<article class="layer-card compact">'
        + '<div class="layer-card-head"><h3>' + esc(row.belief_id || row.paper_id || 'claim') + '</h3><span>' + esc(row.qualifier || 'unqualified') + '</span></div>'
        + '<p>' + esc(row.content_preview || '') + '</p>'
        + '<p><strong>Support / attack:</strong> ' + esc(row.incoming_support_count || 0) + ' / ' + esc(row.incoming_attack_count || 0) + '</p>'
        + '</article>';
    }));
  }

  function renderAnnotations(payload) {
    const summary = payload.summary || {};
    html('layer-stats', statGrid([
      { label: 'Beliefs touched', value: summary.total_beliefs || 0 },
      { label: 'Annotations', value: summary.total_annotations || 0 },
      { label: 'Artifact role', value: summary.artifact_role || 'unknown' },
      { label: 'Source', value: summary.canonical_source || 'unknown' }
    ]));
    html('layer-summary-copy', [
      'The annotation layer stores human- or system-authored notes about what needs attention in the belief network. ',
      'Right now it is a derived overlay, not yet the whole annotation inventory, which means this page is useful and honest but still incomplete.'
    ].join(''));
    html('layer-primary-list', cardList(payload.by_type || [], function (row) {
      return '<article class="layer-card compact">'
        + '<div class="layer-card-head"><h3>' + esc(row.type) + '</h3><span>' + esc(row.count) + '</span></div>'
        + '<p>Active annotations of this type currently present in the regenerated overlay.</p>'
        + '</article>';
    }));
    html('layer-secondary-list', cardList(payload.annotations || [], function (row) {
      return '<article class="layer-card">'
        + '<div class="layer-card-head"><h3>' + esc(row.type) + '</h3><span>' + esc(row.status || 'active') + '</span></div>'
        + '<p><strong>Target:</strong> ' + esc((row.target_type || 'item') + ' · ' + (row.target_id || 'unknown')) + '</p>'
        + '<p>' + esc(row.content || '') + '</p>'
        + '<p><strong>Confidence:</strong> ' + esc(row.confidence == null ? '—' : row.confidence) + '</p>'
        + '</article>';
    }));
  }

  function renderInterpretation(payload) {
    const summary = payload.summary || {};
    const boundary = payload.boundary_map || {};
    const zoneClass = boundary.zone_classification || {};
    html('layer-stats', statGrid([
      { label: 'High-VOI questions', value: summary.high_voi_count || 0 },
      { label: 'Medium-VOI questions', value: summary.medium_voi_count || 0 },
      { label: 'Average completeness', value: summary.average_completeness || 0 },
      { label: 'Active boundary beliefs', value: zoneClass.active_boundary_count || 0 },
      { label: 'Periphery beliefs', value: zoneClass.identified_periphery_count || 0 }
    ]));
    html('layer-summary-copy', [
      'The interpretation layer is where the system stops listing evidence and starts asking what the current field still does not know. ',
      'It prioritizes frontier questions, boundary beliefs, and validation completeness so research planning can be audited instead of improvised.'
    ].join(''));
    html('layer-primary-list', cardList(payload.frontier_questions || [], function (row) {
      return '<article class="layer-card">'
        + '<div class="layer-card-head"><h3>' + esc(row.framework_name || row.belief_id) + '</h3><span>' + esc(row.voi_bucket || 'voi') + ' · ' + esc(row.voi_score || 0) + '</span></div>'
        + '<p><strong>Zone:</strong> ' + esc(row.zone || 'unknown') + '</p>'
        + '<ul class="layer-bullets">' + (row.question_set || []).map(function (q) { return '<li>' + esc(q) + '</li>'; }).join('') + '</ul>'
        + '</article>';
    }));
    html('layer-secondary-list', cardList(payload.validation_beliefs || [], function (row) {
      return '<article class="layer-card compact">'
        + '<div class="layer-card-head"><h3>' + esc(row.belief_id) + '</h3><span>' + esc(row.replication_status || 'unknown') + '</span></div>'
        + '<p><strong>Completeness:</strong> ' + esc(row.validation_completeness || 0) + '</p>'
        + '<p><strong>Support / challenge:</strong> ' + esc(row.supporting_evidence_count || 0) + ' / ' + esc(row.challenging_evidence_count || 0) + '</p>'
        + '</article>';
    }));
  }

  const RENDERERS = {
    argumentation: renderArgumentation,
    annotations: renderAnnotations,
    interpretation: renderInterpretation
  };

  document.addEventListener('DOMContentLoaded', async function () {
    const config = window.KA_LAYER_PAGE;
    if (!config || !window.KA_DATA_ADAPTER || typeof window.KA_DATA_ADAPTER.loadPayload !== 'function') {
      return;
    }
    const payload = await window.KA_DATA_ADAPTER.loadPayload(config.payload, {});
    href('layer-brief-link', config.briefHref || '#');
    const renderer = RENDERERS[config.payload];
    if (renderer) renderer(payload);
    if (payload && payload.source_file) {
      text('layer-source-copy', payload.source_file);
    } else if (payload && payload.source_files) {
      text('layer-source-copy', Object.values(payload.source_files).join(' · '));
    }
  });
})();

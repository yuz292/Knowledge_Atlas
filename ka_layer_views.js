(function () {
  function getFocus() {
    const params = new URLSearchParams(window.location.search);
    return {
      paperId: params.get('paper_id') || '',
      title: params.get('title') || '',
    };
  }

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

  function show(id, shouldShow) {
    const el = document.getElementById(id);
    if (el) el.style.display = shouldShow ? '' : 'none';
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

  function focusMarkup(focus, copy) {
    if (!focus.paperId) return '';
    const label = focus.title ? focus.title + ' (' + focus.paperId + ')' : focus.paperId;
    return '<div class="layer-focus-copy"><strong>Focused article:</strong> ' + esc(label) + '. ' + esc(copy) + '</div>';
  }

  function renderArgumentation(payload) {
    const focus = getFocus();
    const summary = payload.summary || {};
    const focusedClaims = focus.paperId
      ? (payload.claim_nodes || []).filter(function (row) { return row.paper_id === focus.paperId; })
      : (payload.claim_nodes || []);
    const focusedClusters = focus.paperId
      ? (payload.debate_clusters || []).filter(function (row) { return (row.papers || []).indexOf(focus.paperId) !== -1; })
      : (payload.debate_clusters || []);
    const focusedPapers = focus.paperId
      ? (payload.paper_nodes || []).filter(function (row) { return row.paper_id === focus.paperId; })
      : (payload.paper_nodes || []);
    html('layer-stats', statGrid([
      { label: focus.paperId ? 'Focused papers' : 'Paper nodes', value: focus.paperId ? focusedPapers.length : (summary.paper_node_count || 0) },
      { label: focus.paperId ? 'Focused claims' : 'Claim nodes', value: focus.paperId ? focusedClaims.length : (summary.claim_node_count || 0) },
      { label: 'Claim edges', value: summary.claim_edge_count || 0 },
      { label: focus.paperId ? 'Linked clusters' : 'Debate clusters', value: focus.paperId ? focusedClusters.length : (summary.cluster_count || 0) },
      { label: 'Claims surfaced', value: focus.paperId ? focusedClaims.length : (summary.total_claims || 0) },
      { label: 'Unique theories', value: summary.unique_theories || 0 }
    ]));
    const coverage = payload.coverage_report || {};
    html('layer-summary-copy', focusMarkup(focus, 'This layer can already pivot to paper-linked claim nodes and debate clusters because the argumentation payload carries explicit paper ids.') + [
      'The argumentation layer is the conflict-and-support surface that sits above the article corpus. ',
      'It currently spans ' + (focus.paperId ? focusedPapers.length : (summary.paper_node_count || 0)) + ' paper-level nodes and ' + (focus.paperId ? focusedClaims.length : (summary.claim_node_count || 0)) + ' claim-level nodes in the active view. ',
      'Stance coverage is still thin at ' + Math.round(Number(coverage.stance_coverage_rate || 0) * 10000) / 100 + '%, which is a real QA gap rather than something to hide.'
    ].join(''));
    html('layer-primary-list', cardList(focusedClusters, function (row) {
      return '<article class="layer-card">'
        + '<div class="layer-card-head"><h3>' + esc(row.cluster_id) + '</h3><span>' + esc(row.paper_count) + ' papers</span></div>'
        + '<p>This cluster currently groups ' + esc(row.paper_count) + ' papers around ' + esc(row.theory_count) + ' theory anchors.</p>'
        + '<p><strong>Theories:</strong> ' + esc((row.theories || []).join(', ') || 'None surfaced') + '</p>'
        + '<p><strong>Sample papers:</strong> ' + esc((row.papers || []).join(', ')) + '</p>'
        + '</article>';
    }));
    html('layer-secondary-list', cardList(focusedClaims, function (row) {
      return '<article class="layer-card compact">'
        + '<div class="layer-card-head"><h3>' + esc(row.belief_id || row.paper_id || 'claim') + '</h3><span>' + esc(row.qualifier || 'unqualified') + '</span></div>'
        + '<p>' + esc(row.content_preview || '') + '</p>'
        + '<p><strong>Support / attack:</strong> ' + esc(row.incoming_support_count || 0) + ' / ' + esc(row.incoming_attack_count || 0) + '</p>'
        + '</article>';
    }));
  }

  function renderAnnotations(payload) {
    const focus = getFocus();
    const summary = payload.summary || {};
    const focusedAnnotations = focus.paperId
      ? (payload.annotations || []).filter(function (row) {
          const target = String(row.target_id || '');
          const content = String(row.content || '');
          return target.indexOf(focus.paperId) !== -1 || content.indexOf(focus.paperId) !== -1;
        })
      : (payload.annotations || []);
    const hasDirectFocus = !!focusedAnnotations.length;
    html('layer-stats', statGrid([
      { label: 'Beliefs touched', value: summary.total_beliefs || 0 },
      { label: focus.paperId ? 'Focused notes' : 'Annotations', value: focus.paperId ? focusedAnnotations.length : (summary.total_annotations || 0) },
      { label: 'Artifact role', value: summary.artifact_role || 'unknown' },
      { label: 'Source', value: summary.canonical_source || 'unknown' }
    ]));
    html('layer-summary-copy', focusMarkup(focus, hasDirectFocus
      ? 'The current overlay includes annotations that reference this paper id directly.'
      : 'The current overlay is only partially paper-linked, so this focused view falls back to the global annotation surface when no direct match is present.') + [
      'The annotation layer stores human- or system-authored notes about what needs attention in the belief network. ',
      'Right now it is a derived overlay, not yet the whole annotation inventory, which means this page is useful and honest but still incomplete.'
    ].join(''));
    html('layer-primary-list', cardList(payload.by_type || [], function (row) {
      return '<article class="layer-card compact">'
        + '<div class="layer-card-head"><h3>' + esc(row.type) + '</h3><span>' + esc(row.count) + '</span></div>'
        + '<p>Active annotations of this type currently present in the regenerated overlay.</p>'
        + '</article>';
    }));
    html('layer-secondary-list', cardList(hasDirectFocus ? focusedAnnotations : (payload.annotations || []), function (row) {
      return '<article class="layer-card">'
        + '<div class="layer-card-head"><h3>' + esc(row.type) + '</h3><span>' + esc(row.status || 'active') + '</span></div>'
        + '<p><strong>Target:</strong> ' + esc((row.target_type || 'item') + ' · ' + (row.target_id || 'unknown')) + '</p>'
        + '<p>' + esc(row.content || '') + '</p>'
        + '<p><strong>Confidence:</strong> ' + esc(row.confidence == null ? '—' : row.confidence) + '</p>'
        + '</article>';
    }));
  }

  function renderInterpretation(payload) {
    const focus = getFocus();
    const summary = payload.summary || {};
    const boundary = payload.boundary_map || {};
    const zoneClass = boundary.zone_classification || {};
    const focusedBeliefs = focus.paperId
      ? (payload.validation_beliefs || []).filter(function (row) {
          return String(row.belief_id || '').indexOf(focus.paperId) !== -1;
        })
      : (payload.validation_beliefs || []);
    const hasDirectFocus = !!focusedBeliefs.length;
    html('layer-stats', statGrid([
      { label: 'High-VOI questions', value: summary.high_voi_count || 0 },
      { label: 'Medium-VOI questions', value: summary.medium_voi_count || 0 },
      { label: 'Average completeness', value: summary.average_completeness || 0 },
      { label: focus.paperId ? 'Focused beliefs' : 'Active boundary beliefs', value: focus.paperId ? focusedBeliefs.length : (zoneClass.active_boundary_count || 0) },
      { label: 'Periphery beliefs', value: zoneClass.identified_periphery_count || 0 }
    ]));
    html('layer-summary-copy', focusMarkup(focus, hasDirectFocus
      ? 'This focused view found validation beliefs whose ids explicitly carry this paper id.'
      : 'Interpretation outputs are still belief-centric rather than paper-centric, so this focused view falls back to the global frontier while noting the linkage gap.') + [
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
    html('layer-secondary-list', cardList(hasDirectFocus ? focusedBeliefs : (payload.validation_beliefs || []), function (row) {
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
    const focus = getFocus();
    show('layer-focus-strip', !!focus.paperId);
    if (focus.paperId) {
      html('layer-focus-strip', '<strong>Focused article</strong>: ' + esc(focus.title || focus.paperId) + ' <span class="layer-focus-id">(' + esc(focus.paperId) + ')</span>');
    }
    const renderer = RENDERERS[config.payload];
    if (renderer) renderer(payload);
    if (payload && payload.source_file) {
      text('layer-source-copy', payload.source_file);
    } else if (payload && payload.source_files) {
      text('layer-source-copy', Object.values(payload.source_files).join(' · '));
    }
  });
})();

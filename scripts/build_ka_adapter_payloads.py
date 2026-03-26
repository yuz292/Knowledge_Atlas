#!/usr/bin/env python3
import json
import re
from collections import defaultdict, Counter
from pathlib import Path
from datetime import datetime

CURRENT_YEAR = datetime.now().year
TITLE_REJECT_PATTERNS = [
    r'^contents lists available at', r'^science of the total environment\b', r'^landscape and urban planning\b',
    r'^frontiers in psychology\b', r'^ann\. n\.y\. acad\. sci\.', r'^march \d{4} \| volume',
    r'^article type:', r'^doi:', r'rights reserved', r'elsevier b\.v\.', r'copyediting, typesetting, pagination',
]
ABSTRACT_TRIM_MARKERS = [' Published by', ' 1. Introduction', '1. Introduction', ' Introduction ', ' * Corresponding author', ' Contents lists available at ScienceDirect ', ' Contents lists available at']


ROOT = Path('/Users/davidusa/REPOS')
AE = ROOT / 'Article_Eater_PostQuinean_v1_recovery'
OUT = ROOT / 'Knowledge_Atlas' / 'data' / 'ka_payloads'
OUT.mkdir(parents=True, exist_ok=True)

FRONTS_PATH = AE / 'data' / 'rebuild' / 'research_fronts_v5.json'
CLAIMS_PATH = AE / 'data' / 'rebuild' / 'gold_claims.jsonl'
REPAIRS_PATH = AE / 'data' / 'rebuild' / 'bibliographic_repairs.json'
DEEP_STATS_DIR = AE / 'data' / 'verification_runs' / 'v6_deep_stats_adjudication'
MAIN_CONCLUSION_DIR = AE / 'data' / 'verification_runs' / 'v6_main_conclusion_adjudication'
ARG_GRAPH_PATH = AE / 'data' / 'rebuild' / 'argumentation_graph_v5.json'
CLAIM_ARG_GRAPH_PATH = AE / 'data' / 'rebuild' / 'claim_argument_graph_v1.json'
ANNOTATIONS_PATH = AE / 'data' / 'rebuild' / 'annotations_regenerated.json'
INTERPRETATION_SUMMARY_PATH = AE / 'data' / 'interpretation_space' / 'phase4' / 'phase4_summary.json'
FRONTIER_QUESTIONS_PATH = AE / 'data' / 'interpretation_space' / 'phase4' / 'prioritized_frontier_questions.json'
VALIDATION_COMPLETENESS_PATH = AE / 'data' / 'interpretation_space' / 'phase4' / 'validation_completeness.json'
BOUNDARY_MAP_PATH = AE / 'data' / 'interpretation_space' / 'phase4' / 'boundary_map.json'

INSTRUMENT_PATTERNS = {
    'EEG': [' eeg ', 'electroencephal', 'alpha asymmetry', 'frontal theta', 'erp '],
    'EDA': [' eda ', 'electrodermal', 'skin conductance', 'scr ', 'scl '],
    'HRV': [' hrv ', 'heart rate variability', 'rmssd', 'heart rate'],
    'Cortisol': ['cortisol', 'salivary cortisol'],
    'Pupil': ['pupil', 'pupill'],
    'PVT': [' pvt ', 'psychomotor vigilance'],
    'NASA-TLX': ['nasa tlx', 'task load index', 'tlx '],
    'fNIRS': ['fnirs', 'functional near infrared'],
    'EMG': [' emg ', 'electromyography', 'corrugator'],
    'Self-report': ['self report', 'questionnaire', 'survey', 'rating scale', 'stai', 'panas'],
}


def slugify(text: str) -> str:
    return ''.join(ch.lower() if ch.isalnum() else '_' for ch in text).strip('_')[:80]


def humanize(text):
    if text in (None, ''):
        return ''
    if isinstance(text, (int, float)):
        return str(text)
    return str(text).replace('theory_', '').replace('_', ' ').replace('.', ' ').strip().title()


def compact_text(text, limit=220):
    value = ' '.join(str(text or '').split())
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + '…'


def clean_doi(value):
    text = str(value or '').strip()
    if not text or text.endswith('.json'):
        return ''
    return text


def publishable_title(text):
    value = ' '.join(str(text or '').split()).strip()
    if not value:
        return ''
    low = value.lower()
    if any(re.search(pattern, low) for pattern in TITLE_REJECT_PATTERNS):
        return ''
    if value.startswith('•'):
        return ''
    if len(value.split()) < 3:
        return ''
    return value


def sanitize_year(value):
    try:
        year = int(value)
    except Exception:
        return None
    if year < 1900 or year > CURRENT_YEAR + 1:
        return None
    return year


def sanitize_abstract(text):
    value = ' '.join(str(text or '').split()).strip()
    if not value:
        return ''
    for marker in ABSTRACT_TRIM_MARKERS:
        idx = value.find(marker)
        if idx > 200:
            value = value[:idx].rstrip()
            break
    return value


def title_status(title):
    value = str(title or '').strip()
    if not value:
        return 'missing'
    if not publishable_title(value):
        return 'blocked'
    if value.endswith((',', ':')) or len(value.split()) < 5:
        return 'provisional'
    return 'good'


def abstract_status(text):
    value = sanitize_abstract(text)
    if not value:
        return 'missing'
    if len(value) < 350:
        return 'provisional'
    return 'good'


def doi_status(value):
    return 'good' if clean_doi(value) else 'missing'


def subject_count_status(value):
    return 'good' if value not in (None, '', 0) else 'missing'


def load_bibliographic_repairs():
    if not REPAIRS_PATH.exists():
        return {}
    try:
        payload = json.loads(REPAIRS_PATH.read_text())
        return payload.get('papers', {})
    except Exception:
        return {}


def load_deep_stat_adjudications():
    payload = {}
    if not DEEP_STATS_DIR.exists():
        return payload
    for path in DEEP_STATS_DIR.glob('PDF-*.deep_stats_adjudication.json'):
        try:
            obj = json.loads(path.read_text())
        except Exception:
            continue
        paper_id = obj.get('paper_id') or path.name.split('.')[0]
        payload[paper_id] = obj.get('decisions') or {}
    return payload


def load_main_conclusion_adjudications():
    payload = {}
    if not MAIN_CONCLUSION_DIR.exists():
        return payload
    for path in MAIN_CONCLUSION_DIR.glob('PDF-*.main_conclusion_adjudication.json'):
        try:
            obj = json.loads(path.read_text())
        except Exception:
            continue
        paper_id = obj.get('paper_id') or path.name.split('.')[0]
        payload[paper_id] = obj.get('decision') or {}
    return payload


def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def warrant_bucket(value):
    if isinstance(value, (int, float)):
        if value >= 0.67:
            return 'High'
        if value >= 0.4:
            return 'Medium'
        return 'Low'
    return humanize(value) or 'Unknown'


def summarize_methodology(method_profile, article_type):
    if not isinstance(method_profile, dict):
        return humanize(article_type) or 'Current rebuild article record.'
    bits = []
    if method_profile.get('study_design'):
        bits.append(humanize(method_profile['study_design']))
    if method_profile.get('method_families'):
        bits.append('Methods: ' + ', '.join(humanize(x) for x in method_profile['method_families'][:3]))
    if method_profile.get('measure_families'):
        bits.append('Measures: ' + ', '.join(humanize(x) for x in method_profile['measure_families'][:3]))
    return '; '.join(bits) if bits else (humanize(article_type) or 'Current rebuild article record.')


def detect_instruments(obj):
    haystack = ' '.join([
        str(obj.get('statement') or ''),
        str(obj.get('iv') or ''),
        str(obj.get('dv') or ''),
        str(obj.get('abstract_clean_text') or ''),
        str((obj.get('structured_result_row') or {}).get('comparison') or ''),
        str((obj.get('structured_result_row') or {}).get('outcome') or ''),
    ])
    lowered = f" {haystack.lower()} "
    found = []
    for label, patterns in INSTRUMENT_PATTERNS.items():
        if any(pat in lowered for pat in patterns):
            found.append(label)
    return found


def classify_front(front):
    label = (front.get('label') or '').lower()
    theories = ' '.join(front.get('shared_theories') or []).lower()
    constructs = ' '.join(front.get('shared_constructs') or []).lower()
    blob = ' '.join([label, theories, constructs])
    if any(x in blob for x in ['neuro', 'brain', 'cognitive_map', 'attention', 'memory', 'locus', 'circadian']):
        return 'Neuroscience'
    if any(x in blob for x in ['stress', 'arousal', 'fatigue', 'well_being', 'sleep', 'circadian', 'thermal']):
        return 'Physiological'
    if any(x in blob for x in ['theory', 'replication', 'method', 'measurement']):
        return 'Methodology'
    if any(x in blob for x in ['wayfinding', 'cog', 'creativity', 'executive', 'attention']):
        return 'Cognitive'
    return 'Environmental'


def load_fronts():
    obj = json.loads(FRONTS_PATH.read_text())
    fronts = obj.get('fronts', [])
    topic_payload = []
    gap_payload = []
    for front in fronts:
        label = front.get('label') or front.get('front_id') or 'Unlabeled front'
        cat = classify_front(front)
        size = int(front.get('size') or len(front.get('papers') or []))
        voi = round(float(front.get('mean_omega') or 0.0), 2)
        desc_bits = []
        theories = front.get('shared_theories') or []
        constructs = front.get('shared_constructs') or []
        if theories:
            desc_bits.append('Theories: ' + ', '.join(t.replace('theory_', '').replace('_', ' ') for t in theories[:3]))
        if constructs:
            desc_bits.append('Constructs: ' + ', '.join(c.replace('_', ' ') for c in constructs[:4]))
        desc_bits.append(f"Maturity: {front.get('maturity', 'unknown')}.")
        desc = ' '.join(desc_bits) if desc_bits else 'Research front from the current rebuild.'
        topic_payload.append({
            'id': front.get('front_id') or slugify(label),
            'cat': cat,
            'n': size,
            'voi': voi,
            'name': label,
            'desc': desc,
            'maturity': front.get('maturity', 'unknown'),
            'shared_theories': theories,
            'shared_constructs': constructs,
            'contradictions': int(front.get('n_contradictions') or 0),
            'replications': int(front.get('n_replications') or 0),
        })
        if size <= 8 or front.get('maturity') != 'established' or int(front.get('n_contradictions') or 0) > 0:
            if voi >= 0.7:
                voi_label = 'high'
            elif voi >= 0.45:
                voi_label = 'medium'
            else:
                voi_label = 'low'
            gap_type = 'untested' if size <= 8 else 'conflict' if int(front.get('n_contradictions') or 0) > 0 else 'credence'
            gap_payload.append({
                'id': front.get('front_id') or slugify(label),
                'type': gap_type,
                'title': label,
                'description': desc,
                'construct': slugify((constructs[0] if constructs else cat).replace('.', ' ')),
                'context': 'multiple',
                'voi': voi_label,
                'credence': voi,
                'whyMatters': f"This front remains strategically important because its current maturity is {front.get('maturity', 'unknown')} with corpus size {size}.",
                'hypothesisBuild': f"ka_hypothesis_builder.html?front={front.get('front_id')}",
                'evidenceLink': f"ka_evidence.html?front={front.get('front_id')}"
            })
    topic_payload.sort(key=lambda x: (-x['voi'], -x['n'], x['name']))
    gap_payload.sort(key=lambda x: ({'high':0,'medium':1,'low':2}[x['voi']], x['title']))
    return topic_payload, gap_payload


def parse_claims():
    evidence = []
    paper_claims = defaultdict(list)
    paper_meta = {}
    repairs = load_bibliographic_repairs()
    deep_stats = load_deep_stat_adjudications()
    main_conclusions = load_main_conclusion_adjudications()
    with CLAIMS_PATH.open() as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            pid = obj.get('paper_id')
            statement = obj.get('statement') or obj.get('claim') or ''
            result = obj.get('structured_result_row') or {}
            theories = []
            ptf = obj.get('paper_theory_frame') or {}
            theories.extend(ptf.get('canonical_theories') or [])
            theories.extend(obj.get('theory_names') or [])
            repair = repairs.get(pid, {})
            if pid and pid not in paper_meta:
                stat_decisions = deep_stats.get(pid, {})
                sample_decision = stat_decisions.get('sample_n') or {}
                p_value_decision = stat_decisions.get('p_value') or {}
                effect_decision = stat_decisions.get('effect_size') or {}
                paper_meta[pid] = {
                    'paper_id': pid,
                    'title': publishable_title(repair.get('title')) or publishable_title(obj.get('paper_title')) or publishable_title(obj.get('title')) or '',
                    'doi': clean_doi(repair.get('doi') or obj.get('doi')),
                    'year': sanitize_year(repair.get('year') or obj.get('year')),
                    'abstract': sanitize_abstract(repair.get('abstract') or obj.get('abstract_clean_text')) or '',
                    'repair_source': repair.get('source') or '',
                    'abstract_surface_path': repair.get('abstract_surface_path') or '',
                    'theories': theories,
                    'subject_count_total': obj.get('subject_count_total'),
                    'sample_n': sample_decision.get('chosen_value', obj.get('sample_n')),
                    'sample_n_status': sample_decision.get('status') or subject_count_status(obj.get('sample_n')),
                    'p_value': p_value_decision.get('chosen_value'),
                    'p_value_status': p_value_decision.get('status') or 'missing',
                    'effect_size': effect_decision.get('chosen_value'),
                    'effect_size_status': effect_decision.get('status') or 'missing',
                    'article_type': obj.get('article_type') or '',
                    'authors': repair.get('authors') or [],
                    'venue': repair.get('venue') or '',
                    'main_conclusion': (main_conclusions.get(pid) or {}).get('chosen_text') or '',
                    'main_conclusion_status': (main_conclusions.get(pid) or {}).get('status') or 'missing',
                }
            if pid:
                paper_claims[pid].append(obj)
            if len(evidence) < 200:
                result_sentence = result.get('result_sentence') or ''
                fallback_finding = result_sentence or ' -> '.join(
                    x for x in [result.get('comparison'), result.get('outcome')] if x
                )
                outcome_tags = obj.get('outcome_tags') or []
                construct_label = ''
                if outcome_tags:
                    construct_label = humanize(outcome_tags[0].get('canonical'))
                if not construct_label:
                    construct_label = compact_text(result.get('outcome') or obj.get('dv') or 'Unknown', 80)
                warrant_value = obj.get('mechanism_warrant')
                if warrant_value in (None, ''):
                    warrant_value = obj.get('evidence_strength_class')
                warrant_label = warrant_bucket(warrant_value)
                methodology_summary = summarize_methodology(obj.get('method_profile_excerpt'), obj.get('article_type'))
                evidence.append({
                    'id': len(evidence) + 1,
                    'finding': compact_text(statement or fallback_finding or pid, 220),
                    'construct': construct_label,
                    'signal': humanize(obj.get('evidence_strength_class') or obj.get('claim_type') or 'Claim'),
                    'studyType': humanize(obj.get('article_type') or 'Unknown'),
                    'warrant': warrant_label,
                    'credence': round(float(obj.get('severity') or 0.5), 2),
                    'year': sanitize_year(repair.get('year') or obj.get('year')) or '',
                    'citation': pid,
                    'abstract': compact_text(sanitize_abstract(repair.get('abstract') or obj.get('abstract_clean_text')) or 'Abstract not yet recovered from the current rebuild.', 500),
                    'claim': compact_text(statement or fallback_finding or pid, 260),
                    'methodology': methodology_summary,
                    'warrant_chain': result.get('test_statistic') or '',
                    'paper_id': pid,
                    'front_id': obj.get('topic_label') or obj.get('finding_id') or '',
                })
    articles = []
    for pid, claims in paper_claims.items():
        meta = paper_meta.get(pid, {'paper_id': pid, 'title': pid, 'doi': '', 'abstract': '', 'theories': []})
        theory_counter = Counter()
        construct_counter = Counter()
        measure_counter = Counter()
        for c in claims:
            for t in (c.get('theory_names') or []):
                theory_counter[t] += 1
            ptf = c.get('paper_theory_frame') or {}
            for t in (ptf.get('canonical_theories') or []):
                theory_counter[t] += 1
            for tag in (c.get('outcome_tags') or []):
                construct_counter[tag.get('canonical') or ''] += 1
            for tag in (c.get('env_tags') or []):
                construct_counter[tag.get('canonical') or ''] += 1
            method_profile = c.get('method_profile_excerpt') or {}
            for m in (method_profile.get('measure_families') or []):
                measure_counter[m] += 1
            for label in detect_instruments(c):
                measure_counter[label] += 1
        top_theories = [t.replace('theory_', '').replace('_', ' ') for t, _ in theory_counter.most_common(4)]
        top_constructs = [humanize(t) for t, _ in construct_counter.most_common(4) if t]
        top_measures = [humanize(t) for t, _ in measure_counter.most_common(3) if t]
        representative = claims[0] if claims else {}
        representative_result = representative.get('structured_result_row') or {}
        title = publishable_title(meta.get('title')) or publishable_title(representative.get('paper_title')) or publishable_title(representative.get('title'))
        if not title:
            title = compact_text(
                representative_result.get('comparison')
                or representative_result.get('outcome')
                or representative.get('dv')
                or representative.get('iv')
                or pid,
                120,
            )
        articles.append({
            'paper_id': pid,
            'title': title,
            'doi': clean_doi(meta.get('doi')),
            'year': sanitize_year(meta.get('year')),
            'abstract': sanitize_abstract(meta.get('abstract')) or 'Abstract not yet recovered from the current rebuild.',
            'claim_count': len(claims),
            'sample_n': meta.get('sample_n'),
            'p_value': meta.get('p_value'),
            'effect_size': meta.get('effect_size'),
            'subject_count_total': meta.get('subject_count_total'),
            'theories': top_theories,
            'constructs': top_constructs,
            'instruments': top_measures,
            'article_type': meta.get('article_type') or '',
            'authors': meta.get('authors') or [],
            'venue': meta.get('venue') or '',
            'main_conclusion': meta.get('main_conclusion') or '',
            'repair_source': meta.get('repair_source') or '',
            'abstract_surface_path': meta.get('abstract_surface_path') or '',
            'json_status': {
                'title': title_status(title),
                'doi': doi_status(meta.get('doi')),
                'abstract': abstract_status(meta.get('abstract')),
                'sample_n': meta.get('sample_n_status') or 'missing',
                'p_value': meta.get('p_value_status') or 'missing',
                'effect_size': meta.get('effect_size_status') or 'missing',
                'main_conclusion': meta.get('main_conclusion_status') or 'missing',
                'subject_count_total': subject_count_status(meta.get('subject_count_total')),
                'repair_source': meta.get('repair_source') or 'rebuild',
            },
        })
    articles.sort(key=lambda x: (-x['claim_count'], x['paper_id']))
    return evidence, articles[:250]


def build_json_status(articles):
    summary = {
        'papers_total': len(articles),
        'title_good': 0,
        'title_provisional': 0,
        'title_missing_or_blocked': 0,
        'abstract_good': 0,
        'abstract_provisional': 0,
        'abstract_missing': 0,
        'doi_good': 0,
        'doi_missing': 0,
        'sample_n_accepted': 0,
        'sample_n_provisional': 0,
        'sample_n_review_required': 0,
        'sample_n_missing': 0,
        'p_value_accepted': 0,
        'p_value_provisional': 0,
        'p_value_review_required': 0,
        'p_value_missing': 0,
        'effect_size_accepted': 0,
        'effect_size_provisional': 0,
        'effect_size_review_required': 0,
        'effect_size_missing': 0,
        'main_conclusion_accepted': 0,
        'main_conclusion_provisional': 0,
        'main_conclusion_missing': 0,
        'subject_count_good': 0,
        'subject_count_missing': 0,
    }
    rows = []
    for article in articles:
        status = article.get('json_status') or {}
        title_state = status.get('title') or 'missing'
        abstract_state = status.get('abstract') or 'missing'
        doi_state = status.get('doi') or 'missing'
        sample_state = status.get('sample_n') or 'missing'
        p_state = status.get('p_value') or 'missing'
        effect_state = status.get('effect_size') or 'missing'
        conclusion_state = status.get('main_conclusion') or 'missing'
        subject_state = status.get('subject_count_total') or 'missing'
        if title_state == 'good':
            summary['title_good'] += 1
        elif title_state == 'provisional':
            summary['title_provisional'] += 1
        else:
            summary['title_missing_or_blocked'] += 1
        if abstract_state == 'good':
            summary['abstract_good'] += 1
        elif abstract_state == 'provisional':
            summary['abstract_provisional'] += 1
        else:
            summary['abstract_missing'] += 1
        if doi_state == 'good':
            summary['doi_good'] += 1
        else:
            summary['doi_missing'] += 1
        summary[f"sample_n_{sample_state if sample_state in {'accepted', 'provisional', 'review_required'} else 'missing'}"] += 1
        summary[f"p_value_{p_state if p_state in {'accepted', 'provisional', 'review_required'} else 'missing'}"] += 1
        summary[f"effect_size_{effect_state if effect_state in {'accepted', 'provisional', 'review_required'} else 'missing'}"] += 1
        summary[f"main_conclusion_{conclusion_state if conclusion_state in {'accepted', 'provisional'} else 'missing'}"] += 1
        if subject_state == 'good':
            summary['subject_count_good'] += 1
        else:
            summary['subject_count_missing'] += 1
        rows.append({
            'paper_id': article.get('paper_id'),
            'title': article.get('title'),
            'claim_count': article.get('claim_count'),
            'json_status': status,
        })
    return {'summary': summary, 'papers': rows}


def build_dashboard(articles, evidence):
    return {
        'student_name': 'Alex Chen',
        'track': 'Track 2',
        'week_label': 'Week 4 of 10',
        'next_due_days': 3,
        'progress': {
            'apa_submissions': {'done': 7, 'target': 20, 'href': 'ka_article_propose.html'},
            'pdfs_uploaded': {'done': 3, 'target': 10, 'href': 'ka_article_propose.html'},
            'images_tagged': {'done': 24, 'target': 50, 'href': 'ka_tagger.html'},
            'articles_evaluated': {'done': min(6, len(evidence)), 'target': 15, 'href': 'ka_evidence.html'},
        },
        'recent_activity': [
            {'type': f"Evidence rows loaded: {len(evidence)}", 'date': 'Current rebuild', 'badge': 'SYNCED'},
            {'type': f"Article payload size: {len(articles)} papers", 'date': 'Current rebuild', 'badge': 'READY'},
        ],
        'leaderboard': [
            {'rank': 1, 'name': 'Jordan M.', 'count': 18},
            {'rank': 2, 'name': 'Taylor R.', 'count': 15},
            {'rank': 3, 'name': 'You (Alex Chen)', 'count': 12},
        ]
    }


def build_argumentation_payload():
    paper_graph = load_json(ARG_GRAPH_PATH, {})
    claim_graph = load_json(CLAIM_ARG_GRAPH_PATH, {})

    paper_nodes_raw = paper_graph.get('nodes') or {}
    if isinstance(paper_nodes_raw, dict):
        paper_nodes = list(paper_nodes_raw.values())
    else:
        paper_nodes = list(paper_nodes_raw)

    claim_nodes_raw = claim_graph.get('nodes') or {}
    if isinstance(claim_nodes_raw, dict):
        claim_nodes = list(claim_nodes_raw.values())
    else:
        claim_nodes = list(claim_nodes_raw)

    clusters = []
    for cluster in paper_graph.get('debate_clusters') or []:
        theories = cluster.get('theories') or []
        papers = cluster.get('papers') or []
        clusters.append({
            'cluster_id': cluster.get('cluster_id'),
            'paper_count': len(papers),
            'theory_count': len(theories),
            'papers': papers[:12],
            'theories': theories[:10],
        })
    clusters.sort(key=lambda item: (-item['paper_count'], item['cluster_id'] or ''))

    paper_nodes.sort(
        key=lambda node: (
            -(node.get('contradiction_count') or 0),
            -(node.get('claim_count') or 0),
            str(node.get('paper_id') or node.get('belief_id') or ''),
        )
    )
    claim_nodes.sort(
        key=lambda node: (
            -(node.get('incoming_attack_count') or 0),
            -(node.get('incoming_support_count') or 0),
            -(node.get('contradiction_count') or 0),
            str(node.get('belief_id') or ''),
        )
    )

    metadata = paper_graph.get('metadata') or {}
    coverage = paper_graph.get('coverage_report') or {}
    claim_metadata = claim_graph.get('metadata') or {}
    return {
        'summary': {
            'paper_node_count': metadata.get('node_count', len(paper_nodes)),
            'paper_edge_count': metadata.get('edge_count', len(paper_graph.get('edges') or [])),
            'claim_node_count': claim_metadata.get('node_count', len(claim_nodes)),
            'claim_edge_count': claim_metadata.get('edge_count', len(claim_graph.get('edges') or [])),
            'cluster_count': metadata.get('cluster_count', len(clusters)),
            'total_claims': coverage.get('total_claims', 0),
            'stance_coverage_rate': coverage.get('stance_coverage_rate', 0),
            'unique_theories': coverage.get('unique_theories', 0),
            'critical_question_payload_present': bool(claim_metadata.get('critical_question_payload_present')),
        },
        'coverage_report': coverage,
        'debate_clusters': clusters[:12],
        'paper_nodes': [
            {
                'paper_id': node.get('paper_id') or node.get('belief_id'),
                'content_preview': compact_text(node.get('content_preview') or node.get('content') or '', 180),
                'contradiction_count': node.get('contradiction_count') or 0,
                'node_qualifier': node.get('node_qualifier') or node.get('qualifier') or '',
            }
            for node in paper_nodes[:24]
        ],
        'claim_nodes': [
            {
                'belief_id': node.get('belief_id'),
                'paper_id': node.get('paper_id'),
                'content_preview': compact_text(node.get('content_preview') or node.get('content') or '', 180),
                'incoming_support_count': node.get('incoming_support_count') or 0,
                'incoming_attack_count': node.get('incoming_attack_count') or 0,
                'qualifier': node.get('qualifier') or node.get('node_qualifier') or '',
            }
            for node in claim_nodes[:24]
        ],
        'source_files': {
            'paper_graph': str(ARG_GRAPH_PATH.relative_to(ROOT)),
            'claim_graph': str(CLAIM_ARG_GRAPH_PATH.relative_to(ROOT)),
        },
    }


def build_annotations_payload():
    annotations = load_json(ANNOTATIONS_PATH, {})
    by_type = annotations.get('by_type') or {}
    annotation_rows = annotations.get('annotations') or []
    type_rows = [
        {'type': key, 'count': value}
        for key, value in sorted(by_type.items(), key=lambda item: (-item[1], item[0]))
    ]
    return {
        'summary': {
            'total_beliefs': annotations.get('total_beliefs', 0),
            'total_annotations': annotations.get('total_annotations', len(annotation_rows)),
            'artifact_role': annotations.get('artifact_role') or '',
            'canonical_source': annotations.get('canonical_source') or '',
            'description': annotations.get('description') or '',
        },
        'by_type': type_rows,
        'annotations': [
            {
                'id': row.get('id'),
                'type': row.get('type'),
                'target_type': row.get('target_type'),
                'target_id': row.get('target_id'),
                'content': compact_text(row.get('content') or '', 220),
                'confidence': row.get('confidence'),
                'status': row.get('status') or '',
            }
            for row in annotation_rows[:40]
        ],
        'source_file': str(ANNOTATIONS_PATH.relative_to(ROOT)),
    }


def build_interpretation_payload():
    phase4_summary = load_json(INTERPRETATION_SUMMARY_PATH, {})
    frontier = load_json(FRONTIER_QUESTIONS_PATH, {})
    validation = load_json(VALIDATION_COMPLETENESS_PATH, {})
    boundary = load_json(BOUNDARY_MAP_PATH, {})

    questions = []
    for row in frontier.get('questions') or []:
        questions.append({
            'frontier_id': row.get('frontier_id'),
            'belief_id': row.get('belief_id'),
            'framework_name': row.get('resolved_framework_name') or row.get('resolved_framework_id') or row.get('belief_id'),
            'voi_score': row.get('voi_score'),
            'voi_bucket': row.get('voi_bucket'),
            'zone': row.get('zone'),
            'question_set': (row.get('questions') or [])[:3],
            'matching_paper_count': len(row.get('matching_paper_ids') or []),
        })
    questions.sort(key=lambda row: (-(row.get('voi_score') or 0), row.get('framework_name') or ''))

    beliefs = []
    for row in validation.get('beliefs') or []:
        beliefs.append({
            'belief_id': row.get('belief_id'),
            'validation_completeness': row.get('validation_completeness'),
            'replication_status': row.get('replication_status'),
            'supporting_evidence_count': row.get('supporting_evidence_count'),
            'challenging_evidence_count': row.get('challenging_evidence_count'),
            'scope_specified': row.get('scope_specified'),
        })
    beliefs.sort(
        key=lambda row: (
            -(row.get('challenging_evidence_count') or 0),
            row.get('validation_completeness') or 0,
            row.get('belief_id') or '',
        )
    )

    zone_counts = (boundary.get('zone_classification') or {})
    transitions = boundary.get('transition_dynamics') or {}
    return {
        'summary': {
            'analysis_complete': bool(phase4_summary.get('analysis_complete')),
            'average_completeness': (validation.get('average_completeness')),
            'phase3_baseline': validation.get('phase3_baseline'),
            'high_voi_count': frontier.get('high_voi_count', 0),
            'medium_voi_count': frontier.get('medium_voi_count', 0),
            'low_voi_count': frontier.get('low_voi_count', 0),
            'active_boundary_count': zone_counts.get('active_boundary_count', 0),
            'identified_periphery_count': zone_counts.get('identified_periphery_count', 0),
        },
        'phase4_summary': phase4_summary,
        'frontier_questions': questions[:20],
        'validation_beliefs': beliefs[:20],
        'boundary_map': {
            'zone_classification': zone_counts,
            'beliefs_by_zone': boundary.get('beliefs_by_zone') or {},
            'transition_dynamics': transitions,
        },
        'source_files': {
            'phase4_summary': str(INTERPRETATION_SUMMARY_PATH.relative_to(ROOT)),
            'frontier_questions': str(FRONTIER_QUESTIONS_PATH.relative_to(ROOT)),
            'validation_completeness': str(VALIDATION_COMPLETENESS_PATH.relative_to(ROOT)),
            'boundary_map': str(BOUNDARY_MAP_PATH.relative_to(ROOT)),
        },
    }


def build_layers_summary(argumentation, annotations, interpretation):
    return {
        'layers': [
            {
                'id': 'argumentation',
                'title': 'Argumentation Layer',
                'href': 'ka_argumentation.html',
                'brief': 'docs/ARGUMENTATION_LAYER_ONE_PAGER_2026-03-26.md',
                'primary_metric': argumentation.get('summary', {}).get('claim_edge_count', 0),
                'primary_label': 'claim-level support edges',
            },
            {
                'id': 'annotations',
                'title': 'Annotation Layer',
                'href': 'ka_annotations.html',
                'brief': 'docs/ANNOTATION_LAYER_ONE_PAGER_2026-03-26.md',
                'primary_metric': annotations.get('summary', {}).get('total_annotations', 0),
                'primary_label': 'active annotations',
            },
            {
                'id': 'interpretation',
                'title': 'Interpretation Layer',
                'href': 'ka_interpretation.html',
                'brief': 'docs/INTERPRETATION_LAYER_ONE_PAGER_2026-03-26.md',
                'primary_metric': interpretation.get('summary', {}).get('high_voi_count', 0),
                'primary_label': 'high-VOI frontier questions',
            },
        ]
    }


def main():
    topics, gaps = load_fronts()
    evidence, articles = parse_claims()
    dashboard = build_dashboard(articles, evidence)
    json_status = build_json_status(articles)
    argumentation = build_argumentation_payload()
    annotations = build_annotations_payload()
    interpretation = build_interpretation_payload()
    layers = build_layers_summary(argumentation, annotations, interpretation)
    (OUT / 'topics.json').write_text(json.dumps({'topics': topics}, indent=2))
    (OUT / 'gaps.json').write_text(json.dumps({'gaps': gaps}, indent=2))
    (OUT / 'evidence.json').write_text(json.dumps({'evidence': evidence}, indent=2))
    (OUT / 'articles.json').write_text(json.dumps({'articles': articles}, indent=2))
    (OUT / 'dashboard.json').write_text(json.dumps({'dashboard': dashboard}, indent=2))
    (OUT / 'json_status.json').write_text(json.dumps(json_status, indent=2))
    (OUT / 'argumentation.json').write_text(json.dumps(argumentation, indent=2))
    (OUT / 'annotations.json').write_text(json.dumps(annotations, indent=2))
    (OUT / 'interpretation.json').write_text(json.dumps(interpretation, indent=2))
    (OUT / 'layers.json').write_text(json.dumps(layers, indent=2))
    print('Wrote payloads to', OUT)

if __name__ == '__main__':
    main()

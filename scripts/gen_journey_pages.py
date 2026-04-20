#!/usr/bin/env python3
"""Generate the twelve ka_journey_{slug}.html pages from structured content.

Each page describes one of the harder surfaces of the Knowledge Atlas:
what it displays, who needs it and why, the design challenge, the naive
solution now in place, a critique scaffold for each user type, and the
data files/endpoints that would populate the page with real content.
"""
import os
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ROLES = [
    ("public_visitor",  "Public visitor",
     "a scientifically-curious layperson who arrived from a link"),
    ("160_student",     "COGS 160 student",
     "a student working through one of the four tracks"),
    ("researcher",      "Researcher",
     "a working scientist (graduate student, postdoc, faculty) using the Atlas to triage literature"),
    ("practitioner",    "Practitioner",
     "an architect, designer, or clinician looking for actionable evidence"),
    ("admin",           "Administrator",
     "a course or site admin doing quality control"),
]

PAGES = [
    # ── Layer C ──────────────────────────────────────────────────────
    {
        "slug": "en",
        "title": "Epistemic Network (Web of Belief) viewer",
        "eyebrow": "Complicated journey surface · Layer C · Network representations",
        "status": "naive",
        "tier": "High — visual density is the core design problem",
        "roles_served": "researcher, 160_student, admin",
        "displays": [
            "The Epistemic Network (EN), sometimes called the Web of Belief after Quine &amp; Ullian (1978), is a directed graph whose nodes are <em>claims</em> extracted from the corpus and whose edges are <em>evidential relations</em> between those claims — support, undercutting defeat, rebutting defeat, and coherence. The viewer lets a user ask: given a claim I care about (say, <em>\"exposure to fractal patterns reduces self-reported stress\"</em>), which other claims in the Atlas support it, which undercut it, and how densely connected is the local neighbourhood?",
            "At the scale of the full corpus the network has thousands of nodes. The viewer must therefore support two modes of use: (a) a <em>local</em> view anchored on one claim, with its support/defeat neighbourhood visible at once, and (b) a <em>global</em> view in which the density of support vs. defeat edges is legible without node-level detail. The two views are joined by a zoom-and-filter affordance in the sense of Shneiderman (1996).",
            "Every edge in the EN is warranted by at least one <em>warrant</em>: a structured record that cites the source paper, the extraction confidence, the discounting factor applied, and the rule under which the extraction was made. The viewer must surface these warrants on demand; a network whose edges are unaccountable is not an epistemic representation, it is an art installation.",
        ],
        "roles_list": [
            ("researcher", "To check whether a claim they are considering writing into a paper is supported or contested by the corpus. The EN is the fastest way to see a claim's \"local epistemic neighbourhood\"."),
            ("160_student", "Track 2 students use the EN to see which of their candidate papers are already represented as claims, and which are orphans. Track 3 students use it to pick a well-supported claim to operationalise in VR."),
            ("admin", "To detect over-confidence — nodes with many support edges and zero defeat edges are either genuinely settled or the extraction pipeline is not finding disagreements, and the admin wants to know which."),
            ("practitioner", "To skim whether a claim they are about to cite in a design-decision memo stands up to the network's consensus."),
            ("public_visitor", "Likely not well served by the EN directly; a public visitor is better served by the interpretation layer, which already consumes the EN and summarises it in prose."),
        ],
        "challenges": [
            "<b>Density.</b> With ≈ 1,400 papers and an average of ≈ 4 claims each, the full graph has ≈ 5,600 nodes. Force-directed layouts at this scale are unreadable; the viewer must use semantic zoom, topic clustering, or a local-only default view.",
            "<b>Asymmetric edge types.</b> Support, undercutting defeat, and rebutting defeat look the same in a naive node-link drawing. Pollock (1995) and Haack (1993) require the distinction, so the viewer must colour-code or shape-code edges without visually overloading the drawing (Bertin's 1967 retinal-variable budget).",
            "<b>Warrant provenance.</b> Each edge should be inspectable back to the warrant that produced it — with confidence, discounting, and rule — but not permanently displayed. This is a classic <em>details-on-demand</em> problem.",
            "<b>Claim identity.</b> Two papers may make the same claim in different words. The viewer's node identity is therefore an NLP clustering decision, and the user needs to see when two visually-distinct nodes are in fact the same claim (and when the clustering is wrong).",
            "<b>Temporal evolution.</b> The EN changes as papers are added and re-extracted. A static viewer hides this; a dynamic one risks overloading the frame. A timeline scrubber is appealing but perishes in the hands of users who do not read the axis.",
        ],
        "naive": {
            "body": "The current page renders a single force-directed node-link graph of the entire EN using D3. Nodes are black circles; edges are grey straight lines. Clicking a node centers the layout and darkens the edges to its first-order neighbours. There is no edge-type distinction (support vs. defeat), no filtering, no warrant panel, no search, no zoom, and no legend.",
            "why": "A reviewer opening the page cannot tell support from defeat (the structural point of an epistemic network), cannot find a specific claim (no search), cannot see why any edge exists (no warrant on hover), and cannot survive the 5,600-node layout (the browser pins one CPU). The page satisfies the minimum structural requirement — it is a network drawing — and fails every epistemic and ergonomic requirement the representation was designed to satisfy. It is a placeholder, not a viewer.",
        },
        "files": [
            ("data", "data/ka_payloads/epistemic_network.json", "Array of <code>{id, claim_text, paper_ids, cluster_id}</code>, plus edges <code>{source, target, type: support|undercut|rebut|coherence, warrant_id, confidence}</code>. <b>Not yet wired;</b> currently a stub."),
            ("api",  "/api/warrants/{id}", "Returns the full warrant record for a given edge: rule, source paper, extracted claim, discount factor, rater."),
            ("lib",  "ka_en_render.js", "The D3-based rendering module. Current version is the naive force-directed layout; needs semantic-zoom and edge-type encoding passes."),
            ("data", "data/ka_payloads/claim_clusters.json", "Claim-identity clustering: maps <code>claim_id</code> → <code>cluster_id</code>. Produced by Article_Eater's coherence pipeline."),
            ("missing", "topic_membership_index", "Per-node topic-bundle tags, so that filtering by topic is possible. Currently absent; blocks the \"show me the EN just for lighting papers\" use case."),
            ("lib",  "Article_Eater_PostQuinean_v1_recovery/src/services/bridge_warrants.py", "The warrant service that should feed /api/warrants/{id}. Already exists upstream; the adapter to the Atlas's HTTP surface is not yet written."),
        ],
        "status_note": "This is the single page with the highest design leverage on the site. Four of the T1 theoretical frameworks (Quine &amp; Ullian 1978, Pollock 1995, Haack 1993, Bender &amp; Koller 2020) directly constrain what the viewer must show; any redesign has to take a position on all four.",
    },
    # ── BN ─────────────────────────────────────────────────────────────
    {
        "slug": "bn",
        "title": "Bayesian Network viewer",
        "eyebrow": "Complicated journey surface · Layer C · Network representations",
        "status": "naive",
        "tier": "High — abstractness of probabilistic variables is the core problem",
        "roles_served": "researcher, practitioner, 160_student",
        "displays": [
            "The Bayesian Network (BN) viewer shows a directed acyclic graph of causal variables drawn from the Atlas's mechanism layer: architectural features (e.g. <code>window-to-wall ratio</code>, <code>reverberation time</code>), intermediate cognitive/affective states (e.g. <code>attention restoration</code>, <code>cortisol level</code>), and outcomes (e.g. <code>self-reported stress</code>, <code>task accuracy</code>). Nodes carry conditional probability tables (CPTs) or, where the evidence is thin, qualitative influence labels.",
            "The viewer lets a user ask three kinds of question: a <em>predictive</em> question (given a setting of architectural features, what is the probability distribution over outcomes?), an <em>interventional</em> question in Pearl's (2009) sense (if I set feature X to value v — do(X=v) — what happens to Y?), and a <em>counterfactual</em> question (had X been different, what would Y have been for this specific case?). The three types need different UI affordances and many viewers collapse them into one.",
            "Probability values in the Atlas's BN are almost never tightly constrained by data; they are elicited from the corpus via meta-analysis plus expert elicitation. The viewer must therefore show uncertainty on every edge — credibility intervals, sample sizes, elicitation method — rather than quoting point values that invite false precision.",
        ],
        "roles_list": [
            ("researcher", "To test whether a proposed causal story is coherent with the corpus — a BN of your own theory overlaid on the Atlas's lets you see where your story adds edges the corpus does not support."),
            ("practitioner", "Design-decision support. \"If I increase window-to-wall ratio from 20% to 40%, what happens to reported stress?\" The BN is the only representation that answers this in quantified form."),
            ("160_student", "Track 3 students use the BN to pick a causal chain to operationalise in VR; Track 4 students use it as a redesign target, because CPT tables are visually hostile and invite an obvious critique."),
            ("admin", "To audit for isolated subgraphs — variables with no parents and no children — which usually indicate an extraction error."),
            ("public_visitor", "A public visitor will not know what a conditional probability table is and should be routed either to the Question-Answering layer or to a simplified plain-language summary generated from the BN."),
        ],
        "challenges": [
            "<b>Probability is abstract.</b> CPT tables are the representation experts expect and the representation novices flee. The viewer needs to present at least three levels of detail: a plain-language qualitative summary, an interactive probability slider, and the raw CPT for researchers.",
            "<b>Causal assumptions are hidden.</b> A BN <em>asserts</em> a causal direction on every edge. The viewer must make the assumption visible (\"this arrow means the paper made a causal claim; 2 of 4 cited papers instead made a correlational claim\") to avoid overselling.",
            "<b>Interventions vs. observations.</b> Pearl's do-calculus distinguishes conditioning from intervening, and the UI must too. A slider that sets a value needs to be clearly labelled as intervention (<code>do(X = v)</code>) not observation.",
            "<b>Uncertainty propagation.</b> Propagating uncertainty through a BN is computationally manageable but visually overwhelming. The viewer must show how much uncertainty is \"in\" an answer and avoid reporting a tight posterior when the priors were wide.",
            "<b>Inference cost.</b> Exact inference is #P-hard; even approximate inference on ≈ 200-node networks takes seconds in a browser. The viewer must queue, cache, and show progress.",
        ],
        "naive": {
            "body": "The current page renders a static DAG produced by Graphviz, with node labels and edge arrows but no CPTs, no sliders, no query affordance, and no uncertainty display. Clicking a node opens a modal with the node's name and a raw JSON dump of its CPT.",
            "why": "The page shows the BN but does not let the user <em>use</em> it. None of the three question types (predictive, interventional, counterfactual) is supported. The raw JSON CPT modal exposes machine-readable structure but not the semantic content a researcher or practitioner is trying to extract. A practitioner asking the core use-case question — \"what happens to stress if I double the window area?\" — has no way to ask it.",
        },
        "files": [
            ("data", "data/ka_payloads/bayesian_network.json", "Node list with CPTs, edge list with causal direction and source-paper count, plus credibility-interval metadata."),
            ("api",  "/api/bn/query", "Accepts a query of the form <code>{evidence: {X: v}, intervention: {Y: w}, target: Z}</code> and returns a posterior distribution over Z with credibility intervals."),
            ("lib",  "BN_graphical/bn_inference.py", "The Bayesian-network inference module from the sibling BN_graphical repo. Needs an HTTP adapter exposed to the Atlas."),
            ("data", "data/ka_payloads/bn_uncertainty_meta.json", "Per-edge uncertainty metadata: sample size, elicitation source, credibility bounds."),
            ("missing", "ka_bn_render.js", "Browser-side renderer supporting semantic zoom, intervention sliders, and uncertainty bars. Not yet implemented."),
        ],
        "status_note": "Tight dependency on the sibling BN_graphical repo; the two repos share variables but not code. A working BN viewer requires a contract document pinning variable names and value domains, which does not yet exist.",
    },
    # ── Interpretation layer ───────────────────────────────────────────
    {
        "slug": "interpretation",
        "title": "Interpretation layer",
        "eyebrow": "Complicated journey surface · Layer D · Reading evidence",
        "status": "naive",
        "tier": "Medium-high — the prose layer of the knowledge graph",
        "roles_served": "public_visitor, researcher, 160_student",
        "displays": [
            "The interpretation layer is where the Atlas talks <em>about</em> the evidence it has indexed. For each topic bundle (e.g. <code>luminous × cog.attention</code>) an interpretation is a short structured commentary that names the main claim the bundle supports, the qualifications, the pattern of disagreement, and the open questions. Interpretations are the layer that converts a pile of warrants into something a human can read in two minutes.",
            "Each interpretation has a provenance trail: which warrants from the EN underlie each sentence, which moderator variables are considered, and which claims are explicitly excluded for lack of evidence. The viewer must make that trail discoverable without cluttering the reading experience.",
            "Interpretations are not authoritative in the sense a review paper is; they are <em>defeasible</em> (Pollock 1987). The page must communicate that they can change as new warrants are added, and must show the timestamp and version history of each interpretation.",
        ],
        "roles_list": [
            ("public_visitor", "The interpretation layer is the main payoff for a public visitor: they came with a question, and this page answers it in prose grounded in the evidence base."),
            ("researcher",     "To see how the Atlas's synthesis agrees or disagrees with a review paper they have already read; the discrepancies are informative."),
            ("practitioner",   "To find a citation-backed one-paragraph summary they can paste into a design memo."),
            ("160_student",    "Track 2 students audit whether the interpretation's cited warrants actually say what the interpretation claims. Track 4 students treat the prose as a redesign target."),
            ("admin",          "To flag interpretations whose provenance trail has stale warrants — e.g., a warrant has since been downgraded but the interpretation still quotes it confidently."),
        ],
        "challenges": [
            "<b>Prose-plus-links.</b> The interpretation is a short essay but every claim must be anchored to a warrant. The UX for inline citations is thorny; the most obvious solution (superscripts) clutters at density.",
            "<b>Confidence gradient.</b> Sentences within one interpretation carry different confidence levels; the viewer must visually distinguish a strongly-supported sentence from a \"this is one study's speculation\" sentence without treating the entire interpretation as equally provisional.",
            "<b>Versioning.</b> Interpretations re-write when the evidence changes. The user needs to know whether they are reading the current version and what changed last.",
            "<b>Authorship and accountability.</b> Interpretations in the Atlas can be LLM-generated, human-edited, or human-written. The page must flag which, because interpretations produced by an LLM have a different error profile than human-authored ones.",
            "<b>Disagreement display.</b> When an interpretation explicitly notes \"the literature disagrees\", the page must show the two sides in a way that is balanced rather than false-balanced — i.e., weight the disagreement by evidence strength.",
        ],
        "naive": {
            "body": "The current page renders the interpretation as plain markdown converted to HTML, with plain links at the end for citations. There is no inline anchor between sentences and warrants; no confidence marker per sentence; no version banner; no authorship flag; no disagreement rendering.",
            "why": "A reader cannot tell which sentence of the interpretation is grounded in which warrant, which means they cannot tell whether a claim they doubt is supported by one 2010 paper or by a dozen replications. The interpretation therefore reads as if it were a review article — more authoritative than it should be — and defeats the Atlas's reason for being a defeasible synthesis rather than a static review.",
        },
        "files": [
            ("data", "data/ka_payloads/interpretations.json", "Per-bundle interpretation records: <code>{bundle_id, text, sentence_warrants: [{sentence_idx, warrant_ids, confidence}], authors, version, timestamp}</code>."),
            ("api",  "/api/interpretations/{bundle_id}/history", "Version history for a given interpretation."),
            ("data", "data/ka_payloads/warrants.json", "The warrant records cited by each interpretation sentence."),
            ("lib",  "ka_interpretation_render.js", "Markdown renderer with inline warrant anchors; not yet built."),
            ("missing", "sentence_confidence_classifier", "A per-sentence confidence estimator. Could be LLM-produced but not wired into the payload pipeline."),
        ],
        "status_note": "The interpretation layer is the Atlas's most user-facing surface and the one where poor design most directly misleads the public. It is an obvious T4.f redesign candidate.",
    },
    # ── Argumentation ──────────────────────────────────────────────────
    {
        "slug": "argumentation",
        "title": "Argumentation layer",
        "eyebrow": "Complicated journey surface · Layer D · Reading evidence",
        "status": "absent",
        "tier": "High — no implementation yet",
        "roles_served": "researcher, 160_student",
        "displays": [
            "The argumentation layer would render Dung's (1995) abstract argumentation frameworks over the Atlas's claim corpus: nodes are arguments (claim + supporting reasons), edges are <em>attacks</em> (one argument defeats another), and the computation produces an <em>acceptability labelling</em> — which arguments are IN (accepted), OUT (rejected), or UNDEC (undecided) under a given semantics (grounded, preferred, stable).",
            "Unlike the EN, which shows epistemic support, the argumentation layer shows the <em>argumentative structure</em>: which argument defeats which, and which coherent sets of arguments survive mutual attack. It is the view that makes contested claims visible as contested, without resolving the contest.",
            "The page does not yet exist. What follows is a spec for a page that would be the right target for T4's redesign loop in a future quarter.",
        ],
        "roles_list": [
            ("researcher", "To see whether a minority-view argument they hold is actually defeated by the majority, or merely outnumbered. Dung's semantics separate those."),
            ("160_student", "Track 4 students use the argumentation layer as a critique-heavy target — no naive solution is deployed, so they must reason about the specification first."),
            ("admin", "To audit whether the Atlas's arguments are diverse enough — a corpus with no attacks is suspicious."),
            ("practitioner", "Indirect; practitioners are usually better served by the Interpretation layer, which should quote the argumentation layer's labelling."),
            ("public_visitor", "Probably not suitable — abstract argumentation semantics require more background than a public visitor typically brings. Better routed to the interpretation layer."),
        ],
        "challenges": [
            "<b>Semantics is a choice, not a default.</b> Grounded, preferred, and stable semantics give different IN/OUT labellings; the page must let the user pick, and must explain what the choice means, without trapping the user in a philosophy-of-argumentation lecture.",
            "<b>Attack vs. disagreement.</b> Not all disagreement is an attack in Dung's sense. Mapping corpus disagreement onto the attack relation is an extraction decision the page must surface.",
            "<b>Scale.</b> At corpus scale, the attack graph is dense; visualising it is the same density problem as the EN, with an added layer of per-argument labelling that changes with semantics.",
            "<b>Explanation.</b> A user who sees \"this argument is OUT\" needs to see <em>why</em> — which attackers defeat it, and whether those attackers are themselves defeated. Recursive explanation is a distinctive requirement.",
            "<b>No familiar metaphor.</b> Unlike a belief network (which people can read as a mind-map) or a topic page (which people can read as a category browser), an argumentation framework has no everyday metaphor. The page must invent one.",
        ],
        "naive": {
            "body": "No naive solution is deployed. The placeholder currently points visitors to the Interpretation layer and notes that an argumentation viewer is planned.",
            "why": "The critique exercise for this page is therefore a <em>specification critique</em> rather than an implementation critique. The student must argue, from each user's perspective, what the page would have to do for that user; the design problem is constrained by the absence of a defaulted metaphor.",
        },
        "files": [
            ("data", "data/ka_payloads/argumentation_framework.json", "Argument list with textual content and supporting warrant IDs; attack relation; labellings under each semantics."),
            ("api", "/api/argumentation/label", "Accepts a semantics choice and returns labelling."),
            ("lib", "argumentation_solver", "Off-the-shelf Dung semantics solver; candidates: <code>py-arg</code>, <code>argupy</code>, or a hand-rolled graph-search. None currently wired."),
            ("missing", "attack-extraction pipeline", "A pipeline that turns EN defeat edges into Dung attacks, taking account of the defeat type. Not yet designed."),
            ("missing", "ka_argumentation_render.js", "Browser renderer; does not exist."),
        ],
        "status_note": "This is a Track 4 candidate whose highest-value deliverable is an informed spec, not a working prototype; the spec itself is the learning outcome.",
    },
    # ── QA ─────────────────────────────────────────────────────────────
    {
        "slug": "qa",
        "title": "Question-answering layer",
        "eyebrow": "Complicated journey surface · Layer D · Reading evidence",
        "status": "prototype",
        "tier": "Medium-high — hallucination vs. grounding is the central risk",
        "roles_served": "public_visitor, practitioner, researcher",
        "displays": [
            "The question-answering (QA) layer accepts a natural-language question (\"does exposure to daylight improve task performance?\") and returns an answer that is grounded in the corpus: a short prose answer, a confidence band, a list of the warrants cited, and a disclosure of what the system would not answer (because the corpus is silent or inconsistent).",
            "The QA surface is the one most vulnerable to LLM hallucination. The design problem is therefore not just \"return a helpful answer\" but \"refuse to answer when the corpus does not support one, and never cite a warrant the retrieval step did not actually return.\" Grounding is the load-bearing requirement.",
            "The prototype supports single-turn questions and does not yet handle follow-ups or comparative questions; it also does not route a question to the right Atlas surface (interpretation, EN, BN) — every question currently hits the same retrieval-plus-generation pipeline.",
        ],
        "roles_list": [
            ("public_visitor", "This is where the public visitor most often lands. The question-answering surface is the front door for anyone with a specific question rather than an exploration appetite."),
            ("practitioner", "To get a design-memo-ready paragraph on demand, backed by citations they can follow."),
            ("researcher", "Cautiously — researchers use QA to check whether the Atlas thinks a claim is supported, then they verify by clicking through to the EN and warrants directly."),
            ("160_student", "Track 2 students audit QA answers against their reading of the cited warrants; discrepancies are a learning payload. Track 4 students redesign the disclosure of uncertainty."),
            ("admin", "To monitor for hallucination: answers that cite warrants not in the retrieval set are a correctness bug."),
        ],
        "challenges": [
            "<b>Refusing to answer.</b> The most important design affordance is a clean \"the corpus does not support an answer to this\" path. Most QA interfaces have a weak version of this; the Atlas needs a strong one because the cost of a confident wrong answer is higher here than in general-purpose QA.",
            "<b>Citation fidelity.</b> Every sentence in the answer should be anchored to at least one retrieved warrant. The UI must surface the anchor, and the backend must enforce it.",
            "<b>Question routing.</b> Some questions are best answered from the interpretation layer, some from the BN, some from the topic page. A single QA endpoint that routes internally is appealing; a visible router is more honest.",
            "<b>Follow-ups.</b> Users ask follow-up questions (\"okay, what about older adults specifically?\"). The prototype does not carry context forward.",
            "<b>Disagreement.</b> Corpus disagreement must produce an answer like \"there are two positions, here is the evidence for each\" — not a centroid.",
        ],
        "naive": {
            "body": "The prototype accepts a text box, POSTs to a retrieval endpoint that returns the top five warrants by embedding similarity, and feeds those plus the question into an LLM. It returns the LLM's output with a list of the five warrant titles below. Confidence is not reported; refusal is not attempted; follow-ups are not supported.",
            "why": "The prototype has the right bones — retrieval-augmented generation with cited warrants — but the two most important affordances (refusal and confidence) are missing. A user who asks a question outside the corpus's coverage currently gets an answer anyway; a user who asks about a well-studied area gets the same confident tone as a user who asks about an under-studied one. The grounding contract is not enforced at the UI layer: there is nothing stopping the LLM from citing a warrant in the wrong spot, and nothing showing the user that the citation is real.",
        },
        "files": [
            ("api", "/api/qa/ask", "Accepts <code>{question, history?}</code>, returns <code>{answer, per_sentence_warrants, confidence, refusal_reason?}</code>."),
            ("lib", "ka_qa_pipeline.py", "Retrieval-augmented generation pipeline. Currently uses OpenAI embeddings + GPT-4; refusal heuristics are weak."),
            ("data", "data/ka_payloads/warrant_embeddings.npy", "Pre-computed warrant embeddings for retrieval."),
            ("missing", "confidence-calibration model", "Maps retrieval-quality signals to a confidence band the UI can display. Not wired."),
            ("missing", "follow-up context store", "Session-scoped conversation memory. Not wired."),
            ("lib", "ka_qa_render.js", "Browser-side renderer; currently renders the LLM output verbatim, does not anchor sentences to warrants."),
        ],
        "status_note": "The QA layer has the highest reputational risk of any surface on the site because a confident wrong answer here is publicly embarrassing. It is the page where refusal discipline matters most.",
    },
    # ── Mechanism ──────────────────────────────────────────────────────
    {
        "slug": "mechanism",
        "title": "Mechanism layer",
        "eyebrow": "Complicated journey surface · Layer E · Mechanisms &amp; theories",
        "status": "naive",
        "tier": "Medium-high — cross-scale mechanism chains",
        "roles_served": "researcher, practitioner, 160_student",
        "displays": [
            "The mechanism layer shows the causal pathways linking architectural and environmental features to psychological and physiological outcomes. Pathways are chains of intermediate states: for example, <em>fractal pattern in visual field → parasympathetic activation → reduced cortisol → lower self-reported stress</em>. Each link in the chain is warranted by papers in the corpus.",
            "Mechanisms span multiple levels of analysis — retinal, neural, cognitive, affective, behavioural — and pathways that are coherent at one scale may be speculative at another. The viewer must show the scale of each link and whether the link is supported by direct measurement, by theoretical inference, or by analogy.",
            "Unlike the Bayesian network (which <em>quantifies</em> dependencies) or the epistemic network (which shows <em>evidential</em> relations), the mechanism layer shows <em>constitutive</em> causal structure. The three representations are sibling views on the same underlying corpus but answer different questions.",
        ],
        "roles_list": [
            ("researcher", "To propose or refute a mediating-variable hypothesis — the mechanism layer is the natural place to see whether a proposed mediator is already a recognised node."),
            ("practitioner", "To translate a design intervention at feature-level into a plausible outcome-level effect via the intervening states. Practitioners want to know the <em>why</em>, not just the <em>what</em>."),
            ("160_student", "Track 1 students use mechanisms to anchor their tagging schema. Track 3 students operationalise a single mechanism chain in VR."),
            ("admin", "To detect mechanism chains with gaps — links that no paper in the corpus actually supports."),
            ("public_visitor", "A curious visitor can follow a chain to learn the science; the page must be legible at this level without oversimplifying."),
        ],
        "challenges": [
            "<b>Cross-scale composition.</b> A chain that goes retina → neural → cognitive → affective → behavioural passes through at least four disciplines. The viewer must communicate the scale jump, because a chain whose scale is hidden is one whose weakest link is also hidden.",
            "<b>Directness of support.</b> A link supported by a direct measurement is different from a link supported only by theoretical analogy. The page must mark the difference and avoid suggesting uniform warrant.",
            "<b>Alternative mechanisms.</b> Most outcome-feature pairs have more than one proposed mechanism. The page must show the competitors, not the winner, and must indicate when the evidence decides between them.",
            "<b>Granularity.</b> Mechanisms can be collapsed (A → Z) or expanded (A → B → C → … → Z). The user needs to pick the granularity they are reading at.",
            "<b>Citation density.</b> A four-link chain typically cites 8–20 papers. The viewer must make that count visible without making the page a bibliography.",
        ],
        "naive": {
            "body": "The current page renders each mechanism as a flat linear diagram with nodes and unlabelled arrows. Hover reveals the name of the mediator; there is no scale marker, no directness marker, no alternative-mechanism display, and no citation listing per link.",
            "why": "A researcher reading the naive diagram cannot tell whether a given link is supported by ten direct studies or by one theoretical analogy; a practitioner cannot tell which link in the chain would be the most leverage-bearing design target; a student cannot tell which mechanism is the consensus one and which is the minority view. The page has the shape of a mechanism view but not the content.",
        },
        "files": [
            ("data", "data/ka_payloads/mechanisms.json", "Mechanism records: <code>{id, topic_bundle, chain: [{node, scale, directness, warrant_ids}], alternatives: [id]}</code>."),
            ("data", "data/ka_payloads/mechanism_nodes.json", "The node taxonomy, with scale labels (retinal, neural, cognitive, affective, behavioural) and plain-language glosses."),
            ("lib", "ka_mechanism_render.js", "Chain renderer; currently shows flat node-link chains; needs scale and directness encoding."),
            ("missing", "alternative-mechanism crosswalk", "Per-pair, the list of competing mechanisms. Partially populated from the crosswalk table but not exposed in the payload pipeline."),
            ("api", "/api/mechanism/{id}/warrants", "Returns the warrants underlying every link in a named mechanism. Currently returns all warrants at once; should paginate by link."),
        ],
        "status_note": "The mechanism layer is tightly coupled to the theory layer (each mechanism is predicted by some theory) and to the BN (each mechanism's quantified version is a subgraph of the BN). Design changes here must be checked against both.",
    },
    # ── Theory ─────────────────────────────────────────────────────────
    {
        "slug": "theory",
        "title": "Theory deep-dive",
        "eyebrow": "Complicated journey surface · Layer E · Mechanisms &amp; theories",
        "status": "prototype",
        "tier": "Medium — content-heavy but bounded",
        "roles_served": "researcher, 160_student, public_visitor",
        "displays": [
            "The theory deep-dive is the page that lets a user read about one of the 24 theoretical frameworks the Atlas indexes — the eleven T1 \"foundational\" theories (e.g. Attention Restoration Theory, Stress Recovery Theory, Prospect-Refuge) and the thirteen T1.5 domain-specific theories (e.g. fractal-dimension theory of visual preference, biophilic hypothesis variants).",
            "For each theory the page shows its core claim in plain language, the mechanisms it predicts, the outcomes it has been used to explain, the empirical warrants that support or undercut its predictions, and the relationships to neighbouring theories (compatible, competing, specialises, generalises).",
            "Theories are the Atlas's most stable content, but they are also the content most prone to overclaiming. The page must communicate theoretical maturity — how much of the theory is actually tested — rather than letting each theory look equally well-supported.",
        ],
        "roles_list": [
            ("researcher", "To triage whether a theory's current state of evidence supports the use they want to put it to."),
            ("160_student", "Track 1 students use theories to anchor their tagging schema; Track 3 students pick one theory whose mechanism they will operationalise in VR."),
            ("public_visitor", "A public visitor often arrives at a theory page from a Wikipedia link or a Google result; the page must land a coherent one-minute read before offering the deeper structure."),
            ("practitioner", "Practitioners rarely want theory deep-dives; they are usually better served by mechanism or topic pages. The theory page should offer a \"for practitioners\" alternative route at the top."),
            ("admin", "To mark a theory as <code>draft</code> / <code>reviewed</code> / <code>contested</code> and to attach the responsible review panel."),
        ],
        "challenges": [
            "<b>Tier distinction.</b> T1 and T1.5 theories need to be visibly distinct; mixing them flattens a principled distinction.",
            "<b>Maturity display.</b> A well-validated theory and a speculative theory render the same on a naive template. The page must surface how much empirical work anchors each claim.",
            "<b>Cross-theory linkage.</b> Users frequently want \"what's the difference between Attention Restoration Theory and Stress Recovery Theory?\" — a comparative view that the deep-dive page does not by itself afford.",
            "<b>Citation density.</b> A well-developed theory has a hundred-plus citations. The page must rank and filter rather than list.",
            "<b>Draft banner.</b> All framework pages are currently marked \"working draft — expert review in progress\"; the page must explain what that means without chilling the reader into doubt.",
        ],
        "naive": {
            "body": "The current page is a long markdown-rendered essay per theory, with headings for <em>core claim</em>, <em>predictions</em>, <em>evidence</em>, and <em>references</em>. There is no comparative view, no maturity display, and no interactivity.",
            "why": "The prose is academically respectable but visually monotonous; a reader cannot see at a glance which theory has a thousand citations versus ten, cannot compare two theories side-by-side, and cannot navigate the graph of theoretical relationships. The draft banner at the top of every page is handled consistently (good) but does not specify what the panel review process will actually check (bad).",
        },
        "files": [
            ("data", "data/ka_payloads/theories.json", "Per-theory records with core claim, predictions, linked mechanisms, linked warrants, and relation edges to sibling theories."),
            ("data", "data/ka_payloads/theory_maturity.json", "Per-theory maturity metrics: citation count in corpus, number of successful vs. failed predictions, review-panel status."),
            ("lib", "ka_framework_page.html (per theory)", "Currently 24 static pages, one per theory. A shared renderer fed by <code>theories.json</code> would reduce duplication."),
            ("api", "/api/theory/compare", "Endpoint for the missing comparative view; not yet implemented."),
            ("missing", "theory-relation graph", "The cross-theory relationships (compatible / competes / specialises / generalises) exist in narrative form but are not a machine-readable graph yet."),
        ],
        "status_note": "The theory layer is the most read surface after the topic pages. It is a sensible T4.f redesign target because the 24 current pages share a common structure and a single template redesign cascades to all of them.",
    },
    # ── Gaps ───────────────────────────────────────────────────────────
    {
        "slug": "gaps",
        "title": "Gaps in the evidence base",
        "eyebrow": "Complicated journey surface · Layer F · Meta-fronts",
        "status": "naive",
        "tier": "Medium — absence is harder to display than presence",
        "roles_served": "researcher, admin, 160_student",
        "displays": [
            "The gaps page displays the cells of the topic × outcome crosswalk where the evidence base is thin, absent, or contested. It is the Atlas's answer to the research-planning question <em>\"where should the next study be?\"</em> and to the admin's question <em>\"where is our coverage worst?\"</em>",
            "Gaps are a negative claim: \"there is no evidence on X.\" Displaying negative claims honestly is harder than displaying positive ones because absence and under-indexing look the same from outside. The page must distinguish a genuine gap in the field's literature from a gap in the Atlas's coverage.",
            "Every cell on the gap map carries a confidence score about the gap itself: \"we are highly confident the field has not studied this\" is a different claim from \"we have not indexed papers on this, but our coverage is patchy here.\"",
        ],
        "roles_list": [
            ("researcher", "To find low-hanging research targets — cells where a single good study would materially advance the field."),
            ("admin", "To prioritise contributor outreach and index expansion. The Atlas's coverage holes drive its T2 scraping queue."),
            ("160_student", "Track 2 students take a gap and audit whether it is real; Track 1 students tag recent papers that might fill one."),
            ("practitioner", "To recognise when a design decision is being made in an evidential vacuum."),
            ("public_visitor", "Possibly — a curious visitor can see that the evidence base is uneven. The page must not mislead a visitor into concluding that \"absence of evidence\" means \"evidence of absence.\""),
        ],
        "challenges": [
            "<b>Two kinds of gap.</b> Field gap (no one studied this) vs. coverage gap (field studied it, we haven't indexed it). The page must separate them visibly.",
            "<b>Absence display.</b> Zero-value cells are invisible in many charts (e.g., a bar chart). The page must use a representation where zero is as visible as high density — typically a heatmap or a \"stars vs. dots\" encoding.",
            "<b>False precision.</b> A cell with \"3 studies\" may be more or less studied than a cell with \"5 studies\" once study quality is weighted. The page must weight rather than count.",
            "<b>Actionability.</b> A raw gap list is depressing; an actionable one is scoped to what a reader could plausibly study.",
            "<b>Update cadence.</b> Gaps move as the corpus grows. The page must show its freshness and warn when it is stale.",
        ],
        "naive": {
            "body": "The current page renders the topic × outcome crosswalk as a plain HTML table with raw study counts per cell, sorted by topic alphabetically. Zero-count cells are blank. There is no distinction between field and coverage gaps, no quality-weighting, no freshness marker, and no action affordance.",
            "why": "Blank cells read as \"nothing here to see\" rather than \"possible research opportunity\"; raw counts mislead by treating a single high-quality meta-analysis and a single opportunistic survey as equivalent. The admin who uses this page to plan outreach cannot tell a field gap from a coverage gap, which is the distinction the page most needs to make.",
        },
        "files": [
            ("data", "data/ka_payloads/crosswalk_density.json", "Per-cell record: <code>{topic, outcome, n_papers, weighted_n, quality_mean, last_ingest_ts, gap_type: field|coverage|mixed}</code>."),
            ("data", "data/ka_payloads/pubmed_coverage_estimate.json", "A coarse estimate of how many papers exist on each topic in the external literature, used to compute the field-vs-coverage distinction. Partially populated."),
            ("lib", "ka_gaps_render.js", "Heatmap renderer; needs the field-vs-coverage encoding."),
            ("api", "/api/gaps/suggest", "Returns scoped, actionable research-target suggestions; not yet wired."),
            ("missing", "quality-weighting model", "Produces <code>weighted_n</code> from raw study counts using a per-paper quality score. Spec exists; implementation pending."),
        ],
        "status_note": "The gaps page is the single most useful surface for an admin planning the next index-expansion sprint.",
    },
    # ── Evidence landscape ─────────────────────────────────────────────
    {
        "slug": "evidence",
        "title": "Evidence-landscape map",
        "eyebrow": "Complicated journey surface · Layer F · Meta-fronts",
        "status": "prototype",
        "tier": "Medium — global orientation surface",
        "roles_served": "researcher, practitioner, public_visitor",
        "displays": [
            "The evidence-landscape map is the global orientation view: it shows, for the entire topic × outcome × architectural-feature space, where the evidence base is dense, defended, mixed, or absent. It answers the question \"what is the overall shape of what the Atlas knows?\" in a single view.",
            "The map is the entry point most often visited by readers who arrive without a specific question. It is also the surface most prone to false-summary: any global view compresses decisions that a user may want to unpack, and the map must let them drill down when they do.",
            "The prototype renders the landscape as a two-dimensional heatmap (topics on one axis, outcomes on the other) with colour encoding evidence status. It is a reasonable first attempt but is not yet multi-scalar — it does not show architectural feature or theoretical framework as additional axes.",
        ],
        "roles_list": [
            ("researcher", "To orient themselves before a literature review."),
            ("practitioner", "To see which outcomes have well-studied architectural interventions, at a glance."),
            ("public_visitor", "The landscape map is often the first interesting page a visitor finds; it is the page that communicates the Atlas's scope."),
            ("160_student", "Track 2 students use the map to triage where to scout new papers."),
            ("admin", "Useful but partly redundant with the gaps page."),
        ],
        "challenges": [
            "<b>Dimensionality.</b> Topic × outcome × feature × theory = four axes. A 2D map chooses two and hides the rest; the page must give at least filter-based access to the hidden axes.",
            "<b>Colour encoding.</b> Five evidence states (defended, mixed, unresolved, thin, absent) crowd the hue budget; encoding by hue alone fails for colour-blind readers.",
            "<b>Resolution.</b> At the full corpus scale each cell is small; at topic scale each cell is large but hides its contents. The page must support semantic zoom.",
            "<b>Stability.</b> The landscape updates as the corpus grows; the page must show its version and warn when it is stale.",
            "<b>Legend density.</b> The legend for the colour scale plus the four axes plus the zoom controls will eat the page unless designed against a layout budget.",
        ],
        "naive": {
            "body": "The prototype shows a fixed-size 2D heatmap on a single canvas, with hue encoding evidence state. Hovering a cell opens a tooltip showing the topic and outcome names and the study count. There is no filter control for architectural feature or theory; no colour-blind mode; no legend; no version indicator; no zoom.",
            "why": "The map communicates the right shape — dense in lighting and acoustic research, sparser in olfactory and thermal — but a researcher wanting to filter by feature (\"just show me findings relevant to open-plan offices\") has no affordance. The colour-blind reader sees a monochrome muddle. The page does not announce its freshness; a cell that was last updated six months ago looks identical to one updated this morning.",
        },
        "files": [
            ("data", "data/ka_payloads/evidence_landscape.json", "Dense tensor <code>{topic, outcome, feature, theory, evidence_state, n_papers, last_update}</code>."),
            ("lib", "ka_landscape_render.js", "Heatmap renderer with D3; prototype works, needs filter controls, zoom, and a colour-blind palette."),
            ("api", "/api/landscape/slice", "Returns a filtered slice of the tensor given query axes."),
            ("missing", "filter-control UI", "Multi-select chips for feature and theory; not yet wired."),
            ("missing", "colour-blind palette", "Should swap hue for a perceptually ordered, colour-blind-safe palette (e.g. viridis sub-range)."),
        ],
        "status_note": "Closely coupled to the gaps page; a single update to the underlying tensor feeds both. They should probably share a filter bar.",
    },
    # ── Research fronts ─────────────────────────────────────────────────
    {
        "slug": "fronts",
        "title": "Research fronts",
        "eyebrow": "Complicated journey surface · Layer F · Meta-fronts",
        "status": "absent",
        "tier": "Medium — temporal signal + noise",
        "roles_served": "researcher, practitioner, 160_student",
        "displays": [
            "The research-fronts page would show which topics in the Atlas have the highest recent publication velocity — where the field is putting its current effort. A front is a topic + time-window combination where the number of high-quality papers indexed in the last, say, 18 months is high relative to the topic's historical baseline.",
            "Fronts are useful for orientation but treacherous for inference: a spike in publications is not evidence of truth, and a dip is not evidence of resolution. The page must present velocity as a navigation signal, not as an epistemic one.",
            "The page does not yet exist. The spec below is the critique target.",
        ],
        "roles_list": [
            ("researcher", "To scout what colleagues in adjacent labs are working on."),
            ("practitioner", "To know which architectural interventions the field is currently re-evaluating — a useful hedge against citing a soon-to-be-superseded claim."),
            ("160_student", "Track 2 students prioritise scouting recent papers on active fronts; the page is their scouting shortlist."),
            ("public_visitor", "Of modest interest; a news-cycle reader might find \"what's new in architecture-cognition research\" appealing, but the page must not mislead them into thinking new = true."),
            ("admin", "To align the Atlas's T2 scraping queue with current field effort."),
        ],
        "challenges": [
            "<b>Baseline selection.</b> \"Velocity\" requires a baseline. Choosing a per-topic historical baseline vs. a corpus-wide baseline produces different front lists; the choice must be visible.",
            "<b>Noise vs. signal.</b> A single high-profile paper can spike publication rates in a way that is news-cycle noise, not a genuine front.",
            "<b>Temporal granularity.</b> 3-month windows are noisy; 2-year windows are stale. The page must let the user pick.",
            "<b>Hype filtering.</b> Some recent-paper spikes are driven by replication failures and controversy, not by the field discovering something; the page should mark contested fronts distinctly.",
            "<b>Embargo.</b> Many recent papers in the Atlas are unreviewed or preprints; fronts driven by preprints need a provenance marker.",
        ],
        "naive": {
            "body": "No naive solution is deployed. The placeholder on this path currently redirects to the evidence-landscape map.",
            "why": "As with the argumentation layer, the critique exercise for this page is a specification critique. A student is asked what a research-front page ought to do before any design is proposed; the student must reason about which of the challenges above is a blocker for each user type.",
        },
        "files": [
            ("data", "data/ka_payloads/paper_timestamps.json", "Per-paper publication date plus venue type (journal, preprint, conference)."),
            ("data", "data/ka_payloads/topic_velocity.json", "Per-topic publication velocity at several temporal granularities. Not yet computed."),
            ("api", "/api/fronts/rank", "Returns ranked fronts for a given window + baseline choice; not yet wired."),
            ("missing", "contested-front detector", "Flags fronts where the recent papers disagree more than the historical baseline."),
            ("missing", "ka_fronts_render.js", "Browser-side renderer."),
        ],
        "status_note": "This is the page where the temptation to over-design is highest — it sounds like a news feed and could easily drift into one. The correct design target is a navigation aid, not a newsroom.",
    },
    # ── Ontology inspector ─────────────────────────────────────────────
    {
        "slug": "ontology",
        "title": "Ontology inspector",
        "eyebrow": "Complicated journey surface · Layer G · Structural inspectors",
        "status": "prototype",
        "tier": "Medium — structural reflection",
        "roles_served": "admin, researcher, 160_student",
        "displays": [
            "The ontology inspector renders the Atlas's controlled vocabulary as an interactive tree (or DAG): the hierarchies of architectural features, outcomes, mechanisms, theoretical frameworks, and measures. It is the page where a user asks \"what concepts does this site recognise, and how are they organised?\"",
            "The inspector is unusual because its content is the site's own structure. It is a reflective view — metadata about the ontology, not about the corpus — and its value is proportional to how legible it makes the ontology's design decisions (which nodes are required, which are deprecated, which are disputed).",
            "The prototype shows a tidy-tree visualisation of the four top-level branches, with nodes collapsible and a plain-text search. It does not yet show provenance (who added this node, when), deprecation status, or disputed-concept markers.",
        ],
        "roles_list": [
            ("admin", "The primary user. Admins maintain the ontology and need to see drift (new papers that don't fit existing nodes), deprecation backlogs, and outstanding merge proposals."),
            ("researcher", "To verify that a concept in their own work has a home in the Atlas's ontology."),
            ("160_student", "Track 1 students use the inspector to anchor tagging; Track 2 students use it to check whether a paper they are about to add fills a new node."),
            ("practitioner", "Of modest interest; practitioners want answers, not vocabulary trees. The inspector should offer a \"for practitioners\" off-ramp to mechanism or topic pages."),
            ("public_visitor", "Unlikely to be useful; the inspector should not be surfaced on the public navbar."),
        ],
        "challenges": [
            "<b>DAG, not a tree.</b> Some concepts have multiple parents. A naive tree widget shows a concept once and hides the duplication; the page must either show the multiple-parent structure honestly or compensate with a cross-link view.",
            "<b>Provenance.</b> Ontology nodes are decisions by specific people at specific times, with specific references. The page must surface that trail without drowning casual readers.",
            "<b>Deprecation.</b> Deprecated nodes still appear in old papers; the page must show the deprecation mapping without hiding the old node entirely.",
            "<b>Disputed concepts.</b> Some concepts are genuinely contested in the field. The page should label that rather than hiding the dispute.",
            "<b>Size.</b> The full ontology has several hundred nodes. Scrolling a tidy-tree at this size is unpleasant; the page needs search + collapse as primary affordances.",
        ],
        "naive": {
            "body": "The prototype shows a collapsible tidy-tree with the four top branches (features, outcomes, mechanisms, theories) expandable on click, and a plain-text search that highlights matching nodes. Nodes are rendered as simple labels with child-count badges. There is no DAG rendering for multi-parent nodes, no provenance tooltip, no deprecation marker, and no dispute marker.",
            "why": "The prototype is a respectable first attempt but hides the structural decisions that make an ontology a design artifact. An admin cannot see which nodes are recent additions or deprecated; a researcher cannot see which nodes are contested; a Track 1 student cannot see which nodes have multiple parents and therefore need more careful tagging judgement.",
        },
        "files": [
            ("data", "data/ka_payloads/ontology.json", "Full node + edge listing with <code>parent_ids</code>, provenance, deprecation map, and disputed-flag."),
            ("lib", "ka_ontology_render.js", "Tidy-tree renderer; works for single-parent nodes, needs a DAG pass."),
            ("api", "/api/ontology/node/{id}/history", "Provenance-over-time for a given node."),
            ("missing", "disputed-concept registry", "List of nodes flagged as contested, with the substance of the dispute. Not yet wired."),
            ("missing", "DAG renderer pass", "Multi-parent nodes should be shown as such; currently rendered multiple times."),
        ],
        "status_note": "The inspector is an admin tool first; public exposure is low-value and should probably be gated behind an admin-only or advanced-user flag.",
    },
    # ── Topic inspector ─────────────────────────────────────────────────
    {
        "slug": "topic_inspector",
        "title": "Topic inspector",
        "eyebrow": "Complicated journey surface · Layer G · Structural inspectors",
        "status": "naive",
        "tier": "Medium — per-topic reflective view",
        "roles_served": "researcher, admin, 160_student",
        "displays": [
            "Where the ontology inspector looks at the whole vocabulary, the topic inspector zooms into a single topic bundle and shows everything the Atlas has about it: the papers, the warrants, the interpretations, the mechanisms, the theories, the related bundles, and the extraction history.",
            "The inspector is the page a researcher lands on when they want to answer \"what does the Atlas know about this exact topic, in full?\" and the page an admin uses to audit a single bundle's quality — which papers belong, which mechanisms are implicated, whether the interpretation is stale.",
            "The page is tightly coupled to the main topic browser; the browser shows the same data at shallower depth. The inspector's job is to make visible what the browser hides.",
        ],
        "roles_list": [
            ("researcher", "To get the full picture on a single topic before citing it in a paper."),
            ("admin", "To audit a specific bundle end-to-end — extraction quality, paper coverage, interpretation freshness."),
            ("160_student", "Track 2 students use the inspector to plan a coverage sweep; Track 4 students use it as a redesign target because the page is dense."),
            ("practitioner", "For deep cases; usually better served by the interpretation layer or a topic page."),
            ("public_visitor", "Not a target user; the inspector should not be linked from public-facing navbars."),
        ],
        "challenges": [
            "<b>Density.</b> A mature topic has dozens of papers, tens of warrants, several mechanisms, and a handful of theories. The inspector must not force the user to scroll through all of it linearly.",
            "<b>Cross-surface links.</b> Every item on the inspector is a pointer into another surface (paper page, warrant view, mechanism layer, theory deep-dive). Designing the link density without over-cluttering is non-trivial.",
            "<b>Extraction-history panel.</b> Admins want to see when the bundle was last re-extracted, what changed, who approved it; that panel is large and must not dominate the page.",
            "<b>Staleness indicators.</b> Some data on the inspector is months old; some is days old. The page must mark freshness at field level.",
            "<b>Comparability.</b> Researchers frequently want to compare two bundles; the inspector is single-bundle and the comparison affordance belongs elsewhere — but the inspector should expose the hook.",
        ],
        "naive": {
            "body": "The current page shows a single long scroll with sections for papers, warrants, interpretation, mechanisms, theories, and history. Each section is a plain list. There is no density collapse, no cross-section anchors, no per-field freshness marker, and no comparison hook.",
            "why": "Scrolling through the inspector takes minutes on a mature bundle; a researcher looking for a specific warrant must search by browser find-on-page. The admin audit task (\"which mechanisms does this bundle cite that are not in the mechanism layer?\") has no built-in affordance and must be done manually. The page works as a data dump but not as a reflective surface.",
        },
        "files": [
            ("data", "data/ka_payloads/topic_bundles.json", "Per-bundle record: papers, warrants, interpretations, mechanisms, theories, history events."),
            ("api", "/api/topic/{id}/history", "Extraction and re-extraction history per bundle."),
            ("lib", "ka_topic_inspector_render.js", "Current long-scroll renderer; needs a section-navigation affordance and per-section collapse."),
            ("missing", "freshness-per-field metadata", "Each section's last-update timestamp; currently only a whole-bundle timestamp is stored."),
            ("missing", "compare-hook endpoint", "A shareable URL for \"compare bundle A and bundle B\"; would link to a separate comparative-view page that does not yet exist."),
        ],
        "status_note": "The inspector is the primary admin audit surface. A redesign here has disproportionate impact on extraction-pipeline quality control.",
    },
]


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Knowledge Atlas complicated surfaces</title>
<meta name="description" content="{title}: what this page displays, who needs it and why, the design challenge, the naive solution in place now, and per-user-type critique prompts.">
<script src="ka_canonical_navbar.js" defer></script>
<script src="ka_user_type.js" defer></script>
<script src="ka_journey_surface.js" defer></script>
<link rel="stylesheet" href="ka_journey_page.css">
</head>
<body data-ka-regime="global" data-ka-active="">
<div id="ka-navbar-slot"></div>

<main class="j-outer">

  <div class="j-header">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{title}</h1>
    <div class="j-meta">
      <span><b>Roles served</b> {roles_served}</span>
      <span><b>Current status</b> <span class="status-pill {status}">{status}</span></span>
      <span><b>Complexity tier</b> {tier}</span>
    </div>
  </div>

  <div class="j-siblings" id="j-siblings-slot"></div>

  <div class="j-section">
    <h2><span class="h2-icon">◧</span>What this page displays<span class="h2-hint">the information on offer</span></h2>
{display_html}  </div>

  <div class="j-section">
    <h2><span class="h2-icon">☰</span>Who needs this, and why<span class="h2-hint">functions served, per user type</span></h2>
    <ul class="role-list">
{roles_html}    </ul>
  </div>

  <div class="j-section">
    <h2><span class="h2-icon">△</span>Why this page is hard to design<span class="h2-hint">the challenges</span></h2>
    <ol>
{challenges_html}    </ol>
  </div>

  <div class="j-section">
    <h2><span class="h2-icon">✗</span>The simple naive solution in place now<span class="h2-hint">what you'll actually see</span></h2>
    <div class="j-naive">
      <span class="j-naive-label">naive — the current implementation</span>
      <div class="j-naive-body"><p>{naive_body}</p></div>
    </div>
    <div class="j-naive-why"><b>Why this is inadequate.</b> {naive_why}</div>
  </div>

  <div class="j-section">
    <h2><span class="h2-icon">✎</span>Critique it from each user's perspective<span class="h2-hint">who is and is not served by the naive solution</span></h2>
    <p>
      For each user type below, write one to three sentences: what in the
      naive solution works for that user, what fails, and what one thing a
      redesign should change first. Your drafts save to your browser; copy
      them into your T4.a or T4.f workspace when you are ready.
    </p>
    <div class="j-critique">
      <span class="j-critique-label">critique by user type</span>
{critique_html}      <button type="button" class="save-btn" onclick="saveCritique('{slug}')">Save critiques (to browser only)</button>
      <span class="j-status" id="j-crit-status">Saved.</span>
    </div>
  </div>

  <div class="j-section">
    <h2><span class="h2-icon">☷</span>Data files and endpoints to populate this page<span class="h2-hint">what a real implementation would call</span></h2>
    <ul class="file-list">
{files_html}    </ul>
  </div>

  <div class="j-section" style="background:#F9F5EE">
    <h2><span class="h2-icon">→</span>Status and next steps</h2>
    <p>{status_note}</p>
  </div>

</main>

<script>
document.addEventListener('DOMContentLoaded', function() {{
  if (window.renderJourneySiblings) window.renderJourneySiblings('{slug}');
  if (window.restoreCritique) window.restoreCritique('{slug}');
}});
</script>
</body>
</html>
"""


def render_page(page):
    display_html = "".join(f"    <p>{p}</p>\n" for p in page["displays"])

    roles_html = ""
    role_lookup = {r[0]: (r[1], r[2]) for r in ROLES}
    rationale_lookup = {role_key: rationale for role_key, rationale in page["roles_list"]}
    for role_key, label, _ in ROLES:
        rationale = rationale_lookup.get(role_key, "")
        roles_html += (
            f'      <li><span class="role-label">{label}</span>{rationale}</li>\n'
        )

    challenges_html = "".join(f"      <li>{c}</li>\n" for c in page["challenges"])

    critique_html = ""
    for role_key, role_label, role_gloss in ROLES:
        critique_html += (
            f'      <div class="role-crit">\n'
            f'        <div class="rc-head">{role_label}</div>\n'
            f'        <div style="font-size:0.82rem;color:#6B6B6B;margin-bottom:6px">'
            f'{role_gloss}</div>\n'
            f'        <textarea id="crit_{role_key}" '
            f'placeholder="What works for this user, what fails, '
            f'and one thing a redesign should change first."></textarea>\n'
            f'      </div>\n'
        )

    files_html = ""
    for ftype, fname, fdesc in page["files"]:
        files_html += (
            f'      <li><span class="file-type {ftype}">{ftype}</span>'
            f'<a>{fname}</a>'
            f'<span class="file-desc">{fdesc}</span></li>\n'
        )

    return TEMPLATE.format(
        slug=page["slug"],
        title=page["title"],
        eyebrow=page["eyebrow"],
        status=page["status"],
        tier=page["tier"],
        roles_served=page["roles_served"],
        display_html=display_html,
        roles_html=roles_html,
        challenges_html=challenges_html,
        naive_body=page["naive"]["body"],
        naive_why=page["naive"]["why"],
        critique_html=critique_html,
        files_html=files_html,
        status_note=page["status_note"],
    )


def main():
    out_dir = ROOT
    count = 0
    for page in PAGES:
        fname = out_dir / f"ka_journey_{page['slug']}.html"
        fname.write_text(render_page(page), encoding="utf-8")
        count += 1
        print(f"wrote {fname.name}")
    print(f"\n{count} journey pages written.")


if __name__ == "__main__":
    main()

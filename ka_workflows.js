/**
 * ka_workflows.js  —  ATLAS Guided Workflow Definitions
 * -------------------------------------------------------
 * Central data store for all role-specific workflows shown on
 * ka_user_home.html (workflow cards) and ka_workflow_hub.html
 * (step-by-step detail page).
 *
 * Each workflow has:
 *   id           — kebab-case identifier
 *   title        — short display name
 *   subtitle     — one-line framing
 *   objective    — what the user will accomplish (displayed prominently)
 *   forRoles     — which user types see this workflow
 *   estimatedTime — rough effort estimate
 *   badge        — category label
 *   badgeColor   — hex colour for badge chip
 *   icon         — emoji icon
 *   steps[]      — ordered step objects (see schema below)
 *
 * Step schema:
 *   id           — string (s1, s2, …)
 *   title        — step name
 *   pageLink     — ATLAS page to navigate to for this step
 *   pageName     — display name for the page link
 *   description  — 2-4 sentence description of what to do
 *   lookFor[]    — 3-4 bullet points of what to notice
 *   imageType    — key into KA_WORKFLOW_IMAGES for illustration
 *   collectArticles — boolean: show article-collector affordance on this step
 */

window.KA_WORKFLOWS = {

  // ─── WORKFLOW DEFINITIONS ───────────────────────────────────────────────────

  workflows: {

    // ── Student / Contributor ──────────────────────────────────────────────

    'first-questions': {
      id: 'first-questions',
      title: 'First Questions',
      subtitle: 'Orient yourself in the evidence landscape',
      objective: 'Surface three research questions the literature actually answers, and three it leaves open — so you know where ATLAS can help and where the real gaps are.',
      forRoles: ['student_explorer', 'contributor'],
      estimatedTime: '45–60 min',
      badge: 'Onboarding',
      badgeColor: '#2A7868',
      icon: '🔍',
      steps: [
        {
          id: 's1',
          title: 'Pick a Topic',
          pageLink: 'ka_topics.html',
          pageName: 'Topics',
          description: 'Browse the Topics page and pick one or two research areas that genuinely interest you. The topics are organised by broad construct (light, space, nature, sound, materials). Do not try to cover everything — the goal is depth over breadth in this first pass.',
          lookFor: [
            'Which areas have many ATLAS-backed questions? (Those have robust evidence.)',
            'Which have very few questions? (Those are real literature gaps.)',
            'Do any topics surprise you by having more or less evidence than expected?',
            'Are the topic labels intuitive? (Note any that confuse you — useful for Phase 3 audit.)'
          ],
          imageType: 'topic-browser',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Generate Search Queries',
          pageLink: 'ka_question_maker.html',
          pageName: 'Question Maker',
          description: 'Use the Question Maker to transform your chosen topic into semantically rich search queries. The goal is to move beyond simple keyword Boolean strings toward queries that find high-signal scientific literature. Try at least three different query reformulations.',
          lookFor: [
            'Does the tool suggest facets or sub-questions you had not considered?',
            'Which query formulation returns the most useful results when you test it in Scholar?',
            'Are the suggested queries specific enough to find measurable claims, or too broad?'
          ],
          imageType: 'query-builder',
          collectArticles: false
        },
        {
          id: 's3',
          title: 'Find and Collect Articles',
          pageLink: 'ka_article_search.html',
          pageName: 'Article Search',
          description: 'Search using at least three of: Google Scholar AI, Elicit, OpenAlex, Consensus, or Scholar GPT. Use the queries you generated in Step 2. When you find a promising article, use the Article Collector (right panel) to save it — you will submit these in Step 4.',
          lookFor: [
            'Do different search tools surface different literature? (They often do.)',
            'Which articles make explicit empirical claims with effect sizes?',
            'Are the findings consistent across studies, or contradictory?'
          ],
          imageType: 'article-search',
          collectArticles: true
        },
        {
          id: 's4',
          title: 'Submit to the Archive',
          pageLink: 'ka_article_propose.html',
          pageName: 'Submit Articles',
          description: 'Submit the best articles you collected to the ATLAS evidence archive. For each submission, write one sentence describing the key empirical claim. This annotation is what makes your submission valuable — the system already has many unannotated PDFs.',
          lookFor: [
            'Does the submission form capture all the metadata you care about?',
            'Is there anything about a paper that the form cannot express? (Note it.)',
            'How long does it take to submit five articles with good annotations?'
          ],
          imageType: 'submit-form',
          collectArticles: true
        },
        {
          id: 's5',
          title: 'Reflect: Answered vs. Open',
          pageLink: 'ka_demo_v04.html',
          pageName: 'Ask ATLAS',
          description: 'Return to the topic you chose in Step 1. Ask ATLAS three questions: one you suspect it can answer well, one you are uncertain about, and one you believe it cannot answer yet. For each, assess whether the response is accurate, hedged appropriately, or over-confident.',
          lookFor: [
            'Which questions does ATLAS handle confidently? Which does it hedge?',
            'Is the hedging calibrated? (Does it hedge when it should and commit when it should?)',
            'What is the gap between what the literature has and what ATLAS surfaces?'
          ],
          imageType: 'qa-interface',
          collectArticles: false
        }
      ]
    },

    'evidence-pipeline': {
      id: 'evidence-pipeline',
      title: 'Evidence Pipeline',
      subtitle: 'From raw article to ATLAS-ready evidence claim',
      objective: 'Take one paper all the way from discovery to a tagged, quality-assessed evidence submission that another researcher can rely on.',
      forRoles: ['contributor', 'researcher'],
      estimatedTime: '60–90 min',
      badge: 'Contribution',
      badgeColor: '#1a56a4',
      icon: '🔬',
      steps: [
        {
          id: 's1',
          title: 'Find a High-Value Paper',
          pageLink: 'ka_article_search.html',
          pageName: 'Article Search',
          description: 'Identify an article that makes an explicit, testable empirical claim about how a physical environment affects human cognition, emotion, or behavior. High-value papers: (1) report effect sizes, (2) describe sample clearly, (3) use controlled or quasi-experimental designs, (4) are peer-reviewed.',
          lookFor: [
            'Does the abstract state a hypothesis and report whether it was supported?',
            'Is there a methods section with enough detail to assess internal validity?',
            'Does the paper measure a construct ATLAS already tracks (check Topics page)?',
            'Is it cited enough to suggest the field considers it credible?'
          ],
          imageType: 'article-search',
          collectArticles: true
        },
        {
          id: 's2',
          title: 'Evaluate Evidence Quality',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'Apply the ATLAS quality rubric to your chosen paper. Assess study design, sample, measurement validity, effect size reporting, and replication status. A paper that fails multiple criteria should be noted but not submitted as strong evidence — it can be submitted with appropriate quality flags.',
          lookFor: [
            'What study design does the paper use? (RCT > quasi-experiment > correlation)',
            'How large is the sample? How representative of the target population?',
            'Are effect sizes reported with confidence intervals?',
            'Has the finding been replicated, or is this the only study?'
          ],
          imageType: 'evidence-card',
          collectArticles: false
        },
        {
          id: 's3',
          title: 'Tag the Evidence Claim',
          pageLink: 'ka_tagger.html',
          pageName: 'Tagger',
          description: 'Identify the specific CNFA construct(s) measured in the paper and tag them. A well-tagged evidence claim links: the environmental IV (e.g., luminance_mean), the psychological DV (e.g., attention_capture), the direction of effect, and the population. Be precise — "office workers in open plans" is more useful than "people".',
          lookFor: [
            'Does the paper\'s IV map cleanly to a CNFA tag, or is it ambiguous?',
            'Is the DV a construct ATLAS currently tracks? If not, flag it as a gap.',
            'What moderators does the paper report? (Size, demographics, context?)',
            'How confident are you in your tag choices? Note any uncertainty.'
          ],
          imageType: 'tagger-ui',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Submit with Annotation',
          pageLink: 'ka_article_propose.html',
          pageName: 'Submit Articles',
          description: 'Submit the paper with your quality assessment and tag annotations. The submission annotation should be a single sentence of the form: "[Study] found that [IV manipulation] [increased/decreased] [DV] by [effect size] in [population] (p = [value])." This precision makes your submission immediately useful.',
          lookFor: [
            'Does your annotation capture the key causal claim?',
            'Is the effect size and direction included?',
            'Would a researcher reading only your annotation know what to look for in the full paper?'
          ],
          imageType: 'submit-form',
          collectArticles: true
        }
      ]
    },

    'deep-dive': {
      id: 'deep-dive',
      title: 'Evidence Deep Dive',
      subtitle: 'Trace one claim from assertion to literature support',
      objective: 'Take a single ATLAS answer and follow its evidence chain back to the literature — assessing confidence, gaps, and alternative interpretations.',
      forRoles: ['student_explorer', 'researcher', 'theory_mechanism_explorer'],
      estimatedTime: '30–45 min',
      badge: 'Analysis',
      badgeColor: '#5c3d8f',
      icon: '🕵️',
      steps: [
        {
          id: 's1',
          title: 'Get an ATLAS Answer',
          pageLink: 'ka_demo_v04.html',
          pageName: 'Ask ATLAS',
          description: 'Ask ATLAS a specific question about how a physical environment affects people. Choose something you have a genuine view on — it is easier to evaluate an answer when you have prior expectations. Note the answer and the confidence level ATLAS reports.',
          lookFor: [
            'Does ATLAS commit to a direction of effect, or hedge?',
            'What evidence does it cite?',
            'Does the answer match your prior expectation? If not, why not?'
          ],
          imageType: 'qa-interface',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Inspect the Evidence',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'Navigate to the evidence cards supporting the answer you received. For each card, read the full citation and assess: How strong is this evidence on its own? Is the study design appropriate to the claim? Are there any red flags (very small n, no replication, industry-funded, etc.)?',
          lookFor: [
            'How many independent studies support the claim?',
            'Are they all from the same lab, or distributed across research groups?',
            'Do the effect sizes converge, or vary wildly across studies?',
            'Are there any studies with contradictory findings?'
          ],
          imageType: 'evidence-card',
          collectArticles: true
        },
        {
          id: 's3',
          title: 'Map the Argument',
          pageLink: 'ka_argumentation.html',
          pageName: 'Argumentation',
          description: 'In the Argumentation view, examine how the evidence is assembled into an argument. Identify the warrant that connects evidence to claim. Ask: is this warrant explicit or implicit? Is it domain-specific or a general epistemic principle?',
          lookFor: [
            'Is the warrant clearly stated, or inferred?',
            'Could a plausible alternative warrant lead to a different conclusion?',
            'Are there defeaters (evidence that weakens the claim) visible in the view?'
          ],
          imageType: 'argument-graph',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Identify Gaps and Note Them',
          pageLink: 'ka_gaps.html',
          pageName: 'Gaps',
          description: 'Navigate to the Gaps page and check whether the gap you identified is already documented. If not, note it in your reflection document. A well-specified gap includes: what the claim is, what evidence is missing, what study design would fill it, and why it matters for architectural practice.',
          lookFor: [
            'Is the gap already in ATLAS, or genuinely new?',
            'Is it a sampling gap (right construct, wrong population) or a construct gap (construct not yet studied)?',
            'What would a study look like that filled this gap?'
          ],
          imageType: 'gap-view',
          collectArticles: true
        }
      ]
    },

    // ── Researcher ──────────────────────────────────────────────────────────

    'hypothesis-test': {
      id: 'hypothesis-test',
      title: 'Hypothesis Test',
      subtitle: 'Assess whether ATLAS supports or challenges a theoretical prediction',
      objective: 'State a testable prediction from a theory of your choice, then systematically evaluate what the ATLAS evidence base says about it — including contrary evidence.',
      forRoles: ['researcher', 'theory_mechanism_explorer'],
      estimatedTime: '60–90 min',
      badge: 'Research',
      badgeColor: '#8b1a2e',
      icon: '⚗️',
      steps: [
        {
          id: 's1',
          title: 'State the Hypothesis',
          pageLink: 'ka_hypothesis_builder.html',
          pageName: 'Hypothesis Builder',
          description: 'Before searching, commit to a specific, falsifiable prediction. Use the Hypothesis Builder to formalise it: IV, DV, direction, moderators, and the theoretical mechanism you expect. A good hypothesis is not "I think nature is good" but "exposure to a window view of vegetation will reduce physiological stress indicators (measured by cortisol or heart rate) more than a matched interior view, in white-collar workers under time pressure."',
          lookFor: [
            'Is your hypothesis specific enough to be falsified?',
            'Have you identified the mechanism, not just the correlation?',
            'What would count as disconfirming evidence?'
          ],
          imageType: 'hypothesis-form',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Search for Supporting Evidence',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'Search the evidence base for studies that bear on your hypothesis. Collect studies that support it AND studies that challenge it. The quality of your analysis depends on including both.',
          lookFor: [
            'Are the supporting studies from high-quality designs (RCT, quasi-experimental)?',
            'Do they measure your specific DV, or a proxy?',
            'What moderators are reported? Are they consistent with your theoretical mechanism?'
          ],
          imageType: 'evidence-card',
          collectArticles: true
        },
        {
          id: 's3',
          title: 'Assess Contrary Evidence',
          pageLink: 'ka_argumentation.html',
          pageName: 'Argumentation',
          description: 'Equally important: actively search for studies that fail to support your hypothesis or point in the opposite direction. A hypothesis that ignores contrary evidence is confirmation-biased. Note: partial support (effect in one subgroup but not another) is evidence about moderators, not failure.',
          lookFor: [
            'Are the null results from adequately powered studies, or small and underpowered?',
            'Do the disconfirming studies measure the same construct, or a related but different one?',
            'Can the contrary evidence be explained by your theoretical mechanism (as a boundary condition)?'
          ],
          imageType: 'argument-graph',
          collectArticles: true
        },
        {
          id: 's4',
          title: 'Render a Verdict',
          pageLink: 'ka_interpretation.html',
          pageName: 'Interpretation',
          description: 'Using the Interpretation page, render a verdict: Does the evidence support, partially support, fail to support, or challenge your hypothesis? Express your confidence level and explain what additional evidence would change your assessment. This is the deliverable: a calibrated belief, not a binary yes/no.',
          lookFor: [
            'What is your all-things-considered credence in the hypothesis?',
            'What is the single piece of evidence that most changes your prior?',
            'What study would you design to resolve the remaining uncertainty?'
          ],
          imageType: 'interpretation-panel',
          collectArticles: false
        }
      ]
    },

    'lit-synthesis': {
      id: 'lit-synthesis',
      title: 'Literature Synthesis',
      subtitle: 'Map what is known, contested, and open in a domain',
      objective: 'Produce a calibrated map of the evidence landscape in one domain — distinguishing robust findings, contested claims, and genuine gaps — suitable for informing a design brief or research proposal.',
      forRoles: ['researcher'],
      estimatedTime: '90–120 min',
      badge: 'Synthesis',
      badgeColor: '#4a7c59',
      icon: '🗺️',
      steps: [
        {
          id: 's1',
          title: 'Define the Domain Boundaries',
          pageLink: 'ka_topics.html',
          pageName: 'Topics',
          description: 'Select the topic area and define its scope. Be explicit about what is inside and outside your review. A scoped synthesis ("effects of indoor plant exposure on office workers\' self-reported stress, 2000–2024") is more useful than an unscopable one ("nature and wellbeing").',
          lookFor: ['Which sub-topics are densely covered?', 'Which are sparse?', 'Are there adjacent topics that clearly bear on your domain?'],
          imageType: 'topic-browser',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Collect the Evidence Base',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'Systematically collect all relevant evidence cards in your domain. Use the Article Collector to build your corpus. Aim for completeness over selectivity in this step — you will filter and assess in Step 3.',
          lookFor: ['Are there papers you expected to find but cannot locate in ATLAS?', 'Are all the study designs represented?', 'What is the temporal spread — are there recent replications?'],
          imageType: 'evidence-card',
          collectArticles: true
        },
        {
          id: 's3',
          title: 'Assess and Categorise',
          pageLink: 'ka_argumentation.html',
          pageName: 'Argumentation',
          description: 'Group your collected evidence into: (a) robust findings — consistent across multiple high-quality studies; (b) promising but thin — supported by 1-2 studies, awaiting replication; (c) contested — studies point in different directions; (d) gaps — expected findings that are absent. Quality of design matters as much as quantity.',
          lookFor: ['Which claims have the most consistent evidence?', 'Where do studies contradict each other — and why?', 'What would a meta-analyst conclude?'],
          imageType: 'argument-graph',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Annotate and Export',
          pageLink: 'ka_annotations.html',
          pageName: 'Annotations',
          description: 'Write a synthesis annotation for each category: a 2-3 sentence summary of what the evidence shows in this domain, with appropriate epistemic hedging. Robust findings get confident statements; contested claims get explicit uncertainty. These annotations are your deliverable.',
          lookFor: ['Is your language calibrated to the evidence strength?', 'Can a non-specialist read your annotations and understand the state of knowledge?'],
          imageType: 'annotation-view',
          collectArticles: false
        }
      ]
    },

    // ── Practitioner ────────────────────────────────────────────────────────

    'design-decision': {
      id: 'design-decision',
      title: 'Design Decision Support',
      subtitle: 'Find the evidence behind a specific architectural choice',
      objective: 'Leave with a concise, evidence-grounded brief on one design decision — knowing what the literature supports, what remains uncertain, and what questions to ask of your client or the building occupants.',
      forRoles: ['practitioner'],
      estimatedTime: '30–45 min',
      badge: 'Practice',
      badgeColor: '#b05e1a',
      icon: '📐',
      steps: [
        {
          id: 's1',
          title: 'Frame the Design Question',
          pageLink: 'ka_question_maker.html',
          pageName: 'Question Maker',
          description: 'Start with a concrete design decision you are facing or anticipating — not "should buildings have good lighting?" but "what ceiling height optimises creative collaboration in a co-working studio for 15-person teams?" The more specific, the more ATLAS can help and the more clearly you will see where the evidence is thin.',
          lookFor: ['Can you operationalise the decision in terms of measurable spatial properties?', 'Is there an expected occupant population you can specify?', 'What outcome matters most — productivity, wellbeing, creative output?'],
          imageType: 'query-builder',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Browse Relevant Evidence',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'Search the evidence base for your decision domain. Focus on studies with populations similar to your target occupants and measurement of the outcome you care about. Collect articles into the Article Collector as you find them.',
          lookFor: ['Do the study populations match your client\'s context?', 'Are effect sizes large enough to be practically significant?', 'Are the environmental manipulations within achievable design parameters?'],
          imageType: 'evidence-card',
          collectArticles: true
        },
        {
          id: 's3',
          title: 'Check ATLAS\'s Reasoning',
          pageLink: 'ka_demo_v04.html',
          pageName: 'Ask ATLAS',
          description: 'Ask ATLAS directly about your decision. Treat the answer not as an oracle but as a first-pass synthesis. Check whether the evidence it cites aligns with what you found in Step 2. Disagreements between your search and ATLAS\'s answer are informative — they reveal either ATLAS gaps or your search gaps.',
          lookFor: ['Does ATLAS\'s answer match the evidence you collected?', 'Does ATLAS hedges where the literature hedges?', 'Is there anything in the evidence you found that ATLAS did not cite?'],
          imageType: 'qa-interface',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Draft the Design Brief Bullet',
          pageLink: 'ka_annotations.html',
          pageName: 'Annotations',
          description: 'Write a single, citable design brief bullet: one claim, the evidence behind it, the confidence level, and the key caveat. Example: "Ceiling heights above 2.9m correlate with improved creative-thinking task performance (Meyers-Levy & Zhu, 2007; effect: d = 0.43), though effect is moderated by task type and may not hold for analytical tasks." This is the practice-ready output.',
          lookFor: ['Is your brief bullet specific enough to inform an actual design parameter?', 'Have you included both the evidence and its limits?', 'Would a structural engineer or client understand it without HCI background?'],
          imageType: 'annotation-view',
          collectArticles: false
        }
      ]
    },

    'client-brief': {
      id: 'client-brief',
      title: 'Client Evidence Brief',
      subtitle: 'Curate a compelling, evidence-backed design rationale',
      objective: 'Assemble a concise set of 5-8 evidence cards that justify specific design choices to a client — showing the scientific basis for decisions without overwhelming non-specialist readers.',
      forRoles: ['practitioner'],
      estimatedTime: '45–60 min',
      badge: 'Practice',
      badgeColor: '#b05e1a',
      icon: '📋',
      steps: [
        {
          id: 's1',
          title: 'Identify the Key Design Claims',
          pageLink: 'ka_topics.html',
          pageName: 'Topics',
          description: 'List the three to five most important design claims you want to substantiate for this client or project. These should be the claims most likely to be questioned ("why biophilic elements?", "why this ceiling height?", "why this acoustic treatment?"). Start from your design rationale, not from ATLAS.',
          lookFor: ['Which of your design choices is most novel or counterintuitive to the client?', 'Which choices are most expensive — those need the strongest justification?'],
          imageType: 'topic-browser',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Find the Evidence',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'For each design claim, find the one or two best-supported pieces of evidence in the ATLAS archive. "Best-supported" means: clear methodology, appropriate population, replicated if possible, and effect size large enough to be practically significant. Collect these into the Article Collector.',
          lookFor: ['Is there a single landmark study that the field widely cites?', 'Are there recent meta-analyses or systematic reviews — those are most authoritative?', 'Are any of the key authors prominent enough that naming them strengthens the brief?'],
          imageType: 'evidence-card',
          collectArticles: true
        },
        {
          id: 's3',
          title: 'Write Plain-Language Summaries',
          pageLink: 'ka_annotations.html',
          pageName: 'Annotations',
          description: 'For each evidence piece, write a plain-language summary (2-3 sentences, no jargon) that a client can read without a research background. Then add a brief note on what the evidence does NOT tell you — every honest brief acknowledges limits. This honesty builds trust.',
          lookFor: ['Can someone without a research background understand your summary?', 'Have you translated the effect size into practical terms ("roughly a 15% improvement in task focus")?', 'Have you been explicit about what the evidence cannot prove?'],
          imageType: 'annotation-view',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Review for Overreach',
          pageLink: 'ka_argumentation.html',
          pageName: 'Argumentation',
          description: 'Before finalising: read your brief as a sceptical client would. Identify any claim that overstates the evidence. Overreach damages credibility more than honest hedging does. The strongest brief is the one that accurately represents both what is known and what is uncertain.',
          lookFor: ['Does any claim say "proves" when it should say "suggests"?', 'Are there alternative interpretations of the evidence that you have not acknowledged?', 'Have you cited the evidence, not just asserted the claim?'],
          imageType: 'argument-graph',
          collectArticles: false
        }
      ]
    },

    // ── Instructor ──────────────────────────────────────────────────────────

    'student-onboarding': {
      id: 'student-onboarding',
      title: 'Student Onboarding',
      subtitle: 'Approve registrations and assign tracks + research questions',
      objective: 'Move all pending student registrations through to fully approved status — with track assignments, research question assignments, and confirmation that students know their next steps.',
      forRoles: ['instructor'],
      estimatedTime: '20–40 min',
      badge: 'Admin',
      badgeColor: '#2A5FA0',
      icon: '🎓',
      steps: [
        {
          id: 's1',
          title: 'Review Pending Registrations',
          pageLink: 'ka_approve.html',
          pageName: 'Approve Students',
          description: 'Open the approval queue. For each pending student, review their track preference and skills statement. A student who has chosen a track that does not match their stated skills is a mismatch to flag — they should be redirected before, not after, they have spent a week on the wrong track.',
          lookFor: ['Which tracks are oversubscribed? Which need more students?', 'Are skills statements specific (good) or generic ("I know programming")?', 'Any students who have not submitted a skills statement at all?'],
          imageType: 'admin-queue',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Balance Track Assignments',
          pageLink: 'ka_approve.html',
          pageName: 'Approve Students',
          description: 'Assign each student to a track, balancing across the four tracks where possible. If a student\'s preference is reasonable, honour it. If the track is full, redirect to their second choice and note the reason. The target is 4-6 students per track for a class of 20.',
          lookFor: ['Are any tracks empty? That creates a problem for Phase 3 cross-audits.', 'Have you documented the rationale for any overrides?'],
          imageType: 'admin-queue',
          collectArticles: false
        },
        {
          id: 's3',
          title: 'Assign Research Questions',
          pageLink: 'ka_approve.html',
          pageName: 'Approve Students',
          description: 'Assign each student one of the eight research questions (Q01–Q08). Avoid giving students on the same track the same question — their track work will be more valuable if they are covering different evidence domains. If possible, match the research question to the student\'s stated topic interests.',
          lookFor: ['Are all 8 questions represented across your cohort?', 'Do any questions map particularly well to specific track work?'],
          imageType: 'admin-assign',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Confirm and Monitor',
          pageLink: 'ka_dashboard.html',
          pageName: 'Dashboard',
          description: 'After approving all students, check the main dashboard to confirm the assignments are reflected in the system. Note any students who have not yet logged in after receiving their approval — they may need a follow-up email.',
          lookFor: ['Have all approved students logged in?', 'Are any students stuck on setup (no articles submitted after one week)?', 'Is the article submission rate roughly on track for the class?'],
          imageType: 'dashboard-view',
          collectArticles: false
        }
      ]
    },

    // ── Theory / Mechanism Explorer ──────────────────────────────────────────

    'mechanism-trace': {
      id: 'mechanism-trace',
      title: 'Mechanism Trace',
      subtitle: 'Follow the causal chain from built environment to human outcome',
      objective: 'Map the full causal mechanism for one environmental effect — from physical stimulus to neural/physiological mediator to psychological/behavioural outcome — and assess where the chain is well-supported versus speculative.',
      forRoles: ['theory_mechanism_explorer', 'researcher'],
      estimatedTime: '60–90 min',
      badge: 'Theory',
      badgeColor: '#5c3d8f',
      icon: '🧠',
      steps: [
        {
          id: 's1',
          title: 'Select an Effect to Trace',
          pageLink: 'ka_demo_v04.html',
          pageName: 'Ask ATLAS',
          description: 'Begin with a known environmental psychology finding — one you believe is real but want to understand at the mechanistic level. State the effect in the form: "[physical property] → [outcome]." Then ask yourself: what is the mechanism? Do not settle for "exposure to nature reduces stress" — push to "which features of nature exposure, through which sensory channels, with what neural mediators, producing what stress-response modulation?"',
          lookFor: ['Can you identify at least one plausible mechanistic pathway?', 'Is the mechanism explicitly stated in the ATLAS answer, or inferred?', 'Are there multiple plausible mechanisms that could produce the same observed effect?'],
          imageType: 'qa-interface',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Find Mechanistic Evidence',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'Search specifically for studies that test the mechanism, not just the input-output relationship. Mechanistic studies typically: measure the mediator directly (e.g., cortisol, EEG), use designs that can establish mediation (e.g., mediation analysis, causal inference), or manipulate the purported mechanism to test whether the effect disappears.',
          lookFor: ['Are there studies that measure the mediating variable directly?', 'Do any studies use designs that allow causal inference about the mechanism?', 'What is the strength of the mechanistic evidence relative to the observational evidence?'],
          imageType: 'evidence-card',
          collectArticles: true
        },
        {
          id: 's3',
          title: 'Map the Causal Chain',
          pageLink: 'ka_argumentation.html',
          pageName: 'Argumentation',
          description: 'Using your collected evidence, map the causal chain with explicit uncertainty at each link. A well-specified mechanism map distinguishes: (a) well-supported links, (b) assumed but untested links, (c) plausible but untested alternatives, and (d) links that are probably spurious. Each "weak link" in the chain is a potential research gap.',
          lookFor: ['Where does the mechanistic chain break down — where is the evidence thinnest?', 'Are there alternative mechanisms that could explain the evidence equally well?', 'Does the mechanism generalise across populations and contexts?'],
          imageType: 'argument-graph',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Identify the Critical Test',
          pageLink: 'ka_hypothesis_builder.html',
          pageName: 'Hypothesis Builder',
          description: 'Identify the "critical test" — the study design that would most decisively adjudicate between competing mechanistic accounts. A critical test ideally: (1) discriminates between two plausible mechanisms, (2) is feasible in a real building, (3) measures the mediating variable directly, and (4) has ecological validity.',
          lookFor: ['What would a sceptic of your preferred mechanism demand as evidence?', 'Is the critical test technically feasible within current environmental psychology methods?', 'What is the smallest study that would be informative?'],
          imageType: 'hypothesis-form',
          collectArticles: false
        }
      ]
    }

  }, // end workflows

  // ─── ROLE CONFIGURATION ──────────────────────────────────────────────────

  byRole: {
    student_explorer:         ['first-questions', 'deep-dive', 'evidence-pipeline'],
    contributor:              ['evidence-pipeline', 'first-questions', 'deep-dive'],
    researcher:               ['hypothesis-test', 'lit-synthesis', 'evidence-pipeline', 'deep-dive'],
    practitioner:             ['design-decision', 'client-brief', 'deep-dive'],
    instructor:               ['student-onboarding'],
    theory_mechanism_explorer:['mechanism-trace', 'hypothesis-test', 'deep-dive']
  },

  // ─── ROLE META ────────────────────────────────────────────────────────────

  roleMeta: {
    student_explorer: {
      label: 'Student Explorer',
      icon: '🎒',
      color: '#2A7868',
      bgLight: '#f0fff4',
      description: 'You are in the orientation phase — learning what ATLAS contains, how evidence is structured, and where the gaps are. The First Questions workflow is the right place to start.',
      tagline: 'Explore the evidence landscape before you build in it.'
    },
    contributor: {
      label: 'Contributor',
      icon: '🔧',
      color: '#1a56a4',
      bgLight: '#eff6ff',
      description: 'You are actively contributing to the ATLAS evidence base — finding articles, tagging claims, and building the pipeline. Your work directly determines what future researchers and practitioners can rely on.',
      tagline: 'Build the evidence base one verified claim at a time.'
    },
    researcher: {
      label: 'Researcher',
      icon: '🔬',
      color: '#8b1a2e',
      bgLight: '#fff1f2',
      description: 'You are using ATLAS to support your own research — testing hypotheses, synthesising literature, and identifying gaps worth filling. You bring methodological scepticism that the system needs.',
      tagline: 'Test your hypotheses against the evidence the field has actually produced.'
    },
    practitioner: {
      label: 'Practitioner',
      icon: '📐',
      color: '#b05e1a',
      bgLight: '#fff7ed',
      description: 'You are an architect, designer, or consultant using ATLAS to ground your practice in evidence. You need specific, actionable guidance — not textbook summaries — that you can translate into design parameters.',
      tagline: 'Evidence-grounded design requires knowing what the science actually shows.'
    },
    instructor: {
      label: 'Instructor',
      icon: '🎓',
      color: '#2A5FA0',
      bgLight: '#eff6ff',
      description: 'You manage the course workflow — registrations, track assignments, research question allocation, and student progress monitoring. Your workflows are administrative but their downstream effects are academic.',
      tagline: 'The quality of student work begins with the clarity of your setup.'
    },
    theory_mechanism_explorer: {
      label: 'Theory Explorer',
      icon: '🧠',
      color: '#5c3d8f',
      bgLight: '#faf5ff',
      description: 'You are interested in the mechanistic underpinnings of environmental effects — why they happen, not just that they happen. ATLAS\'s argumentation layer and theory guides are your primary entry points.',
      tagline: 'Understanding mechanism is the difference between knowing and understanding.'
    }
  },

  // ─── IMAGE TYPE DESCRIPTIONS (SVG / CSS art descriptions) ────────────────

  imageTypes: {
    'topic-browser':       { label: 'Topics Browser', symbol: '🗂️', color: '#2A7868' },
    'query-builder':       { label: 'Query Builder',  symbol: '🔍', color: '#1a56a4' },
    'article-search':      { label: 'Article Search', symbol: '📰', color: '#5c3d8f' },
    'submit-form':         { label: 'Submit Articles', symbol: '📤', color: '#b05e1a' },
    'evidence-card':       { label: 'Evidence Card',  symbol: '📊', color: '#8b1a2e' },
    'argument-graph':      { label: 'Argument Map',   symbol: '🔗', color: '#2A5FA0' },
    'qa-interface':        { label: 'ATLAS QA',       symbol: '💬', color: '#4a7c59' },
    'hypothesis-form':     { label: 'Hypothesis',     symbol: '⚗️', color: '#8b1a2e' },
    'tagger-ui':           { label: 'Tagger',         symbol: '🏷️', color: '#1a56a4' },
    'gap-view':            { label: 'Gap Map',        symbol: '🕳️', color: '#6b7280' },
    'interpretation-panel':{ label: 'Interpretation', symbol: '⚖️', color: '#5c3d8f' },
    'annotation-view':     { label: 'Annotations',   symbol: '📝', color: '#2A7868' },
    'admin-queue':         { label: 'Approval Queue', symbol: '📋', color: '#2A5FA0' },
    'admin-assign':        { label: 'Assignment',     symbol: '📌', color: '#2A5FA0' },
    'dashboard-view':      { label: 'Dashboard',      symbol: '📈', color: '#4a7c59' }
  }

}; // end KA_WORKFLOWS

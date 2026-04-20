# T4.e Replication report — {your_id}

*Deliverable*: T4.e — Paired reproducibility check
*Pair*: {your_id} attempting to reproduce findings from {partner_id}
*Period*: Week 7
*Submit at*: `160sp/tracks/t4/{your_id}/pilot/replication_report.md`

---

## How to use this template

You received five findings from your partner (schema fields only, no screenshots, no pilot quotes, no severity). For each, open the stated page, perform the stated scenario, and record what actually happened on your machine. Repeat for all ten reproductions (five each way means you write ten rows below).

Every row must have:

- A **Verdict** from the four-value set: `FULL | PARTIAL | NONE | UNDERSPECIFIED`.
- A **Browser / viewport** line (e.g. `Safari 17.3, 1440×900`). Reproductions without environment metadata cannot be cross-checked.
- A **Timestamp** in `YYYY-MM-DD HH:MM` form. The site changes; when you looked matters.
- A numbered **Steps taken** list, verbatim where possible. Think-aloud applies to yourself here too.
- A literal **What I actually observed** paragraph, 30–60 words.
- If (and only if) the verdict is `NONE` or `PARTIAL`, a **Failure-mode hypothesis** from the five-value set: `schema-incomplete | page-absent | viewport-specific | interaction-missed | genuine-regression`, plus ≤ 30 words of evidence for that hypothesis.

Delete this "how to use" section before submitting.

---

## Summary (fill in after you have written the ten rows)

| Verdict | Count |
|---------|-------|
| FULL | {n} |
| PARTIAL | {n} |
| NONE | {n} |
| UNDERSPECIFIED | {n} |
| **Total** | **10** |

Failure-mode distribution (from the NONE / PARTIAL rows):

| Failure mode | Count |
|--------------|-------|
| schema-incomplete | {n} |
| page-absent | {n} |
| viewport-specific | {n} |
| interaction-missed | {n} |
| genuine-regression | {n} |

---

## Rows

### F-{partner_id_01} — {partner's title}

**Verdict**: FULL | PARTIAL | NONE | UNDERSPECIFIED
**Browser / viewport**: {e.g. Safari 17.3, 1440×900}
**Timestamp**: {YYYY-MM-DD HH:MM}

**Steps taken** (numbered, verbatim if possible):

1. {navigated to URL}
2. {did action}
3. {did action}

**What I actually observed** (30–60 words, literal):

{Literal description of what happened on your machine. Quote visible text where relevant. Do not paraphrase into "the site seemed to"; describe what you saw.}

**Failure-mode hypothesis**: {only if NONE or PARTIAL; pick one of: schema-incomplete | page-absent | viewport-specific | interaction-missed | genuine-regression}

**Evidence** (≤ 30 words): {one sentence of evidence, not speculation}

---

### F-{partner_id_02} — {partner's title}

**Verdict**:
**Browser / viewport**:
**Timestamp**:

**Steps taken**:

1.
2.

**What I actually observed**:

**Failure-mode hypothesis**:
**Evidence**:

---

### F-{partner_id_03} — {partner's title}

**Verdict**:
**Browser / viewport**:
**Timestamp**:

**Steps taken**:

1.

**What I actually observed**:

**Failure-mode hypothesis**:
**Evidence**:

---

### F-{partner_id_04} — {partner's title}

**Verdict**:
**Browser / viewport**:
**Timestamp**:

**Steps taken**:

1.

**What I actually observed**:

**Failure-mode hypothesis**:
**Evidence**:

---

### F-{partner_id_05} — {partner's title}

**Verdict**:
**Browser / viewport**:
**Timestamp**:

**Steps taken**:

1.

**What I actually observed**:

**Failure-mode hypothesis**:
**Evidence**:

---

### F-{partner_id_06} — {partner's title}

**Verdict**:
**Browser / viewport**:
**Timestamp**:

**Steps taken**:

1.

**What I actually observed**:

**Failure-mode hypothesis**:
**Evidence**:

---

### F-{partner_id_07} — {partner's title}

**Verdict**:
**Browser / viewport**:
**Timestamp**:

**Steps taken**:

1.

**What I actually observed**:

**Failure-mode hypothesis**:
**Evidence**:

---

### F-{partner_id_08} — {partner's title}

**Verdict**:
**Browser / viewport**:
**Timestamp**:

**Steps taken**:

1.

**What I actually observed**:

**Failure-mode hypothesis**:
**Evidence**:

---

### F-{partner_id_09} — {partner's title}

**Verdict**:
**Browser / viewport**:
**Timestamp**:

**Steps taken**:

1.

**What I actually observed**:

**Failure-mode hypothesis**:
**Evidence**:

---

### F-{partner_id_10} — {partner's title}

**Verdict**:
**Browser / viewport**:
**Timestamp**:

**Steps taken**:

1.

**What I actually observed**:

**Failure-mode hypothesis**:
**Evidence**:

---

## Reflection (≈ 250 words; graded separately)

Write a reflection covering:

1. **Which schema fields were most load-bearing?** Which of the partner's fields made the reproductions easiest (e.g. a specific URL with a query string), and which were too vague to be useful (e.g. "somewhere on the home page")?
2. **Was the failure-mode distribution surprising?** If you expected most non-reproductions to be `genuine-regression` and they were actually `schema-incomplete`, that is informative about audit quality rather than site instability.
3. **One concrete schema revision you would propose.** Given what you learned from being on the receiving end of the schema, what would you change about T4.a's finding template?
4. **One citation from the replication literature.** Brandt et al. (2014) is the default starting point; any of the cited references in `ka_t4_e_reproducibility.html` is acceptable. The band-3 reflection engages with that citation rather than treating it as decoration.

---

## References

Brandt, M. J., IJzerman, H., Dijksterhuis, A., Farach, F. J., Geller, J.,
    Giner-Sorolla, R., Grange, J. A., Perugini, M., Spies, J. R., &
    van 't Veer, A. (2014). The Replication Recipe: What makes for a
    convincing replication? *Journal of Experimental Social Psychology,
    50*, 217–224. https://doi.org/10.1016/j.jesp.2013.10.005

{add any additional citations you use here}

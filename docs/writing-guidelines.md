# Writing Guidelines

Rules for prose in REPORT.md and Quarto chapters. Enforced by `tools/report-check.py`.

## Principle

Research reports state findings. They do not narrate themselves, predict the
reader's confusion, or dress evidence in promotional language. Most institutional
credibility comes from what you refuse to write.

---

## Voice (Positive Style)

### Core Traits

- **Impact-first.** Lead with what changed, then the mechanism. The finding
  goes in sentence one, not after three paragraphs of background.
- **Number-anchored.** Specific figures over adjectives. "63% of respondents
  rated usefulness ≥ 4" over "a strong majority found it useful." Numbers
  are the credibility.
- **Plain-language translation.** Every technical concept gets a one-line
  human gloss on first use. Pass the Grandmother Test.
- **Active voice where natural.** "We recruited 120 organisations" over
  "120 organisations were recruited by the research team."
- **Declarative rhythm.** Short, factual sentences. Em-dashes to define
  inline — "the stated-demand screen — a conjunctive rule requiring both
  usefulness and probability thresholds."
- **Confident, not promotional.** State the accomplishment; don't sell it.
  Let the evidence carry the weight.

### Before/After Framing

When describing what the study reveals or what a proposition changes, use
concrete before/after contrasts rather than abstract claims:

- "Manual model discovery across fragmented repositories → searchable
  catalog with provenance metadata"
- Not: "A revolutionary improvement to the AI ecosystem"

---

## Anti-Style: Banned Words and Phrases

### Hype and Marketing-Speak

These kill credibility in a research document:

| Banned | Replacement |
|--------|-------------|
| groundbreaking | State the finding plainly |
| revolutionary | Describe what changed |
| cutting-edge | Name the technique |
| game-changing | Show the before/after |
| seamless | Almost never literally true |
| state-of-the-art | Cite the benchmark instead |
| unprecedented | Unprovable without checking all precedent |
| transformative | Show the transformation with numbers |
| next-generation | Name the version or capability |
| paradigm shift | Describe the actual change |
| world-class / best-in-class | Against what benchmark? |

### AI-Tells (Machine-Written Markers)

| Banned | Why |
|--------|-----|
| "delve into" | LLM tell; adds nothing |
| "in today's fast-paced world" | Filler |
| "it is important to note" | Just state the thing |
| "it is worth noting" | Just state the thing |
| "stands as a testament to" | Promotional |
| "plays a pivotal/crucial role" | Intensifier; say what it does |
| "navigate the landscape" | Metaphor doing no work |
| "in the realm of" | Use "in" |
| "harness the power of" | Use "use" |
| "underscore / showcase" | Use "show" or "demonstrate" |
| robust (as filler) | Vague; name the property |
| leverage / leveraging | Use "use" |

### Empty Intensifiers

Cut, or replace with the figure:

- "significantly / dramatically / vastly" → give the number
- "vital / crucial / paramount" → say why it matters

### Self-Narrating Patterns

The report should not describe its own structure except in a designated
"Document Structure" section (typically §1.5). Elsewhere:

| Don't write | Write instead |
|-------------|--------------|
| "This chapter presents the methodology" | (Just present the methodology) |
| "This section describes the findings" | (Just describe the findings) |
| "As mentioned in §3 above" | (State the fact; cite if needed) |
| "The reader should note that" | (State it directly) |
| "Rather than left implicit" | (Make the disclosure directly) |

---

## Structural Anti-Patterns

- **Burying the lead** — the impact goes in sentence one, not after
  three paragraphs of background.
- **Implementation-first** — say what changed for people, then how.
  "Researchers can query models without provisioning infrastructure"
  over "we deployed containerized inference workflows."
- **Unexplained jargon** — every acronym or technical term gets a
  plain-language gloss on first use.
- **Fabricated specificity** — never invent a percentage or metric.
  "Early results show promise" if the data isn't final.
- **Hedging** — say it or cut it. No "it could be argued that."
- **Numbered lists where a sharp paragraph would do.**

---

## No Internal Machinery in Reader-Facing Prose

**Write the substance, not the authority for it.**

The report is the public deliverable. How the study governs itself — which internal
artifact authorised a decision, where that authorisation is filed, which requirement or
task it came from — is traceability metadata. It belongs in the records that carry it,
never in the report.

A methodological commitment should read as the study's own reasoning, because that is
the form a reviewer can check. Citing the internal artifact that authorised it gives a
reviewer nothing to check and reads as bureaucracy.

### Never in REPORT.md, the chapters, or the generated analysis outputs

| Category | Examples |
| :--- | :--- |
| Constitution principle citations | `(Constitution IV)`, `per Constitution XII` |
| The constitution or its Research Contract, as a named artifact | "transcribed from the constitution's Research Contract" |
| Spec Kit identifiers | `FR-201`, `SC-704`, `T012`, `DEC-001`, `DEV-001` |
| Spec references | `spec 005`, `specs/007-report-completion`, `tasks.md` |
| Internal role jargon | `study owner`, `study-owner` |
| Repository paths | `docs/sampling-plan.md`, `evidence/viability-thresholds.json`, `instrument/lib/derivation.ts` |
| Issue references | `#166` |
| The report file itself | `REPORT.md` |

### Rewrites

| Instead of | Write |
| :--- | :--- |
| "Recruitment provenance is not a respondent construct (Constitution IV)." | "Recruitment provenance is not a respondent construct. No analysis groups respondents by a label the respondent supplied." |
| "Transcribed from the constitution's Research Contract, approved by the study owner on 5 August 2026 (`docs/decision-log.md`, DEC-001)." | Nothing. State the research questions. |
| "The sampling plan is specified in full in `docs/sampling-plan.md`." | "…set out in full in the accompanying sampling and recruitment plan." |
| "Thresholds are frozen in `evidence/viability-thresholds.json` at version 1.0.0." | "Thresholds are frozen in an accompanying machine-readable ledger at version 1.0.0." |
| "**Study-owner thresholds** are normative choices." | "**Study-defined thresholds** are normative choices." |
| "This is a study-owner decision recorded in the decision log." | "This is a decision of the study team, recorded and dated before collection." |
| "Both are reported separately (Constitution VI)." | "Both are reported separately. No composite of the two is computed anywhere." |

### Three things this rule does not remove

**Dated approvals and version freezes stay.** "The frame was approved on 2 August 2026
against those five artifacts" is a reproducibility statement and a reviewer needs it.
Drop the internal role label and the file path, keep the fact and the date.

**Companion artifacts may be referenced, by description.** The sampling plan, the
threshold ledger, and the governance record are deliverables a reviewer should be able
to request. Name them as accompanying documents, not as repository paths — where the
study happens to be stored is an implementation detail.

**Published tooling may be cited as a source.** Naming the instrument's published
source, an audit tool, or an analysis pipeline in a provenance disclosure is a citation,
of the same kind as naming your statistical software. Cite it with a reference number
like any other source.

### Words that look like violations and are not

The checker is deliberately narrow, because three legitimate usages sit close to the
banned pattern:

- "the **constitutional** auditor" — the Commission on Audit
- "**Constitutional** Commissions" — a class of Philippine government body
- "a **constitutional** body, the Judiciary, or the Legislature" — a frame category

`Constitution` followed by a roman numeral is always a principle citation.
`Constitutional` followed by anything else is ordinary English. If a legitimate phrase
does trip the check, widen the exemption rather than rewording sound prose.

### Where this material does belong

| Content | Home |
| :--- | :--- |
| Principle statements and the research contract | the constitution |
| Owner decisions, protocol deviations | the decision log |
| Requirement and task identifiers | the relevant spec |
| Predecessor artifact dispositions | the migration register |
| Report-to-instrument traceability | the concordance record |

---

## Pre-Publication Checklist

Before declaring a draft done:

1. Does the impact land in the first sentence of each section?
2. Did a hype word or AI-tell slip in? (Run `npm run lint:report`)
3. Is every number traceable to a source or derivation?
4. Would a skeptic or reviewer catch something overstated?
5. Will the claims still be accurate if the study timeline extends?
6. Are inference limits stated alongside every finding?
7. Does every claim map to a measurement, a sample, and a boundary?
8. Does any sentence cite an internal artifact instead of making its own case?

---

## Enforcement

```bash
npm run lint:report
```

`tools/report-check.py` runs four checks over REPORT.md, `index.qmd`,
`references.qmd`, the Quarto chapters, the generated analysis outputs, and the sampling
plan:

| Check | Catches |
| :--- | :--- |
| Anti-style sweep | Hype, AI-tells, empty intensifiers, self-narration |
| Heading hierarchy | A skipped level, such as h2 followed by h4 |
| Internal machinery | Governance and process references in reader-facing prose |
| Citation integrity | Dangling `[n]` citations with no matching entry in references.qmd |

Any match fails the build with `--strict`. Citation lines and HTML comments are
excluded from the anti-style sweep, so quoted material does not trip it.

**The generated analysis outputs are checked too.** Those files are pasted into the
findings chapter as they are, so prose written inside an analysis module is report prose
and is held to the same standard.

### Exemptions

Two, both narrow, and each because the check would otherwise contradict the document's
purpose:

| Exempt | From | Why |
| :--- | :--- | :--- |
| `.specify/`, `docs/`, `specs/`, `tools/` | Internal-machinery check | These are the governance layer. They exist to carry principle citations, identifiers, and paths |
| `references.qmd` | Internal-machinery check | A bibliography legitimately contains URL path segments and the names of cited tools |
| `docs/writing-guidelines.md` | Anti-style sweep | This file has to quote the banned vocabulary in order to ban it |

Every exemption is partial. The writing guide is still checked for heading hierarchy
and internal machinery; the governance documents are still swept for hype and
AI-tells. A checker that fails on its own rulebook, or on the constitution it enforces,
teaches people to ignore it — so the exemptions exist, and they are kept as tight as
possible.

If a legitimate phrase trips a check, widen the exemption. Do not reword sound prose to
satisfy a pattern that was too broad.

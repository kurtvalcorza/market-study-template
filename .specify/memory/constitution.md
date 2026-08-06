<!--
  TEMPLATE — Replace all [bracketed placeholders] with your study's specifics.
  Remove this comment block once the constitution is ratified for your study.
-->

# [Study Name] Constitution

## Research Contract

Approved by the study owner on [date]. Research questions and scope are
study-owner decisions (see Study Owner and Decision Rights). The decision is
recorded here, and REPORT.md restates it in its own voice rather than authoring
or citing it.

### Primary decision

[State the primary decision the study exists to inform — e.g., whether to
proceed with a product, policy, or initiative based on external evidence.]

### Research questions

- **RQ1 — [Short label].** [Full research question]
- **RQ2 — [Short label].** [Full research question]
- **RQ3 — [Short label].** [Full research question]
- **RQ4 — [Short label].** [Full research question]

[Add or remove RQs as needed. Each must map to a decision use.]

### Primary outcome

**[Name the primary outcome]**, reported as a distribution with its mean, median,
and an explicit uncertainty statement.

[List supporting outcomes here, noting which RQ each answers.]

### Status of any derived screens or thresholds

[If the study defines a threshold or screen (e.g., a conjunctive rule), describe
it here and note that it is a secondary, study-defined reporting rule — not a
validated boundary. State that it is reported after the raw distributions and
always beside its sensitivity analysis, consistent with Principle VII.]

## Core Principles

### I. Decision and Research-Question Primacy

Every item, transformation, classification, and analysis MUST map to an
approved research question, a decision use, or a necessary validity/control
function. No derived variable without a decision use. If a survey item does
not populate an RQ, a predefined table/figure, or a validity check, its
inclusion requires explicit justification from the study owner.

### II. Minimum Sufficient Measurement

Use the smallest set of direct measures capable of answering the study
questions. Raw or minimally transformed responses are preferred over composite
scores, personas, quadrants, inferred classes, and route-specific instruments.

### III. Measurement Before Interpretation

Demand-critical structured answers are immutable once submitted. Qualitative
probes may explain an answer but MUST NOT coach, reconcile, or revise the
quantitative measurement used in primary analysis. Apparent tensions between
measures are data, not errors to repair.

### IV. Recruitment Variables Are Not Respondent Constructs

Frame attributes govern recruitment and coverage. Respondent-reported attributes
are descriptive analytical variables unless independently known before
invitation. Response-derived attributes MUST NOT determine quota assignment.

### V. Bounded Inference

The survey reports scenario-bound stated preference from a targeted
non-probability sample. It MUST NOT translate stated probability into realized
adoption, sample shares into national prevalence, or demand evidence into
technical, commercial, economic, or operational viability.

### VI. Separate Constructs Remain Separate

Distinct measures that answer different questions MUST NOT be combined into a
composite index without a defensible measurement model.

### VII. Raw Evidence Before Thresholds

Primary reporting leads with the underlying distributions. Any thresholded
screen is secondary, fixed before production, explicitly study-defined unless
externally validated, and accompanied by sensitivity analysis.

### VIII. Uncertainty Is Valid Data

"Don't know", "cannot assess", and "not applicable" are legitimate
organisational responses where appropriate. The instrument MUST NOT manufacture
precision by forcing judgments respondents cannot support. Item-level
denominators are reported.

### IX. Respondent Burden Is a Design Constraint

The core instrument MUST target a median completion time of no more than
[target minutes, e.g. 12] minutes and approximately [target item count, e.g.
12–15] substantive structured questions. Additional items require explicit
research or control justification from the study owner. A progress indicator
MUST be visible to respondents throughout.

### X. Human-Readable and Reproducible Analysis

A reviewer MUST be able to reconstruct every headline result from the survey
items and a short analysis specification. Retain provenance, versioning,
invitation integrity, duplicate handling, immutable raw responses,
deterministic derivation, and report-side validation.

### XI. Pre-Fielding Freeze

Production collection MUST NOT begin until the proposition, instrument,
sampling plan, primary analysis plan, thresholds, missing-data rules,
privacy/retention rules, cognitive-pilot disposition, and empty result tables
are frozen and versioned.

### XII. Evidence-Stream Independence

[If your study has multiple evidence streams — e.g., demand validation,
technical readiness, economic viability — state here that each is assessed
under its own method and limits before any integration chapter combines them.]

## Complexity Stop-Rule

Complexity requires evidence of need. After the design reaches fielding freeze,
a new survey item, route, derived variable, score, classification, control, or
analytical layer MUST respond to a documented defect or required decision that
cannot be addressed adequately by the existing design. Precaution, convenience,
or hypothetical future usefulness alone is insufficient.

Once the redesign passes:

1. Method review
2. Report–instrument concordance
3. Cognitive pilot and burden target
4. Synthetic analysis dry run
5. Privacy/security review

Stop redesigning and field the study unless a concrete blocker is found.

## Study Owner and Decision Rights

**Study Owner**: [Name, Role]

Spec Kit and automated checks enforce contracts but do not own decisions.
Substantive construct, rule, and scope decisions are explicitly human-owned
and recorded as decisions. The study owner holds final authority over:

- Research questions and scope
- Proposition scenario approval
- Sampling-plan approval
- Instrument wording and pilot disposition
- Thresholds before fielding
- Fielding changes
- Viability thresholds (if applicable)
- Final interpretation where evidence streams conflict

Model-assisted work may propose or implement artifacts, but the study owner
decides and the decision is recorded.

## Fielding-Change Policy

Once the first production response is accepted, the following are locked for
that methodology/instrument version:

- Proposition scenario
- Substantive survey items
- Response scales and anchors
- Primary outcome definition
- Screen thresholds (if any)
- Primary analysis rules
- Missing-data treatment that affects headline outputs

Any unavoidable substantive change after production starts MUST:

1. Create a new methodology/instrument version
2. Preserve earlier responses under the version originally fielded
3. Record the reason and effective date
4. Document whether responses across versions remain analytically comparable
5. Prevent silent pooling where comparability is not established

## Protocol Deviation and Decision Log

Any departure from the frozen protocol MUST be recorded prospectively rather
than repaired silently after analysis. Each deviation record states: date,
decision owner, reason, affected spec/version, affected outputs, and
disposition.

## Writing Standard

All prose in REPORT.md, the Quarto chapters, and the generated analysis outputs
MUST comply with `docs/writing-guidelines.md`. The report checker
(`tools/report-check.py`) enforces banned vocabulary, structural patterns,
heading hierarchy, and the separation of governance from reporting below. Hype,
filler, AI-tells, and self-narrating prose are not permitted in research outputs.

The generated analysis outputs are held to the same standard as the report,
because they are pasted into the findings chapter unchanged. Prose written inside
an analysis module is report prose.

### Governance Is Recorded, Not Reported

The report is the public deliverable; this constitution and the study's records
are the governance layer. The two MUST NOT be mixed.

Reader-facing prose MUST NOT cite the artifact that authorised a statement.
Specifically, it MUST NOT contain principle citations from this constitution, the
constitution or its Research Contract as a named artifact, requirement or task
identifiers, spec references, decision or deviation identifiers, internal role
labels, repository paths, or issue references. Which internal artifact authorised
a decision, and where that authorisation is filed, is traceability metadata.

A methodological commitment MUST be written so that it stands on its own
reasoning. That is what a reviewer can check; an internal citation is not.

Three things this does not restrict:

1. **Dated approvals and version freezes are reportable.** The date a frame,
   scenario, threshold, or instrument version was approved or frozen is
   reproducibility evidence and MUST be retained. Only the internal role label
   and the file path are removed.
2. **Companion artifacts may be referenced by description.** The sampling plan,
   threshold ledger, and governance record are deliverables a reviewer may
   request, and may be named as accompanying documents rather than as paths.
3. **Published tooling may be cited as a source**, with a reference number, in a
   provenance disclosure.

Every principle in this constitution MUST therefore be enforced twice: as a
design constraint on the study, and as a claim the report makes in its own voice
without citing this document. A principle that appears in the report only as a
citation has not been written into the report at all.

Governance material has a defined home. Principle statements and the research
contract belong in this constitution; owner decisions and protocol deviations in
the decision log; requirement and task identifiers in the relevant spec;
predecessor dispositions in the migration register; report-to-instrument
traceability in the concordance record.

## Governance

This constitution supersedes all other project practices. Amendments require:

1. A documented reason tied to an observed defect, mandatory requirement, or
   study-owner decision
2. Study-owner approval
3. Version increment (semantic: MAJOR for principle removal/redefinition,
   MINOR for additions, PATCH for clarifications)
4. Updated `LAST_AMENDED_DATE`

All specs and implementations MUST verify compliance with these principles.
The Complexity Stop-Rule applies to this constitution itself — do not add
principles without evidence of need.

**Version**: 0.1.0 | **Ratified**: [date] | **Last Amended**: [date]

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

## Pre-Publication Checklist

Before declaring a draft done:

1. Does the impact land in the first sentence of each section?
2. Did a hype word or AI-tell slip in? (Run `npm run lint:report`)
3. Is every number traceable to a source or derivation?
4. Would a skeptic or reviewer catch something overstated?
5. Will the claims still be accurate if the study timeline extends?
6. Are inference limits stated alongside every finding?
7. Does every claim map to a measurement, a sample, and a boundary?

---

## Enforcement

Run the anti-style checker:

```bash
npm run lint:report
# or directly:
python tools/report-check.py REPORT.md chapters/*.qmd --strict
```

Any match in report prose (outside citation lines and HTML comments)
fails the build with `--strict`.

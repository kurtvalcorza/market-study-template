# Writing Guidelines

Rules for prose in REPORT.md and Quarto chapters. Enforced by `tools/report-check.py`.

## Principle

Research reports state findings. They do not narrate themselves, predict the
reader's confusion, or dress evidence in promotional language. If a sentence
would survive unchanged in a press release, it does not belong in a
methodology document.

## Anti-Style: Banned Words and Phrases

The following are flagged by the report checker and will fail the build.

### Hype and Filler

| Banned | Why |
|--------|-----|
| groundbreaking | Promotional; let the evidence speak |
| revolutionary | Promotional |
| cutting-edge | Promotional |
| game-changing | Promotional |
| seamless | Almost never literally true |
| leverage / leveraging | Corporate filler; use "use" |
| delve | LLM tell; adds nothing |
| robust | Vague intensifier |
| state-of-the-art | Promotional; date-bound claim without citation |
| unprecedented | Unprovable unless you've checked all precedent |
| transformative | Promotional |
| vital | Intensifier; say why it matters instead |
| crucial | Intensifier |
| paramount | Intensifier |

### Announcements Instead of Statements

| Banned | Write instead |
|--------|--------------|
| "it is important to note" | Just state the thing |
| "it is worth noting" | Just state the thing |
| "this chapter states / reads / profiles..." | State the content directly |
| "a/the reader" | Address no one; state the fact |
| "rather than left implicit / unstated" | Make the disclosure; don't announce that you're making it |

### Self-Narrating Patterns

The report should not describe its own structure except in a designated
"Document Structure" section (typically §1.5). Elsewhere, sentences like
"This section presents the methodology" add nothing — the heading already
says that. Write the methodology instead.

## Positive Guidance

- **Descriptive register.** State what was done, what was found, what it
  means within the stated inference limits.
- **Active voice where natural.** "We recruited 120 organisations" over
  "120 organisations were recruited by the research team."
- **Concrete over abstract.** "Usefulness ratings ranged from 2 to 5
  (median 4)" over "The results demonstrate strong perceived value."
- **Inference limits on every claim.** Every finding sentence should be
  traceable to a measurement, a sample, and a stated boundary.
- **Numbers over adjectives.** If you can quantify it, do. "63% of
  respondents" over "a majority of respondents."

# Market Study Template

A ready-to-use scaffold for structured market research studies. Clone it,
replace the placeholders, and start writing specs.

You get:
- A Quarto book that renders your methodology report to PDF and DOCX
- A TypeScript instrument codebase (scales, derivation, validation) deployable as a Next.js form on Vercel
- Pre-specified analysis contracts so your Chapter 8 outputs exist before you collect data
- [GitHub Spec Kit](https://github.com/github/spec-kit) for iterative, spec-driven development
- An anti-style writing checker that keeps hype and filler out of your report

---

## Getting Started

### 1. Create your repo

Click **Use this template** on GitHub (or clone locally):

```bash
gh repo create my-study --template kurtvalcorza/market-study-template --private --clone
cd my-study
```

### 2. Replace placeholders

Find-and-replace these `{{PLACEHOLDER}}` values across the repo:

| Placeholder | Files | What to put |
|-------------|-------|-------------|
| `{{STUDY_SLUG}}` | package.json, _quarto.yml | Your repo/project name, e.g. `product-demand-study` |
| `{{STUDY_TITLE}}` | package.json, REPORT.md, _quarto.yml | Full study title |
| `{{STUDY_SUBTITLE}}` | REPORT.md, _quarto.yml | Subtitle or scope line |
| `{{AUTHOR_1}}` | _quarto.yml | Lead institution or author |
| `{{AUTHOR_2}}` | _quarto.yml | Second institution (add more in _quarto.yml if needed) |
| `{{RQ1}}` – `{{RQ4}}` | REPORT.md | Your research questions (add or remove as needed) |
| `{{TARGET_N}}` | docs/sampling-plan.md | Target sample size |
| `{{BURDEN_MINUTES}}` | docs/instrument-spec.md | Target median completion time |

Quick way to find them all:

```bash
grep -r "{{" --include="*.md" --include="*.json" --include="*.yml" .
```

### 3. Install dependencies

```bash
npm install
```

### 4. Start the Spec Kit workflow

Open the project in your coding agent (Claude Code, Kiro, Codex) and run:

1. `/speckit-constitution` — establish your study's governing principles
2. `/speckit-specify` — write the instrument specification
3. `/speckit-plan` — create the implementation plan
4. `/speckit-tasks` — generate actionable tasks
5. `/speckit-implement` — build it

---

## How the Repo is Organized

```
├── REPORT.md                 # Methodology document — the source of truth
├── _quarto.yml               # Book build: renders REPORT to PDF + DOCX
├── chapters/                 # Quarto chapter files (.qmd)
│   ├── introduction.qmd
│   ├── methodology.qmd
│   ├── findings.qmd
│   └── ...
├── instrument/
│   ├── lib/                  # Core logic: scales, derivation, validation (TypeScript)
│   ├── app/                  # Survey form UI (Next.js, added during implementation)
│   └── tests/                # Unit tests (Vitest)
├── analysis/
│   ├── contracts/            # Pre-specified output tables/figures (empty templates)
│   ├── code/                 # Analysis scripts (populated after collection)
│   └── outputs/              # Generated results (raw data is gitignored)
├── evidence/                 # Study artifacts: recruitment ledger, deviation log
├── docs/
│   ├── writing-guidelines.md # Voice, anti-style rules, pre-pub checklist
│   ├── data-dictionary.md    # Every variable: name, type, source, range
│   ├── sampling-plan.md      # Frame, recruitment method, disposition ledger
│   └── instrument-spec.md    # Item-by-item specification
├── tools/
│   └── report-check.py       # Anti-style and structural linter
├── .specify/                 # Spec Kit: templates, scripts, workflows
├── .claude/skills/           # Spec Kit agent skills
├── .github/                  # Issue + PR templates
├── .editorconfig             # Editor formatting defaults
└── .gitignore
```

---

## The Workflow

This template follows a 10-step lifecycle from design to deliverable:

| Phase | Step | What happens | Where |
|-------|------|--------------|-------|
| Design | 1. Constitution | Decision rights, complexity stop-rule, governance | `.specify/memory/constitution.md` |
| Design | 2. Instrument spec | Items, scales, derivation rules, burden target | `docs/instrument-spec.md` + spec |
| Design | 3. Sampling plan | Frame, strata, target N, recruitment, disposition | `docs/sampling-plan.md` |
| Design | 4. Report structure | REPORT.md and Quarto chapters fleshed out | `REPORT.md`, `chapters/` |
| Build | 5. Instrument logic | Scales, validation, screen rules in TypeScript | `instrument/lib/` |
| Build | 6. Form UI | Next.js survey app, deployed to Vercel | `instrument/app/` |
| Build | 7. Analysis contract | Pre-specified tables/figures, empty shells | `analysis/contracts/` |
| Test | 8. Cognitive pilot | Real users, measure completion time vs burden target | — |
| Field | 9. Data collection | Production responses | — |
| Report | 10. Analysis & render | Execute contracts, generate outputs, render Quarto book | `analysis/`, `_output/` |

---

## Commands

### Development

```bash
npm run build          # TypeScript type-check (no emit)
npm test               # Run instrument tests (Vitest)
npm run test:coverage  # Tests with coverage report
npm run lint           # ESLint on TypeScript
npm run lint:report    # Anti-style checker on REPORT.md + chapters
```

### Report Rendering

```bash
quarto render              # Both PDF and DOCX → _output/
quarto render --to pdf     # PDF only (requires XeLaTeX + Arial)
quarto render --to docx    # DOCX only
```

### Anti-Style Checker

```bash
python tools/report-check.py REPORT.md chapters/*.qmd --strict
```

Fails on hype, AI-tells, self-narrating prose, and heading hierarchy violations.
See `docs/writing-guidelines.md` for the full banned-word list and positive
writing guidance.

---

## Design Principles

These are baked into the template structure. Override them in your constitution
if your study requires different choices.

1. **One path, no routing.** Every respondent answers the same instrument.
2. **Structured responses are final.** Nothing downstream can alter a primary outcome value.
3. **Descriptive metadata, not analytical classifications.** Context variables are for subgroup reporting, not derivations.
4. **Methodology and instrument versioned together.** One repo, one commit history.
5. **Inference limits on every claim.** §7 states what the evidence can and cannot support.
6. **Complexity requires evidence of need.** New items, scores, or classifications need a documented reason.
7. **Numbers over adjectives.** The anti-style checker enforces this.

---

## Requirements

| Tool | Purpose | Install |
|------|---------|---------|
| Node.js >= 20 | Runtime for instrument logic | [nodejs.org](https://nodejs.org) |
| Python >= 3.9 | Report checker script | Usually pre-installed |
| Quarto >= 1.4 | Report rendering | [quarto.org](https://quarto.org/docs/get-started/) |
| XeLaTeX | PDF rendering (via Quarto) | `quarto install tinytex` |
| Arial font | PDF typography | Usually pre-installed on Windows/macOS |
| Spec Kit CLI | Development workflow | `uv tool install specify-cli` |

---

## License

[MIT](LICENSE)

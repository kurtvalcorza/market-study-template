# Market Study Template

A scaffold for structured market research studies combining:
- A methodology report (Quarto book → PDF/DOCX)
- A web-based survey instrument (TypeScript + Next.js on Vercel)
- Pre-specified analysis contracts
- Spec Kit for iterative spec-driven development

## Quick Start

1. Clone or use this as a GitHub template
2. Find-and-replace all `{{PLACEHOLDER}}` values (listed below)
3. Run `npm install`
4. Start the Spec Kit workflow: constitution → specify → plan → tasks → implement

## Placeholders

Replace these across the repo before your first commit:

| Placeholder | Where | Example |
|-------------|-------|---------|
| `{{STUDY_SLUG}}` | package.json, _quarto.yml | `aiaas-market-study` |
| `{{STUDY_TITLE}}` | package.json, REPORT.md, _quarto.yml | `Readiness Assessment for DIMER` |
| `{{STUDY_SUBTITLE}}` | REPORT.md, _quarto.yml | `Market Demand and AI Adoption Barriers` |
| `{{AUTHOR_1}}` | _quarto.yml | `Research Institute Name` |
| `{{AUTHOR_2}}` | _quarto.yml | `Sponsoring Agency` |
| `{{RQ1}}` – `{{RQ4}}` | REPORT.md | Your research questions |
| `{{TARGET_N}}` | docs/sampling-plan.md | `120` |
| `{{BURDEN_MINUTES}}` | docs/instrument-spec.md | `12` |

## Directory Structure

```
├── REPORT.md                # Methodology document (source of truth)
├── _quarto.yml              # Book build config (PDF + DOCX)
├── chapters/                # Quarto chapter .qmd files
├── instrument/
│   ├── lib/                 # Core logic: scales, derivation, validation
│   ├── app/                 # Next.js form UI (Vercel deployment)
│   └── tests/               # Vitest tests for instrument logic
├── analysis/
│   ├── contracts/           # Pre-specified output templates
│   ├── code/                # Analysis scripts
│   └── outputs/             # Generated results (raw data gitignored)
├── evidence/                # Study artifacts (recruitment ledger, deviations)
├── docs/
│   ├── data-dictionary.md   # Variable definitions
│   ├── sampling-plan.md     # Frame, recruitment, disposition
│   └── instrument-spec.md   # Item-by-item specification
├── .specify/                # Spec Kit config, templates, workflows
└── .claude/skills/          # Spec Kit agent skills
```

## Tooling

| Tool | Purpose | Version |
|------|---------|---------|
| Node.js | Runtime | >= 20 |
| TypeScript | Instrument logic | ^5.6 |
| Vitest | Testing | ^3.0 |
| Quarto | Report rendering | >= 1.4 |
| Spec Kit | Development workflow | 0.15.2 |
| Next.js | Form UI | Added during implementation |

## Workflow

The Spec Kit sequence for a typical study:

1. **Constitution** — decision rights, complexity stop-rule, governance
2. **Instrument spec** — item-by-item design, scales, derivation rules
3. **Sampling plan** — frame, target N, recruitment method, disposition
4. **Report structure** — REPORT.md and Quarto chapters fleshed out
5. **Instrument implementation** — core logic in `instrument/lib/`
6. **Form UI** — Next.js app in `instrument/app/`, deployed to Vercel
7. **Analysis contract** — pre-specified tables/figures in `analysis/contracts/`
8. **Cognitive pilot** — test completion time against burden target
9. **Fielding** — collect data
10. **Analysis & reporting** — execute contracts, render Quarto book

## Design Principles

- One instrument path, no conditional routing
- Structured responses are final — no post-collection alteration
- Descriptive metadata collected for subgroup reporting, never for derivations
- Inference limits stated explicitly in §7
- Methodology document and instrument versioned together
- Test mode always available; production gates only block real collection

## Rendering the Report

```bash
quarto render              # builds both PDF and DOCX to _output/
quarto render --to pdf     # PDF only
quarto render --to docx    # DOCX only
```

Requires: Quarto >= 1.4, XeLaTeX (for PDF), Arial font installed.

## License

Private by default. Set your own license before publishing.

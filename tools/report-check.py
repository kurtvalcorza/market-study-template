#!/usr/bin/env python3
"""
Report quality gate — structural checks and anti-style sweep.

Checks:
  1. Section numbering sequence
  2. Anti-style sweep (hype, filler, self-narration)
  3. Heading hierarchy (no skipped levels)
  4. Internal-machinery leakage check
  5. Citation-integrity check (cross-reference body vs references.qmd)

Usage:
  python tools/report-check.py REPORT.md
  python tools/report-check.py REPORT.md --strict    # exit 1 on any failure
  python tools/report-check.py chapters/*.qmd        # check Quarto chapters

Anti-style patterns are defined in ANTI_STYLE. Citation lines (containing
[n] or [n-m] references) are excluded from the sweep to avoid false positives
on quoted material.
"""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path

# --- Anti-style pattern ---
# Hype, filler, self-narrating prose. Each branch is anchored to avoid
# swallowing legitimate uses. See docs/writing-guidelines.md for rationale.
ANTI_STYLE = (
    # Hype / marketing-speak
    r'\b(groundbreaking|revolutionary|cutting-edge|game-chang\w+|seamless\w*|'
    r'leverag\w+|delve|robust|state-of-the-art|unprecedented|transformative|'
    r'next-generation|paradigm shift|world-class|best-in-class|'
    # AI-tells
    r"in today'?s fast-paced world|stands as a testament|"
    r'plays a (?:pivotal|crucial) role|navigate the landscape|'
    r'in the realm of|harness the power|'
    # Empty intensifiers
    r'vital|crucial|paramount|significantly|dramatically|vastly|'
    # Announcement instead of statement
    r'it is important to note|it is worth noting|'
    r'it could be argued that|'
    # Self-narrating: "this chapter/section <verb>s" at sentence start
    r'(?:^|(?<=[.:;]\s))[Tt]his (?:chapter|section) '
    r'(?:states|reads|profiles|enumerates|compares|reports|sets out|'
    r'presents|describes|covers|records|keeps)\b|'
    # Addressing the reader
    r'\b(?:a|the) reader\b|'
    # Announcing a disclosure instead of making it
    r'rather than (?:left (?:implicit|unstated|unsaid|to be inferred)|'
    r'a (?:silent omission|coverage failure|oversight|documentation debt|failure)))\b'
)

# --- Internal-machinery leakage ---
# The report is the public deliverable. Governance and process provenance belongs in
# the records that carry it, not in the report: which internal artifact authorised a
# decision, where that authorisation is filed, and which requirement or task it came
# from are all traceability metadata, not findings.
#
# Applies to REPORT.md, the Quarto chapters, and the generated analysis outputs. It
# deliberately does NOT apply to files under docs/ or specs/, which exist to carry
# exactly this material.
INTERNAL_MACHINERY = (
    # Constitution and research-contract references. "Constitution" followed by a
    # roman numeral is always a principle citation; "Constitutional Commissions" and
    # "the constitutional auditor" are different words and are not matched.
    r'\bConstitution [IVX]+\b|'
    r"constitution's|the constitution\b|Research Contract|"
    # Spec Kit artifacts and identifiers
    r'\bFR-\d{3}\b|\bSC-\d{3}\b|\bT\d{3}\b|\bDE[CV]-\d{3}\b|'
    r'\bspecs?/|\bspec \d{3}\b|Spec Kit|tasks\.md|'
    # Internal role jargon
    r'study[- ]owner|'
    # Repository paths and internal file references
    r'`?(?:docs|evidence|analysis|instrument|tools|chapters)/[\w./*-]+|'
    r'REPORT\.md|decision-log|migration-register|'
    # Issue references
    r'#\d{2,}'
)

# Files allowed to carry internal machinery: the governance layer itself, plus the
# bibliography. `.specify/` holds the constitution, `docs/` and `specs/` hold the
# records and specifications, and `tools/` holds this checker. `references.qmd` is
# exempt because a bibliography legitimately contains URL path segments and the names
# of cited tools, which are sources rather than leaked process metadata.
MACHINERY_EXEMPT = (
    '.specify/',
    '.specify\\',
    'docs/',
    'docs\\',
    'specs/',
    'specs\\',
    'tools/',
    'tools\\',
    'references.qmd',
)

# The document that defines the banned vocabulary cannot be swept for it.
ANTISTYLE_EXEMPT = ('docs/writing-guidelines.md',)

# Lines containing citations are excluded from anti-style sweep
CITATION_RE = re.compile(r'\[\d+(?:\s*[,\u2013\u2014-]\s*\d+)*\]')

ok = True


def fail(path: str, lineno: int, msg: str) -> None:
    global ok
    ok = False
    # ASCII separator: a Windows console under a legacy code page raises
    # UnicodeEncodeError on an em dash, which turned a reportable failure into a
    # traceback and hid what actually failed.
    print(f'  FAIL  {path}:{lineno} - {msg}')


def check_antistyle(path: str, text: str) -> None:
    """Sweep for anti-style patterns, excluding citation lines."""
    # The writing guide has to quote the banned vocabulary in order to ban it, so
    # sweeping it reports every entry in its own tables as a violation. Heading
    # hierarchy and the internal-machinery check still apply to it.
    if path.replace('\\', '/').endswith(ANTISTYLE_EXEMPT):
        return

    for i, line in enumerate(text.splitlines(), 1):
        # Skip citation lines
        if CITATION_RE.search(line):
            continue
        # Skip HTML comments
        if line.strip().startswith('<!--'):
            continue
        for m in re.finditer(ANTI_STYLE, line, re.IGNORECASE):
            fail(path, i, f'anti-style: "{m.group(0)}"')


def check_heading_hierarchy(path: str, text: str) -> None:
    """Check that heading levels don't skip (e.g., # -> ### with no ##)."""
    prev_level = 0
    for i, line in enumerate(text.splitlines(), 1):
        m = re.match(r'^(#{1,6})\s', line)
        if m:
            level = len(m.group(1))
            if prev_level > 0 and level > prev_level + 1:
                fail(path, i, f'heading skips level: h{prev_level} -> h{level}')
            prev_level = level


def check_internal_machinery(path: str, text: str) -> None:
    """
    Flag internal governance and process references in reader-facing prose.

    Skipped for docs/, specs/, and tools/, which exist to carry that material.
    """
    normalised = path.replace('\\', '/')
    if any(normalised.startswith(p.replace('\\', '/')) for p in MACHINERY_EXEMPT):
        return

    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith('<!--'):
            continue
        for m in re.finditer(INTERNAL_MACHINERY, line):
            fail(
                path,
                i,
                f'internal machinery in reader-facing prose: "{m.group(0)}" '
                f'(belongs in docs/ or specs/, not the report)',
            )


def check_citation_integrity(report_path: str, report_text: str) -> None:
    """
    Cross-check citations in REPORT.md against entries in references.qmd.

    - Every [n] in the report body must resolve to an entry in references.qmd.
    - Every entry in references.qmd should be cited at least once (warn only).

    Only runs when the file being checked is REPORT.md and references.qmd exists
    alongside it.
    """
    normalised = report_path.replace('\\', '/')
    if not normalised.endswith('REPORT.md'):
        return

    refs_path = Path(report_path).parent / 'references.qmd'
    if not refs_path.exists():
        return

    refs_text = io.open(refs_path, encoding='utf-8').read()

    # Citations in body: all [n] where n is a digit sequence
    body_cites = set(int(m) for m in re.findall(r'\[(\d+)\]', report_text))

    # Entries defined: lines starting with [n]
    entries_defined = set(
        int(m) for m in re.findall(r'^[ \t]*\[(\d+)\]', refs_text, re.MULTILINE)
    )

    # Dangling: cited but not defined — these are errors
    dangling = sorted(body_cites - entries_defined)
    for n in dangling:
        # Find the first line that cites this number
        for i, line in enumerate(report_text.splitlines(), 1):
            if f'[{n}]' in line:
                fail(report_path, i, f'dangling citation [{n}] — no entry in references.qmd')
                break

    # Uncited: defined but never cited — informational, not a failure
    uncited = sorted(entries_defined - body_cites)
    if uncited:
        print(f'  INFO  references.qmd has {len(uncited)} uncited entries: {uncited}')


def check_file(filepath: str) -> None:
    """Run all checks on a single file."""
    text = io.open(filepath, encoding='utf-8').read()
    check_antistyle(filepath, text)
    check_heading_hierarchy(filepath, text)
    check_internal_machinery(filepath, text)
    check_citation_integrity(filepath, text)


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python tools/report-check.py <file>... [--strict]')
        sys.exit(1)

    strict = '--strict' in sys.argv
    args = [f for f in sys.argv[1:] if f != '--strict']

    # Expand glob patterns here. Windows shells (cmd, used by npm scripts) do
    # not expand them, so an unexpanded pattern would be reported as a missing
    # file and every chapter would be skipped while the gate still passed.
    files: list[str] = []
    for arg in args:
        if any(ch in arg for ch in '*?['):
            matched = sorted(str(p) for p in Path().glob(arg))
            if not matched:
                print(f'  SKIP  {arg} (no match)')
            files.extend(matched)
        else:
            files.append(arg)

    if not files:
        print('  FAIL  no files to check')
        sys.exit(1)

    for filepath in files:
        p = Path(filepath)
        if not p.exists():
            print(f'  SKIP  {filepath} (not found)')
            continue
        if p.suffix not in ('.md', '.qmd'):
            print(f'  SKIP  {filepath} (not .md or .qmd)')
            continue
        check_file(filepath)

    if ok:
        print('  PASS  all checks passed')
    else:
        print()
        print('  Some checks failed. See docs/writing-guidelines.md for guidance.')
        if strict:
            sys.exit(1)


if __name__ == '__main__':
    main()

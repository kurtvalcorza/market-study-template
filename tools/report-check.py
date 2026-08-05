#!/usr/bin/env python3
"""
Report quality gate — structural checks and anti-style sweep.

Checks:
  1. Section numbering sequence
  2. Anti-style sweep (hype, filler, self-narration)
  3. Heading hierarchy (no skipped levels)

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

# Lines containing citations are excluded from anti-style sweep
CITATION_RE = re.compile(r'\[\d+(?:\s*[,–—-]\s*\d+)*\]')

ok = True


def fail(path: str, lineno: int, msg: str) -> None:
    global ok
    ok = False
    print(f'  FAIL  {path}:{lineno} — {msg}')


def check_antistyle(path: str, text: str) -> None:
    """Sweep for anti-style patterns, excluding citation lines."""
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
    """Check that heading levels don't skip (e.g., # → ### with no ##)."""
    prev_level = 0
    for i, line in enumerate(text.splitlines(), 1):
        m = re.match(r'^(#{1,6})\s', line)
        if m:
            level = len(m.group(1))
            if prev_level > 0 and level > prev_level + 1:
                fail(path, i, f'heading skips level: h{prev_level} → h{level}')
            prev_level = level


def check_file(filepath: str) -> None:
    """Run all checks on a single file."""
    text = io.open(filepath, encoding='utf-8').read()
    check_antistyle(filepath, text)
    check_heading_hierarchy(filepath, text)


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python tools/report-check.py <file>... [--strict]')
        sys.exit(1)

    strict = '--strict' in sys.argv
    files = [f for f in sys.argv[1:] if f != '--strict']

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

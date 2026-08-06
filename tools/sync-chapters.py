#!/usr/bin/env python3
"""
Copy REPORT.md sections into the Quarto chapter files.

REPORT.md is the source of truth for content. The chapter files mirror it for
typeset rendering. Copying by hand drifts, so the copy is scripted and checkable.

Heading depth is deliberately one level shallower in the chapters: in a Quarto
book each chapter file's `#` is the chapter heading and `number-sections: true`
generates the numbers, so `## §7 Methodology` / `### 7.1 Study Design` becomes
`# Methodology` / `## Study Design`. Heading text and order are preserved exactly.

Usage:
  python tools/sync-chapters.py            # write the chapter files
  python tools/sync-chapters.py --check    # exit 1 if any chapter is stale
"""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path

REPORT = Path('REPORT.md')

# REPORT.md section number -> chapter file. Order matches _quarto.yml.
# UPDATE THIS MAPPING for your study's sections.
CHAPTERS: dict[str, str] = {
    '1': 'chapters/introduction.qmd',
    '2': 'chapters/literature-review.qmd',
    '3': 'chapters/methodology.qmd',
    '4': 'chapters/findings.qmd',
    '5': 'chapters/conclusions.qmd',
}

SECTION_RE = re.compile(r'^## §(\d+) (.+)$')
SUBSECTION_RE = re.compile(r'^### \d+\.\d+ (.+)$')
# Deeper headings shift by the same one level. Demoting h3 alone left an h4 under
# an h2, which is a skipped level and fails the heading-hierarchy check.
SUBSUB_RE = re.compile(r'^#### (.+)$')


def split_sections(text: str) -> dict[str, tuple[str, list[str]]]:
    """Map each REPORT.md section number to its title and body lines."""
    lines = text.split('\n')
    marks = [
        (i, m.group(1), m.group(2))
        for i, line in enumerate(lines)
        for m in [SECTION_RE.match(line)]
        if m
    ]
    sections: dict[str, tuple[str, list[str]]] = {}
    for i, number, title in marks:
        # A section ends at the next h2 of any kind, not only the next numbered
        # one. REPORT.md ends with an unnumbered "## References" that has its own
        # chapter file, and it must not be swallowed into the last section.
        end = next(
            (
                j
                for j in range(i + 1, len(lines))
                if lines[j].startswith('## ')
            ),
            len(lines),
        )
        sections[number] = (title, lines[i + 1:end])
    return sections


def render(title: str, body: list[str]) -> str:
    """Build chapter file content from a report section."""
    out = [f'# {title}', '']
    for line in body:
        m = SUBSECTION_RE.match(line)
        m4 = SUBSUB_RE.match(line)
        if m:
            out.append(f'## {m.group(1)}')
        elif m4:
            out.append(f'### {m4.group(1)}')
        elif line.strip() == '---':
            continue
        elif line.strip() == '<!-- landscape:begin -->':
            out.append('')
            out.append('```{=latex}')
            out.append('\\begin{landscape}')
            out.append('```')
            out.append('')
        elif line.strip() == '<!-- landscape:end -->':
            out.append('')
            out.append('```{=latex}')
            out.append('\\end{landscape}')
            out.append('```')
            out.append('')
        else:
            out.append(line)
    while out and out[-1].strip() == '':
        out.pop()

    text = '\n'.join(out) + '\n'

    # Asset paths in REPORT.md are relative to the repository root. Chapter files
    # live one level down, so Quarto would resolve `assets/x.png` as
    # `chapters/assets/x.png` and fail the render.
    text = text.replace('](assets/', '](../assets/')

    return text


def main() -> None:
    check_only = '--check' in sys.argv

    if not REPORT.exists():
        print(f'  FAIL  {REPORT} not found')
        sys.exit(1)

    sections = split_sections(io.open(REPORT, encoding='utf-8').read())

    missing = [n for n in CHAPTERS if n not in sections]
    if missing:
        print(f'  FAIL  REPORT.md has no section §{", §".join(missing)}')
        sys.exit(1)

    stale: list[str] = []
    for number, path in CHAPTERS.items():
        title, body = sections[number]
        content = render(title, body)
        target = Path(path)
        current = (
            io.open(target, encoding='utf-8').read() if target.exists() else None
        )

        if current == content:
            print(f'  OK    {path}')
            continue

        if check_only:
            stale.append(path)
            print(f'  STALE {path}')
        else:
            io.open(target, 'w', encoding='utf-8', newline='\n').write(content)
            subs = content.count('\n## ')
            print(f'  WROTE {path} ({subs} subsections)')

    if check_only and stale:
        print()
        print(f'  {len(stale)} chapter(s) out of sync with REPORT.md.')
        print('  Run: python tools/sync-chapters.py')
        sys.exit(1)


if __name__ == '__main__':
    main()

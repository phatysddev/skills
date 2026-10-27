#!/usr/bin/env python3
"""Read-only, partial local HTML inspection. No rendering, JS or network access."""
from __future__ import annotations

import argparse
from collections import defaultdict
from html.parser import HTMLParser
import json
from pathlib import Path
import re

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
EXCLUDED = {'.git', 'node_modules', 'vendor', 'dist', 'build', '.next', 'coverage', '.venv', 'venv', '__pycache__'}


class Inspector(HTMLParser):
    # The stdlib only treats script/style as raw contents. For our structural
    # scan, RCDATA elements also keep apparent inner tags as text; entity
    # decoding does not affect these diagnostics.
    CDATA_CONTENT_ELEMENTS = HTMLParser.CDATA_CONTENT_ELEMENTS + ('textarea', 'title')

    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.lines = source.splitlines(keepends=True)
        self.offsets = [0]
        for line in self.lines:
            self.offsets.append(self.offsets[-1] + len(line))
        self.stack = []
        self.issues = []
        self.ids = defaultdict(list)
        self.controls = []
        self.labels = set()
        self.document = False
        self.viewport = False
        self.templates = 0
        self.template_depth = 0

    def issue(self, code, level, message, line=None):
        self.issues.append({'code': code, 'level': level, 'line': line or self.getpos()[0], 'message': message})

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'template':
            self.template_depth += 1
            self.templates += 1
        if self.template_depth:
            return
        self.document |= tag == 'html'
        self.viewport |= tag == 'meta' and (a.get('name') or '').lower() == 'viewport'
        if a.get('id'):
            self.ids[a['id']].append(self.getpos()[0])
        if tag == 'label' and a.get('for'):
            self.labels.add(a['for'])
        if tag in {'input', 'select', 'textarea'}:
            kind = (a.get('type') or 'text').lower()
            if tag != 'input' or kind not in {'hidden', 'submit', 'reset', 'button'}:
                self.controls.append((tag, a, 'label' in self.stack, self.getpos()[0]))
        if tag == 'img' and not any(k in a for k in ('alt', 'aria-label', 'aria-labelledby')) and a.get('aria-hidden') != 'true' and a.get('role') not in {'presentation', 'none'}:
            self.issue('image-alt-review', 'review', 'Image has no static alternative text; review purpose and runtime naming.')
        # HTML permits omitted option end tags, including before an optgroup.
        if tag in {'option', 'optgroup'} and 'option' in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index('option')]
        if tag == 'optgroup' and self.stack and self.stack[-1] == 'optgroup':
            self.stack.pop()
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.template_depth:
            if tag == 'template':
                self.template_depth -= 1
            return
        line, col = self.getpos()
        offset = self.offsets[line - 1] + col
        raw = self.source[offset:self.source.find('>', offset) + 1]
        if re.match(r'</[\w:-]+\s+\S', raw):
            self.issue('closing-tag-attributes', 'error', 'Closing tag contains attributes or other invalid trailing content.')
        if tag == 'option' and 'option' not in self.stack:
            self.issue('orphan-option-end', 'error', 'Closing option has no open option in static markup.')
        if tag in self.stack:
            index = len(self.stack) - 1 - self.stack[::-1].index(tag)
            self.stack = self.stack[:index]

    def handle_data(self, data):
        if not self.template_depth and self.stack and self.stack[-1] in {'select', 'optgroup'} and data.strip():
            self.issue('select-text-outside-option', 'error', 'Non-whitespace select text is outside an option; a visible option may be missing.')

    def finish(self):
        for lines in self.ids.values():
            if len(lines) > 1:
                self.issue('duplicate-id', 'error', f'Duplicate static ID occurs on lines {", ".join(map(str, lines))}.', lines[1])
        for tag, a, wrapped, line in self.controls:
            named = wrapped or a.get('id') in self.labels or bool((a.get('aria-label') or '').strip()) or bool((a.get('title') or '').strip())
            refs = (a.get('aria-labelledby') or '').split()
            if refs and all(ref in self.ids for ref in refs):
                named = True
            if tag == 'input' and (a.get('type') or '').lower() == 'image' and a.get('alt'):
                named = True
            if not named:
                self.issue('control-name-review', 'review', 'No static naming association found; inspect computed accessible name and dynamic labels.', line)
        if self.document and not self.viewport:
            self.issue('viewport-review', 'review', 'HTML document has no viewport meta; verify intended narrow-screen behavior.', 1)
        return {'issues': sorted(self.issues, key=lambda i: (i['line'], i['code'])), 'excluded_templates': self.templates}


def inspect(source):
    parser = Inspector(source)
    parser.feed(source)
    parser.close()
    return parser.finish()


def run(paths):
    files = set()
    gaps = []
    for value in paths:
        p = Path(value)
        if p.is_symlink() or not p.exists():
            gaps.append({'path': str(p), 'reason': 'Missing or symbolic input; not read.'})
            continue
        p = p.resolve()  # Normalize OS aliases such as macOS /var before scoped traversal.
        candidates = p.rglob('*') if p.is_dir() else [p]
        found = False
        for candidate in candidates:
            if candidate.suffix.lower() not in {'.html', '.htm'} or not candidate.is_file():
                continue
            relative = candidate.relative_to(p) if p.is_dir() else Path(candidate.name)
            if any(part in EXCLUDED for part in relative.parts) or candidate.is_symlink() or any(parent.is_symlink() for parent in candidate.parents):
                continue
            found = True
            files.add(candidate)
        if not found:
            gaps.append({'path': str(p), 'reason': 'No eligible local HTML files.'})
    reports = []
    for p in sorted(files):
        try:
            reports.append({'path': str(p), **inspect(p.read_text(encoding='utf-8'))})
        except (OSError, UnicodeError, ValueError) as exc:
            gaps.append({'path': str(p), 'reason': type(exc).__name__})
    errors = sum(i['level'] == 'error' for report in reports for i in report['issues'])
    reviews = sum(i['level'] == 'review' for report in reports for i in report['issues'])
    return {'scope': 'Static local HTML only; no JS/render/CSS/accessibility compliance or visual verdict. Template contents excluded.', 'files': reports, 'coverage_gaps': gaps, 'summary': {'files': len(reports), 'errors': errors, 'review_candidates': reviews}}, (2 if gaps else 1 if errors else 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+', help='Scoped HTML file(s) or directories')
    args = parser.parse_args()
    result, status = run(args.paths)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return status


if __name__ == '__main__':
    raise SystemExit(main())

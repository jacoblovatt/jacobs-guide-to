#!/usr/bin/env python3
"""Check the assembled artifact, local URLs/anchors, search and PDF basics."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'build' / 'site'
PREFIX = tomllib.loads((ROOT / 'site.toml').read_text())['site']['prefix']


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links = set(), []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for name in ('href', 'src', 'poster'):
            if attrs.get(name):
                self.links.append(attrs[name])
        if tag == 'img' and not attrs.get('alt', '').strip():
            raise ValueError('Image lacks alternative text')


def check():
    if not (SITE / 'index.html').is_file():
        raise ValueError('Missing site: run make public first.')
    if not re.fullmatch(r'/[a-z0-9-]+/', PREFIX):
        raise ValueError('site.prefix must be /project-slug/')
    pages = {p: Page(p.read_text()) for p in SITE.rglob('*.html')}
    errors = []
    count = 0

    def link(source, href):
        nonlocal count
        u = urlsplit(urljoin('https://local.invalid' + PREFIX + source.relative_to(SITE).as_posix(), href))
        if u.scheme not in ('http', 'https') or u.netloc != 'local.invalid':
            return
        count += 1
        path = unquote(u.path)
        if not path.startswith(PREFIX):
            errors.append(f'{source.relative_to(SITE)}: link escapes project prefix: {href}')
            return
        target = SITE / path.removeprefix(PREFIX)
        if target.is_dir():
            target = target / 'index.html'
        if not target.is_file():
            errors.append(f'{source.relative_to(SITE)}: missing {href}')
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f'{source.relative_to(SITE)}: missing anchor {href}')

    for p, page in pages.items():
        for href in page.links:
            link(p, href)
        text = p.read_text()
        if re.search(r'\?\?(?:eq|fig|tbl|sec)-', text):
            errors.append(f'{p.name}: unresolved cross-reference')
    for p in SITE.rglob('*.css'):
        for match in re.finditer(r'url\(\s*[\'\"]?([^\)\'\"]+)', p.read_text()):
            link(p, match[1].strip())
    for p in SITE.rglob('*'):
        if p.is_symlink() or p.suffix in ('.qmd', '.tex', '.bib', '.yml', '.yaml'):
            errors.append(f'Unexpected source or symlink in artifact: {p.relative_to(SITE)}')
    for book in sorted(p for p in SITE.iterdir() if p.is_dir()):
        search = book / 'search.json'
        entries = json.loads(search.read_text())
        if not entries:
            errors.append(f'{book.name}: empty search index')
        for item in entries:
            link(search, item['href'])
        # Search must cover each actual book HTML page and no missing page.
        indexed = {item['href'].split('#')[0] for item in entries}
        for p in book.glob('*.html'):
            if p.name not in indexed:
                errors.append(f'{book.name}: search does not cover {p.name}')
        pdf = book / f'{book.name}.pdf'
        info = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True, check=True).stdout
        if 'A4' not in info:
            errors.append(f'{pdf.name}: expected A4 pages')
        text = subprocess.run(['pdftotext', str(pdf), '-'], capture_output=True, text=True, check=True).stdout
        if 'Jacob' not in text:
            errors.append(f'{pdf.name}: missing expected PDF text')
    pilot = SITE / 'calculus' / 'why-integrating-factors-work.html'
    text = pilot.read_text()
    for needle in ['eq-exact-derivative', 'fig-solution-family', 'ref-openstax-linear', 'sec-solutions', 'footnote']:
        if needle not in text:
            errors.append(f'Pilot lacks {needle}')
    if errors:
        raise ValueError('\n'.join(errors))
    print(f'PASS: {len(pages)} HTML pages, {count} local links/resources/anchors under {PREFIX}, search coverage and A4 PDFs.')
    print('External URLs and browser behaviour need separate review.')


if __name__ == '__main__':
    try:
        check()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)

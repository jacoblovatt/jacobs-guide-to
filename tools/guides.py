#!/usr/bin/env python3
"""Small orchestration layer: Quarto owns rendering and chapter selection."""
import argparse
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'build'
VERSION = (ROOT / '.quarto-version').read_text().strip()
ENV = dict(os.environ, XDG_CACHE_HOME=str(BUILD / 'cache'),
           XDG_DATA_HOME=str(BUILD / 'data'))


def run(args, **kwargs):
    try:
        return subprocess.run([str(a) for a in args], check=True, env=ENV, **kwargs)
    except subprocess.CalledProcessError as error:
        if kwargs.get('capture_output'):
            print(error.stderr or error.stdout or '', file=sys.stderr)
        raise


def quarto():
    local = ROOT / '.tools' / f'quarto-{VERSION}' / 'bin' / 'quarto'
    exe = os.environ.get('QUARTO') or (str(local) if local.is_file() else shutil.which('quarto'))
    if not exe:
        raise ValueError('Quarto is missing. Run make setup (official local binary), or install the pinned version on PATH.')
    actual = run([exe, '--version'], capture_output=True, text=True).stdout.strip()
    if actual != VERSION:
        raise ValueError(f'Quarto {VERSION} required, found {actual}. Run make setup or set QUARTO to the pinned binary.')
    return exe


def guide_names():
    return sorted((p.parent.name for p in (ROOT / 'guides').glob('*/_quarto.yml')),
                  key=lambda name: (name != 'calculus', name))


def guide_name():
    name = os.environ.get('GUIDE', 'calculus')
    if not re.fullmatch(r'[a-z][a-z0-9-]*', name) or name not in guide_names():
        raise ValueError(f'Unknown guide {name!r}; choose: {", ".join(guide_names())}')
    return name


def safe_output(path):
    path.relative_to(BUILD)
    for parent in [path, *path.parents]:
        if parent == ROOT:
            break
        if parent.is_symlink():
            raise ValueError(f'Unsafe generated directory symlink: {parent}')


def reset(path):
    # Only these fixed generated children may be removed. Never accept a CLI path.
    allowed = [BUILD / 'staging', BUILD / 'books', BUILD / 'site', BUILD / 'preview']
    if path not in allowed:
        raise ValueError(f'Unsafe generated directory: {path}')
    safe_output(path)
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def inspect(name):
    result = run([quarto(), 'inspect', ROOT / 'guides' / name], capture_output=True, text=True)
    cfg = json.loads(result.stdout)['config']
    chapters = cfg['book']['chapters']
    if not chapters or chapters[0] != 'index.qmd':
        raise ValueError(f'{name}: first chapter must be index.qmd')
    if len(set(str(c) for c in chapters)) != len(chapters):
        raise ValueError(f'{name}: duplicate chapter')
    for chapter in chapters:
        if not isinstance(chapter, str) or not re.fullmatch(r'[a-z][a-z0-9-]*\.qmd', chapter):
            raise ValueError(f'{name}: use flat, descriptive chapter filenames, got {chapter!r}')
    if cfg['book']['output-file'] != name:
        raise ValueError(f'{name}: book.output-file must equal guide directory name')
    return cfg


def copy_file(source, target):
    if source.is_symlink() or not source.is_file():
        raise ValueError(f'Missing file or symlink not supported: {source}')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def stage(name, cfg):
    """Do not expose unselected chapters or their asset directories to Quarto."""
    source = ROOT / 'guides' / name
    dest = BUILD / 'staging' / 'guides' / name
    copy_file(source / '_quarto.yml', dest / '_quarto.yml')
    for chapter in cfg['book']['chapters']:
        copy_file(source / chapter, dest / chapter)
        assets = source / 'assets' / Path(chapter).stem
        if assets.exists():
            for asset in assets.rglob('*'):
                if asset.is_symlink():
                    raise ValueError(f'Symlinks are not supported: {asset}')
                if asset.is_file():
                    copy_file(asset, dest / asset.relative_to(source))
    bib = cfg.get('bibliography', [])
    for filename in ([bib] if isinstance(bib, str) else bib):
        if not re.fullmatch(r'[a-z][a-z0-9-]*\.bib', filename):
            raise ValueError('Bibliographies must be flat .bib filenames')
        copy_file(source / filename, dest / filename)
    return dest


def prepare():
    reset(BUILD / 'staging')
    # Everything in shared is explicitly public. Keep scratch material elsewhere.
    for file in (ROOT / 'shared').rglob('*'):
        if file.is_file():
            copy_file(file, BUILD / 'staging' / 'shared' / file.relative_to(ROOT / 'shared'))


def render(name, cfg, fmt):
    project = stage(name, cfg)
    run([quarto(), 'render', project, '--to', fmt])
    return project / '_book'


def public_copy(source, dest):
    # TeX and canonical sources are for authors, not the deployed artifact.
    blocked = {'.tex', '.log', '.aux', '.qmd', '.bib', '.yml', '.yaml'}
    for file in source.rglob('*'):
        if file.is_symlink():
            raise ValueError(f'Unexpected output symlink: {file}')
        if file.is_file() and file.suffix not in blocked:
            copy_file(file, dest / file.relative_to(source))


def catalogue(configs):
    cards = []
    summaries = {
        'calculus': 'Why integrating factors work: a complete teaching chapter with exercises and solutions.',
        'prehistory': 'Starter introduction and proposed topics. Chapters are still to come.',
        'word-games': 'Starter introduction and proposed topics. Chapters are still to come.',
        'arithmetic': 'Starter introduction and proposed topics. Chapters are still to come.',
    }
    for name, cfg in configs.items():
        title = html.escape(cfg['book']['title'])
        summary = html.escape(summaries.get(name, 'A growing guide by Jacob Lovatt.'))
        cards.append(f'<article><h2><a href="{name}/index.html">{title}</a></h2><p>{summary}</p>'
                     f'<p><a href="{name}/index.html">Read online</a> · '
                     f'<a href="{name}/{name}.pdf">Download PDF</a></p></article>')
    page = '''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Jacob’s Guides</title><link rel="stylesheet" href="catalogue.css"></head>
<body><a class="skip" href="#main">Skip to content</a><header><p class="eyebrow">Jacob Lovatt · Living guides</p>
<h1>Jacob’s Guides</h1><p class="intro">Learning, explained one chapter at a time.</p>
<p>Notes developed into careful explanations, worked examples and questions to try.
Read online or take a PDF away with you.</p></header><main id="main">''' + '\n'.join(cards) + '''</main>
<footer><p>These guides grow as I learn. The calculus pilot is ready to read; the other guides are starting points.</p>
<p><a href="https://jacoblovatt.github.io/">Jacob’s blog</a></p></footer></body></html>'''
    (BUILD / 'site' / 'index.html').write_text(page)
    copy_file(ROOT / 'shared' / 'catalogue.css', BUILD / 'site' / 'catalogue.css')
    (BUILD / 'site' / '.nojekyll').touch()


def doctor():
    failures = []
    if sys.version_info < (3, 11):
        failures.append('Python 3.11+')
    for tool, fix in [('git', 'Install Git'), ('make', 'Install GNU Make'),
                      ('xelatex', 'Install TeX Live with XeTeX, or use Quarto TinyTeX'),
                      ('pdfinfo', 'Install Poppler tools'), ('pdftotext', 'Install Poppler tools')]:
        print(f'{tool}: {shutil.which(tool) or fix}')
        if not shutil.which(tool):
            failures.append(tool)
    print(f'Python: {sys.version.split()[0]} (3.11+ required)')
    try:
        print(f'Quarto: {quarto()} ({VERSION})')
    except ValueError as error:
        print(error)
        failures.append('quarto')
    if failures:
        raise ValueError('Missing prerequisites: ' + ', '.join(failures) + '. See docs/setup.md.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['doctor', 'html', 'pdf', 'public', 'preview', 'serve'])
    args = parser.parse_args()
    if args.command == 'doctor':
        return doctor()
    if args.command == 'serve':
        # A prefix-shaped local tree catches accidental root-relative links.
        import http.server
        import functools
        import tomllib
        prefix = tomllib.loads((ROOT / 'site.toml').read_text())['site']['prefix']
        if not re.fullmatch(r'/[a-z0-9-]+/', prefix):
            raise ValueError('site.prefix must be /project-slug/')
        if not (BUILD / 'site' / 'index.html').is_file():
            raise ValueError('Run make public first.')
        reset(BUILD / 'preview')
        shutil.copytree(BUILD / 'site', BUILD / 'preview' / prefix.strip('/'))
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(BUILD / 'preview'))
        print(f'Catalogue: http://127.0.0.1:8000{prefix}', flush=True)
        with http.server.ThreadingHTTPServer(('127.0.0.1', 8000), handler) as server:
            server.serve_forever()
        return
    if args.command == 'preview':
        name = guide_name()
        return run([quarto(), 'preview', ROOT / 'guides' / name, '--to', 'html', '--no-browser'])
    names = guide_names() if args.command == 'public' else [guide_name()]
    configs = {name: inspect(name) for name in names}
    prepare()
    if args.command == 'public':
        reset(BUILD / 'site')
        for name, cfg in configs.items():
            public_copy(render(name, cfg, 'all'), BUILD / 'site' / name)
        catalogue(configs)
        print('Public collection: build/site/index.html')
    else:
        out = render(names[0], configs[names[0]], args.command)
        target = BUILD / 'books' / names[0] / args.command
        safe_output(target)
        if target.exists():
            # Bounded subtree; name was validated and format is an argparse choice.
            shutil.rmtree(target)
        public_copy(out, target)
        print(f'Output: {target.relative_to(ROOT)}')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, subprocess.CalledProcessError, OSError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)

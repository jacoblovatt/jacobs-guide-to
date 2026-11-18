#!/usr/bin/env python3
"""Bounded regression in a clean temporary source copy; never edits real chapters."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid
from guides import ROOT, quarto


def main():
    exe = quarto()
    with tempfile.TemporaryDirectory(prefix='jacobs-guides-') as tmp:
        checkout = Path(tmp) / 'source'
        shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(
            '.git', '.tools', 'build', '_book', '.quarto', '__pycache__'))
        env = dict(os.environ, QUARTO=str(Path(exe).resolve()))
        log = ROOT / 'build' / 'publication-regression.log'
        with log.open('w') as output:
            def make(*args):
                subprocess.run(['make', *args], cwd=checkout, env=env, stdout=output,
                               stderr=subprocess.STDOUT, check=True)

            # Exercise the documented interface from a clean source copy.
            make('doctor')
            make('html', 'GUIDE=calculus')
            make('pdf', 'GUIDE=calculus')
            guide = checkout / 'guides' / 'calculus'
            cfg = guide / '_quarto.yml'
            original = cfg.read_text()
            marker = 'PUBLICATION_PROBE_' + uuid.uuid4().hex
            draft = 'EXCLUDED_DRAFT_' + uuid.uuid4().hex
            (guide / 'publication-probe.qmd').write_text(
                '# Publication probe\n\n' + marker +
                '\n\n[Probe resource](assets/publication-probe/probe.txt)\n')
            (guide / 'unselected-probe.qmd').write_text('# Unselected probe\n\n' + draft + '\n')
            for name, content in [('publication-probe', marker), ('unselected-probe', draft)]:
                assets = guide / 'assets' / name
                assets.mkdir()
                (assets / 'probe.txt').write_text(content)
            cfg.write_text(original.replace('    - index.qmd\n', '    - index.qmd\n    - publication-probe.qmd\n'))
            make('public')
            make('check')
            site = checkout / 'build' / 'site'
            assert (site / 'calculus' / 'publication-probe.html').is_file()
            assert (site / 'calculus' / 'assets' / 'publication-probe' / 'probe.txt').is_file()
            assert marker in (site / 'calculus' / 'search.json').read_text()
            # Both an unlisted draft and its unreferenced resources must be absent.
            assert not (site / 'calculus' / 'unselected-probe.html').exists()
            assert not (site / 'calculus' / 'assets' / 'unselected-probe').exists()
            cfg.write_text(original)
            # Leave the source and asset in place; exclusion must be driven by configuration.
            make('public')
            make('check')
            assert not (site / 'calculus' / 'publication-probe.html').exists()
            assert not (site / 'calculus' / 'assets' / 'publication-probe').exists()
            for file in site.rglob('*'):
                if not file.is_file():
                    continue
                data = file.read_bytes()
                assert marker.encode() not in data and draft.encode() not in data, file
                if file.suffix == '.pdf':
                    text = subprocess.check_output(['pdftotext', str(file), '-'])
                    assert marker.encode() not in text and draft.encode() not in text, file
            # Invalid input and render failures must fail rather than silently succeeding.
            bad = subprocess.run(['make', 'html', 'GUIDE=../calculus'], cwd=checkout, env=env,
                                 stdout=output, stderr=subprocess.STDOUT)
            assert bad.returncode != 0
            chapter = guide / 'why-integrating-factors-work.qmd'
            chapter.unlink()
            bad = subprocess.run(['make', 'html', 'GUIDE=calculus'], cwd=checkout, env=env,
                                 stdout=output, stderr=subprocess.STDOUT)
            assert bad.returncode != 0
        print('PASS: clean-copy daily commands, unpublished draft/resource exclusion, unpublishing, repeat build, PDFs/search, failure handling.')
        print(f'Detailed build log: {log.relative_to(ROOT)}')


if __name__ == '__main__':
    main()

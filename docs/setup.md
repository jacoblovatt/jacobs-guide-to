# Setup

The implementation was tested on Fedora 43, Bash, Git 2.52.0, Python 3.14.0,
GNU Make 4.4.1, Neovim and XeTeX/TeX Live 2023. Quarto 1.11.9 is pinned in
`.quarto-version`; its official Linux amd64 archive was checked against the
release SHA-256 file before extraction into ignored `.tools/`.

```bash
make setup
make doctor
make public
make check
```

No Python packages are required for builds or checks: helpers use the standard
library, including `tomllib` (Python 3.11+). `make setup` downloads the portable
Quarto release, verifies its checksum and supports Linux x86_64/aarch64. It is
safe to repeat. On other platforms, install the same version from
[Quarto's official downloads](https://quarto.org/docs/download/).
A matching Quarto on PATH also works; `QUARTO=/absolute/path/to/quarto` overrides
selection. No GitHub login is needed. Cache/data directories are confined to
ignored `build/cache/` and `build/data/`.

## PDF tooling

This machine already renders with system XeLaTeX. The style uses TeX Gyre
Pagella and Heros, Latin Modern Mono, KOMA-Script and the normal Quarto/Pandoc
LaTeX packages. Automatic TeX package installation is disabled, so builds do not
silently modify a system TeX distribution.

For a machine without TeX, the supported smaller route is
[Quarto TinyTeX](https://quarto.org/docs/output-formats/pdf-basics.html):

```bash
quarto install tinytex
```

Use the pinned local Quarto binary if it is not on PATH. TinyTeX has not been
tested here; package additions may be necessary. You can explicitly enable
`latex-auto-install` for a user-owned TinyTeX setup after reviewing that choice.
The recorded tested route is a full system TeX Live installation.

On Fedora, the corresponding system setup (only if needed) is approximately:

```bash
sudo dnf install git make python3 curl texlive-scheme-medium texlive-xetex poppler-utils
```

Review package availability for your Fedora release and add any missing LaTeX
package reported by the compiler. This command was not needed or run here.
System installation requires administrator permission; the portable Quarto
installation does not. `make doctor` checks executables; the actual PDF render
is the definitive package/font check.

CI uses Ubuntu 24.04, Python 3.13, pinned Quarto, and explicitly installed Ubuntu
TeX Live/XeTeX/font/Poppler packages. OS package updates are not frozen, so PDF
bytes need not be identical across machines. Content and structure are
reproducible; this is not a bit-for-bit archival build.

The committed figure is an original PNG generated with Pillow 11.3.0 on this
machine; Pillow is not a runtime dependency. The plotted function is
`exp(x)/3 + C*exp(-2*x)` for `C = 2/3, 0, -1/3` on `[-0.6, 1.5]`.

## Editing

Plain Neovim works: `nvim guides/calculus/why-integrating-factors-work.qmd`.
Editor plugins are optional; [Quarto's Neovim guidance](https://quarto.org/docs/tools/neovim.html)
is a later convenience. EPUB is a possible future format, not a prerequisite.

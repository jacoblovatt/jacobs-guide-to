# Jacob’s Guides

A growing collection by Jacob Lovatt, written in Quarto Markdown and built as
searchable HTML books and A4 PDFs. The first complete teaching chapter is
**Why integrating factors work**, in the calculus guide. The other three guides
contain short introductions and explicitly proposed contents.

This checkout is the existing `jacobs-guide-to` repository. The separate Jekyll
blog at `../jacoblovatt.github.io` is preserved. Nothing is published by a local
build, and no blog changes have been applied.

## Start here

```bash
make setup                       # official Quarto 1.11.9, inside ignored .tools/
make doctor                      # check prerequisites; see docs/setup.md
make preview GUIDE=calculus       # live Quarto preview; Ctrl-C to stop
make html GUIDE=calculus
make pdf GUIDE=calculus
make public                      # clean, selected HTML + PDF collection
make check                       # local links, anchors, search and PDF checks
make serve                       # http://127.0.0.1:8000/jacobs-guide-to/
```

`make setup` needs internet, curl, tar and sha256sum. Python 3.11+, GNU Make,
Quarto and a supported TeX distribution are needed. The local machine already
has working TeX Live 2023; no privileged installation was needed. Run
`make regression` for the slower clean-copy and draft-exclusion check.

For collection navigation and PDF download links, use `make public` and
`make serve`. Single-format outputs are useful for checking one book; they
do not include the collection catalogue or the other output format.

## Where to write and read

| Path | Purpose |
| --- | --- |
| `guides/<guide>/*.qmd` | Canonical chapters; one source for HTML and PDF |
| `guides/<guide>/_quarto.yml` | Book metadata and the authoritative ordered public chapter list |
| `guides/<guide>/assets/<chapter-stem>/` | Reviewed assets belonging to that chapter |
| `shared/` | Public common theme, defaults and a small shared include |
| `templates/` | Chapter, starter-guide and blog-introduction templates |
| `build/books/<guide>/html/` | Single-guide HTML output |
| `build/books/<guide>/pdf/` | Single-guide PDF output |
| `build/site/` | Complete deployable catalogue, books, resources and PDFs |
| `docs/blog-proposal/` | Reviewable Jekyll post and proposed navigation page |

Guide names are `calculus`, `prehistory`, `word-games` and `arithmetic`.
Generated output, local tools and caches are ignored; commit sources, assets,
configuration, documentation and workflows. Keep private notes outside this
repository, even if a file would not be rendered.

## Next chapter

```bash
cp templates/chapter.qmd guides/calculus/limits-and-continuity.qmd
nvim guides/calculus/limits-and-continuity.qmd
```

Choose a stable filename and replace the template title, anchors and teaching
prompts. Put images in `assets/limits-and-continuity/`. A new file is excluded
from public builds until explicitly added to `book.chapters` in the guide’s
`_quarto.yml`. Review the argument, sources, examples and solutions before
adding it; then run `make public`, `make check` and inspect HTML/PDF.

The writing cycle is **capture a question → explain it → add evidence and
examples → review → publish**. See [the writing workflow](docs/writing.md) for
review-ready drafts, previewing, includes and corrections.

## Handoff

- [Setup and tested dependencies](docs/setup.md)
- [Architecture and publication boundaries](docs/architecture.md)
- [Publishing activation and blog integration](docs/publishing.md)
- [Five-pass validation record and remaining checks](docs/validation.md)

Publishing is a distinct later decision. The manual Pages workflow is prepared
but has not run. After reviewing the local collection, review/commit/merge the
source, enable **GitHub Actions** as the Pages source for this guides repository,
and manually run **Publish guides (manual)** on `main`. See the exact checklist
in `docs/publishing.md`; no public repository creation, push or deployment has
been performed here.

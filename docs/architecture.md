# Architecture and scope

The existing `jacobs-guide-to` checkout is the guides monorepo; renaming it is
unnecessary. The actual remotes identify the owner as `jacoblovatt`. No identity
was inferred from the shell username. There was only the initial README and an
untracked build prompt when implementation began; that prompt is preserved.
The isolated branch is `build/jacobs-guides`.

The separate `jacoblovatt.github.io` repository remains a Jekyll blog. Its local
configuration identifies `https://jacoblovatt.github.io`, empty baseurl, Jekyll
4.4, Minima 2.5, kramdown/GFM, post/page layouts, and optional page-level
MathJax. `.github/workflows/pages.yml` builds with Bundler and deploys a Pages
artifact. Remote Pages settings and repository visibility require authenticated
inspection and have not been verified. Two untracked posts were preserved.

## Sources and configuration

Each guide is an independent Quarto book with its own `_quarto.yml`. The
supported `metadata-files` mechanism loads `shared/_book.yml`. The shared
SCSS theme is compiled by Quarto into each book's generated CSS; a raw CSS link
outside a nested book would break after assembly, so no such link is used.
The author is Jacob Lovatt and language is British English. Native Quarto
features supply book navigation, search, cross-references, citations, footnotes
and PDF output. Narrative content stays in `.qmd`.

The standard-library Python helper uses `quarto inspect` to read resolved book
configuration; there is no second chapter list or YAML parser dependency. Make
is the only command interface. No root Quarto book tries to render all projects.
`make public` renders each book separately, then assembles a catalogue and the
four books into `build/site/`. It does not run Jekyll or change the blog.

## Publication boundary

`book.chapters` is the single authoritative public selection and order. Flat
filenames keep the helper small; nested parts/appendices can be introduced
later if genuinely needed. A draft flag is not used as an exclusion mechanism.

Before rendering, the helper creates a fresh bounded `build/staging/`. It copies
only each selected chapter, the book configuration, configured bibliographies,
`assets/<selected-chapter-stem>/`, and public shared files. An unselected draft
and its assets therefore cannot enter search, HTML, PDF or the copied artifact.
Selected asset folders and everything in `shared/` are public: review every
file there, including unused files. Other resources must be moved under the
owning chapter's folder. This explicit resource convention keeps staging small
and auditable without a second publication manifest.

The output `build/site/` is recreated from scratch on every public build;
unpublishing cannot retain stale chapter pages or assets. Cleanup accepts only
fixed generated directories and validated guide names, never a user-supplied
arbitrary path. Do not run two builds concurrently in the same checkout: they
share staging. Quarto's direct preview uses its own ignored `_book/` instead.

`make preview` is local authoring output; it is never a deployment artifact.
It navigates the configured chapter list. For unfinished explanations, work in
private notes outside this repository, then create an unlisted review-ready
chapter here. Local preview is not a private storage mechanism. Anything
committed to a public repository is public, even when omitted from rendering.

All site links are relative, so they work at the project-site prefix recorded
in `site.toml`. The local server deliberately serves that prefix instead of `/`.
Each book owns a separate search index. HTML mathematics uses Quarto's default
MathJax CDN; initial typesetting needs reader network access. Offline HTML
bundling can be added later; downloaded PDFs are self-contained.

## Deliberate limits

The three starter books are introductions and plans, not completed textbooks.
There is no full blog syndication, custom filter, database, JavaScript framework,
submodule or execution cache. Code examples are non-executing by default.
EPUB, an offline math bundle and richer multi-author review can wait until the
writing needs them. The public source license has deliberately not been chosen
on the author's behalf.

References consulted: [Quarto books](https://quarto.org/docs/books/),
[project metadata](https://quarto.org/docs/projects/quarto-projects.html#metadata-includes),
[cross-references](https://quarto.org/docs/authoring/cross-references.html),
[citations](https://quarto.org/docs/authoring/citations.html).

# Repository guidance

- Canonical teaching content is `guides/<slug>/*.qmd`; never edit generated HTML or PDF.
- Each guide is an independent Quarto book. `book.chapters` in its `_quarto.yml` is the single ordered publication list. Keep a flat list of descriptive `.qmd` filenames with `index.qmd` first; `book.output-file` must match the guide slug.
- `make preview GUIDE=calculus`, `make html GUIDE=calculus`, `make pdf GUIDE=calculus`, `make public`, `make check`; `make regression` checks clean-copy builds, exclusion and stale output. `make doctor` checks prerequisites. Quarto is pinned in `.quarto-version`.
- Public builds stage selected chapters, their `assets/<chapter-stem>/` directories, bibliography and public `shared/` files under `build/staging/`. Render books separately and assemble only `build/site/`. Do not copy the whole repository into the artifact.
- Everything in `shared/` is public. Included prose must have no YAML metadata; paths resolve relative to the including chapter. Shared configuration is loaded with supported `metadata-files`; the SCSS theme compiles into each book’s resources.
- Author Jacob Lovatt, language en-GB; use native Quarto equations, references, citations, figures with alt text, and portable teaching blocks. Verify sources and worked solutions.
- Cleanup is restricted to known generated `build/` subdirectories. Reject symlinks and unvalidated guide/path arguments. Generated output, caches and `.tools/` are ignored.
- Preserve the supplied build prompt and unrelated/uncommitted work. The separate `../jacoblovatt.github.io` Jekyll blog is read-only for this task; proposed blog changes belong in `docs/blog-proposal/` until explicitly authorised.
- Do not create public repositories, push, enable Pages or deploy without a separate publishing instruction. Validation workflows have read-only permissions; publishing is manual on main with one assembled artifact.

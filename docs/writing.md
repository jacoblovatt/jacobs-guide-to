# Writing and review

## Capture a question

Keep rough or private scratch notes **outside this repository**. Write the
question you cannot yet explain. Pick a reader and list the knowledge the
explanation assumes.

## Explain it

Copy `templates/chapter.qmd` to a descriptive stable filename, for example
`guides/calculus/limits-and-continuity.qmd`. Replace the example anchors with
unique names; numbering comes from the book, never from the filename.

An unlisted `.qmd` is a review-ready candidate once it has an explanation,
examples and checked answers. It remains excluded until you put it in
`book.chapters`. Keep only material you are willing to expose in a public Git
history in this repository. A comment or `draft: true` does not make it private.

There is deliberately one reviewed chapter list rather than separate preview
and publication manifests. `make preview GUIDE=calculus` previews that list.
For visual review of a candidate, add it to the list on a local review branch,
preview/build it, and commit that selection only after review. A local public
build is still just local output; do not manually deploy a review artifact.
Manual publication is restricted to reviewed `main`.

## Add evidence and examples

Use LaTeX notation inside `$...$` or `$$...$$`, and native Quarto labels such
as `{#eq-product-rule}` and references such as `@eq-product-rule`. The pilot
shows numbered equations, a figure, footnote, citation, table and separate
solutions in both formats.

Place assets for `limits-and-continuity.qmd` in
`guides/calculus/assets/limits-and-continuity/`. This ownership convention is
part of the public staging boundary. Review the entire selected folder; even
unused files there are eligible for copying. Add meaningful captions and alt
text. Prefer PNG/JPEG or a PDF-compatible format that needs no extra converter.

Use a verified BibTeX entry in `references.bib` and configure `bibliography` in
`_quarto.yml`. Add `references.qmd` with an unnumbered `References` heading and
a `::: {#refs}` block when introducing references to a starter book. Ordinary
fenced code blocks work without a computation runtime:

```python
# An explanatory code example, not an executed cell.
total = sum([1, 2, 3])
```

### Reuse a real passage, sparingly

The three starter introductions demonstrate the supported include mechanism:

```text
{{< include ../../shared/_reading-note.qmd >}}
```

The included file has no YAML metadata, images or relative links, so it cannot
change a book's title or introduce path ambiguity. Its heading and prose have
been checked in all three HTML/PDF builds. Paths inside an include resolve
relative to the **including chapter**, not to the included file. For a future
shared image, use a project-root path and supply the asset in each project's
reviewed resource boundary; do not assume an include copies resources for you.
See [Quarto includes](https://quarto.org/docs/authoring/includes.html).

Do not split every paragraph into includes. Keep a narrative together unless
an identical passage truly belongs in more than one document.

## Review

1. Check every mathematical step, assumption, example and solution independently.
2. Verify source metadata against accessible originals; do not invent page numbers.
3. Add the reviewed filename in the desired position under `book.chapters`.
4. Run `make public` and `make check`; inspect the HTML and PDF, especially at a
   narrow width and at page breaks. Try navigation, search, equation/figure links
   and the PDF download.
5. Run `make regression` when changing build/publication tooling or boundaries.

An unlisted candidate is review-ready; selection on the reviewed branch means
approved for public output; a successful manual deployment makes it published.
The list controls output, not confidentiality. CI checks builds; it cannot
certify an explanation's teaching quality.

## Publish and correct

Merge reviewed source to `main` and use the separately authorised manual Pages
workflow described in `publishing.md`. Publish a short blog adaptation only
after the canonical chapter URL is live.

To correct an explanation, edit its original `.qmd`, recheck affected examples,
rebuild both formats and redeploy. Keep the descriptive filename and anchors
stable so existing links continue to work. Add a brief correction note if a
previous error could mislead readers. To unpublish a chapter, remove it from
`book.chapters` and rebuild; clean staging removes stale HTML, search entries,
PDF text and owned assets. This cannot remove it from public Git history.

## Add a guide

```bash
cp -r templates/guide guides/new-subject
```

Replace `SLUG` with `new-subject` and `TITLE` with the subject in `_quarto.yml`;
write the introduction and create `assets/index/` only if needed. Then
`make html GUIDE=new-subject`, `make pdf GUIDE=new-subject`, `make public` and
`make check`. The collection discovers guide directories; there is no second
chapter or guide manifest. Edit the catalogue summary in `tools/guides.py` when
you have a useful concise description; otherwise it uses a neutral default.

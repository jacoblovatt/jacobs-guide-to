# Five bounded validation passes

Recorded on 18 November 2026. This is a local validation record, not a claim
that CI or a public deployment has run.

## Pass 1 — Architecture and scope

Confirmed the existing guides and blog remotes and initial working trees.
Created `build/jacobs-guides`. Preserved the supplied prompt and the blog's two
untracked posts; no blog files changed. The guides use canonical `.qmd`,
independent book projects, one shared metadata/theme layer and one ordered
public chapter list per book. No public/remote operations were performed.

## Pass 2 — Content correctness

Reviewed the integrating-factor argument on an interval with continuous
coefficients: choosing an antiderivative P gives mu = exp(P), so mu' = p mu;
multiplying therefore produces the product derivative. Nonvanishing mu makes
both integration and division reversible. The initial-value formula retains
the arbitrary constant through its initial term.

Checked the worked result y = exp(x)/3 + 2 exp(-2x)/3: its derivative plus twice
the function is exp(x), and y(0) = 1. Exercise 1 gives 2 exp(x) - 2 and verifies
y' - y = 2, y(0) = 0. Exercise 2 gives x^2/3 + 5/(3x) on x > 0 and verifies
y' + y/x = x, y(1) = 2. Domain restrictions and normalising the leading
coefficient are stated. The original figure uses the same solution family.

Verified the OpenStax section, title, authors, publisher and 2016 publication
year against the accessible source's citation information. No historical claim,
quotation or page number was invented. The other three guides state explicitly
that they are introductions and proposed contents rather than completed books.

## Pass 3 — Build and paths

Ran setup (idempotent existing installation), doctor, individual HTML/PDF,
complete public builds and checks using Quarto 1.11.9 and system XeLaTeX.
Rendered all four HTML books and all four PDFs. The final assembled artifact
contains seven HTML pages and passes 219 local link/resource/anchor checks
under `/jacobs-guide-to/`. CSS font resources, search hrefs, page coverage and
A4 PDF text/metadata are included in these checks. External links are not
batch-crawled; the cited OpenStax source was opened separately.

Found and fixed a real inheritance/path issue: a shared raw CSS link outside
the nested book would point outside the assembled artifact. Switched to the
supported shared SCSS theme, which Quarto compiles into each book's own
`site_libs`. Checked the final links. Shared prose includes render correctly
in all three starters without changing their titles or metadata.

The publication regression uses a fresh temporary source copy. It first adds a
unique selected probe chapter with a linked text resource and confirms they
are built, while a different unselected probe stays excluded. It then removes
only the selected chapter's configuration entry and rebuilds, leaving that
source and resource in place. It checks that no probe HTML, assets, PDF text,
search entries or marker bytes survive. The probe is never added to the real
chapters. The check also confirms failure for invalid guide names and missing
chapter source. A test-fixture correction made the resource explicitly linked,
so the regression verifies actual resource publication before removal.

Generated-directory checks reject symlink ancestors. Python compilation,
installer shell syntax and workflow YAML parsing passed. Quarto failures
propagate through Make and include captured diagnostics.

## Pass 4 — Reader experience

Rasterised and visually inspected all eight calculus PDF pages and all nine
starter PDF pages using Poppler. Checked page numbering, margins, equations,
callout, figure, table, references and page transitions: no clipping or overlap
was observed. PDF named destinations include equation/section/footnote targets;
URL annotations contain the verified reference. PDF links were inspected
structurally, not clicked in a desktop reader.

Started `make preview GUIDE=calculus`; Quarto reported watching for changes and
served HTTP 200 at its printed loopback URL. Started the prefix-shaped
`make serve` preview and received HTTP 200 for the catalogue, pilot HTML and
PDF. Preview processes were stopped after checking.

**Remaining reader check:** desktop and narrow-screen browser screenshots,
interactive search, mobile menu and MathJax typesetting could not be verified.
The connected browser was discoverable, but repeated documented attempts to
bind/navigate a preview tab failed in the browser control layer with an
undefined `timeoutMs` error. No substitute browser automation was installed.
Responsive styles and HTML alt text were checked statically, which does not
replace visual browser review. Run `make serve`, inspect at normal width and
about 390 px wide, and try search/navigation/downloads before first deployment.

## Pass 5 — Reproducibility and handoff

The temporary-copy regression excludes `.git`, `.tools`, build output and
Quarto caches, and uses the already installed pinned Quarto binary through
`QUARTO`. It runs the documented doctor, individual HTML/PDF, public and check
commands with fresh output. This validates source/build reproducibility, not a
fresh OS or full package installation. `make setup` was checked for repeat
safety; the initial official archive and its SHA-256 were verified separately.

Confirmed generated site, preview output, caches and portable tools are ignored.
Inspected the four final PDFs. README, templates, writing instructions, blog
proposals and exact Pages activation steps are present. Work remains uncommitted
on the isolated branch for review; no unrelated files were staged or committed.

The two workflows have been prepared and parsed locally, but require a real
GitHub run to validate the runner environment, Pages eligibility/settings,
environment protection and deployment. The existing blog pipeline was not run
because no blog changes were applied. A TinyTeX installation and EPUB output
were not tested. The remaining publishing action is an explicit reviewed
activation and manual run of the single guides deployment workflow.

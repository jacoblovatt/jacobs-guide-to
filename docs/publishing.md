# Publishing handoff

No remote repository was created, no commit was pushed, no Pages settings were
changed and no public site was deployed during implementation. Local builds
need no GitHub authentication. These workflows are prepared source files and
have not run remotely.

## Verified identity and unresolved remote settings

Local Git configuration gives:

- Guides origin: `git@github.com:jacoblovatt/jacobs-guide-to.git`.
- Blog origin: `git@github.com:jacoblovatt/jacoblovatt.github.io.git`.
- Blog configured URL: `https://jacoblovatt.github.io`, baseurl empty.
- Proposed guides URL: `https://jacoblovatt.github.io/jacobs-guide-to/`.
- Project prefix: `/jacobs-guide-to/`, recorded in `site.toml`.

The guides remote already exists in local configuration, so a new repository
is not a prerequisite. Its actual visibility, plan eligibility and live Pages
configuration remain unverified without authentication. No `gh` CLI was
installed. The blog's existing workflow was inspected locally; its current
live deployment status was not queried.

## Activate after local review

1. Run `make public`, `make check`, and `make serve`. Review the catalogue,
   complete calculus chapter and PDFs. The local URL is
   `http://127.0.0.1:8000/jacobs-guide-to/`.
2. Review `git status` and diffs on `build/jacobs-guides`. Preserve the original
   build prompt and review it before deciding whether to commit it. Commit the
   intended source, docs, templates, assets and workflows; do not commit
   `build/`, `.tools/` or the separate blog's untracked posts.
3. After a distinct instruction to publish, push the reviewed branch and merge
   it to `main`. The **Validate guides** workflow should pass there or on the
   pull request; it builds but never deploys.
4. In **jacoblovatt/jacobs-guide-to**, open **Settings → Pages → Build and
   deployment → Source** and select **GitHub Actions**. Do not change the
   `jacoblovatt.github.io` blog repository's settings.
5. Check repository eligibility. GitHub documents Pages for public repositories
   on Free, and private repositories on appropriate paid plans. A private source
   repository does not by itself make the resulting Pages site private. Check
   the intended audience and account plan before activation.
6. Configure the `github-pages` environment to allow deployments only from
   `main`; optionally require a reviewer. Enable Actions if disabled. No personal
   access token or custom deployment secret is needed by these workflows.
7. Open **Actions → Publish guides (manual) → Run workflow → main**. This is the
   concrete public deployment step. The build compares Pages' actual base path
   against `site.toml`, renders the collection and uploads **one** Pages artifact.
   A separate environment-protected job deploys it.
8. Open the URL reported by the deployment. Test catalogue/book navigation,
   search for “integrating factor”, figure/equation/footnote links and the PDF
   download. Then consider the proposed blog integration below.

If the repository is renamed or gets a custom domain, revise `site.toml`, the
proposed URLs in blog files/templates and these instructions, then rerun the
prefix check. The current helper intentionally expects a project-site prefix;
a root-domain site needs a small reviewed adjustment. All generated reader
links are relative and do not hard-code the account or a deployment domain.

## CI and permissions

`validate.yml` runs on pull requests, pushes to main and manual dispatch. Its
only token permission is `contents: read`, and checkout does not retain Git
credentials. It does not use Pages credentials, environment secrets or
`pull_request_target`. It performs clean renders and the exclusion regression.

`deploy.yml` is manual and checks that the selected ref is main. Its build job
has read-only contents/Pages access. Only the deploy job gets `pages: write`
and `id-token: write`; that job is tied to the `github-pages` environment.
Both workflows use Ubuntu 24.04, Python 3.13, Quarto from `.quarto-version`, and
explicitly installed TeX Live/Poppler tools. A first remote run is still needed
to verify runner/package behaviour and actual Pages settings.

Action majors were checked against official sources during implementation:
checkout v7 (release v7.0.1), setup-python v7 (release v7.1.0), Quarto setup v2,
configure-pages v5, upload-pages-artifact v4 and deploy-pages v4. Major action
refs receive upstream fixes; Quarto itself is pinned. Review upgrades when
changing the toolchain.

Later, automatic publication can be enabled by adding a push-to-main trigger
to `deploy.yml` after branch protection/review rules are in place. Keep one
assembled artifact and one deployment job; do not create a separate deployment
for every book.

## Blog integration proposal

The existing blog is Jekyll 4.4/Minima 2.5 with kramdown, default post layouts,
`title`, optional `subtitle`, and array `tags` conventions. Its post URLs use
`/:year-:month-:day-:title/`. The proposed post uses plain Markdown and full
canonical links; it needs no Quarto syntax or MathJax.

Reviewable files are in `docs/blog-proposal/`:

- `2026-11-18-why-integrating-factors-work.md`: copy to the blog's `_posts/`
  only after approving it and checking the canonical chapter URL is live.
- `guides.md`: proposed page for the blog repository root, linking to the
  catalogue. After approval, add `guides.md` to `_config.yml` → `header_pages`.

The current Minima header follows `header_pages`. An additional navigation data
file also exists, but it is not the authoritative setting for this theme's
header; avoid maintaining competing navigation lists. The proposed change is
one new page and one header entry. Do not modify existing post URLs, content or
the existing deployment workflow. Date the post appropriately when publishing
if that happens later. Full-chapter syndication is deferred.

Official references:
[Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages),
[Quarto GitHub Pages](https://quarto.org/docs/publishing/github-pages.html),
[Quarto Actions](https://github.com/quarto-dev/quarto-actions),
[checkout releases](https://github.com/actions/checkout/releases),
[setup-python releases](https://github.com/actions/setup-python/releases).

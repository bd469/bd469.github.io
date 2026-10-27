# Beixi (Chloe) Du — personal website

Live site: https://bd469.github.io/

A responsive, build-free academic portfolio hosted on GitHub Pages from the root of `main`.

## Content

- **About:** biography and selected publications.
- **Publications:** papers and a keyboard-accessible Research tab.
- **Financial Engineering:** portfolio project, industry experience, and a Coinbase project preview.
- **Life with Cats:** five photographs with an accessible enlarged-photo viewer.
- **CV:** existing CV PDF, education, and skills.

`index.html` contains all page content, so the site remains readable with JavaScript disabled. Styling lives in `assets/styles.css`; navigation and gallery behavior live in `assets/site.js`. Section URLs use hashes (for example `/#publications`, `/#research`, and `/#cats`); browser Back/Forward and older section links remain supported.

## Updating content

- Add or edit paper entries in `index.html` under `#papers-panel`. Update selected entries under `#about` when appropriate. Keep author order, contribution notes, and publication status aligned with the manuscript.
- The two uploaded PDFs are stored unchanged in `papers/retriever-free-retrieval.pdf` and `papers/the-prestige.pdf`.
- Replace the text in `#coinbase-project` with the project description when available. No results, dates, affiliations, or project link have been invented; the available CV copies did not contain a Coinbase entry.
- Add finance projects as articles in `#financial-engineering`.
- The five existing cat images remain at their original root paths. Optimized WebP copies in `assets/images/` are used in the gallery; clicking a photo opens the original in the viewer. Update captions and alt text in `#cats` when changing images.
- CV buttons use `cv_job.pdf`; `resume.pdf` remains available at its original URL. The CV file was not rewritten as part of the redesign.
- Update `sitemap.xml` when making substantial changes.

## Preview and publish

Run `python3 -m http.server 8765` from this directory and open http://localhost:8765/.

Commit and push changes to `main`. GitHub Pages publishes the repository root; no dependencies, package installation, or build step are required.

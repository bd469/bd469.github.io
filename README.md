# Beixi (Chloe) Du — personal website

Live site: https://bd469.github.io/

A responsive, build-free academic portfolio hosted on GitHub Pages from the root of `main`. The November 2026 redesign uses a compact, continuous academic layout inspired by https://carrie-lin.github.io/, with original styling and Beixi's existing content and assets.

## Content

- **Introduction:** portrait, Cornell and UCLA AIVC affiliations, biography, and contact links.
- **News:** dated research updates already supported by the existing record.
- **Research:** three publication rows with figures, author credits, status, and links.
- **Industry Experience:** compact entries for the Coinbase capstone, Western Securities internship, and Huatai Securities internship. The capstone is explicitly labeled as a project, not employment, without “Cornell MFE.”
- **CV:** the existing two-page PDF linked from the introduction; no separate CV section.
- **Outside of Research:** six cat photographs, including a foster cat, with an accessible enlarged-photo viewer.

`index.html` contains all content. Native section links work with JavaScript disabled. Styling lives in `assets/styles.css`; legacy hash compatibility and the gallery viewer live in `assets/site.js`. Section URLs use hashes (for example `/#publications`, `/#industry-experience`, and `/#cats`); older research links lead to publications, and older finance links lead to industry experience. Photos still open directly without JavaScript.

## Updating content

- Add or edit paper entries in `index.html` under `#publications`. There is only one canonical publication list. Keep author order, contribution notes, and publication status aligned with the manuscript.
- The two uploaded PDFs are stored unchanged in `papers/retriever-free-retrieval.pdf` and `papers/the-prestige.pdf`.
- The industry entries summarize the November 2026 record. Update `#industry-experience` and `#coinbase-project` when roles or dates change. Keep the capstone distinct from internships.
- The five existing cat images remain at their original root paths. Optimized WebP copies in `assets/images/` are used in the gallery; clicking a photo opens the original in the viewer. The foster-cat photograph is preserved unchanged at `assets/images/foster-cat.png`. Update captions and alt text in `#cats` when changing images.
- CV buttons use `cv_job.pdf` with a dated cache-busting query; `resume.pdf` remains available at its original URL. Replace `cv_job.pdf` and update the query date when publishing a new CV.
- The unverified Cornell GPA is omitted from the HTML. The PDF itself has not been edited in this design change.
- Update `sitemap.xml` when making substantial changes.

## Preview and publish

Run `python3 -m http.server 8765 --bind 127.0.0.1` from this directory and open http://localhost:8765/. You can also open `index.html` directly: this site has no build step, API, external fonts, or runtime dependencies.

Run `python3 tests/check_site.py` to check HTML nesting, IDs, local links and assets, publication/photo/industry counts, removal of the detailed research and CV sections, and preservation of the Google verification tag. Run `node --check assets/site.js` to check JavaScript syntax. Browser checks should cover narrow screens, legacy section links, and the photo viewer's buttons and Escape key.

Commit and push changes to `main`. GitHub Pages publishes the repository root; no dependencies, package installation, or build step are required.

## Search discovery

The homepage has a descriptive title starting with Beixi Du, a canonical URL, crawlable HTML, and linked WebSite/ProfilePage/Person structured data. `robots.txt` allows crawling and advertises `sitemap.xml`.

Google Search Console ownership for the URL-prefix property `https://bd469.github.io/` was verified on October 27, 2026 using the `google-site-verification` meta tag in `index.html`. Keep this tag in place to retain ownership verification. Google accepted a homepage indexing request on October 27, 2026 and added the URL to its priority crawl queue; this is a request, not confirmation that the page is indexed. The sitemap was submitted to Search Console. Its initial report showed “Couldn’t fetch,” but a subsequent Google live URL test on October 27, 2026 confirmed “Page fetch: Successful” and “Crawl allowed: Yes”; the public URL also returned HTTP 200 with valid XML. The Sitemaps report had not yet updated at the end of setup. Check the report for processing updates. Submission does not guarantee indexing or ranking.

"""Dependency-free checks for the static academic website."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.ids = []
        self.links = []
        self.errors = []
        self.papers = 0
        self.cats = 0
        self.headings = 0
        self.industry_entries = 0
        self.cat_links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == 'img' and 'alt' not in attrs:
            self.errors.append('Image without alternative text')
        classes = attrs.get('class', '').split()
        self.papers += 'publication-card' in classes
        self.cats += 'cat-photo' in classes
        if 'cat-photo' in classes:
            self.cat_links.append(attrs['href'])
        self.headings += tag == 'h1'
        self.industry_entries += 'industry-entry' in classes

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f'Unexpected closing tag: {tag}; stack: {self.stack[-3:]}')
        else:
            self.stack.pop()


page = SiteParser()
html = (ROOT / 'index.html').read_text()
page.feed(html)
page.close()
assert not page.errors, '\n'.join(page.errors)
assert not page.stack, f'Unclosed tags: {page.stack}'
assert page.headings == 1, 'Expected exactly one h1'
assert page.papers == 3, 'Expected all three publications'
assert page.cats == 6, 'Expected all six cat photos'
assert page.cat_links[:5] == [f'assets/images/cats/{name}-photo.webp' for name in ('lucky', 'ss', 'dd', 'tt', 'xx')], 'Use all five background-preserving photos in the original order'
assert page.cat_links[5] == 'assets/images/foster-cat.png', 'Keep the foster-cat photo unchanged'
assert '<figcaption>' not in html, 'Gallery captions should stay removed'
assert page.industry_entries == 3, 'Expected two internships and one capstone'
assert '<h1>Beixi (Chloe) Du</h1>' in html, 'Name should use one consistent type size'
assert 'class="section-nav"' not in html, 'The content menu should stay removed'
assert html.count('class="research-intro"') == 1
assert html.index('class="research-intro"') < html.index('id="news"'), 'Research interests belong in the introduction'
assert 'Publications &amp; Manuscripts' in html
assert html.count('Equal contribution') == 1, 'Keep one shared contribution legend'
assert '* Equal contribution.</p>' in html
assert 'within each paper' not in html
assert 'class="contribution"' not in html, 'Remove repeated per-paper contribution notes'
assert 'Department of Mathematics' not in html
assert 'preprint' not in html.lower()
assert 'Submitted to' not in html and 'ACC 2027' not in html, 'Do not display pending submission venues'
assert html.count('<span>arXiv · 2026</span>') == 2, 'Show the public arXiv status of both manuscripts'
publications = html.split('<section id="publications"', 1)[1].split('</section>', 1)[0]
assert '.pdf' not in publications.lower() and '>PDF<' not in publications, 'Paper entries must link to external landing pages, not PDFs'
assert publications.count('>Paper</a>') == 3
for paper_id in ('2610.35868', '2610.38103', '2604.24663'):
    assert publications.count(f'href="https://arxiv.org/abs/{paper_id}"') == 2, 'Each paper title and Paper link should lead to its arXiv record'
assert '>Project Page</a>' in publications and '>Code</a>' in publications
assert not list((ROOT / 'papers').glob('*.pdf')), 'Do not host paper PDFs on the website'
assert 'href="cv_job.pdf?v=20261113-arxiv"' in html, 'Link to the latest CV with its arXiv-only manuscript status'
assert 'Cornell MFE' not in (ROOT / 'index.html').read_text()
assert '<section id="cv"' not in (ROOT / 'index.html').read_text()
assert '<section id="research"' not in (ROOT / 'index.html').read_text()
assert all(count == 1 for count in Counter(page.ids).values()), 'Duplicate IDs'
for link in page.links:
    parsed = urlsplit(link)
    if parsed.scheme or parsed.netloc:
        continue
    if parsed.path:
        assert (ROOT / unquote(parsed.path)).is_file(), f'Missing local asset: {link}'
    elif parsed.fragment:
        assert parsed.fragment in page.ids, f'Broken section link: {link}'
assert 'google-site-verification' in (ROOT / 'index.html').read_text()
print(f'PASS: balanced HTML, {len(page.ids)} unique IDs, {len(page.links)} links/assets, 3 publications, 6 photos, SEO verification retained.')

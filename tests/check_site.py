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
assert page.industry_entries == 3, 'Expected two internships and one capstone'
assert '<h1>Beixi (Chloe) Du</h1>' in html, 'Name should use one consistent type size'
assert 'class="section-nav"' not in html, 'The content menu should stay removed'
assert html.count('class="research-intro"') == 1
assert html.index('class="research-intro"') < html.index('id="news"'), 'Research interests belong in the introduction'
assert 'Publications &amp; Manuscripts' in html
assert html.count('Equal contribution') == 1, 'Keep one shared contribution legend'
assert 'class="contribution"' not in html, 'Remove repeated per-paper contribution notes'
assert 'Department of Mathematics' not in html
assert 'preprint' not in html.lower()
assert 'Submitted to ACC 2027' in html, 'Preserve the submitted, not accepted, status'
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

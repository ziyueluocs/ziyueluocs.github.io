#!/usr/bin/env python3
"""Check the deployable artifact for broken links and content regressions."""

from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json

from build_site import ROOT, OUTPUT, load_publications


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.papers = 0
        self.h1 = 0
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id: {attrs["id"]}'
            self.ids.add(attrs['id'])
        for name in ('href', 'src'):
            if name in attrs:
                self.links.append(attrs[name])
        if tag == 'li' and 'paper' in attrs.get('class', '').split():
            self.papers += 1
        if tag == 'h1':
            self.h1 += 1


def check():
    pages = {path.resolve(): Page(path) for path in OUTPUT.rglob('*.html')}
    for path, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            if not url.path:
                target = path
            elif url.path.startswith('/'):
                target = OUTPUT / unquote(url.path.lstrip('/'))
            else:
                target = path.parent / unquote(url.path)
            if target.is_dir():
                target = target / 'index.html'
            target = target.resolve()
            assert target.is_relative_to(OUTPUT), f'Link escapes output: {href}'
            assert target.is_file(), f'Broken local link in {path.name}: {href}'
            if url.fragment and target in pages:
                assert unquote(url.fragment) in pages[target].ids, f'Missing anchor: {href}'

    path = OUTPUT / 'index.html'
    text = path.read_text(encoding='utf-8')
    home = pages[path.resolve()]
    profile = json.loads((ROOT / '_data/profile.json').read_text(encoding='utf-8'))
    assert home.h1 == 1
    assert home.papers == len(load_publications())
    assert {'contact', 'about', 'research', 'publications', 'top', 'main'} <= home.ids
    assert text.index('id="contact"') < text.index('id="about"')
    assert profile['email_display'] in text
    assert profile['school']['name'] in text
    assert profile['university']['name'] in text
    for forbidden in ('noindex', 'design-preview/', 'review-bar', 'study-select', 'mailto:', 'luo.1457'):
        assert forbidden not in text, f'Unexpected content in homepage: {forbidden}'
    assert 'advised by' in text and 'Zongpeng Li' in text
    assert 'https://www.insc.tsinghua.edu.cn/info/1157/4007.htm' in text
    assert 'href="https://ziyueluocs.github.io/"' in text
    assert not (OUTPUT / 'design-preview').exists()
    assert not (OUTPUT / '_data').exists()
    assert (OUTPUT / 'assets/pdf/CV.pdf').read_bytes() == (ROOT / 'assets/pdf/CV.pdf').read_bytes()
    print(f'Checked {len(pages)} HTML pages: local links, anchors, metadata, {home.papers} publications, and CV parity.')


if __name__ == '__main__':
    check()

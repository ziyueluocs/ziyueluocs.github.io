#!/usr/bin/env python3
"""Build the selected academic homepage with Python's standard library."""

from collections import defaultdict
from hashlib import sha256
from html import escape
from pathlib import Path
from string import Template
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '_site'
ASSETS = (
    'assets/css/academic.css',
    'assets/js/academic.js',
    'assets/img/favicon.svg',
    'assets/img/portrait.jpg',
    'assets/pdf/CV.pdf',
)


def link(url, label):
    return f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'


def markdown_links(value):
    """Render the inline links used by the existing publication source."""
    chunks = []
    start = 0
    for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', value):
        chunks.extend((escape(value[start:match.start()]), link(match[2], match[1])))
        start = match.end()
    chunks.append(escape(value[start:]))
    return ''.join(chunks)


def load_publications():
    text = (ROOT / '_pages/publications.md').read_text(encoding='utf-8')
    body = text.split('---', 2)[2]
    papers = []
    for paragraph in re.split(r'\n\s*\n', body.strip()):
        match = re.fullmatch(r'(.*?)\. "(.*?)," (.*)', paragraph.strip(), re.S)
        if not match:
            raise ValueError(f'Unrecognized publication: {paragraph[:80]}')
        authors, title, citation = match.groups()
        years = re.findall(r'\b(?:19|20)\d{2}\b', citation)
        if not years:
            raise ValueError(f'Publication has no year: {title}')
        papers.append(dict(authors=authors, title=title, citation=citation, year=int(years[-1])))
    if not papers:
        raise ValueError('The publication list is empty.')
    return papers


def paper_markup(paper, name):
    authors = escape(paper['authors']).replace(escape(name), f'<strong>{escape(name)}</strong>')
    if len(paper['authors']) > 400:
        names = paper['authors'].split(', ')
        first = ', '.join(names[:3])
        summary = escape(first).replace(escape(name), f'<strong>{escape(name)}</strong>')
        authors = (
            f'<details class="coauthors"><summary>{summary}, and {len(names) - 3} coauthors'
            '<span class="expand-label">Show all</span></summary>'
            f'<p>{authors}</p></details>'
        )
    else:
        authors = f'<p class="authors">{authors}</p>'
    return (
        f'<li class="paper"><h4>{markdown_links(paper["title"])}</h4>{authors}'
        f'<p class="venue">{escape(paper["citation"])}</p></li>'
    )


def bibliography(papers, name):
    grouped = defaultdict(list)
    for paper in papers:
        grouped[paper['year']].append(paper)
    sections = []
    for year in sorted(grouped, reverse=True):
        items = '\n'.join(paper_markup(paper, name) for paper in grouped[year])
        sections.append(
            f'<section class="year-group" aria-labelledby="year-{year}">'
            f'<h3 class="year" id="year-{year}">{year}</h3>'
            f'<ol class="paper-list" role="list">{items}</ol></section>'
        )
    return '\n'.join(sections)


def asset_url(path):
    """Changing an asset also changes its URL, including the downloadable CV."""
    digest = sha256((ROOT / path).read_bytes()).hexdigest()[:12]
    return f'/{path}?v={digest}'


def redirect_page(title, target, site_url):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={escape(target, quote=True)}">
<link rel="canonical" href="{escape(site_url + target, quote=True)}">
<title>{escape(title)} | Ziyue Luo</title></head>
<body><p>Continue to <a href="{escape(target, quote=True)}">{escape(title)}</a>.</p></body></html>
'''


def build():
    profile = json.loads((ROOT / '_data/profile.json').read_text(encoding='utf-8'))
    papers = load_publications()
    values = {key: escape(profile[key], quote=True) for key in (
        'name', 'position', 'email_display', 'office', 'location',
        'site_url', 'description', 'scholar_url',
    )}
    values['school_name'] = escape(profile['school']['name'])
    for institution in ('university',):
        for key in ('name', 'url'):
            values[f'{institution}_{key}'] = escape(profile[institution][key], quote=True)
    values.update(
        biography_html=profile['biography_html'],
        research_html=profile['research_html'],
        profile_links='\n'.join(link(item['url'], item['label']) for item in profile['profiles']),
        publications_html=bibliography(papers, profile['name']),
        cv_url=asset_url('assets/pdf/CV.pdf'),
        stylesheet_url=asset_url('assets/css/academic.css'),
        script_url=asset_url('assets/js/academic.js'),
        favicon_url=asset_url('assets/img/favicon.svg'),
        portrait_url=asset_url('assets/img/portrait.jpg'),
    )
    template = Template((ROOT / '_templates/home.html').read_text(encoding='utf-8'))
    homepage = template.substitute(values)

    # _site is generated output, never a source directory. Start with a clean
    # artifact so legacy theme files and design studies cannot be published.
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    (OUTPUT / 'index.html').write_text(homepage, encoding='utf-8')
    for path in ASSETS:
        target = OUTPUT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, target)
    for route, title, target in (
        ('publications', 'Publications', '/#publications'),
        ('cv', 'CV', values['cv_url']),
    ):
        directory = OUTPUT / route
        directory.mkdir()
        (directory / 'index.html').write_text(redirect_page(title, target, profile['site_url']), encoding='utf-8')
    (OUTPUT / '404.html').write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>Page not found | {values['name']}</title>
<link rel="stylesheet" href="{values['stylesheet_url']}"></head>
<body class="concept-a"><main class="site-shell"><div class="not-found"><h1>Page not found</h1>
<p>The page you requested could not be found.</p><p><a href="/">Return to {values['name']}'s homepage</a></p>
</div></main></body></html>
''', encoding='utf-8')
    (OUTPUT / '.nojekyll').touch()
    (OUTPUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {profile["site_url"]}/sitemap.xml\n', encoding='utf-8')
    (OUTPUT / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f'<url><loc>{escape(profile["site_url"])}/</loc></url></urlset>\n', encoding='utf-8',
    )
    print(f'Built {OUTPUT}: homepage, legacy routes, and {len(papers)} publications.')


if __name__ == '__main__':
    build()

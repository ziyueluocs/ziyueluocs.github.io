#!/usr/bin/env python3
"""Build ten local design studies from the existing publication source.

No dependencies. Run from any directory with: python3 design-preview/build.py
The Jekyll site, its routes, and its deployment configuration are left intact.
"""
from html import escape
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VARIANTS = {
    'a': ('Classic', '经典书页', '居中阅读，衬线标题。熟悉的学术主页，多一点排版质感。'),
    'b': ('Faculty', '侧栏档案', '个人信息常驻左侧，正文独立展开。适合专注浏览研究与论文。'),
    'c': ('Air', '清浅蓝调', '轻盈的浅蓝页眉，清晰的无衬线排版。现代，但依然安静。'),
    'd': ('Bulletin', '大学公报', '对称刊头与双栏简介，带一点学术期刊的正式感。'),
    'e': ('Essential', '极简名片', '小标题、小照片、紧凑的阅读列。把视觉存在感降到最低。'),
    'f': ('Letter', '书信手稿', '暖白纸面、蓝色页边、通篇衬线文字。像一封认真排版的信。'),
    'g': ('Grid', '瑞士网格', '明确的对齐线、章节编号与不对称排版。理性、清晰、有秩序。'),
    'h': ('Index', '研究索引', '论文先出现，个人介绍在右侧。目录式排版，适合快速查找成果。'),
    'i': ('Chronicle', '论文年鉴', '沿着浅蓝时间线浏览论文，年份更突出，阅读节奏更舒展。'),
    'j': ('Portrait', '居中人物', '圆形照片与姓名居中，下方安静地展开正文。温和、轻巧。'),
}

def link(url, label, cls=''):
    return f'<a href="{escape(url, quote=True)}" class="{cls}">{label}</a>'

def markdown_links(value):
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                  lambda m: link(m[2], m[1]), escape(value))

def publications():
    body = (ROOT / '_pages/publications.md').read_text().split('---', 2)[2]
    result = []
    for paragraph in re.split(r'\n\s*\n', body.strip()):
        match = re.fullmatch(r'(.*?)\. "(.*?)," (.*)', paragraph.strip(), re.S)
        if not match:
            raise ValueError(f'Unrecognized publication: {paragraph[:80]}')
        authors, title, citation = match.groups()
        year = int(re.findall(r'\b(?:19|20)\d{2}\b', citation)[-1])
        result.append(dict(authors=authors, title=title, citation=citation, year=year))
    assert len(result) == 17, 'Review publication count when source changes.'
    return result

PAPERS = publications()
SCHOLAR = 'https://scholar.google.com/citations?user=ZEpJnx0AAAAJ'
CV = '../assets/pdf/CV.pdf'
PORTRAIT = '../assets/img/portrait.jpg'

def paper_markup(p, indexed=False):
    authors = escape(p['authors']).replace('Ziyue Luo', '<strong>Ziyue Luo</strong>')
    if len(p['authors']) > 400:
        names = p['authors'].split(', ')
        authors = f'<details class="coauthors"><summary><strong>Ziyue Luo</strong>, Jiaxuan Cai, Cedric Le Denmat, and {len(names) - 3} coauthors<span class="expand-label">Show all</span></summary><p>{authors}</p></details>'
    else:
        authors = f'<p class="authors">{authors}</p>'
    title_and_authors = f'<h4>{markdown_links(p["title"])}</h4>{authors}'
    if indexed:
        return f'<li class="paper index-paper"><div class="index-paper-main">{title_and_authors}</div><p class="venue">{escape(p["citation"])}</p></li>'
    return f'<li class="paper">{title_and_authors}<p class="venue">{escape(p["citation"])}</p></li>'

def bibliography(indexed=False):
    sections = []
    for year in dict.fromkeys(p['year'] for p in PAPERS):
        items = ''.join(paper_markup(p, indexed) for p in PAPERS if p['year'] == year)
        sections.append(f'<section class="year-group" aria-labelledby="year-{year}"><h3 class="year" id="year-{year}">{year}</h3><ol class="paper-list" role="list">{items}</ol></section>')
    return ''.join(sections)

BIO = '''<p>I am a professor in the School of Cyber Science and Engineering at <a href="https://www.whu.edu.cn/">Wuhan University</a>. Previously, I was a postdoctoral researcher and then a research scientist at <a href="https://www.osu.edu/">The Ohio State University</a>, working with <a href="https://cse.osu.edu/people/shroff.11">Ness B. Shroff</a> and <a href="https://kevinliu-osu.github.io/">Jia (Kevin) Liu</a>.</p>
<p>I received my Ph.D. in Computer Science from <a href="https://www.hku.hk/">The University of Hong Kong</a>, advised by <a href="https://i.cs.hku.hk/~cwu/index.html">Chuan Wu</a>, and my B.E. from <a href="https://www.whu.edu.cn/">Wuhan University</a>, advised by <a href="https://www.insc.tsinghua.edu.cn/info/1157/4007.htm">Zongpeng Li</a>.</p>'''
RESEARCH = '''<p>My research focuses on optimizing distributed systems, with an emphasis on efficient resource scheduling. Recently, I have been working on the analysis and optimization of distributed machine learning systems.</p>'''

def social_links():
    return '<div class="social-links" aria-label="Academic profiles">' + ' '.join([
        link(SCHOLAR, 'Google Scholar'),
        link('https://orcid.org/0000-0002-1253-8137', 'ORCID'),
        link('https://www.linkedin.com/in/ziyue-luo-93b58914b', 'LinkedIn'),
        link(CV, 'CV <span class="filetype">PDF</span>'),
    ]) + '</div>'

def portrait():
    return f'<img class="portrait" src="{PORTRAIT}" alt="Portrait of Ziyue Luo" width="425" height="591" fetchpriority="high">'

def reviewbar(variant):
    choices = ''.join(f'<a href="{key}.html" aria-label="{key.upper()} {value[1]}" title="{key.upper()} · {value[1]}" {"aria-current=page" if key == variant else ""}><span>{key.upper()}</span></a>' for key, value in VARIANTS.items())
    options = ''.join(f'<option value="{key}.html" {"selected" if key == variant else ""}>{key.upper()} · {value[1]}</option>' for key, value in VARIANTS.items())
    return f'<aside class="review-bar" aria-label="Design preview controls"><a class="back-to-studies" href="./">← <span lang="zh-CN">全部 10 个方案</span></a><nav aria-label="Choose a design">{choices}</nav><span class="current-study" lang="zh-CN">{variant.upper()} · {VARIANTS[variant][1]}</span><select class="study-select" aria-label="切换设计方案">{options}</select></aside>'

def nav():
    return f'<nav class="site-nav" aria-label="Main navigation"><a href="#contact">Contact</a><a href="#about">About</a><a href="#research">Research</a><a href="#publications">Publications</a>{link(CV, "CV")}</nav><button class="theme-toggle" type="button" aria-label="Switch to dark theme">Dark</button>'

def contact():
    return '''<section id="contact" class="contact-section page-section" aria-labelledby="contact-heading"><h2 id="contact-heading">Contact</h2><div class="section-content"><p class="email-address"><strong>Email:</strong> luozywh [at] outlook.com</p><p class="office-address"><strong>Office:</strong> Room C509, School of Cyber Science and Engineering<br>Wuhan University, Wuhan, China</p></div></section>'''

def paper_section(indexed=False):
    return f'<section id="publications" class="publications page-section" aria-labelledby="publications-heading"><div class="section-heading"><h2 id="publications-heading">Publications</h2>{link(SCHOLAR, "Google Scholar ↗", "section-link")}</div><div class="section-content">{bibliography(indexed)}</div></section>'

def head(title):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><meta name="description" content="Ziyue Luo, Professor in the School of Cyber Science and Engineering at Wuhan University. Distributed systems and distributed machine learning."><meta name="color-scheme" content="light dark"><title>{title}</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="more-styles.css"><script src="preview.js" defer></script></head>'''

def page(variant):
    name, _, _ = VARIANTS[variant]
    common_top = f'<header class="site-header"><a class="wordmark" href="#about">Ziyue Luo<span class="wordmark-dot" aria-hidden="true">.</span></a><div class="header-tools">{nav()}</div></header>'
    identity = '<div class="identity"><h1>Ziyue Luo</h1><p class="position">Professor</p><p class="affiliation">School of Cyber Science and Engineering<br><a href="https://www.whu.edu.cn/">Wuhan University</a></p></div>'
    about = f'<section id="about" class="about-section" aria-labelledby="about-heading"><h2 id="about-heading">About</h2>{BIO}</section>'
    research = f'<section id="research" class="research-section page-section" aria-labelledby="research-heading"><h2 id="research-heading">Research</h2><div class="section-content">{RESEARCH}</div></section>'
    if variant == 'a':
        main = f'''{common_top}<main id="main" class="site-main"><section class="classic-intro" aria-label="Ziyue Luo"><div class="intro-copy">{identity}{contact()}{social_links()}</div>{portrait()}</section><section id="about" class="biography" aria-labelledby="about-heading"><h2 id="about-heading">About</h2>{BIO}</section>{research}{paper_section()}</main>'''
    elif variant == 'b':
        main = f'''<div class="faculty-layout"><aside class="faculty-sidebar" aria-label="Profile">{portrait()}{identity}<span class="sidebar-email">luozywh [at] outlook.com</span>{nav()}{social_links()}<p class="sidebar-location">Room C509<br>Wuhan University, Wuhan, China</p></aside><main id="main" class="site-main">{about}{research}{paper_section()}{contact()}</main></div>'''
    elif variant == 'c':
        main = f'''{common_top}<main id="main"><section class="air-masthead" aria-label="Ziyue Luo"><div class="masthead-inner"><div>{identity}<p class="research-line">Distributed systems &amp;<br>machine learning.</p>{social_links()}</div>{portrait()}</div></section><div class="air-body">{about}{research}{paper_section()}{contact()}</div></main>'''
    elif variant == 'd':
        main = f'''<header class="bulletin-header"><p class="institution-line">Wuhan University</p>{identity}<div class="header-tools">{nav()}</div></header><main id="main" class="site-main"><div class="bulletin-overview"><section id="about" class="about-section" aria-labelledby="about-heading"><h2 id="about-heading">About</h2>{BIO}{social_links()}</section><div class="bulletin-research">{portrait()}{research}</div></div>{paper_section()}{contact()}</main>'''
    elif variant == 'e':
        main = f'''<main id="main" class="site-main"><header class="essential-header"><div>{identity}{social_links()}</div>{portrait()}</header><div class="essential-nav header-tools">{nav()}</div>{about}{research}{paper_section()}{contact()}</main>'''
    elif variant == 'f':
        main = f'''<div class="letter-sheet"><header class="letter-header"><div>{identity}<span class="letter-email">luozywh [at] outlook.com</span></div>{portrait()}</header><div class="header-tools letter-nav">{nav()}</div><main id="main" class="site-main">{about}{research}{paper_section()}{contact()}</main><div class="letter-profiles">{social_links()}</div></div>'''
    elif variant == 'g':
        main = f'''<header class="grid-header"><div class="grid-header-line"><p>Professor <span>/</span> Wuhan University</p><div class="header-tools">{nav()}</div></div><div class="grid-identity">{identity}{portrait()}</div>{social_links()}</header><main id="main" class="site-main">{about}{research}{paper_section()}{contact()}</main>'''
    elif variant == 'h':
        main = f'''<header class="index-header"><div class="index-identity">{portrait()}{identity}</div><div class="header-tools">{nav()}</div></header><main id="main" class="index-layout"><div class="index-record">{paper_section(indexed=True)}</div><aside class="index-profile" aria-label="Researcher profile">{about}{research}{social_links()}{contact()}</aside></main>'''
    elif variant == 'i':
        main = f'''{common_top}<main id="main" class="site-main"><div class="chronicle-intro"><div class="chronicle-identity">{identity}{portrait()}{social_links()}</div><div class="chronicle-overview">{about}{research}</div></div>{paper_section()}{contact()}</main>'''
    elif variant == 'j':
        main = f'''<header class="portrait-header"><div class="header-tools">{nav()}</div></header><main id="main" class="site-main"><section class="portrait-identity" aria-label="Ziyue Luo">{portrait()}{identity}{social_links()}</section>{about}{research}{paper_section()}{contact()}</main>'''
    else:
        raise ValueError(f'Unknown design: {variant}')
    footer = '<footer class="site-footer"><span>Ziyue Luo</span><a href="#main">Back to top ↑</a></footer>'
    return head(f'Ziyue Luo | {name} design study') + f'<body class="concept concept-{variant}"><a class="skip-link" href="#main">Skip to content</a>{reviewbar(variant)}<div class="site-shell">{main}{footer}</div></body></html>\n'

def gallery():
    studies = ''
    for index, (key, (name, title, description)) in enumerate(VARIANTS.items()):
        loading = 'eager' if index < 3 else 'lazy'
        new_label = '<span class="new-study">新增</span>' if index >= 3 else ''
        studies += f'''<article class="study" id="study-{key}"><a class="study-image" href="{key}.html" aria-label="打开方案 {key.upper()}：{title}"><div class="mini-browser" aria-hidden="true"><i></i><i></i><i></i><span>ziyueluocs.github.io</span></div><div class="iframe-crop"><iframe src="{key}.html?embed=1" title="{title}预览" tabindex="-1" inert loading="{loading}"></iframe></div></a><div class="study-caption"><div class="study-title"><span class="study-letter">{key.upper()}</span><h2>{title}<span>{name}</span></h2>{new_label}</div><p>{description}</p><a class="open-study" href="{key}.html">查看完整方案 <span aria-hidden="true">↗</span></a></div></article>'''
    study_index = ''.join(f'<a href="#study-{key}"><b>{key.upper()}</b>{value[1]}</a>' for key, value in VARIANTS.items())
    return head('Ziyue Luo | 10 个学术主页设计方案') + f'''<body class="gallery"><main class="gallery-shell"><header class="gallery-top"><a class="gallery-wordmark" href="./">Ziyue Luo<span>.</span></a><span>ACADEMIC HOMEPAGE / 10 DESIGN STUDIES</span></header><section class="gallery-intro" lang="zh-CN"><p class="eyebrow">同一份内容，十种阅读方式</p><h1>找到你喜欢的学术主页。</h1><p>以研究和论文为中心，用一点清浅的蓝色。<br>A、B、C 是第一轮方案，D 至 J 是这次新增的七个方向。</p><div class="palette" aria-label="设计配色"><span style="--swatch:#c5d8e8"></span><span style="--swatch:#edf4f9"></span><span style="--swatch:#355f7f"></span><span class="palette-label">Sky blue · Paper white · Ink blue</span></div><a class="start-new" href="d.html">从新增方案 D 开始看 <span aria-hidden="true">↗</span></a></section><nav class="study-index" aria-label="按名称定位方案" lang="zh-CN">{study_index}</nav><section class="studies" aria-label="十个设计方案" lang="zh-CN">{studies}</section><section class="design-notes" lang="zh-CN"><div><h2>这轮比较什么</h2><p>比较字体气质、信息密度、照片位置和论文的阅读方式。十版都保留同一份简介、17 篇论文和 CV；可以选整版，也可以组合喜欢的细节。</p></div><div><h2>参考与取舍</h2><p>参考 <a href="https://jonbarron.info/">Jon Barron</a> 的阅读结构和 <a href="https://www.cs.cmu.edu/~dpathak/">Deepak Pathak</a> 的学术内容组织；按 <a href="https://vercel.com/design/guidelines">Vercel 界面准则</a> 处理键盘焦点、移动布局和锚点。浅蓝色取意于 <a href="https://www.apple.com/iphone-air/">iPhone Air Sky Blue</a>，深蓝链接保证可读性。</p></div></section><footer class="gallery-footer"><span>10 个完整方案 · 本地预览 · 尚未发布</span><a href="README.md">设计说明</a></footer></main></body></html>\n'''

if __name__ == '__main__':
    for key in VARIANTS:
        (HERE / f'{key}.html').write_text(page(key))
    (HERE / 'index.html').write_text(gallery())
    print(f'Built {len(VARIANTS)} design studies and comparison page, with {len(PAPERS)} publications each.')

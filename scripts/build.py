"""Build the Chinese Hyprland Wiki with Python 3.11+ and Pandoc 3.8+."""
import argparse
import html
import json
import os
import posixpath
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'scripts/build-data.json').read_text())
UPSTREAM = 'https://wiki.hypr.land/'
REPOSITORY = 'https://github.com/banana815/hyprland-wiki-zh-cn'
HEAD = re.compile(r'<h([1-6])(?:\s[^>]*)?>(.*?)</h\1>', re.S)
SHORT = re.compile(r'^\s*{{[<%]\s*(/?[\w_]+)(.*?)\s*[>%]}}\s*$', re.M)
ALERTS = {'Note': '说明', 'Important': '重要', 'Tip': '提示', 'Warning': '警告', 'Caution': '注意'}
LABELS = {
    'Examples': '示例', 'Example': '示例', 'Example background': '背景示例',
    'Example image': '图片示例', 'Example input-field': '输入框示例',
    'Example label': '标签示例', 'Example listener': '监听器示例', 'Example output': '输出示例',
    'Example shape': '形状示例', 'Parameters example': '参数示例',
    'Workspaces widget': '工作区组件', 'Active window title widget': '活动窗口标题组件',
    'From Upstream': '从上游安装', 'From Your Distro': '从发行版安装',
    'From hyprnix (Recommended)': '从 hyprnix 安装（推荐）', 'From Nixpkgs': '从 Nixpkgs 安装',
    'From the Flake': '从 flake 安装', 'GNOME Keyring PAM setup': '配置 GNOME 密钥环 PAM',
    'Manual': '手动安装', 'Generic': '通用', 'Nixpkgs repository': 'Nixpkgs 仓库',
    'The Hyprland flake': 'Hyprland flake',
}
escape = html.escape


@dataclass
class Page:
    route: str       # Site-relative directory, including the trailing slash
    title: str
    weight: int
    markdown: str
    file: str        # File relative to the Markdown source directory

    def link(self, target):
        """Return a link relative to the page directory, including the site base."""
        return posixpath.relpath(target or '.', self.route or '.').rstrip('/') + '/'


def read_pages(directory):
    pages = {}
    for file in sorted(directory.rglob('*.md')):
        raw = file.read_text()
        parts = re.split(r'^---\s*$', raw, maxsplit=2, flags=re.M)
        file_name = file.relative_to(directory)
        path = file_name.with_suffix('')
        if path.name == '_index':
            path = path.parent
        route = '' if str(path) == '.' else path.as_posix() + '/'
        weight = DATA['weights'].get(route, 0)
        if len(parts) == 3 and not parts[0].strip():
            title = re.search(r'^title:\s*(.+?)\s*$', parts[1], re.M)[1].strip("'\x22")
            markdown = parts[2]
        else:
            first = re.match(r'^# (.+?)\n', raw)
            if not first:
                raise ValueError(f'{file}: missing page title')
            title, markdown = first[1], raw[first.end():]
        pages[route] = Page(route, title, weight, markdown, file_name.as_posix())
    missing = DATA['headings'].keys() - pages.keys()
    if missing:
        raise ValueError('Missing translated routes: ' + ', '.join(sorted(missing)))
    return pages


def children_of(route, pages):
    return sorted((p for p in pages.values() if p.route != route and p.route.startswith(route)
                   and '/' not in p.route[len(route):].strip('/')), key=lambda p: (p.weight, p.title))


def link_to(current, dest):
    mark = ' aria-current="page"' if current.route == dest.route else ''
    return f'<a href="{escape(current.link(dest.route))}"{mark}>{escape(dest.title)}</a>'


def navigation(current, route, pages):
    items = []
    for page in children_of(route, pages):
        link = link_to(current, page)
        descendants = navigation(current, page.route, pages)
        if descendants:
            opened = ' open' if current.route.startswith(page.route) else ''
            link = f'<details{opened}><summary>{link}</summary>{descendants}</details>'
        items.append('<li>' + link + '</li>')
    return '<ul>' + ''.join(items) + '</ul>' if items else ''


def preprocess(page, pages):
    def shortcode(m):
        tag, attrs = m.group(1,2)
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', attrs))
        if tag == 'subpage_list':
            return '\n\n' + '\n'.join('- ' + link_to(page, p) for p in children_of(page.route, pages)) + '\n\n'
        if tag == 'link_list':
            return '\n\n**官方历史版本（英文）**\n\n' + '\n'.join(f'- [v{v}]({UPSTREAM}{v}/)' for v in DATA['versions']) + '\n\n'
        if tag in ('tab', 'details'):
            label = attrs.get('name', attrs.get('title', '详情'))
            label = escape(LABELS.get(label, label))
            if tag == 'details':
                opened = '' if attrs.get('closed') == 'true' else ' open'
                return f'\n\n<details class="example"{opened}><summary>{label}</summary>\n\n'
            return f'\n\n<section class="tab-panel" data-tab="{label}"><strong class="tab-label">{label}</strong>\n\n'
        if tag in ('tabs', 'steps'):
            return f'\n\n<div class="{tag}">\n\n'
        ending = {'/tabs':'div', '/steps':'div', '/details':'details', '/tab':'section'}.get(tag)
        if ending:
            return f'\n\n</{ending}>\n\n'
        raise ValueError(f'{page.route}: unknown shortcode {tag}')

    # Restrict transformations to prose. Leave fenced examples byte-for-byte intact.
    chunks = []
    prose = []
    fence = None
    def flush():
        s = SHORT.sub(shortcode, ''.join(prose))
        # Native Markdown carries upstream aliases. The HTML headings receive the same IDs below.
        s = re.sub(r'^<a id="[^"]+"></a>\s*\n(?=#{1,6} )', '', s, flags=re.M)
        s = re.sub(r'(\]\([^\s)]+)[ \t]+\)', r'\1)', s)
        # Goldmark allows pipe tables to follow a paragraph without a blank line.
        s = re.sub(r'(?<=[^\n])\n(?=\|[^\n]*\n\|[ :|-]+\|[ \t]*$)', '\n\n', s, flags=re.M)
        s = re.sub(r'^\\\[\s*$|^\\\]\s*$', '$$', s, flags=re.M)
        s = re.sub(r'\\\((.+?)\\\)', lambda m: '$' + m[1] + '$', s)
        chunks.append(s)
        prose.clear()
    for line in page.markdown.splitlines(keepends=True):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence:
            chunks.append(line)
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*', line):
                fence = None
        elif marker:
            flush()
            chunks.append(line)
            fence = marker[1]
        else:
            prose.append(line)
    flush()
    return ''.join(chunks)


def plain(value):
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', value)).split())


def localize_links(value, page, pages):
    def replace(m):
        href = html.unescape(m[1])
        if href.startswith('#'):
            return m[0]
        target = urlsplit(href)
        if not target.scheme and not target.netloc and target.path.endswith('.md'):
            filename = posixpath.normpath(posixpath.join(posixpath.dirname(page.file), unquote(target.path)))
            dest = next((item for item in pages.values() if item.file == filename), None)
            if dest is None:
                raise ValueError(f'{page.file}: unknown Markdown target {href}')
            suffix = ('?' + target.query if target.query else '') + ('#' + target.fragment if target.fragment else '')
            return 'href="' + escape(page.link(dest.route) + suffix) + '"'
        url = urlsplit(urljoin(UPSTREAM + page.route, href))
        if url.netloc not in ('wiki.hypr.land', 'wiki.hyprland.org') or url.scheme not in ('http','https'):
            return m[0]
        route = unquote(url.path).strip('/')
        if route:
            route += '/'
        if route not in pages:
            return m[0]
        out = page.link(route) + ('?' + url.query if url.query else '') + ('#' + url.fragment if url.fragment else '')
        return 'href="' + escape(out) + '"'
    return re.sub(r'href="([^"]*)"', replace, value)


def render(page, pages, output):
    markdown = preprocess(page, pages)
    result = subprocess.run(['pandoc', '-f', 'gfm', '-t', 'html5', '--wrap=none',
                             '--mathml', '--preserve-tabs', '--no-highlight'],
                            input=markdown, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(page.route + ': ' + result.stderr)
    body = localize_links(result.stdout, page, pages)
    # Match Hugo's footnote and backlink IDs so existing bookmarked references resolve.
    body = re.sub(r'(id="|href="#)(fn(?:ref)?)(\d+)"', r'\1\2:\3"', body)
    for src, translated in ALERTS.items():
        body = body.replace(f'<div class="title">\n<p>{src}</p>', f'<div class="title">\n<p>{translated}</p>')
    headings = []
    official = DATA['headings'].get(page.route, [])
    def heading(m):
        index = len(headings)
        anchor = official[index] if index < len(official) else f'section-{index+1}'
        title = plain(m[2])
        headings.append((anchor, title, int(m[1])))
        return f'<h{m[1]} id="{escape(anchor)}">{m[2]} <a class="permalink" href="#{escape(anchor)}" aria-label="本节链接">#</a></h{m[1]}>'
    body = HEAD.sub(heading, body)
    if len(official) != len(headings):
        raise ValueError(f'{page.route}: expected {len(official)} headings, rendered {len(headings)}')
    root = page.link('')
    home = link_to(page, pages[''])
    nav = navigation(page, '', pages)
    toc = ''.join(f'<a class="level-{level}" href="#{escape(a)}">{escape(t)}</a>' for a,t,level in headings)
    segments = page.route.strip('/').split('/')
    crumbs = ''.join('<span>›</span>' + link_to(page, pages['/'.join(segments[:i])+'/'])
                     for i in range(1, len(segments)))
    contents = f'<h2>本页目录</h2>{toc}<hr>' if toc else ''
    full = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(page.title)} · Hyprland Wiki 中文版</title><link rel="icon" href="{root}assets/hyprland.svg">
<link rel="stylesheet" href="{root}assets/wiki.css"><script defer src="{root}assets/site.js"></script></head>
<body data-root="{root}"><a class="skip" href="#main">跳至正文</a>
<header><div class="bar"><a class="brand" href="{root}"><img src="{root}assets/hyprland.svg" width="28" height="28" alt="">Hyprland Wiki</a>
<nav class="top-links" aria-label="项目链接"><a href="https://hypr.land/">Hyprland 官网</a><a href="https://hypr.land/hall_of_fame">作品展示</a><a href="https://hypr.land/news">新闻</a><a href="{REPOSITORY}">GitHub</a></nav>
<a class="original" href="{UPSTREAM}{page.route}">英文原文</a><button id="menu" type="button" aria-controls="sidebar" aria-expanded="false">目录</button></div></header>
<div class="layout"><aside id="sidebar"><a class="version" href="{page.link('version-selector/')}">文档版本 · 最新 Git</a>
<label class="search">搜索文档<input id="query" type="search" placeholder="标题、参数或关键词"></label>
<nav id="results" aria-label="搜索结果" hidden><p id="result-status" role="status"></p><ul></ul></nav>
<nav id="tree" aria-label="文档导航">{home}{nav}</nav></aside>
<main id="main"><nav class="crumb" aria-label="当前位置">{home}{crumbs}</nav><article><h1>{escape(page.title)}</h1>{body}</article>
<footer><span>Hyprland Wiki · 非官方中文译本</span><span><a href="{root}LICENSE">BSD-3-Clause 许可证</a> · <a href="{UPSTREAM}{page.route}">英文原文</a></span></footer></main>
<aside class="rail">{contents}<label class="theme">外观 <select id="theme"><option value="system">跟随系统</option><option value="light">浅色</option><option value="dark">深色</option></select></label></aside></div></body></html>
"""
    dest = output / page.route
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'index.html').write_text(full)
    return {'path': page.route, 'title': page.title, 'text': plain(body)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'docs')
    parser.add_argument('--output', type=Path, default=ROOT / 'public')
    args = parser.parse_args()
    pages = read_pages(args.source)
    args.output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / 'assets', args.output / 'assets', dirs_exist_ok=True)
    shutil.copy2(ROOT / 'LICENSE', args.output)
    (args.output / '.nojekyll').touch()
    with ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 1)) as pool:
        entries = list(pool.map(lambda page: render(page, pages, args.output), pages.values()))
    (args.output / 'assets/search.json').write_text(json.dumps(entries, ensure_ascii=False, separators=(',', ':')))
    print(f'Built {len(pages)} pages in {args.output}')


if __name__ == '__main__':
    main()

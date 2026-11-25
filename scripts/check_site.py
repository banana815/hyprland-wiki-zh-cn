#!/usr/bin/env python3
"""Check a built Chinese Wiki. Supply upstream rendered pages for a parity audit."""
import argparse
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.media = []
        self.code = []
        self.heading_ids = set()
        self.in_main = self.in_pre = self.in_heading = False
        self.row_count = 0
        self.prose = []
        self.lang = ''
        self.body_links = []
        self.content_depth = 0
        self.translated_article = False
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == 'html':
            self.lang = attr.get('lang', '')
        if tag == 'main':
            self.in_main = True
        if tag == 'div' and self.in_main and (self.content_depth or 'content' in attr.get('class', '').split()):
            self.content_depth += 1
        if tag == 'article' and self.in_main:
            self.translated_article = True
        if (self.content_depth or self.translated_article) and tag == 'a' and attr.get('href'):
            if not self.in_heading:
                self.body_links.append(attr['href'])
        if tag in ('h2', 'h3', 'h4', 'h5', 'h6'):
            self.in_heading = True
        if attr.get('id'):
            self.ids.add(attr['id'])
            if self.in_main and self.in_heading:
                self.heading_ids.add(attr['id'])
        if tag == 'pre' and self.in_main:
            self.code.append([])
            self.in_pre = True
        if self.in_main and tag == 'tr':
            self.row_count += 1
        if self.in_main and tag in ('img', 'source', 'video') and attr.get('src'):
            self.media.append(attr['src'])
        if tag in ('a', 'link', 'script', 'img', 'source', 'video'):
            url = attr.get('href') or attr.get('src')
            if url:
                self.links.append(url)

    def handle_endtag(self, tag):
        if tag == 'article':
            self.translated_article = False
        if tag == 'div' and self.content_depth:
            self.content_depth -= 1
        if tag == 'main':
            self.in_main = False
        if tag == 'pre':
            self.in_pre = False
        if tag in ('h2', 'h3', 'h4', 'h5', 'h6'):
            self.in_heading = False

    def handle_data(self, data):
        if self.in_pre:
            self.code[-1].append(data)
        elif self.content_depth or self.translated_article:
            self.prose.append(data)

    def examples(self):
        # Syntax highlighters differ in whether they append a final newline.
        return [''.join(parts).rstrip('\n') for parts in self.code]


def routes(content):
    for md in content.rglob('*.md'):
        page = md.relative_to(content).with_suffix('')
        if page.name == '_index':
            page = page.parent
        yield '/' if page == Path('.') else f'/{page.as_posix()}/'


def equivalent_examples(original, translated, comments):
    if len(original) != len(translated):
        return False
    for before, after in zip(original, translated):
        if before == after:
            continue
        before_lines, after_lines = before.splitlines(), after.splitlines()
        if len(before_lines) != len(after_lines):
            return False
        for old, new in zip(before_lines, after_lines):
            if old == new:
                continue
            match = re.search(r'(?:^|\s)(?:#|//|--)\s+([A-Za-z].*?)\s*$', old)
            if not match or match[1] not in comments:
                return False
            if old[:match.start(1)] + comments[match[1]] + old[match.end(1):] != new:
                return False
    return True


def link_identity(url):
    target = urlsplit(url)
    path = unquote(target.path)
    if target.hostname == 'wiki.hypr.land':
        path = path.rstrip('/') + '/'
    return urlunsplit((target.scheme, target.netloc, path, target.query, unquote(target.fragment)))


def check(args):
    pages = {}
    errors = set()
    local_host = 'wiki.test'
    base = f'https://{local_host}/' + args.base_path.strip('/')
    base = base.rstrip('/') + '/'
    base_path = urlsplit(base).path

    comments = json.loads(args.comments.read_text()) if args.comments else {}
    requested = sorted(routes(args.content))
    if not requested:
        raise SystemExit(f'没有找到 Markdown 源文件：{args.content}')
    for route in requested:
        file = args.site / route.strip('/') / 'index.html'
        if not file.is_file():
            errors.add(f'{route} 缺少页面')
            continue
        page = pages[route] = Page(file)
        if not page.lang.lower().startswith('zh'):
            errors.add(f'{route} 缺少中文 lang 标记')
        body = ''.join(page.prose)
        if not re.search(r'[\u3400-\u9fff]', body):
            errors.add(f'{route} 正文无中文')
        if re.search(r'{{[<%]\s*/?(?:tab|tabs|steps|details|link_list|subpage_list)\b', body):
            errors.add(f'{route} 短代码未展开')

        if args.reference:
            name = route.strip('/').replace('/', '+') + '.html'
            capture = args.reference / name
            if not capture.is_file():
                errors.add(f'{route} 缺少上游 HTML 快照')
                continue
            original = Page(capture)
            upstream_base = 'https://wiki.hypr.land' + route
            # Relative destinations resolve the same way on the deployed copy and upstream.
            old_links = {link_identity(urljoin(upstream_base, href)) for href in original.body_links}
            new_links = {link_identity(urljoin(upstream_base, href)) for href in page.body_links}
            for missing in old_links - new_links:
                errors.add(f'{route} 缺少正文链接 {missing}')
            for anchor in original.heading_ids - page.ids:
                errors.add(f'{route} 缺少上游标题锚点 #{anchor}')
            if not equivalent_examples(original.examples(), page.examples(), comments):
                errors.add(f'{route} 代码示例与上游渲染结果不同')
            if page.row_count != original.row_count:
                errors.add(f'{route} 表格行数与上游不同 ({page.row_count}/{original.row_count})')
            missing = Counter(original.media) - Counter(page.media)
            for url in missing:
                errors.add(f'{route} 缺少上游媒体 {url}')

    # Resolve links as if the site were hosted under its production project prefix.
    cache = {}
    for route, page in pages.items():
        for raw in page.links:
            dest = urlsplit(urljoin(base + route.lstrip('/'), raw))
            if dest.hostname != local_host:
                continue
            path = unquote(dest.path)
            if not path.startswith(base_path):
                errors.add(f'{route} 链接跳出部署目录 {raw}')
                continue
            path = path[len(base_path):]
            file = args.site / path
            if file.is_dir():
                file = file / 'index.html'
            if not file.is_file():
                errors.add(f'{route} 本地目标不存在 {raw}')
                continue
            if dest.fragment and file.suffix == '.html':
                target = '/' + file.relative_to(args.site).as_posix().removesuffix('index.html')
                if target in pages:
                    ids = pages[target].ids
                else:
                    if file not in cache:
                        cache[file] = Page(file).ids
                    ids = cache[file]
                if unquote(dest.fragment) not in ids:
                    errors.add(f'{route} 本地锚点不存在 {raw}')
    for error in sorted(errors):
        print(error, file=sys.stderr)
    print(f'{len(pages)} 页，{sum(len(p.code) for p in pages.values())} 个代码块，'
          f'{sum(p.row_count for p in pages.values())} 行表格，{len(errors)} 个问题')
    return bool(errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('site', type=Path, help='构建后的静态站点目录')
    parser.add_argument('--content', type=Path, default=Path(__file__).resolve().parents[1] / 'docs',
                        help='以原始相对路径组织的 Markdown 目录')
    parser.add_argument('--base-path', default='/hyprland-wiki-zh-cn/')
    parser.add_argument('--comments', type=Path, help='经校对的代码注释对照 JSON，键为原文，值为译文')
    parser.add_argument('--reference', type=Path,
                        help='可选的上游 HTML 快照目录，文件名用 + 代替路径分隔符，首页为 .html')
    sys.exit(check(parser.parse_args()))

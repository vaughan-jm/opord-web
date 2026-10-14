#!/usr/bin/env python3
"""Build opord.co: render src/pages/*.html through src/layout.html into the repo root.

    python3 build.py          # build every page, sitemap.xml and robots.txt, then check them

Edit content in src/pages/, shared settings (email, phone, address…) in src/site.json, styles in
assets/site.css. Cloudflare Pages serves the repo root as-is, so commit the generated .html files too.

Template syntax (deliberately tiny):
    {{key}} / {{a.b}}               value from site.json or the page (HTML-escaped)
    {{#if key}}…{{else}}…{{/if}}    shown only when key is set (non-empty)
    {{> name}}                      include src/partials/name.html
    <!--meta {...json...} -->       first line of a page: path, title, description, nav, noindex…
"""
import datetime, hashlib, html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent.resolve()
SRC = ROOT / 'src'
RAW = {'addressHtml', 'page.body', 'page.head', 'nav.how', 'nav.faq', 'nav.security', 'nav.about', 'nav.contact'}
NAV_KEYS = ['how', 'faq', 'security', 'about', 'contact']


def get(ctx, path):
    cur = ctx
    for part in path.split('.'):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def truthy(v):
    return bool(v) and v != [] and v != {}


def render(text, ctx, depth=0):
    if depth > 5:
        raise RuntimeError('partials nested too deeply')
    text = re.sub(r'\{\{>\s*([\w-]+)\s*\}\}', lambda m: render((SRC / 'partials' / (m.group(1) + '.html')).read_text(), ctx, depth + 1), text)
    pat = re.compile(r'\{\{#if ([\w.]+)\}\}((?:(?!\{\{#if ).)*?)\{\{/if\}\}', re.S)
    while True:
        m = pat.search(text)
        if not m:
            break
        body = m.group(2)
        yes, _, no = body.partition('{{else}}')
        text = text[:m.start()] + (yes if truthy(get(ctx, m.group(1))) else no) + text[m.end():]

    def val(m):
        key = m.group(1)
        v = get(ctx, key)
        if v is None:
            raise KeyError(f'unknown template key: {key}')
        v = str(v)
        return v if key in RAW else html.escape(v, quote=True)
    return re.sub(r'\{\{([\w.]+)\}\}', val, text)


def asset_hash(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()[:10]


def out_name(path):
    return 'index.html' if path == '/' else path.strip('/') + '.html'


def build():
    site = json.loads((SRC / 'site.json').read_text())
    site['year'] = str(datetime.date.today().year)
    site['addressHtml'] = '<br>'.join(html.escape(l) for l in site.get('address') or [])
    site['asset'] = {'css': asset_hash('assets/site.css'), 'js': asset_hash('assets/site.js')}
    layout = (SRC / 'layout.html').read_text()
    pages, built = [], {}
    for f in sorted((SRC / 'pages').glob('*.html')):
        raw = f.read_text()
        m = re.match(r'\s*<!--meta (\{.*?\}) -->\s*', raw, re.S)
        if not m:
            raise SystemExit(f'{f.name}: missing <!--meta {{...}} --> header')
        meta = json.loads(m.group(1))
        body = raw[m.end():]
        path = meta['path']
        full = meta['title'] if meta.get('titleFull') else f"{meta['title']} — {site['brand']}"
        canonical = '' if meta.get('nocanonical') else site['domain'].rstrip('/') + ('/' if path == '/' else path)
        head = ''
        if meta.get('jsonld'):
            org = {
                '@context': 'https://schema.org', '@type': 'Organization',
                'name': site['brand'], 'legalName': site['legalName'], 'url': site['domain'].rstrip('/') + '/',
                'logo': site['domain'].rstrip('/') + '/apple-touch-icon.png', 'description': site['tagline'] + '.',
                'founder': {'@type': 'Person', 'name': site['founder']['name']},
            }
            if site.get('email'):
                org['email'] = site['email']
            if site.get('phone'):
                org['telephone'] = site['phone']
            head += '<script type="application/ld+json">' + json.dumps(org, ensure_ascii=False) + '</script>\n'
        ctx = dict(site)
        ctx['nav'] = {k: (' aria-current="page"' if meta.get('nav') == k else '') for k in NAV_KEYS}
        page = {'fullTitle': full, 'ogTitle': full, 'description': meta['description'], 'canonical': canonical,
                'robots': 'noindex' if meta.get('noindex') else 'index, follow', 'head': head}
        ctx['page'] = page
        page['body'] = render(body, ctx).strip('\n')
        out = render(layout, ctx)
        if '{{' in out or '}}' in out:
            raise SystemExit(f'{f.name}: unrendered template markers remain')
        name = out_name(path)
        (ROOT / name).write_text(out)
        built[path] = out
        pages.append((path, meta))
        print(f'  {name:18s} {len(out.encode()):7d} bytes  {full}')

    today = datetime.date.today().isoformat()
    urls = [p for p, meta in pages if not meta.get('noindex')]
    order = ['/', '/about', '/contact', '/security', '/sms', '/privacy', '/terms']
    urls.sort(key=lambda p: order.index(p) if p in order else 99)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in urls:
        sm.append(f"  <url><loc>{site['domain'].rstrip('/')}{'/' if p == '/' else p}</loc><lastmod>{today}</lastmod></url>")
    sm.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(sm) + '\n')
    (ROOT / 'robots.txt').write_text(f"User-agent: *\nAllow: /\n\nSitemap: {site['domain'].rstrip('/')}/sitemap.xml\n")
    check(built)


def check(built):
    """Every internal link must point at a page that exists, and every #fragment at an id on that page."""
    ids = {p: set(re.findall(r'\sid="([^"]+)"', h)) for p, h in built.items()}
    files = {p.strip('/') for p in ['assets', 'media']}
    bad = []
    for p, h in built.items():
        for href in re.findall(r'\shref="([^"]+)"', h):
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                continue
            target, _, frag = href.partition('#')
            if target == '':
                target = p
            if target.startswith('/assets/') or target.startswith('/media/') or target in ('/favicon.svg', '/favicon.ico', '/apple-touch-icon.png'):
                fp = ROOT / target.lstrip('/').split('?')[0]
                if not fp.exists():
                    bad.append(f'{p}: missing file {href}')
                continue
            if target not in built:
                bad.append(f'{p}: link to missing page {href}')
                continue
            if frag and frag not in ids[target]:
                bad.append(f'{p}: missing anchor {href}')
        for src in re.findall(r'\s(?:src|poster)="([^"]+)"', h) + [s.split()[0] for ss in re.findall(r'\ssrcset="([^"]+)"', h) for s in ss.split(',')]:
            if src.startswith('/'):
                fp = ROOT / src.lstrip('/').split('?')[0]
                if not fp.exists():
                    bad.append(f'{p}: missing file {src}')
        dup = [i for i in ids[p] if len(re.findall(r'\sid="' + re.escape(i) + '"', h)) > 1]
        if dup:
            bad.append(f'{p}: duplicate ids {dup}')
        if len(re.findall(r'<h1[\s>]', h)) != 1:
            bad.append(f'{p}: needs exactly one <h1>')
    if bad:
        print('\n'.join('  ✗ ' + b for b in bad))
        raise SystemExit(1)
    print(f'  ✓ links, anchors, files and headings check out across {len(built)} pages')


if __name__ == '__main__':
    build()

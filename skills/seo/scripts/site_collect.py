#!/usr/bin/env python3
"""site_collect.py — ONE polite pass over a site, capturing everything downstream needs.

Why this exists
---------------
Written after an audit burned ~20 minutes of wall-clock on avoidable mistakes:
a spoofed Googlebot UA plus a burst of un-paced requests tripped the host's rate
limiter, a 10-minute crawl produced zero output because progress was never
flushed to disk, and the same 56 pages were then fetched a SECOND time because
the first pass captured head tags but not body text.

This script exists so the correct behaviour is the path of least resistance:

  * ONE request per URL, capturing head tags AND body text AND hashes AND image
    alt stats AND JSON-LD AND placeholder markers. Never crawl a site twice.
  * Probes the host with a single request and auto-paces before any bulk loop.
  * Real browser UA by default. Never spoof Googlebot for bulk fetching — hosts
    treat unverified Googlebot UAs with extra suspicion (Wix returns 429).
  * Writes incrementally, so a timeout or Ctrl-C keeps everything collected so far.
  * --resume skips URLs already in the output file.

Usage
-----
    export PYTHONIOENCODING=utf-8            # Windows: emoji/encoding safety

    # from a sitemap (discovers and expands sitemap indexes)
    python site_collect.py --site https://example.com --out evidence.json

    # from an explicit URL list
    python site_collect.py --url-file urls.txt --out evidence.json

    # resume an interrupted run
    python site_collect.py --url-file urls.txt --out evidence.json --resume

    # crawler-access spot check (few URLs, several UAs) - NOT for bulk crawling
    python site_collect.py --url-file top5.txt --out ua.json --ua-matrix

Output: a JSON list, one object per URL. Feed it to analysis agents/scripts —
they should read THIS FILE, not re-fetch the site.
"""

import argparse, hashlib, json, os, re, sys, time
from urllib.parse import urljoin, urlparse

try:
    import requests
except ImportError:
    sys.exit("pip install requests beautifulsoup4 lxml")

BROWSER_UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36')

# Only for --ua-matrix spot checks on a handful of URLs. Never for bulk crawling.
CRAWLER_UAS = {
    'googlebot': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'bingbot': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'gptbot': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.2; +https://openai.com/gptbot',
    'claudebot': 'Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)',
    'perplexitybot': 'Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)',
    'oai-searchbot': 'Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)',
}

# Unedited site-builder boilerplate. Presence on a live page is a real finding.
PLACEHOLDER_MARKERS = [
    "I'm a paragraph", "I&#39;m a paragraph", "Click here to add your own text",
    "This is a great space to write", "add your own image by double clicking",
    "I'm a title", "I&#39;m a title", "Lorem ipsum",
    "double click me and you can start adding your own content",
    "I'm a product description", "Tell your visitors the story",
    "Your content goes here", "Add a Title", "Describe your image",
]


def strip_tags(html):
    html = re.sub(r'<(script|style|noscript|template)[^>]*>.*?</\1>', ' ', html, flags=re.I | re.S)
    html = re.sub(r'<!--.*?-->', ' ', html, flags=re.S)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = html.replace('&nbsp;', ' ')
    return re.sub(r'\s+', ' ', html).strip()


def dechrome(text):
    """Drop shared nav/footer so duplicate detection compares real page content."""
    t = re.sub(r'^.*?Use tab to navigate through the menu items\.\s*(Log In)?', '', text, flags=re.S)
    t = re.sub(r'(TERMS\s*&(amp;)?\s*CONDITIONS|Do Not Sell My Personal Information).*$', '', t, flags=re.S | re.I)
    return t.strip()


def all_matches(html, pattern):
    return re.findall(pattern, html, re.I | re.S)


def extract(url, resp):
    """Everything a downstream analyst could need, from one response."""
    html = resp.text

    # Count ALL occurrences, never just the first — duplicate head tags are
    # themselves a finding, and querySelector()-style 'first match' hides them.
    titles = all_matches(html, r'<title[^>]*>(.*?)</title>')
    descs = all_matches(html, r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']')
    canons = all_matches(html, r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)')
    robots = all_matches(html, r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)')
    og = dict(re.findall(r'<meta[^>]+property=["\'](og:[^"\']+)["\'][^>]+content=["\'](.*?)["\']',
                         html, re.I | re.S))
    hreflang = all_matches(html, r'<link[^>]+hreflang=["\']([^"\']+)')

    headings = {}
    for lvl in range(1, 7):
        hs = [strip_tags(x) for x in all_matches(html, r'<h%d[^>]*>(.*?)</h%d>' % (lvl, lvl))]
        headings['h%d' % lvl] = [h for h in hs if h]

    imgs = re.findall(r'<img\b[^>]*>', html, re.I)
    no_alt = [i for i in imgs if not re.search(r'\balt\s*=', i, re.I)]
    empty_alt = [i for i in imgs if re.search(r'\balt\s*=\s*["\']\s*["\']', i, re.I)]
    filename_alt = [i for i in imgs
                    if re.search(r'\balt\s*=\s*["\'][^"\']*\.(jpg|jpeg|png|webp|gif|svg)["\']', i, re.I)]

    # JSON-LD: parse it. A string match on a type name false-positives on
    # framework config blobs (see _process/schema-grep-false-positives.md).
    ld_raw = all_matches(html, r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>')
    ld_types, ld_parsed, ld_errors = [], [], 0
    for block in ld_raw:
        try:
            data = json.loads(block.strip())
        except Exception:
            ld_errors += 1
            continue
        ld_parsed.append(data)

        def walk(o):
            if isinstance(o, dict):
                t = o.get('@type')
                if t:
                    ld_types.extend(t if isinstance(t, list) else [t])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(data)

    body = strip_tags(html)
    main = dechrome(body)
    host = urlparse(url).netloc
    internal = set()
    for href in re.findall(r'<a[^>]+href=["\']([^"\'#]+)', html, re.I):
        absu = urljoin(url, href)
        if urlparse(absu).netloc == host:
            internal.add(urlparse(absu).path or '/')

    ph = {m: html.count(m) for m in PLACEHOLDER_MARKERS if m in html}

    return {
        'url': url,
        'final_url': resp.url,
        'status': resp.status_code,
        'redirected': resp.url.rstrip('/') != url.rstrip('/'),
        'headers': {k.lower(): v for k, v in resp.headers.items()
                    if k.lower() in ('content-type', 'content-encoding', 'cache-control',
                                     'x-robots-tag', 'strict-transport-security', 'server',
                                     'x-cache', 'content-language')},
        'html_bytes': len(html),
        'wire_bytes': len(resp.content),

        'title': titles[0].strip() if titles else None,
        'title_count': len(titles),
        'title_len': len(titles[0].strip()) if titles else 0,
        'all_titles': [t.strip() for t in titles] if len(titles) > 1 else None,

        'description': descs[0].strip() if descs else None,
        'description_count': len(descs),
        'description_len': len(descs[0].strip()) if descs else 0,

        'canonical': canons[0] if canons else None,
        'canonical_count': len(canons),
        'all_canonicals': canons if len(canons) > 1 else None,
        'canonical_is_self': bool(canons) and canons[0].rstrip('/') == url.rstrip('/'),

        'robots_meta': robots,
        'robots_meta_count': len(robots),
        'og': og,
        'hreflang': hreflang,

        'headings': headings,
        'h1_count': len(headings['h1']),
        'heading_total': sum(len(v) for v in headings.values()),

        'img_count': len(imgs),
        'img_no_alt': len(no_alt),
        'img_empty_alt': len(empty_alt),
        'img_filename_alt': len(filename_alt),

        'jsonld_blocks': len(ld_raw),
        'jsonld_types': sorted(set(ld_types)),
        'jsonld_parse_errors': ld_errors,
        'jsonld': ld_parsed,

        'word_count': len(body.split()),
        'main_word_count': len(main.split()),
        'main_hash': hashlib.md5(main.encode('utf-8', 'replace')).hexdigest()[:12],
        'body_sample': body[:400],

        'internal_link_count': len(internal),
        'internal_paths': sorted(internal)[:400],

        'placeholder_hits': ph,
        'placeholder_total': sum(ph.values()),
        'double_encoded_entities': len(re.findall(r'&amp;(amp|quot|#39|mdash|lt|gt);', html)),
    }


def undecodable(resp):
    """Detect a response we received but cannot actually read.

    Guard against a silent-failure class that produced completely fabricated
    numbers on first run: advertising `Accept-Encoding: br` without the `brotli`
    package installed. The server compresses with brotli, requests cannot decode
    it, and `.text` returns binary noise. Every regex then matches nothing, so the
    output looks like "0 H1s, 0 JSON-LD blocks, 3432 words" — plausible, wrong,
    and silent. Word count was counting binary garbage split on whitespace.

    NEVER let this fail quietly. A crawl that cannot read the page must say so.
    """
    if resp is None or resp.status_code != 200:
        return None
    ctype = resp.headers.get('content-type', '')
    if 'html' not in ctype.lower():
        return None
    head = resp.text[:3000].lower()
    if '<html' in head or '<!doctype' in head or '<body' in head or '<head' in head:
        return None
    enc = resp.headers.get('content-encoding', '(none)')
    return ('HTML response is not decodable (content-encoding: %s). '
            'If "br", install brotli:  python -m pip install brotli' % enc)


class Collector:
    def __init__(self, ua=BROWSER_UA, delay=4.0, timeout=45):
        self.s = requests.Session()
        # Deliberately do NOT set Accept-Encoding. urllib3 advertises only the
        # encodings it can actually decode; overriding it invites the silent
        # brotli failure described in undecodable().
        self.s.headers.update({'User-Agent': ua, 'Accept-Language': 'en-US,en;q=0.9',
                               'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8'})
        self.delay, self.timeout = delay, timeout

    def get(self, url, tries=4):
        for i in range(tries):
            try:
                r = self.s.get(url, timeout=self.timeout, allow_redirects=True)
                if r.status_code == 429:
                    back = 30 * (i + 1)
                    print('    429 - backing off %ds and slowing to %.1fs' % (back, self.delay + 2),
                          flush=True)
                    self.delay += 2          # permanently slow down; don't re-trip it
                    time.sleep(back)
                    continue
                return r
            except Exception as e:
                print('    error (%s) retry %d' % (str(e)[:70], i + 1), flush=True)
                time.sleep(6 * (i + 1))
        return None

    def probe(self, url):
        """ONE request before any bulk loop, to calibrate pacing."""
        print('probing %s ...' % url, flush=True)
        t0 = time.time()
        r = self.get(url)
        if r is None:
            sys.exit('probe failed - host unreachable or hard-blocking. Do not start a bulk crawl.')
        elapsed = time.time() - t0
        bad = undecodable(r)
        if bad:
            sys.exit('probe FAILED: %s\nAborting before the bulk crawl - a crawl that '
                     'cannot read pages would emit fabricated zeros.' % bad)
        # Pace off observed latency, floor 3s. Cheap insurance against a throttler.
        self.delay = max(3.0, min(8.0, round(elapsed * 2, 1)), self.delay)
        print('  status %s in %.1fs, decodable -> pacing %.1fs between requests'
              % (r.status_code, elapsed, self.delay), flush=True)
        return r


def discover_urls(c, site):
    """Expand robots.txt sitemap + sitemap indexes into a flat URL list."""
    base = site.rstrip('/')
    found, seen = [], set()
    candidates = []
    r = c.get(base + '/robots.txt')
    if r is not None and r.status_code == 200:
        candidates += re.findall(r'(?im)^\s*sitemap:\s*(\S+)', r.text)
    candidates.append(base + '/sitemap.xml')
    queue, done = list(dict.fromkeys(candidates)), set()
    while queue:
        sm = queue.pop(0)
        if sm in done:
            continue
        done.add(sm)
        time.sleep(c.delay)
        r = c.get(sm)
        if r is None or r.status_code != 200:
            print('  sitemap %s -> %s (skipped)' % (sm, r.status_code if r else 'ERR'), flush=True)
            continue
        locs = re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', r.text)
        if '<sitemapindex' in r.text:
            print('  index %s -> %d child sitemaps' % (sm, len(locs)), flush=True)
            queue += locs
        else:
            new = [u for u in locs if u not in seen]
            seen.update(new)
            found += new
            print('  %s -> %d urls' % (sm, len(locs)), flush=True)
    return found


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument('--site', help='Origin; discovers URLs from robots.txt + sitemaps')
    src.add_argument('--url-file', help='File with one URL per line')
    p.add_argument('--out', required=True, help='Output JSON path')
    p.add_argument('--delay', type=float, default=4.0, help='Seconds between requests (default 4)')
    p.add_argument('--timeout', type=int, default=45)
    p.add_argument('--limit', type=int, help='Cap number of URLs')
    p.add_argument('--resume', action='store_true', help='Skip URLs already present in --out')
    p.add_argument('--ua-matrix', action='store_true',
                   help='Spot-check crawler UAs on the given URLs (use on <=5 URLs, not bulk)')
    a = p.parse_args()

    c = Collector(delay=a.delay, timeout=a.timeout)

    if a.site:
        c.probe(a.site)
        urls = discover_urls(c, a.site)
    else:
        urls = [l.strip() for l in open(a.url_file, encoding='utf-8') if l.strip()]
        c.probe(urls[0])

    if a.limit:
        urls = urls[:a.limit]

    if a.ua_matrix:
        # Deliberately serial and paced. Comparing CONTENT across UAs, not just status:
        # a different byte count with identical content is not a finding.
        out = []
        for u in urls[:5]:
            for name, ua in CRAWLER_UAS.items():
                c.s.headers['User-Agent'] = ua
                r = c.get(u)
                rec = {'url': u, 'ua': name, 'status': r.status_code if r else None}
                if r is not None and r.status_code == 200:
                    e = extract(u, r)
                    rec.update({'wire_bytes': e['wire_bytes'], 'word_count': e['word_count'],
                                'title': e['title'], 'h1_count': e['h1_count'],
                                'main_hash': e['main_hash']})
                out.append(rec)
                print('  %-14s %-4s %s' % (name, rec['status'], u), flush=True)
                time.sleep(c.delay)
            c.s.headers['User-Agent'] = BROWSER_UA
        json.dump(out, open(a.out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        print('\nWROTE %s' % a.out)
        print('Compare main_hash/word_count across UAs. Identical content + different '
              'byte count = client JS only, NOT cloaking.')
        return

    results, done = [], set()
    if a.resume and os.path.exists(a.out):
        results = json.load(open(a.out, encoding='utf-8'))
        done = {r['url'] for r in results}
        print('resuming: %d already collected' % len(done), flush=True)

    todo = [u for u in urls if u not in done]
    print('\ncollecting %d urls at %.1fs pacing (~%.1f min)\n'
          % (len(todo), c.delay, len(todo) * c.delay / 60), flush=True)

    for i, u in enumerate(todo):
        r = c.get(u)
        bad = undecodable(r)
        if bad:
            # Loud, not silent. Record the failure instead of fabricating zeros.
            rec = {'url': u, 'status': r.status_code, 'error': bad, 'UNREADABLE': True}
        elif r is not None:
            rec = extract(u, r)
        else:
            rec = {'url': u, 'status': 0, 'error': 'unreachable'}
        results.append(rec)
        flags = []
        if rec.get('UNREADABLE'):
            flags.append('!! UNREADABLE - DO NOT USE')
        if rec.get('placeholder_total'):
            flags.append('PLACEHOLDER')
        if rec.get('h1_count') == 0:
            flags.append('no-h1')
        if not rec.get('description'):
            flags.append('no-desc')
        if rec.get('canonical_count', 0) > 1:
            flags.append('DUP-CANONICAL')
        print('[%d/%d] %s w=%s ld=%s %s %s'
              % (i + 1, len(todo), rec.get('status'), rec.get('word_count'),
                 rec.get('jsonld_blocks'), u, ' '.join(flags)), flush=True)
        # Flush every iteration: a timeout must never discard collected work.
        json.dump(results, open(a.out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        time.sleep(c.delay)

    print('\nWROTE %s (%d records)' % (a.out, len(results)))
    print('Downstream analysis should READ THIS FILE, not re-fetch the site.')


if __name__ == '__main__':
    main()

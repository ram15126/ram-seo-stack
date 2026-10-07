# Client-rendered SPAs: why "HTTP 200" and "0 words" both lie

Client-side-rendered single-page apps break two whole families of audit check at
once. Both failure modes produce confident, quotable, wrong output. This has now
happened on more than one site in this workspace.

---

## Failure mode 1 — every path returns 200, so existence checks are meaningless

An SPA hosted on a static host with a catch-all rewrite serves the same HTML
shell for **every** path. `/llms.txt`, `/sitemap_index.xml`, `/does-not-exist`,
`/asdfasdf` — all HTTP 200, all the same bytes.

Any check shaped *"I requested it and got 200, therefore it exists"* returns a
false positive. Observed hits:

- `llms_txt_checker.py` → `exists: true`, `full_exists: true`
- `ai_crawler_policy_matrix.py` → `llms_txt_available: true`,
  `alignment: "documented"` (inherits the above)
- `sitemap_checker.py` → reports `sitemap_index.xml` and `sitemap-index.xml` as
  present-but-invalid, when they simply do not exist

**The tell:** identical `content-length` across unrelated paths, and
`content-type: text/html` on something that should be `text/plain` or
`application/xml`.

**How to check properly:**

```bash
curl -sS -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" \
  "https://site.com/llms.txt" "https://site.com/definitely-not-a-real-path-xyz"
```

Identical size and type on both → the site returns a shell for everything, and
**no 200 on that host proves a file exists.** Confirm from the body, not the status.

This is also a real finding in its own right — it means the site soft-404s, so
every mistyped or hallucinated URL is an indexable page. Report it as such.

---

## Failure mode 2 — raw-HTML scripts see an empty page

Anything parsing the raw response on a CSR site measures the shell, not the
page. Observed output on a site whose rendered pages were fine:

| Script | Reported | Actual (rendered) |
|---|---|---|
| `internal_links.py` | 0 links, 0 pages found | 39 internal links on the homepage |
| `a11y_seo_checker.py` | 0 H1s, no `<main>` | 1 H1, `<main>` present |
| `duplicate_content.py` | thin content, 0 words, **Critical** | 583 words |
| `image_inventory.py` | 0 images | images present |
| `broken_links.py` | "No links found on page" | 39 links |
| `readability.py --url` | 6 words, "extremely difficult" | 4,203 words |
| `eeat_signal_checker.py` | score 20 | partly real, but not for the stated reason |
| `crawl_audit.py` | all N pages share one title/description, 0 H1s | each page has a unique title and H1 after render |

Do **not** ship any of these to a client without re-measuring.

**The tell:** `crawl_audit.py` reporting that every URL has an identical title
*and* identical meta description *and* zero H1s. That combination is not a site
with duplicate-content problems — it is a site that has not rendered.

---

## What to do instead

1. **Detect CSR first, before running the content suite.** One request:
   if the raw HTML has no `<h1>` and no `<a href>` but the site clearly has
   pages, everything downstream needs rendering.
2. **Render once, extract everything.** A single Playwright pass over the URL
   list that dumps title, description, canonical, `og:*`, headings, links,
   images, JSON-LD, word count and body text per URL is far cheaper than
   running fifteen render-capable scripts, and it gives one consistent
   artefact to audit from.
3. **Use the Googlebot smartphone UA** and `networkidle` plus a short settle.
4. **Scroll before trusting animated content.** Scroll-triggered counters and
   lazy sections render as `0` or empty on load. Check both states — the
   difference is itself a finding, but a "Likely", not a "Confirmed", since
   Googlebot does scroll during rendering.
5. **Keep the raw-HTML result too.** The gap between raw and rendered *is* the
   technical finding: what non-rendering crawlers (most AI crawlers, social
   scrapers, Bing's non-render path) actually receive.

---

## Failure mode 3 — the expensive one: two sets of head tags

This one cost a withdrawn client report, so it goes first in practice even
though it was found last.

An SPA typically ships **two** sets of head tags:

1. **Static defaults** in `index.html` — usually the homepage's title,
   description, canonical and `og:*`. Deliberate: it gives non-JS scrapers a
   sane link preview.
2. **Per-route tags** injected at runtime by React Helmet, Vue Meta, Svelte
   `<svelte:head>` or similar.

Both exist in the DOM simultaneously. The framework-injected ones carry a marker
attribute — `data-rh` (react-helmet-async), `data-react-helmet`, `data-vue-meta`.

**The trap:** `document.querySelector('link[rel=canonical]')` returns the
**first** match — the static default. The correct per-route tag sits directly
beneath it, unread. You then report "every page canonicalises to the homepage"
across the whole site, with consistent evidence, and it is completely wrong.

**Always use `querySelectorAll` and report the count:**

```js
Array.from(document.querySelectorAll('link[rel="canonical"]'))
     .map(e => ({href: e.href, helmet: e.hasAttribute('data-rh')}))
```

Apply the same to `meta[name=description]`, `meta[name=robots]`,
`meta[property^="og:"]` and `meta[name^="twitter:"]`.

**A count above 1 is itself the finding** — and a different, usually smaller one
than "the tag is missing":

- **Duplicate `rel=canonical`:** Google may disregard all of them and pick a
  canonical itself. Real issue, High not Critical. Fix = delete the static one.
- **Duplicate `robots`:** the most restrictive directive wins. A static
  `index, follow` plus an injected `noindex` resolves to `noindex` — which may
  be exactly what the developer intended. Do not report it as broken until you
  know which way it resolves.
- **Duplicate `description` / `og:*`:** cosmetic conflict, Low.

**The meta-lesson, which generalises past SPAs entirely:**

> A finding that appears on **100% of pages** should raise suspicion of the
> method, not confidence in the finding.

Real problems are usually uneven. Perfect consistency across every URL is the
signature of one methodological error repeated N times. Before writing up a
sitewide finding, deliberately try to disprove it by a second, different route —
raw `curl`, browser devtools by hand, Google's Rich Results Test.

---

## A third one, unrelated to SPAs

`cache_compression_checker.py` reported *"Compressible response is not
Brotli/gzip encoded"* on a site where Brotli was active. The check did not send
an `Accept-Encoding` request header, so the server correctly returned an
uncompressed response.

**Always re-test compression explicitly before reporting it:**

```bash
curl -sSI -H "Accept-Encoding: br, gzip" "https://site.com/asset.js" | grep -i content-encoding
```

The *caching* half of that script's output (`max-age`, validators) was accurate
in the same run. A script being wrong about one thing does not make it wrong
about everything — check the specific claim, not the whole tool.

---

## Pre-send checklist for any client-facing deliverable

Run this before a report leaves the workspace. Each item exists because it was
missed at least once.

- [ ] **Tag extraction used `querySelectorAll`, not `querySelector`** — and the
      count is reported
- [ ] **Any 100%-of-pages finding was independently re-tested** by a second method
- [ ] **Every command in the document was actually run** — including paths to
      files referenced in it
- [ ] **Every npm package named was checked for last publish date** — do not
      recommend abandoned packages
- [ ] **Every config snippet was reasoned through end to end** — does the
      `vercel.json` you wrote actually produce the outcome you claim?
- [ ] **Every third-party domain named resolves**
- [ ] **The date on the document is today's date**
- [ ] **Scope claims match scope tested** — "every page" vs "every page tested"
- [ ] **Compressed vs decompressed sizes are labelled** — a 340 KB bundle may be
      123 KB on the wire
- [ ] **`noindex` / `nofollow` were checked before calling a page "missing" from
      a sitemap** — excluding a `noindex` page is correct, not a defect

# Auditing a Wix site: what behaves differently

Client-neutral notes from auditing Wix-hosted sites. Wix breaks several default
assumptions in this workspace — most importantly the assumption that the target
is a code repo you can edit.

## 1. There is no repo. Do not propose code or plugins.

The default posture in `SKILL.md` — "most target sites are code, not WordPress,
so ship the fix yourself" — **does not apply**. Every fix routes through the Wix
Editor, the Wix SEO panel, Wix Stores product fields, or the URL Redirect
Manager. An audit that hands a Wix client a code diff is unusable.

Also: Wix relabels and reorganises its dashboard regularly. Give menu paths as
navigational hints, explicitly caveated, not as exact keystrokes — and never let
the *finding* depend on the menu path being current.

## 2. Wix rate-limits request bursts with HTTP 429

A burst of ~10 fast requests earned sustained `429 Too Many Requests`, and it
persisted long enough to look like a site-level block.

**This nearly produced a false "Googlebot is blocked" finding.** A fetch with a
Googlebot UA returned 429 while a browser UA returned 200, which reads exactly
like UA-based blocking. It was not — it was cumulative rate limiting from the
preceding burst.

**Rules:**
- Space requests **4–8 s apart**. A 56-page crawl takes ~5 minutes; accept it.
- Back off 30–60 s on a 429, and **re-test any access finding after a cooldown**
  before believing it.
- Test crawler access by fetching the *same* path with several UAs, spaced out,
  and compare. Never conclude "blocked" from a single 429.
- **Never spoof Googlebot for bulk fetching** — Wix 429s it while serving a
  browser UA fine. Use a browser UA; reserve crawler UAs for small spot checks.

**And crawl the site only once.** On the audit that produced these notes, all 56
pages were fetched twice because the first pass captured head tags but not body
text — ~5 minutes thrown away. `skills/seo/scripts/site_collect.py` exists to
prevent this: one paced pass captures head tags, headings, body text, content
hash, image alt stats, parsed JSON-LD, placeholder markers and internal links,
flushing to disk every iteration with `--resume` support. Analysis reads that
JSON; it does not re-fetch. Parallel agents must share the one collected artifact
rather than each fetching the origin — see the multi-agent note below.

## 2b. Do not fan out agents against one rate-limited origin

Tempting fix for a slow crawl: N agents crawling in parallel. On a throttled host
this is strictly worse — the rate limit is per-origin, so N concurrent crawlers
trip it N times faster and every one of them ends up in backoff.

The workspace's `references/agents/*.md` role definitions each begin with "use
WebFetch to retrieve the target URL", so running six of them concurrently means
six independent fetch storms against the same host. Collect centrally **first**,
then fan out analysts over the saved artifact where there is no network
contention at all.

## 3. Bot and browser get different byte counts — usually not a finding

Wix serves known crawler UAs a smaller response than browsers (observed
201 KB vs 383 KB on the same URL). This looks like cloaking. Check before
reporting it:

```bash
curl -s --compressed -A "$BOT_UA"     "$URL" -o bot.html
curl -s --compressed -A "$BROWSER_UA" "$URL" -o browser.html
# compare CONTENT, not size
```

On the site observed, both had identical title, canonical, word count (1,505),
H2 count (18), image count (213) and product-link count (105). The delta was
client-side JS only. **Content parity = not a finding.** Report it only if the
extracted content actually differs.

## 4. Wix is SSR — raw-HTML scripts work fine

Unlike the CSR SPAs in `spa-soft-200-false-positives.md`, Wix server-renders.
Raw `curl` + regex/BeautifulSoup gives accurate titles, headings, word counts and
JSON-LD. Rendering is not required for most checks, which makes a Wix audit much
cheaper than an SPA audit.

Corollary: Wix does **not** exhibit the soft-200 trap — a nonsense path correctly
returns a real 404, and `llms.txt` is served as genuine `text/plain`. Still probe
for it (one nonsense-path request), but expect it to pass.

## 5. Wix auto-generates `llms.txt` and an MCP endpoint

Wix ships `/llms.txt` and a live MCP endpoint at `/_api/mcp` with no client
action. The `llms.txt` typically has a decent business summary but lists **only
the homepage** — so it is present-but-thin rather than missing. It is not
editable from the SEO panel today, so "rewrite llms.txt" may be a non-actionable
recommendation. Check editability before recommending it.

## 6. Wix's own schema is correct — overrides are where bugs live

Wix-native schema (gift cards, native product pages) uses valid lowercase
schema.org properties. So if product schema is malformed, suspect a **custom
structured-data override** in `Settings → SEO → Structured data markup` or
injected custom code.

**Use a Wix-native page as an internal control.** Comparing a native page's
JSON-LD against the suspect template on the same site turns "your schema is
broken" into "your override broke it, here is the setting" — a much more
actionable finding, and it rules out a platform bug.

## 7. Things Wix does well — record them so nobody "fixes" them

Consistently observed and worth stating in the report, because clients often pay
someone to fix these unnecessarily:

- www/HTTPS canonicalisation, single-hop, all four variants
- Brotli compression, HSTS, `X-Content-Type-Options`
- Excellent TTFB (~40 ms) behind Fastly
- Exactly one `rel=canonical` per page, correctly self-referencing
- Segmented sitemap index by content type
- Genuine 404s on non-existent paths

## 8. Wix quirks that are real but not worth prioritising

- **`lastmod` is deploy-stamped, not edit-stamped** — every page in a sitemap
  shares one date. Carries no signal; not fixable. Note it so it is not
  misdiagnosed later as a staleness problem.
- **Text tags are set per-element in the editor**, so "no H1" is extremely common:
  headline boxes default to visual styling without a semantic tag. Expect to find
  many pages with zero H1 and several with the body paragraph marked H1.
- **Promo banners are often marked `<h6>`**, making them the only heading on a
  page.
- **Product images default to `alt=""`** unless alt text is entered per product in
  Wix Stores. On a large catalogue this is the single biggest image finding, and
  it is genuine — the images sit inside product links, so they are not decorative.

## Related

- `schema-grep-false-positives.md` — Wix's Thunderbolt config blob makes
  `grep "FAQPage"` return a false hit
- `spa-soft-200-false-positives.md` — the CSR failure modes Wix mostly avoids
- `schema-nested-price-false-positive.md` — price can be valid but nested

# Cross-brand process notes

Reusable learnings only. **No client names, no brand-specific facts** — those
live in `brands/<brand>/`.

Write here when something is true regardless of which client you're working on:
a script quirk, a tactic that worked, a false positive worth watching for.

---

## Index — every note in this folder

The rest of this README carries the rules inline. These are the full write-ups.
**Check this list before reporting any finding that sounds like one of them.**

### Standard operating procedures

| Note | What it settles |
|---|---|
| [blog-content-sop.md](blog-content-sop.md) | Post length, Google's helpful-content gate, what moves AI citation, design spec, pre-flight checklist |
| [skill-stack-sop.md](skill-stack-sop.md) | The four layers of this system and how to export it to a new project |
| [connecting-search-console.md](connecting-search-console.md) | Service-account GSC setup, repeatable |

### Absence is the easiest claim to get wrong

| Note | The trap |
|---|---|
| [prove-the-fetch-before-reporting-absence.md](prove-the-fetch-before-reporting-absence.md) | Prove the fetch succeeded before calling anything missing |
| [crawl-site-truncation-fakes-absence.md](crawl-site-truncation-fakes-absence.md) | `crawl_site` truncates each page — "not in the crawl" ≠ absent |
| [lazy-loaded-widgets-need-a-real-viewport.md](lazy-loaded-widgets-need-a-real-viewport.md) | A headless browser cannot prove a lazy-loaded widget is absent |
| [hidden-tab-suppresses-entrance-animations.md](hidden-tab-suppresses-entrance-animations.md) | A hidden tab suppresses entrance animations — the page is not blank |
| [spa-soft-200-false-positives.md](spa-soft-200-false-positives.md) | On client-rendered SPAs both "HTTP 200" and "0 words" lie |
| [js-overwrites-correct-server-side-head-tags.md](js-overwrites-correct-server-side-head-tags.md) | Check head tags in raw HTML *and* rendered DOM — they disagree |
| [form-broken-verify-structurally-not-visually.md](form-broken-verify-structurally-not-visually.md) | The four structural checks before calling a form broken |

### Parser and script artefacts

| Note | The trap |
|---|---|
| [html-parser-false-positives-alt-and-title.md](html-parser-false-positives-alt-and-title.md) | Valueless `alt` and SVG `<title>` — 1,182 false "missing alt" |
| [schema-grep-false-positives.md](schema-grep-false-positives.md) | Grepping a schema type name matches text that isn't schema |
| [schema-nested-price-false-positive.md](schema-nested-price-false-positive.md) | "Missing price" is usually `offers.priceSpecification`, which is valid |
| [schema-script-blind-spots.md](schema-script-blind-spots.md) | Five ways the schema scripts silently mislead |
| [meta-content-truncated-at-apostrophe.md](meta-content-truncated-at-apostrophe.md) | Live bug in `site_collect.py` |
| [compare-only-like-for-like-extraction.md](compare-only-like-for-like-extraction.md) | Two crawlers on identical bytes disagree — never mix methods |
| [word-count-is-not-content-quality.md](word-count-is-not-content-quality.md) | And it inverts on AI-written pages |
| [topic-clustering-term-stripping-cuts-both-ways.md](topic-clustering-term-stripping-cuts-both-ways.md) | Stripping site-wide terms fixes one false positive, creates another |

### Measurement discipline

| Note | The rule |
|---|---|
| [verify-commands-must-measure-the-claim.md](verify-commands-must-measure-the-claim.md) | Run the command, and check it measures what you claim |
| [pagespeed-caches-identical-results.md](pagespeed-caches-identical-results.md) | Back-to-back runs are ONE sample, not two |
| [common-crawl-proves-crawler-access.md](common-crawl-proves-crawler-access.md) | Prove crawler access with Common Crawl, not UA tests |
| [ua-matrix-poisons-the-bulk-crawl.md](ua-matrix-poisons-the-bulk-crawl.md) | Run the crawler-UA matrix *after* the bulk crawl |
| [broad-match-volume-hides-the-intent.md](broad-match-volume-hides-the-intent.md) | Volume tells you nothing until you ask what it's made of |
| [free-volume-sources-and-their-gotchas.md](free-volume-sources-and-their-gotchas.md) | What each free volume source actually measures |
| [location-scoped-search-unlocks-non-us-serps.md](location-scoped-search-unlocks-non-us-serps.md) | The "US results only" limit is liftable |
| [content-length-splits-by-ai-platform.md](content-length-splits-by-ai-platform.md) | The studies disagree, and the disagreement is the finding |
| [vendored-references-carry-fabricated-citations.md](vendored-references-carry-fabricated-citations.md) | Verify a vendored reference before building on it |

### Site- and stack-specific behaviour

| Note | What differs |
|---|---|
| [wix-site-audit-quirks.md](wix-site-audit-quirks.md) | Auditing a Wix site |
| [spa-language-switcher-without-urls.md](spa-language-switcher-without-urls.md) | Client-side language switchers hide complete translations |
| [forms-wired-for-the-wrong-host.md](forms-wired-for-the-wrong-host.md) | Check the submit target against the actual host |
| [gsc-domain-property-reveals-hacked-subdomains.md](gsc-domain-property-reveals-hacked-subdomains.md) | Scan the Pages tab for stray hostnames |
| [next-dev-and-build-share-dot-next.md](next-dev-and-build-share-dot-next.md) | Never run both at once |

### Environment

| Note | What bites |
|---|---|
| [run-scripts-from-workspace-root.md](run-scripts-from-workspace-root.md) | Or `.env` never loads |
| [firecrawl-mcp-is-search-only.md](firecrawl-mcp-is-search-only.md) | It cannot crawl |
| [ssrf-guard-dns-resolver-mismatch.md](ssrf-guard-dns-resolver-mismatch.md) | Validate through the resolver the fetch will use |

---

## Known false positives

Both encountered in real audits. Verify before reporting either.

- **`sitemap_checker.py` "404" errors.** It probes common sitemap filenames
  (`/sitemap_index.xml`, `/sitemap-index.xml`) and reports 404 on ones that
  don't exist. Not a site problem. It can also double-count URLs when it reads
  the same sitemap via two discovery paths, producing false "duplicate URL"
  warnings.
- **`llms_txt_checker.py` "found (HTTP 200)".** Single-page apps serve their
  HTML shell for any unknown path, so *every* URL returns 200. Fetch the file
  and confirm it is actually plain text.
- **`product_schema_checker.py` "Offer is missing price / priceCurrency".** The
  price is often present but nested in `offers.priceSpecification`, which is
  valid Schema.org. Common in WooCommerce and Shopify schema output. See
  `schema-nested-price-false-positive.md` before reporting it.
- **"N images missing alt text".** A valueless `alt` attribute (`<img … alt src=…>`)
  is spec-equivalent to `alt=""` — correct decorative markup — but both
  BeautifulSoup (`img.get('alt') is None`) and a naive `\balt\s*=` regex count it
  as missing. Observed: 1,182 reported missing, **0** genuinely missing.
- **"Multiple `<title>` tags on every page".** Inline SVG icon sprites contain
  `<title>star</title>` as the SVG accessible-name element. Count only inside
  `<head>`. Observed: 16 in-document, 1 in `<head>`.

  Both of the above are detailed in
  `html-parser-false-positives-alt-and-title.md`, along with the lazy-loader
  `data:image/svg+xml` placeholder trap that breaks `src`-based image checks.

- **`curl -L` reporting "200" on a URL that actually redirects.** `-L` follows
  redirects silently, so the status, body, `<title>` and canonical you get all
  belong to the *destination*. This produced a full false finding — "a duplicate
  page returning 200 with a canonical" — when the URL in fact returned a clean
  `301`. **Never use `-L` to establish what a URL returns.** Use
  `curl -sS -o /dev/null -w "%{http_code} -> %{redirect_url}\n"` with no `-L`.
  Reserve `-L` for when you deliberately want the final page's content.

**General rule: an HTTP 200 is not proof a file exists.** Check what came back.

**Second rule: a file existing is not proof it is correct.** A genuine llms.txt
can still list URLs that have since 404'd — generator plugins snapshot the site
and are rarely re-run. Check contents against live status, and regenerate
llms.txt *last* in any cleanup sequence.

## Environment quirks

- **Windows:** `export PYTHONIOENCODING=utf-8` before running the seo scripts.
  Several print emoji status icons and crash mid-output on the default `cp1252`
  console encoding — losing findings already collected.
- **Script arguments are inconsistent** — some take a positional URL, others
  `--url`. Check `skills/seo/scripts/INDEX.md` before invoking.
- **`python` from PowerShell is a dead Microsoft Store stub.** `python`,
  `python3` and `py` all resolve to `…\WindowsApps\*.exe` and fail with
  *"Program 'python.exe' failed to run: The file cannot be accessed by the
  system"* — which reads like a permissions problem but is just the Store alias.
  The real interpreter is reachable **from the Bash tool** at
  `~/AppData/Local/Python/bin/python` (3.14.x, with requests /
  bs4 / lxml installed). Run the seo scripts through Bash, not PowerShell.
- **PageSpeed API** rate-limits anonymous calls hard. Use a free API key in
  `.env` as `PAGESPEED_API_KEY`.
- **Git Bash vs Python paths:** bash resolves `/tmp` to the Windows temp dir,
  Python resolves it to `C:\tmp`. Use relative paths when a shell command and a
  Python script share a file.
- **Git Bash mangles leading-slash arguments — set `MSYS_NO_PATHCONV=1`.** Any
  script taking a URL *path* as an argument (`robots_path_tester.py <site>
  /path /other`) silently receives `C:/Program Files/Git/path` instead of
  `/path`. The script runs, reports success, and every URL in its output is
  meaningless. Affects `curl` calls with path arguments too. There is no error —
  only wrong results — so it is easy to publish. Prefix the command:
  `MSYS_NO_PATHCONV=1 python skills/seo/scripts/robots_path_tester.py …`
- **Beware null bytes when heredoc-ing Python that contains JS.** Writing a
  script whose body embeds JavaScript string literals can introduce a literal
  `\x00` that Python rejects with the unhelpful "source code cannot contain null
  bytes", pointing at a line that looks fine. Check with
  `python -c "print(open(p,'rb').read().find(b'\x00'))"` rather than re-reading
  the source. Prefer native DOM APIs that avoid nested quoting (e.g.
  `input.labels` instead of building a `label[for="…"]` selector by string
  concatenation).

## Method notes

- **Never infer duplicate content from similar slugs.** Two URLs that look like
  variants of each other (`/product/x/` and `/product/x-2/`,
  `/product/x-ragi-veldt-grape/` and `/product/y-ragi-veldt-grape/`) are very
  often *different products with badly-named slugs*. Fetch both, compare
  `<title>` and body text, and get a similarity ratio before using the word
  "duplicate". On one audit, four alleged duplicate pairs reduced to **one** real
  duplicate under this test — and the real finding underneath was the opposite
  problem: **slugs that misdescribe their own page** (a URL reading
  `ragi-veldt-grape` serving a Horsegram product). A client disproves a false
  duplicate claim in ten seconds by opening both pages.
  Rule of thumb: >90% similarity = duplicate · 30–70% = boilerplate overlap only.
- **`competitor_gap.py` output is mostly unusable without heavy filtering.** Three
  failure modes seen together on one run: (1) `overlap_topics: 0` is an
  **exact-string match artefact** — it compares raw heading text, which almost
  never matches across two sites, so "0 overlap / all your topics unique" is
  meaningless; (2) it crawls only `--max-pages` per site, so it reports topics as
  "gaps" that the client demonstrably covers (flagged "call recording" as a gap on
  a site with three call-recording pages); (3) a competitor that blocks or
  redirects the crawler returns 0 topics and silently drops out of the comparison
  while still appearing in the output. Check `pages_crawled` and `topics` per
  competitor before trusting anything. Expect ~3 of 50 "gaps" to be real; the rest
  are heading fragments like "two way street" and "identify needs".
- **Separate navigation links from contextual links before judging internal
  linking.** Raw internal-link counts are dominated by nav and footer. A page
  showing "46 internal links" had **1** editorial link. Identify nav targets by
  inbound frequency (a path linked from ≥90% of pages is nav, 25–90% is usually a
  recent-posts/related widget), subtract those plus `/category/` and `/page/`
  paths, and count what remains. Same method reveals the direction problem:
  spokes appearing to link to their hub 100% of the time is usually just the hub
  sitting in the nav menu — real cluster integrity is **hub → spoke**, which is
  the direction that is almost always missing.
- **FAQ schema must be checked against *rendered* page text, not the presence of
  an FAQ heading.** Detecting a "Frequently Asked Questions" H2 misses accordion
  markup and headings labelled "FAQs", producing false positives in both
  directions. The correct test: extract every `Question.name` from the JSON-LD,
  then search the rendered DOM for the first ~6 words of each. Found four money
  pages carrying 8–10 `Question` nodes with **zero** matching visible text — a
  Google structured-data policy violation, and invisible to any heading-based
  check. Verify in a browser, since JS-injected accordions are a real possibility.
- **`image_weight_audit.py` inflates totals.** It counts every `<img>` tag, so an
  image used three times on a page is counted three times, and off-site tracking
  pixels (`facebook.com/tr?...`) are counted as images. Deduplicate by `src` and
  measure with HTTP HEAD before quoting a megabyte figure. Observed gap on one
  audit: script said 4.7 MB / 40 images, measured reality was 3.34 MB / 30.
- **PageSpeed lab scores are not reproducible — always run twice and quote a
  range.** Observed spread on a single unchanged page: score 48 vs 59, LCP
  6,911 ms vs 5,267 ms, in back-to-back runs. Quoting one number invites the
  client to re-run it and get something different. Quote the range and the
  threshold it fails against, which is the part that is stable.
- **A URL in a sitemap that canonicals elsewhere is a tidiness issue, not a
  duplicate-content issue.** Check the canonical before escalating severity —
  page-builder header/footer template URLs often render a full page clone but
  canonical correctly, which means they are already handled.
- **Re-audits must re-measure the same way as the baseline, or they invent trends.**
  A raw `grep -c` on rendered HTML and a count on visible extracted text give
  different numbers for the same page. Observed: a placeholder-text count read 16
  at baseline (visible text) and 24 at re-audit (raw HTML) — implying a
  regression, when the visible count was unchanged and the extra hits were inside
  a newly added JSON-LD block. Always re-run the baseline's own extraction method
  before declaring better or worse.
- **A crawler that follows redirects will report the redirect as a duplicate.**
  After a slug rename with correct 301s, `crawl_audit.py` recorded both the old
  URL and its destination as separate pages and flagged duplicate titles/H1s —
  making correctly-done work look like a new problem. Before reporting duplicates
  on a site that has just been reorganised, request each URL with redirects
  **unfollowed** and check for `301`.
- **Adding schema over placeholder content is a regression, not progress.**
  Watch for this specifically on re-audits: a client can action "add FAQPage
  schema" while skipping "write the answers first", which publishes dummy text to
  Google as structured data — worse than the original visible-only placeholder.
  When recommending schema on a page with placeholder copy, make the ordering
  explicit and re-check that page first on the next pass.
- **Test page templates, not pages.** A 25-page site usually has ~4 templates.
  Testing all pages repeats the same answer; testing one hides the worst case.
- **NAP checks must read markup, not just visible text.** `local_seo_checker.py`
  scans rendered text and will miss numbers that only exist in `Organization`
  JSON-LD `telephone` or in chat-widget config (JoinChat/WhatsApp `data-settings`).
  On one audit, visible-text scanning found 2 numbers; extracting schema and the
  widget config found **4** — and the schema number, which Google treats as
  authoritative, matched none of the visible ones. Always grep
  `"telephone":"` and the widget config separately. Also check whether visible
  numbers are `tel:` links at all.
- **Record what is already correct**, not only what is broken. Prevents
  regressions, and it is why clients trust the rest of the report.

## Standard operating procedures

- **`blog-content-sop.md`** — the blog playbook for every brand: how long a post
  should be (and why the usual advice is wrong), Google's own helpful-content
  questions as a publishing gate, the spam policies that actually apply, what
  measurably moves AI citation, the design and typography spec, which content
  types earn citations and links, and a pre-flight checklist.

  Three things in it correct claims that circulate widely and are wrong:
  - Google states plainly it has **no preferred word count**.
  - The "position 1 averages 1,890 words" figure is **misattributed** to
    Backlinko's 11.8M-result study, which found *no* correlation between length
    and position.
  - Google states you do **not** need `llms.txt`, AI text files, or special schema
    to appear in AI Overviews or AI Mode.

## Tooling notes

- **`free-volume-sources-and-their-gotchas.md`** — which free keyword tools give
  usable volume data and how each one distorts it. Key points: Bing Webmaster
  Tools gives *exact* integers with no daily cap but measures Bing demand
  (~3% share in India — relative signal only, never a client-facing figure);
  Google Keyword Planner shows `1K-10K` buckets unless the Ads account has
  active spend, with a no-spend workaround; Semrush's free 10 searches/day are
  shared across all its tools. Explore free, validate on the metered paid tool.

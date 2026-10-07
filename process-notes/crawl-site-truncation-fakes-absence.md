# `crawl_site` truncates each page — "not found in the crawl" is not absence

**Type:** tool quirk / false negative
**Cost when missed:** nearly shipped "this competitor doesn't sell the product
category we're comparing against" — about a rival whose collection page for that
exact category ranks #3 in Google.

## What happens

`crawl4ai`'s `crawl_site` returns roughly the first **2,000 characters of
markdown per page**. On a typical Shopify/Elementor theme, that budget is
consumed by sitewide boilerplate — announcement bar, mega-menu, cart drawer,
currency selector — **before reaching the page's own H1 or body copy**.

The result is a crawl that looks successful (HTTP 200, 19 pages, no errors) but
whose captured text is mostly navigation. Evidence comes back as `title` and
`slug` only, and any term that lives in body copy is silently missing.

## The false finding it produces

A miner reported that a competitor had "no <product> anywhere in 19 pages",
and reasonably inferred they were a general store rather than a category
specialist. One direct fetch of `/collections/<product>` returned **seven**
product variants, each named by type — which turned out to be the most
actionable finding in that whole analysis.

The crawler's silence was a character budget, not a fact about the business.

## What to do

- **Never conclude a competitor lacks a product, page or term from a `crawl_site`
  pass alone.** Absence in a truncated crawl is `Unverified`, never `Confirmed`.
- **Check the SERP evidence you already have.** If a URL ranked for the term that
  qualified the competitor, that URL exists and has content — the crawl just
  didn't reach it. This contradiction is free to spot and settles it instantly.
- **Fetch the specific URL directly** with `crawl_page` or a plain request when a
  category matters. One targeted fetch beats twenty truncated ones.
- **Read the evidence-type mix as a health check.** A file that is nearly all
  `title` and `slug` with almost no `h1`/`h2`/`body` did not read the pages — it
  read the navigation. Treat low `h1` share as a truncation warning.
- Prefer `crawl_pages` with a known URL list, or `crawl_page` with a
  `css_selector` such as `main`, which strips the boilerplate and spends the
  budget on content.

## Related

`never-report-broken-from-automation` — same failure mode, different tool: an
automated pass cannot prove absence. `prove-the-fetch-before-reporting-absence`
is the general rule; this file is the specific budget that triggers it.

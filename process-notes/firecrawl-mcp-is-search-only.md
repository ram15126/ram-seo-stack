# The Firecrawl MCP here is search-only — it cannot crawl

The Firecrawl server connected to this workspace exposes **only**:

- `firecrawl_search` (web / news / images, with `site:`, `related:`,
  `intitle:`, `includeDomains` / `excludeDomains`, and `github` / `research` /
  `pdf` / `developer` categories)
- `firecrawl_developer_search`
- `firecrawl_research_*` (papers)

There is **no** `scrape`, `crawl`, `map` or `extract`. Firecrawl's hosted
product has those; this MCP connection does not expose them. Any plan that says
"use Firecrawl to go through the site" will fail at the first fetch.

## What to use instead

| Job | Tool |
|---|---|
| Discover who ranks / find candidate domains | `firecrawl_search` — this is what it is good for |
| Crawl a site breadth-first | `crawl4ai` `crawl_site` (depth + `max_pages`, hard cap 50) |
| Fetch a batch of known URLs | `crawl4ai` `crawl_pages` (cap 20 per call) |
| Fetch one page | `crawl4ai` `crawl_page`, or `WebFetch` |
| Full audit capture of our own site | `site_collect.py` — one pass, house standard |

## The JS-rendering trap

`crawl4ai` defaults to `wait_seconds: 0`. A client-side-rendered site returns
its empty HTML shell, which reads as "this page has no content". Pass
`wait_seconds: 6` for SPA-ish sites, and if it still comes back empty report
**"could not read"**, never "they have nothing there". A headless fetch cannot
prove absence — the same rule as
`never-report-broken-from-automation`.

## Why it matters

Tool availability is not the same as tool existence. Before designing a
pipeline around an MCP capability, list the server's actual tools. A plan built
on a tool that is not connected costs a full redesign after the work has
already started.

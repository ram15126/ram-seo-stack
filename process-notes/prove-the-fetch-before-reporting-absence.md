# Prove the fetch succeeded before reporting anything as absent

**Class:** false positive, highest severity
**Written:** 25 August 2026, after hitting it three ways in one afternoon

## What happened

A new pre-flight checker was pointed at a live blog post. It returned a clean,
confident, fully formatted audit:

```
[FAIL] indexable: Page carries a noindex directive.
[FAIL] answer_block: No H1 or H2 found.
[FAIL] schema_article: No Article/BlogPosting schema.
[FAIL] byline: No visible byline and no author URL in schema.
[FAIL] meta_description: No meta description.
... nine findings in total
```

Every one was false. The fetch had returned **zero bytes**. The script parsed an
empty string, found nothing in it, and reported the nothing as findings about the
page.

Three separate causes surfaced on the same URL within ten minutes:

1. **The SSRF guard blocked it** — `Blocked: URL resolves to private/internal IP
   (64:ff9b::12a1:e556)`. That is a NAT64 address for a perfectly public host.
   See `ssrf-guard-dns-resolver-mismatch.md`.
2. **A real HTTP 404** on a retry — the resolver is inconsistent between runs, so
   the same URL failed two different ways.
3. **Client-side rendering** — a raw fetch of an SPA returns the shell, and every
   content check reports its subject missing.

## Why this class is worse than other false positives

A normal false positive is one wrong finding among right ones. This produces a
**complete report in which every finding is wrong**, and it is indistinguishable
from a real audit of a badly built page. Nothing in the output looks broken. It
would have gone to a client as a nine-item fix list for problems that do not
exist.

It is also the easiest to miss when writing the script, because the failure path
produces no exception — an empty document parses fine.

## Rule

**Every collector must prove it has a document before it says anything is missing
from that document.** Gate on all of these, in order, and stop on any of them:

1. **Fetch error.** `seo_common.fetch_url` returns `status=None` plus an `error`
   string when it fails. Check `error` — not just status.
2. **HTTP >= 400.**
3. **Soft 404** — status 200 with not-found text in the body.
4. **Thin/no-heading body** — under ~150 words with zero headings almost always
   means client-side rendering. Re-fetch with the `crawl4ai` MCP (`crawl_page`,
   `wait_seconds=6`) and audit that.

When any gate trips, return **that one finding and nothing else**, and say
explicitly that nothing was checked. A one-line honest failure beats a nine-line
confident fiction.

**The same rule applies to comparison inputs.** In a competitor diff, a page that
failed to load contributes zero claims and reads as "this competitor covers
nothing" — which inflates the target's apparent uniqueness and hides real gaps.
Drop unreadable competitors and name them in the output; never silently count
them as empty.

## The general form

> A zero from a collector is a claim about the collector as much as about the
> page. Before reporting "absent", establish that the thing which would have
> contained it was actually retrieved.

## Related

- `spa-soft-200-false-positives.md` — the rendering case
- `ssrf-guard-dns-resolver-mismatch.md` — the blocking case
- `schema-script-blind-spots.md` — the same shape one layer down: a parser that
  strips scripts makes a page with valid JSON-LD report "no structured data"
- `never-report-broken-from-automation.md` — the original of this family

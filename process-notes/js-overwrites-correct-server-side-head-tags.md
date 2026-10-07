# Check head tags in BOTH raw HTML and rendered DOM — they can disagree

The existing SPA note (`spa-soft-200-false-positives.md`) covers *duplicate* head
tags, where `querySelector` returns a stale static tag and the framework-injected
one hides beneath it. This is the adjacent case, and it produces the opposite
error: **the server sends a correct tag and client-side JS replaces it with a
wrong one.** Count stays at 1, so a duplicate check finds nothing.

## What it looks like

A prerendering layer (edge middleware, a prerender service, a build-time HTML
rewrite) injects correct per-route `<title>`, `<meta description>` and
`<link rel=canonical>`. Then the app hydrates and a "TitleUpdater"-style component
sets the same tags again from its own data — which can be stale.

Observed on one site: 4 of 7 blog posts served a correct self-referencing
canonical in raw HTML, and after hydration pointed at an older slug that rendered
a "Post Not Found" view.

```
raw HTML  : <link rel="canonical" href="/blog/are-you-really-an-nri">        <- correct
rendered  : <link rel="canonical" href="/blog/are-you-really-an-nri-most-…">  <- dead page
```

## Why it matters which one you report

The two audiences differ, and the fix differs:

- **Googlebot renders JavaScript before selecting a canonical** → it sees the
  broken one. The bug is real and severe.
- **AI crawlers and social scrapers do not render** → they see the correct one.
- If you only fetch raw HTML, you conclude canonicals are fine. **False negative.**
- If you only read the rendered DOM, you conclude the site has no server-side meta
  and recommend an SSR migration to fix it. **Wrong fix** — the prerendering
  already works; one stale data field is the actual defect, and it is a small edit.

## The check

Fetch both, diff per URL. Never one or the other.

```python
raw    = re.findall(r'<link rel="canonical" href="([^"]+)"', requests.get(u).text)
render = page.evaluate("()=>Array.from(document.querySelectorAll('link[rel=canonical]')).map(e=>e.href)")
# compare, and report BOTH values when they differ
```

Apply the same diff to `<title>`, `meta[name=description]` and `meta[name=robots]`.
A `robots` disagreement is the dangerous one: server `index,follow` overwritten by
a client-side `noindex` will deindex pages while raw-HTML checks look clean.

## Tell

Raw HTML byte-length that **varies per URL** (4961–5784 in the observed case)
means per-route prerendering is happening. A constant byte-length across every
URL means one static shell and no prerendering. That single number tells you which
kind of site you are auditing before you check anything else.

## The general lesson

Extend the existing rule. It is not only "use `querySelectorAll` and report the
count" — it is:

> The rendered DOM is not a superset of the raw HTML. JS can *remove* and *replace*
> correct server output, not just add to it. Any head-tag finding needs both
> observations before it is safe to write down.

# Location-scoped search returns real non-US SERPs — the "US results only" limit is lifted

**Type:** capability change / corrects a documented blocker

## The old limit

Earlier research in this workspace recorded, correctly at the time:

> "The web search available to me returns US results, so it cannot be used to
> infer google.in SERPs. Any statement about who ranks in India would be
> invented."

That produced real gaps: competitor sets left `TBD`, and keyword documents that
could describe themes but never say who ranked.

## What works now

`firecrawl_search` accepts a **`location`** parameter. Passing `location: "India"`
returns genuine google.in results — verified by the result set itself: ₹ pricing,
Zepto and Flipkart listings, amazon.in rather than amazon.com, and Indian
national brands appearing where US equivalents would otherwise sit.

```
firecrawl_search(query="<product> online buy india", location="India", limit=15)
```

Also useful on the same tool: `site:`, `related:`, `intitle:`, `inurl:` operators,
plus `includeDomains` / `excludeDomains` (mutually exclusive), and
`sources: [{type:"news"}]`.

## What this does and does not license

**Now sayable:** "As of <date>, searching `<query>` from an India location signal,
these domains appeared in this order." That is a reading of a result page, and
the reader can repeat it.

**Still not sayable:**
- **"They rank #3."** One location-scoped API call is a *snapshot*, not a
  rank-tracked average. Google personalises by finer location, device, history
  and time. Report it as a position observed on a date, with the query, and let
  the number carry its own caveat.
- **Anything about volume.** A SERP shows who competes, never how many people
  search. Position evidence does not become a volume figure by being nearby.
- **Local-pack or map results.** These vary by precise geography, far below
  country granularity.

## Why it matters

The blocker was recorded as a permanent limit rather than a tool gap, so it kept
being inherited by later documents. **Re-test a documented limitation before
building around it** — capability notes age faster than findings do, and an
inherited "impossible" is expensive: it left one brand's competitor table empty
for five weeks.

## Related

`prove-the-fetch-before-reporting-absence` — same principle from the other
direction: confirm the tool actually can't do the thing before writing it down
as something that cannot be done.

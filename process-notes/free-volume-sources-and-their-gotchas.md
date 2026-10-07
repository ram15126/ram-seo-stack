# Free search-volume sources: what each one actually measures

Researched 2026-09-06. Free keyword tools are not interchangeable — each
distorts volume in a specific, predictable way. Pick by the distortion you can
tolerate, and never mix sources inside one deliverable.

## The split that matters

**Search volume** (demand for a term) is estimable for free.
**Actual traffic** (visits a page receives) is not. Every free "traffic" figure
outside the site's own analytics is modelled from position x assumed CTR.
Do not put a free-tier competitor traffic estimate in a client report.

## Sources and their distortions

| Source | Gives | Distortion to account for |
|---|---|---|
| Bing Webmaster Tools -> Keyword Research | Exact integers, no daily cap, CSV export, question filter | It is **Bing** demand. In India Google holds ~97% share, so absolutes come from a thin slice. Use for relative ranking + question mining only. |
| Google Search Console | True impressions/clicks/queries | Own/verified sites only. Also a keyword tool: mine queries ranking 11-30. |
| Google Keyword Planner | The upstream source most tools resell | Shows **buckets** (`1K-10K`) without active ad spend. Two keywords in one bucket can differ 7x. |
| Keyword Surfer (Chrome) | In-SERP volumes, unlimited, free | Estimates. A triage tool, not a research tool. |
| Semrush free account | Full-quality data | 10 searches/day **shared across all tools** — clicking through to Keyword Overview burns a second one. |
| Ahrefs Free | Site audit + backlinks, 5k pages/project/mo | Verified own domains only. No competitor research at all. |

## Keyword Planner bucket workarounds

1. Run a minimal campaign for a few days — unlocks precise averages.
2. CPC-slider method, no spend: enter the keyword in `[exact match]` brackets,
   open the **Forecast** tab, drag max CPC to maximum, read the **Impressions**
   column. Approximates monthly volume.

Evidence note: the spend gate is not documented in Google's own help pages —
it is consistently reported by practitioners and visible in Google Ads
community threads. Label it `Likely`, not `Confirmed`.

## Quota discipline when a paid tool is metered

Explore free (Bing WMT + Surfer + GSC), validate paid. Spend metered credits
only on terms that already survived the free pass. Client-facing volume figures
come from the paid source, never from the free triage layer.

See also [[broad-match-volume-hides-the-intent]].

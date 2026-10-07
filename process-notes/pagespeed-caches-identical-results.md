# PageSpeed returns a cached result — back-to-back runs are ONE sample, not two

**Type:** measurement trap / false positive
**Cost when missed:** would have reported a 36% speed collapse that never happened

## What happened

A re-audit measured mobile LCP at **6,761 ms** against a previous **4,960 ms** — a large,
alarming regression. A second run was fired immediately to confirm it. It returned
**6,761 ms, 4,220 ms FCP, 650 ms TTFB — identical to the millisecond.**

That identity is the tell. Two genuine Lighthouse runs never agree to the millisecond across
four metrics. The PageSpeed Insights API caches results per URL+strategy for a few minutes,
so a quick "confirmation" run just replays the first result.

Five runs spaced ~70 seconds apart gave:

```
4,959 · 4,964 · 5,110 · 5,402 · 5,410 ms   (median 5,110)
```

Statistically indistinguishable from the 4,960 ms it was being compared against. **There was
no regression.** The 6,761 ms reading was a cold-cache outlier at the top of the spread.

## The rule

- **Identical PSI numbers across runs = one cached sample.** Treat it as a single
  observation, never as corroboration.
- **Space samples at least 60 seconds apart** and take **five**, then report the **median**
  and the range — never a single figure and never the first run.
- **The performance *score* is far noisier than the metrics.** The same site scored 39, 51,
  54, 56, 59, 61, 62 across one session while LCP stayed in a 450 ms band. Report LCP/FCP;
  treat score movement under ~10 points as meaningless.
- Before attributing any speed change to the site, **diff the asset inventory** (count of
  external scripts and stylesheets). If nothing was added or removed, the change is far more
  likely measurement noise or a Lighthouse version change than a real regression.
- **Record the Lighthouse version** (`lighthouseResult.lighthouseVersion`) with every
  measurement, or later comparisons cannot rule out a scoring-engine change. The wrapper
  script's JSON output does not include it — query the API directly when it matters.

## Related

Same family as [[word-count-is-not-content-quality]] and the entity-decoding trap: a number
that moved because the *measurement* changed, not the thing being measured.

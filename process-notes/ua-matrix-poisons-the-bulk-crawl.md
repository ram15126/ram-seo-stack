# Run the crawler-UA matrix AFTER the bulk crawl, never before

## What happened

On an audit of a WordPress.com/Atomic-hosted site, the order of operations was:

1. Probe the host — fine, 200s.
2. **Crawler-UA spot check** — 12 requests to `/`, each with a different bot UA
   (Googlebot, Bingbot, GPTBot, ClaudeBot, PerplexityBot, CCBot …), 2s apart.
   The last two returned `429`.
3. Start the bulk collection pass over 303 sitemap URLs.

Step 3 never collected a single record. The collector's own probe request
429'd repeatedly and escalated its backoff (30s → 60s → 90s) without ever
reaching the crawl loop. Two restarts later it was still stuck. The bulk pass
had to be abandoned and rescoped to a priority subset.

## Why

Presenting a dozen different bot user-agents from one IP in ~30 seconds is
exactly the signature edge firewalls are built to catch. The host applied an
IP-level rate limit that persisted for **several minutes after** the spot check
finished — long enough to poison the bulk crawl that followed.

The spot check is cheap (≤12 requests). The bulk crawl is expensive (hundreds of
requests, tens of minutes). Ordering them the wrong way round means the cheap
step destroys the expensive one.

## The rule

**Bulk collection first, UA matrix last.**

```
1. site_collect.py --url-file …      # the expensive pass, browser UA only
2. …analysis…
3. site_collect.py --ua-matrix       # ≤5 URLs, at the very end
```

If the UA matrix must run first (e.g. it's the whole point of the job), then:

- space requests **≥15s apart**, not 2s
- interleave a plain browser UA between each bot UA — this doubles as the
  control that distinguishes *UA-based blocking* from *rate limiting*
- budget a cooldown of **several minutes** before starting any bulk pass

## The control that makes the result trustworthy

A run of bot UAs all returning 403 proves nothing on its own — it is equally
consistent with "this host blocks bot UAs" and "I just tripped the rate
limiter". The interleaved pattern separates them:

```
browser   200
googlebot 403
browser   200      <- rate limiting would have hit this too
claudebot 403
browser   200
```

Browser requests surviving between the 403s is what makes it UA-based blocking
rather than throttling. Without that control the finding is not reportable.

## Also worth knowing

`429` and the blocking `403` were different responses — different body sizes and
different `Server-Timing` cache verdicts (`BYPASS` vs the normal path). Check the
body and headers, not just the status code, before concluding which one you hit.

Related: [[spa-soft-200-false-positives]] — same lesson, different shape: the
status code alone never settles the question.

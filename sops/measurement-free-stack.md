# Measuring AEO/GEO With a Free Stack
Status: ACTIVE | Last verified: 2026-09-07 | Review by: 2026-12 (fast-moving)

Built for the constraint: **GSC + free tiers only, no Ahrefs/Semrush/Profound seat.**
Everything here is [T1] from Google's own documentation unless marked.

## The single biggest asset: GSC Generative AI performance report

**Status:** Launched 2026-06-03; **worldwide to all sites since 2026-08-31** [T1].
Docs: support.google.com/webmasters/answer/16984139
Direct link: search.google.com/search-console/performance/search-analytics/ai

**Covers:** AI Overviews and AI Mode. Discover AI has a *separate* report
(answer/16983858). Search Labs experiments are **excluded**.

**What you get — exactly four dimensions:**
| Dimension | Detail |
|---|---|
| Pages | Final URL after redirects, assigned to the **canonical**, not the duplicate |
| Countries | Where the search originated |
| Devices | Desktop / tablet / mobile |
| Dates | Hourly → monthly granularity, Pacific Time |

**What you DO NOT get — read this before promising a client anything:**
- **No clicks. No CTR. No average position.** Impressions only.
- **No query dimension.** You can see *which of your pages* got cited. You can
  never see *which queries* triggered the citation. This is the hard ceiling of
  free AI measurement and no workaround inside GSC exists.
- **No historical backfill.** Data starts 2026-05-18 [T2, widely reported].
- Standard GSC limits apply: **1,000-row cap**, preliminary (dotted-line) recent data.

**The critical accounting fact most agencies get wrong:**
> "The generative AI performance report includes data from the **Web search type in
> the Performance report**" [T1].

AI impressions are **already folded into your main Performance report totals** — they
are not additive. This means the pattern everyone has been reporting since 2024 —
*impressions up, clicks flat, CTR collapsing* — is **partly an artefact of AI
impressions inflating the denominator**, not purely a behavioural collapse.

**Consequence for client reporting:** Never present raw sitewide CTR decline as
"AI is stealing our clicks" without first accounting for AI impressions.

> **CORRECTION, 2026-09-07 (Opus audit finding, critical).** This section previously
> prescribed **non-AI CTR = total clicks / (total impressions − AI impressions)**.
> **That formula is wrong and biased upward.** It keeps AI-driven clicks in the
> numerator while removing AI impressions from the denominator, so it overstates non-AI
> CTR by however many clicks the AI surfaces produced.
>
> The correct quantity is
> **(total clicks − AI clicks) / (total impressions − AI impressions)**.
>
> **And it is not computable today.** Google's generative AI report supplies
> **impressions only — no clicks** (verified at
> support.google.com/webmasters/answer/16984139). Without AI clicks the numerator
> cannot be corrected, so the true non-AI CTR cannot be derived from GSC as it stands.

**What you can honestly do instead:** report the corrected formula as **bounded**, not
computed. Total CTR is a lower bound on non-AI CTR; `clicks / (impressions − AI
impressions)` is an upper bound. If **both bounds are stable**, the dilution story
holds. If they straddle the decline, say the data cannot separate the two — which is
still more than most agencies will tell the client.

## The opt-out control — a client decision, not a technical one
Google shipped a Search Console toggle to exclude a site from generative AI features
(answer/16908024) [T1].
- Applies to: AI Overviews, AI Mode, AI Overviews in Discover.
- Opting out = **"no traffic or impressions from our generative AI features."**
- Google states it is **not used as a ranking signal outside those features** — so
  classic organic ranking is unaffected.

**Position:** Do not opt out for ordinary clients. You forfeit the impressions and
the reporting data, and gain nothing measurable. Only consider it for sites whose
entire value is gated content the AI would substitute for wholesale. Note that a
missing AI report can *mean the client already opted out* — check this before
diagnosing "we have no AI visibility."

## Building the rest of the measurement stack for free

GSC gives you *your* citation impressions. It does not give you queries, competitors,
or non-Google engines. Fill those gaps:

1. **Prompt-panel tracking (substitute for Profound/Peec).**
   Maintain a fixed set of 50–150 buyer-intent prompts per client. Run them on a
   fixed schedule against ChatGPT, Perplexity, Gemini, Claude. Record: brand
   mentioned y/n, cited y/n, position in answer, competitors named, URL cited.
   This is the only way to measure non-Google AI visibility without paying.
   **Fix the prompt set and the schedule** — drift in the panel destroys comparability.
   Expect run-to-run variance; treat single runs as noise, use rolling medians over
   ≥3 runs before reporting a change.

2. **Server log analysis for AI crawlers.** Free, first-party, and unfakeable.
   Segment hits by user-agent for the AI crawlers (see knowledge/aeo-geo/ai-crawlers.md).
   Crawl frequency is a leading indicator of citation eligibility — a page never
   fetched by OAI-SearchBot cannot be cited by ChatGPT search.

3. **GSC query data as the fan-out proxy.** You cannot see AI Mode queries, but the
   long-tail question queries in the ordinary Performance report are the closest free
   signal to what fan-out decomposes into. Mine them for the question cluster.

4. **Bing Webmaster Tools.** Free, and ChatGPT/Copilot search leans on Bing's index.
   If Bing hasn't indexed the page, that path to citation is closed.

## The honest reporting frame for clients
Report three separate KPIs. Never merge them, because they have decoupled:
1. **Classic rank/traffic** — GSC clicks, positions.
2. **AI citation impressions** — GSC generative AI report.
3. **AI answer share** — your prompt panel: how often the brand is named/cited.

A client can lose (2) while holding (1). See registry/CONFLICTS.md C-002 — AIO
citation has substantially decoupled from top-10 ranking. Reporting them as one
number hides the actual failure and is the most common measurement error in the market.

## Known gaps in this stack — state them to clients
- No query-level AI attribution. Nobody has this free; paid tools infer it, they
  don't observe it either.
- No AI click data from Google at all, at any price, as of 2026-09.
- Prompt panels measure *your sample*, not the population of real user prompts.
  They are directionally useful and must not be reported as market share.

---
name: competitor-keyword-mining
description: >
  Multi-agent competitor discovery and keyword mining. Finds who actually
  competes with a brand in organic search, mines what those competitors target
  and how their content is structured, merges everything into one deduplicated
  keyword table, validates it adversarially, and turns the survivors into an
  implementation plan. Use when the user says "find my competitors",
  "competitor keywords", "what are they ranking for", "steal their keywords",
  "keyword gap", "what should we copy from them", or gives a site URL and asks
  what to write next. For building "X vs Y" comparison pages, use
  research-competitors.md instead -- that is a different job.
---

# Competitor Keyword Mining

Six stages. Files are the bus between them, not conversation context. Every
stage is resumable, and every stage can be inspected on disk after it runs.

**Default mode is free-mode: no paid keyword API.** This means the output
carries **no search volume and no keyword difficulty score**, because nothing
in the free path measures either. Priority is a *tier* built from named,
checkable evidence. Say this explicitly in the deliverable. See
"Optional: paid metrics" at the end for turning Mangools on.

---

## Why it is shaped this way

Three failure modes drove the design. Do not undo them.

1. **A crawl does not reveal keywords.** It reveals titles, H-tags, slugs and
   internal links -- what a competitor *targets*. That a page targets a term is
   `Confirmed` (a page was fetched and read). That the term is a good
   opportunity for us is `Likely`. Collapsing the two is how a report gets
   forwarded and then contradicted.
2. **Parallel agents that all call the same API collide.** Every paid or
   rate-limited call belongs to exactly one serialized stage.
3. **Deduplication is not a thinking task.** A model asked to dedupe a few
   hundred terms silently drops rows and invents merges. Stage 4 is a script.

---

## Prerequisites

- `brands/<brand>/brief.md` must exist. If it does not, run `intake.md` first.
- Crawling uses the `crawl4ai` MCP (`crawl_site`, `crawl_pages`, `crawl_page`).
  **The Firecrawl MCP in this workspace has no scrape or crawl tool** -- it is
  search only. Use `firecrawl_search` for SERP discovery in Stage 1, never for
  fetching page bodies.
- Windows: `export PYTHONIOENCODING=utf-8` before running any script here.
- Run scripts from the workspace root.

Create the staging directory before Stage 1:

```bash
mkdir -p "brands/<brand>/research/mining/mined" "brands/<brand>/research/mining/ours"
```

---

## Stage 0 -- Brand context

Read `brands/<brand>/brief.md`. Extract: what they sell, who they sell to,
target country/language, current site structure, and any competitors the client
has already named. If the brand is ambiguous, **ask** -- never infer it from
whichever brand was discussed most recently.

No agent. No cost.

---

## Stage 1 -- Scout (1 agent, strong model)

Read `references/agents/competitor-scout.md` and dispatch one agent.

Its job: profile our site, derive seed terms, discover competitor candidates
from three independent sources, then **disqualify the ones that are not
competitors**. Output is `research/mining/competitor-set.md` plus
`research/mining/ours/site.json`.

### CHECKPOINT -- stop here

Present the competitor set to the user with the evidence for each, and wait.

A wrong competitor poisons every later stage and wastes the entire crawl
budget. Approval costs seconds; a bad set costs the whole run. Do not proceed
past this point without an explicit answer.

---

## Stage 2 -- Metrics broker (skipped in free mode)

Off by default. See "Optional: paid metrics" below.

In free mode, the demand evidence comes from Stage 3's query-sourced signals
(autocomplete, People Also Ask) and from competitor repetition in Stage 4.

---

## Stage 3 -- Miners (N agents in parallel, cheap model)

Read `references/agents/competitor-miner.md`. Dispatch **one agent per approved
competitor**, all in a single message so they run concurrently.

Each miner writes exactly one file:
`research/mining/mined/<competitor-domain>.json`

**Miners return a one-paragraph summary to the conversation, never the
candidate list.** The list goes to disk. Returning it burns context on data the
merge script is about to read from the file anyway.

Miners have **no API access** and make no paid calls.

---

## Stage 4 -- Merge (script, free, deterministic)

```bash
PYTHONIOENCODING=utf-8 python skills/seo/scripts/keyword_merge.py "brands/<brand>/research/mining"
```

Normalises and deduplicates terms, merges evidence across competitors, joins
our own coverage, flags competitor brand terms, and assigns a priority tier.

Outputs `merged/keywords-master.csv` and `merged/summary.json`.

Scoring inputs, all free and all checkable:

| Signal | Why it counts |
|---|---|
| Competitor count | Independent competitors betting on the same topic is the demand proxy. This replaces search volume. |
| Evidence strength | A term in a title tag is a targeting decision; the same words in body copy are not. |
| Hub / inbound internal links | The pages a competitor links to hardest are the pages they believe earn. Their own link graph reveals their priorities. |
| Query-sourced | Appeared in autocomplete or PAA, so the query provably exists rather than being one brand's phrasing. |
| Brand-term penalty | You cannot rank for a competitor's brand name. |

Read `merged/summary.json` before continuing. If `our_coverage_known` is false,
Stage 1 failed to profile our site and every term is wrongly bucketed `new`.
Fix that before Stage 5.

---

## Stage 5 -- Validator (1 agent, strong model)

Read `references/agents/keyword-validator.md` and dispatch one agent against
`merged/keywords-master.csv`.

It works top-down from the highest tier and cuts, with a reason recorded for
every cut. It does **not** re-dedupe -- that is already done.

Output: `research/mining/merged/keywords-validated.csv` and a cut log.

---

## Stage 6 -- Strategist (1 agent, strong model)

Read the validated CSV and `brands/<brand>/brief.md`. Produce the plan.

1. **Cluster** survivors into pillar/spoke groups. If a cluster has no viable
   pillar, say so rather than inventing one.
2. **Funnel split** TOFU/MOFU/BOFU. Research the split for this niche against
   sources -- do not assume a ratio.
3. **Map** each cluster: which existing pages get re-optimized (`re-optimize`
   bucket, with our URL already in the CSV), which need new pages.
4. **Sequence** into a 90-day plan, ordered by effort-to-evidence ratio, not by
   tier alone. Name the assumption behind every timing estimate.
5. **Hand off**: each new page becomes an input to `content-brief.md`.

### Deliverables

```
brands/<brand>/research/mining/competitor-set.md        who, and why they qualify
brands/<brand>/research/mining/merged/keywords-master.csv     everything found
brands/<brand>/research/mining/merged/keywords-validated.csv  what survived
brands/<brand>/research/competitor-playbooks.md         what each rival does structurally
brands/<brand>/reports/keyword-opportunity-plan.md      client-facing
```

The client-facing report carries `Confirmed` and `Likely` findings only, each
with a **Verify** block. For a keyword claim the verify route is the competitor
URL plus the Ctrl+F term that shows the targeting. Run every command before
publishing it.

State plainly in the report: *"This plan carries no search-volume or
difficulty figures. Those require KWFinder or Search Console data, which was
not used for this run."* Never substitute an invented number.

---

## Cost and pacing

- Stage 3 dominates. Cap each miner at 30-40 pages; `crawl_site` is hard-capped
  at 50 and that cap is a feature.
- 5-8 competitors is the working range. Below 3 the repetition signal is too
  weak to mean anything; above 8 the marginal competitor adds noise.
- Miners on a cheap model, Stages 1/5/6 on a strong one.
- If a competitor's site is client-side rendered, pass `wait_seconds: 6` to
  `crawl_pages`. A JS-rendered page that returns an empty shell must be
  reported as "could not read", never as "they have no content there".

---

## Optional: paid metrics (Mangools)

Off by default. Turn on only when the user asks and quota allows.

Stage 2 becomes one **serialized** agent -- never parallel -- that:

1. Calls `kwfinder_get_quota_limits` first and stops if quota is short.
2. Calls `kwfinder_get_competitor_keywords` per competitor (max 1,000 keywords,
   sorted by estimated organic visits).
3. Calls `kwfinder_find_competitor_domains` **after** step 2, since it requires
   a competitor-keywords lookup on the same URL within 24 hours.
4. Calls `kwfinder_get_keyword_gap_analysis` with our domain against 1-5
   competitors -- keywords they rank for and we do not.

Pace the calls; the API allows only a few per short window. Data from this
stage is `Confirmed` ranking data and outranks any crawl inference it conflicts
with. Write it to `mining/metrics/keywords_confirmed.json` and extend the merge
join rather than replacing the free signals.

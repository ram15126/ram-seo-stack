---
name: geo-cite
description: >
  Make a post citable by AI engines, and measure whether it actually gets cited.
  Covers the extractable-block spec, per-domain tactic selection from the GEO
  paper, per-platform differences, and the off-site half. Use when the user
  wants to be cited by ChatGPT, Perplexity, Gemini or AI Overviews, or asks
  about AEO/GEO/llms.txt.
---

# Get the post cited

**Read `_process/blog-content-sop.md` §3 first.** This playbook executes it.

---

## Step 0 — Kill the myths before spending anything

Google's own words, from *AI features and your website*:

> "There are no additional requirements to appear in AI Overviews or AI Mode,
> nor other special optimizations necessary."

> "You don't need to create new machine readable files, AI text files, or markup
> to appear in these features. There's also no special schema.org structured
> data that you need to add."

**This kills `llms.txt` as a Google AI ranking factor.** It costs almost nothing
to maintain and other tools may read it, so having one is not wrong. It must
never be sold to a client as a Google AI ranking factor or presented as a
competitive advantage. Note that one popular open-source GEO tool weights
llms.txt at 18/100 of its score; that weighting is not evidence-backed.

The only two things that gate AI Overview eligibility:

1. The page is **indexed**
2. The page is **eligible to show with a snippet**

So `noindex`, `nosnippet`, `max-snippet:0` and `data-nosnippet` exclude content
from AI features. Check these before diagnosing anything more exotic —
`preflight_audit.py` does it.

Traffic from AI features appears in Search Console under the standard "Web"
search type. It is not broken out.

---

## Step 1 — The extractable-block spec

These are what an AI actually lifts. Every substantial post gets them.

1. **Answer block, 50–70 words**, immediately after the H1 or first H2.
   Self-contained: names its own subject, gives the verdict, needs no
   surrounding context. Opens with a definition pattern — "X is…", "X refers
   to…". A block starting "It is…" cannot survive being lifted.
2. **Key-fact opener per major section**, 60–130 words, same rules.
3. **A facts table** where the subject allows: claim, value, source. Tables
   extract more reliably than prose.
4. **An FAQ** in question form, answers 2–4 sentences, wired to `FAQPage`
   schema. **The schema text must match the visible text exactly** — a mismatch
   is a structured-data violation. `preflight_audit.py` diffs them
   programmatically; do that rather than eyeballing it.
5. **A sources list**, real and checkable.

---

## Step 2 — Pick the tactic by domain, not by template

This is the GEO paper's actual contribution and almost every tool ignores it.
Measured across 10,000 queries:

| Tactic | Lift (Position-Adjusted Word Count) | Wins in |
|---|---|---|
| **Quotation addition** | **+41%** | People & society, explanation, history |
| **Statistics addition** | **+33%** | Law & government, debate, opinion |
| **Fluency optimisation** | **+29%** | Business, science, health |
| **Cite sources** | **+28%** | Law & government, facts, statements |
| Technical terms | +18% | |
| Authoritative voice | +12% | Debate, history, science |
| **Keyword stuffing** | **−9%** | **Nowhere. It actively hurts.** |

So: classify the post's domain first, then lead with the matching tactic. A
legal explainer earns citations by **sourcing**; a history piece by **quoting**;
a business post by **being well written**; an opinion piece by **taking a
position and backing it with numbers**.

**On the +115.1% figure**, which circulates without its second half — the paper
says cite-sources raised visibility 115.1% *for pages ranked fifth* while the
top-ranked page's visibility *fell 30.3%*. It is a redistribution toward
mid-ranked pages, not free lift. Good news if you rank fifth. Quote both halves
or neither.

**Limits to state honestly:** the study simulates a two-stage generative
pipeline rather than testing live ChatGPT or Perplexity. Treat the ranking of
tactics as robust, the percentages as directional.

---

## Step 3 — Per platform, because they barely overlap

Only ~11% of domains are cited by both ChatGPT and Perplexity. AI Overviews and
AI Mode cite the same URL about 13.7% of the time. **You cannot optimise once.**

From a 680M-citation study:

| Engine | Leans toward |
|---|---|
| **ChatGPT** | Wikipedia (47.9% of its top-10 sources), Reddit, Forbes, G2 |
| **AI Overviews** | Reddit, YouTube, Quora, LinkedIn; listicle-heavy |
| **Perplexity** | Reddit (6.6%), YouTube, forums, expert Q&A |

Reddit is the one source all three cite heavily. Roughly 48% of AI search
citations come from user-generated and community sources overall.

Practical read: if the brand is absent from Reddit and YouTube, on-page work
alone will not produce recommendation-query citations.

Length also splits by platform — AI Overviews skew short (53.4% of citations to
pages under 1,000 words), ChatGPT skews long. Do not state a length target; see
`_process/content-length-splits-by-ai-platform.md`.

---

## Step 4 — Measure, do not just score

This workspace has something most GEO tooling does not: **actual citation
monitoring**, via `mcp__mangools__ai_search_watcher_*`.

- `ai_search_watcher_generate_prompts` / `add_monitor_prompts` — the queries the
  brand should be cited for
- `ai_search_watcher_list_models` — which engines are covered
- `ai_search_watcher_get_monitor` / `list_monitor_prompts` — the results

Mind the quota; it is tight. Set monitors up once for the queries that matter
rather than polling broadly.

A citability score is a prediction. A monitor is a measurement. When you have
the measurement, lead with it and label the score as the prediction it is.

---

## Step 5 — The off-site half, and the honesty that goes with it

On-page work makes a page *citable*. It does not make it *cited* for
recommendation queries ("best X", "who should I use for Y"). For those, an AI
looks for the same name across independent sources.

Ahrefs, 75,000 brands, Spearman correlation:

| Factor | ChatGPT | AI Mode | AI Overviews |
|---|---|---|---|
| YouTube mentions | 0.737 | 0.740 | 0.712 |
| Branded web mentions | 0.664 | 0.709 | 0.656 |
| Domain Rating | 0.266 | 0.285 | 0.326 |
| Number of backlinks | weak — well below branded mentions | | |

Being *talked about* correlates far more strongly than being *linked to*.
Domain Rating — the metric most agencies sell against — sits near the bottom.

**Ship the caveat with the table, every time.** Ahrefs' own words: *"correlation
isn't causation. We've spotted patterns between search metrics and AI mentions,
but that doesn't mean improving these metrics will automatically boost your AI
visibility."* Do not promise causal lift.

The rough 30% on-site / 70% off-site split remains `Likely` — a rule of thumb,
not a measurement. The direction is now `Confirmed`.

---

## Output

- Eligibility verdict first (indexed, snippet-eligible) — everything else is
  moot if these fail.
- The extractable blocks, **written out ready to paste**, not described.
- The domain classification and the tactic chosen, with the reason.
- Per-platform notes where they differ.
- Off-site actions, with the causation caveat attached.
- Never promise citation. Give ranges and name the assumption.

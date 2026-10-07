---
axis: sops
slug: keyword-research
status: active
last_verified: 2026-09-07
tiers_used: [T1, T4]
depends_on: [ranking-systems-evidenced, indexing, measurement-free-stack]
summary: A free-stack keyword research process — practitioner method from Nathan Gotch, graded, adapted to India/local, and cross-checked against our verified layer.
---

# Keyword Research — Free Stack

> **Reader note.** This is a graded write-up of one practitioner's method, adapted by the repo author. Mentions of `registry/`, `fundamentals/`, `corpus/` and `data/` point to the author's private research library and are not included here; the claims they support are quoted with sources where they matter.

## Provenance and how to read this

**Method source:** Nathan Gotch (Gotch SEO), *"My Complete SEO Keyword Research Process"*,
YouTube `9CajZ7SJQ_w`, 2h22m, transcript archived at
`corpus/transcripts/9CajZ7SJQ_w.txt` with timestamps. Every claim below is traceable to
a timestamp.

**Tier: [T4] — practitioner method, single operator, no controlled evidence.**

**Incentives, flagged as required:** he sells the keyword template referenced throughout,
sells **Rankability** (his SEO SaaS, pitched repeatedly and claimed to be "better than
Claude or OpenAI" for this), runs a lead-magnet checklist, and has a book out. The video
is partly a product demo. That does **not** make the method wrong — it means the "this
is too much manual work, use my tool" framing is a sales argument, not a finding.

**How we grade it.** Process claims and factual claims are judged differently:
- **Process** — is it coherent, executable, and does it fail safely? Judged on merit.
- **Facts** — needs a source. Most of his don't have one. Marked below.

He is transparent about the soft parts, to his credit: *"this is not an exact science by
any means. These are my own kind of weighting of these different variables"* [26:02].

---

## The system — six steps

1. **Build a keyword database** (a sheet you can filter)
2. **Pick ONE category to dominate** — not blanket research
3. **Find ideas** from 7–10 sources
4. **Filter** the set down hard
5. **Analyse individual keywords** in depth
6. **Prioritise into a 30–90 day sprint**

## Step 0 — The concept that drives everything: five stages of awareness

[3:06–6:08] Order your targeting by **how close the searcher is to buying**, and
**start at the bottom of the funnel, not the top.**

| Stage | Query shape | Priority |
|---|---|---|
| **Most aware** | "hire [brand] SEO consultant", "Nike cleat discount code", "[tool] free trial" | **Build first** |
| **Product aware** | "[brand] reviews" — brand still in query | Second |
| **Solution aware** | **"best + solution (+ location)"** | *"Where most of the magic happens"* |
| Problem aware | "why isn't my website ranking on Google" | Later |
| Unaware | "how do I get more customers online" | Last |

> *"Don't start at unaware. This is not where you want to start… it's very seductive to
> see all that search volume."* [6:08]

**Why this matters for local and small-business sites:** the "best + solution + location" band is
the sweet spot for Indian local and D2C businesses, and it's the band he says to track in both
classic search and AI answers.

## Step 1 — Demand, not volume

[6:53–9:13] **The core correction.** Volume is *one* variable, not the decider.
*"This is one of the biggest newbie mistakes."*

**Four independent proofs of demand:**
1. **Search volume** — Google Ads Keyword Planner
2. **GSC impressions** — does this topic already get impressions?
3. **User signals** — is anyone discussing it on Reddit/Quora?
4. **First-party data** — what do prospects actually ask you on calls?

**The 80/20 allocation:** 80% of topics should have *some* proven demand; **20% reserved
for zero-volume experimental bets.**

> **Zero search volume is not a reason to skip a keyword** — especially local, and
> especially for new/trending topics, because *"all the data you see in [Keyword Planner]
> is lagging data"* [38:25]. He argues the advantage is precisely there, because
> most SEOs filter on volume alone.

**[T4] claim to treat with caution:** *"there's a lot of bot impressions"* in GSC [7:39].
Plausible, unsourced, and not something we've verified. Don't repeat it to a client as fact.

## Step 2 — The other selection variables

**CPC as a commercial-intent proxy** [9:59]. High CPC means advertisers are paying, so
the term converts. His counter-intuitive read: **no advertisers is a warning, not a blue
ocean** — *"someone wasted their money here more than likely."* **[T4], but the logic is
sound and cheap to check.**

**Organic CTR / SERP features** [10:45]. Count everything that steals a click — AI
Overview, PAA, local pack, shopping, ad blocks. He counts them literally: *"six different
things that are going to take away from organic CTR"* [59:58]. **Bake that into the
traffic projection before committing.**

**Competition at three levels** [11:32–13:48]: domain link profile, page link profile,
and **brand level** for AI answers. Plus **content quality**: *"If they've got subject
matter experts creating their content, you're also going to need to get subject matter
experts. You are not going to be able to come in with some AI slop and beat them."*

> **Our note:** the brand-level/AI portion sits in territory our library has
> **quarantined** — see `registry/AUDIT-LOG.md`. Use the domain/page/content assessment.
> Treat his AI-visibility claims as unverified.

## Step 3 — Where to find keywords, free

In his own words: *"I don't personally use free methods… it's really not scalable"*
[30:39]. Noted — and also the setup for the tool pitch. The free path works; it's slower.

| # | Source | Notes |
|---|---|---|
| 1 | **Google Search Console** | **Start here. Best free source, and the best source for local** — *"a lot of these tools just don't have the data and GSC actually surfaces more data for local queries"* [32:59] |
| 2 | **Google Ads Keyword Planner** | **Geo-filter to the target city** so volume is real local volume, not national |
| 3 | **Reddit** | Find national discussions, then localise them |
| 4 | **Google People Also Ask** | Keep expanding it; it keeps generating |
| 5 | **Perplexity** | Trending topics that have no volume yet |
| 6 | **AI + your own knowledge base** | First-party topic ideas from your own documents |
| 7 | Autocomplete / related searches | Implied throughout |

**On (6):** he describes building an "SEO super intelligence" in Claude from knowledge
files and generating topics from it. **That is what this repository already is.** Point
it at `validated/` and `data/` and you're running that step with a graded corpus rather
than an ungraded one.

### The localisation rule — the sharpest single idea in the video

[44:34–45:20] **Only add a location modifier where the answer genuinely varies by
location.**

- ✅ "How much does an SEO consultant cost **in Chennai**" — pricing genuinely varies
- ❌ "What is creatine **in Chennai**" — creatine is creatine. *"You're just literally
  trying to manipulate the algorithms, plus people aren't going to search that."*

**Another example:** "<product> price in Bangalore" passes (price and availability vary).
"Benefits of <ingredient> in Bangalore" fails.

### Query expansion
[41:31] Don't stop at the seed. "B2B SEO St. Louis" → **"best B2B SEO agencies in
St. Louis"**. Adding modifiers *widens* long-tail capture rather than narrowing it.

## Step 4 — The database

Columns he uses: approval · priority · **source** · **cluster** · keyword · SERP features
· volume · KD · CPC · **position** · current URL · **intent** · **opportunity** ·
keyword type · status · notes · scoring columns.

**Two classifications that carry the strategy:**

**Opportunity, set by current position** [19:09]:
| Position | Class | Action |
|---|---|---|
| **2–15** | **Low-hanging fruit** | **Always highest priority.** Improve the existing page |
| 50+ | Clustering opportunity | Build a dedicated page |
| Not ranking | Untapped | New page required |

**Keyword type** [22:12–23:43]:
- **Primary** — the one core topic of the page. **One per page, no exceptions.**
- **Variation** — slight variant, same page, no action needed
- **Secondary** — ranking on this page but *badly* (e.g. position 67) because the page is
  too broad → **signal to splinter off a dedicated page**

> *"Poor performance is the best signal"* that a page is too broad for a query it's
> picking up. Genuinely useful diagnostic.

**One core topic per page**, placed in: URL, title tag, meta description, H1, and first
sentence [21:26].

## Step 5 — Scoring

He scores volume, KD, CPC, position, intent, relevance, target word count, lowest
competitor domain score, and SERP-feature count into a total.

**[T4] — the weights are entirely his own and he says so.** Don't present the number to a
client as objective. What survives is the *principle*: **never decide on one metric.**
*"If you use just one data point, let's say you just use volume, that's not really
enough."* [57:38]

**Two of his inputs need paid tools** (keyword difficulty, lowest competitor domain
score). On the free stack, drop them and lean on position, intent, CPC, SERP-feature
count and relevance. **The model degrades gracefully** — which is a point in its favour.

## Step 6 — Filter down and sprint

**The funnel:** 500–1,000 raw → ~100 → **25–50 per cluster** → 10–20 to execute.

> *"The skill is how do you take this big keyword set and then figure out what the heck
> to actually work on."* [43:47]

**Sprints of 30–90 days on ONE cluster.** His argument for it is operational, not
algorithmic, and it's the best business point in the video: agencies fall into *"this
perpetual loop of we're doing SEO every month for the client and it never feels like
anyone's ever really finishing anything."* Sprints create completion.

**Pick one cluster and over-invest**: *"attack this cluster super hard to the point where
anyone that tries to come and attack this cluster has no chance."*

---

## Where this connects to our verified layer

**1. His best heuristic has a mechanism he doesn't give — and our DOJ material supplies it.**

He says prioritise positions 2–15 because *"it's easier to get big gains"*. True, but the
real reason is stronger. From **PXR0357** [T1]: NavBoost runs **early, to cull the
candidate pool** before expensive scoring. A page at position 8 **has already survived
that cull.** On-page work can move it because it is already in the set. A brand-new page
must first *enter* the candidate set — a different and harder problem that on-page work
alone cannot solve.

**So his heuristic is right, and now it's mechanistically justified rather than
intuitive.** That's a genuine upgrade to the method.

**2. "Don't chase volume alone" agrees with our evidence discipline** — single-metric
decisions are how folklore takes hold.

**3. One-core-topic-per-page** is the practical form of avoiding cannibalisation, and sits
consistently with `fundamentals/canonicalization.md`: multiple pages targeting one intent
get clustered and Google picks the canonical, not you.

**4. His "count the SERP features stealing CTR"** is the same logic as the AI-impression
dilution correction in `sops/measurement-free-stack.md`.

## Adapting it to a new site

- **GSC needs a verified property.** That is his best source, and the only free one with real
  local query data, so verify a property (even your own site) before you start.
- **Keyword Planner needs a Google Ads account.** Free to create; volumes stay bucketed
  (ranges) unless you are spending.
- **Reddit is thinner for Indian local queries.** Weight Indian sources higher: marketplace
  autocomplete (Amazon.in, Flipkart), Quora India, YouTube comments, and community discussion
  where you can see it.

## Open questions this raises
- Is "positions 2–15" the right band, or is it folklore with a plausible story? The
  mechanism supports *some* band; the specific numbers are unsourced.
- Does CPC actually predict conversion value in Indian SMB verticals, where ad markets
  are thinner? Testable against a client's own Ads data.
- His zero-volume advice is directionally supported by the lagging-data argument, but
  we have no measurement of the hit rate on those 20% bets. Track it.

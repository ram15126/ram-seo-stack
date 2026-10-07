# Blog content SOP — length, Google's rules, citation, design, and what to publish

**Scope:** every brand in this workspace. No client facts here by design.
**Written:** 21 August 2026. **Re-check the numbers:** February 2027 (six months).
**Revised 25 August 2026** — §3a corrected against the GEO paper at source (the
tactic ranking was wrong and the +115.1% figure was quoted without its −30.3%
counterpart); §3a-bis added (per-domain tactic selection); §3d upgraded from
`Likely` to `Confirmed` with the Ahrefs 75,000-brand correlation study; §1 flagged
as contested per `content-length-splits-by-ai-platform.md`.

Every figure below is sourced. Where a claim is inference rather than measurement
it says so. If a number here has no source next to it, that is a bug — fix it.

---

## 1. Length: the question is settled, and the answer is "it depends, within a range"

### What Google says

Google's own helpful-content documentation asks, as a *warning sign* that you are
writing for search engines rather than people:

> "Are you writing to a particular word count because you've heard or read that
> Google has a preferred word count? (**No, we don't.**)"
>
> — [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

That is definitive. There is no target to hit. Anyone quoting "Google wants 1,500+
words" is quoting an SEO blog, not Google.

### What the data says — and it is not what most SEO blogs claim

Two large studies, checked at source. **Neither finds that longer content ranks
better.**

**Finding A — no correlation between length and ranking position.**
Backlinko analysed **11.8 million Google search results**. The average word count of
a top-10 result is **1,447 words**, but word counts were **"evenly distributed"
across the top 10** — the study found no direct correlation between length and
ranking position. It reports that longer content helps with *link acquisition*, not
with position.
[Source](https://backlinko.com/search-engine-ranking) · `Confirmed` — read from the
study page, 21 Aug 2026

> **Correction worth knowing.** The widely-repeated claim that "position 1 averages
> 1,890 words, page-two results average 902" is **not** from this study. It
> circulates attached to it, but the 11.8M analysis gives no position-1 figure at
> all. Those numbers are misattributed — do not repeat them, and correct them if a
> client quotes them.

**Finding B — shorter pages get cited by AI.**
Ahrefs analysed **174,048 pages** cited across **560,346 AI Overviews**:

| Cited page length | Share of citations |
|---|---|
| Under 350 words | 16.6% |
| 350–1,000 words | 36.8% |
| 1,000–2,000 words | 30.6% |
| Over 2,000 words | 16.0% |

> **Contested — added 25 Aug 2026.** Other studies measuring *other engines* find
> the opposite (Authoritas: cited pages average 2,290 words; SE Ranking: 2,900+ word
> pages earn 59% more **ChatGPT** citations). The disagreement is real and it is
> platform-shaped — AI Overviews skew short, ChatGPT skews long. Never quote a
> cross-platform length average as a target. See
> `content-length-splits-by-ai-platform.md` in this folder before using any length
> figure with a client.

**53.4% of all AI Overview citations go to pages under 1,000 words.** The Spearman
correlation between word count and citation position is **0.04 — essentially zero**.
Mean cited page: 1,282 words. Position 1 cited pages average 1,270 words; positions
4–10 average 1,690 — longer pages sit *lower* among cited results.
[Source](https://ahrefs.com/blog/short-vs-long-content-in-ai-overviews/) · `Confirmed`

**Finding C — the link correlation inverts at ~1,000 words.**
Ahrefs found a positive correlation between word count and backlinks *up to* 1,000
words, and a negative correlation above it. `Confirmed` (published study)

### What this actually means

Three independent measurements — Google's own statement, an 11.8M-result ranking
study, and a 560k-citation AI study — point the same way: **length is not a ranking
or citation lever.** The measured correlations are approximately zero in both
directions.

Length still matters, but only as a consequence of other things:

- Enough words to cover the topic completely, because completeness is what ranks
- Few enough that the useful part is easy to lift, because extractability is what
  gets cited
- Under ~1,000 words when link acquisition is the goal (Finding C)

**The operating rule:**

> Match total length to the intent. Put short, self-contained, liftable blocks
> *inside* long pages.

A 4,000-word pillar with a 60-word answer block at the top can serve both. The same
pillar written as a continuous essay serves only the first.

### Length by content type — the working table

Set these as a **starting range, not a target.** Write what the topic needs, then
check you are inside the range; if you are well outside it, ask why.

| Content type | Range | Rationale |
|---|---|---|
| Direct answer / definition page | 300–800 | Sits in the 53.4% citation sweet spot |
| FAQ / support answer | 300–700 | Extractability is the whole job |
| Standard informational post | 800–1,500 | Around the 1,282-word mean of cited pages |
| Comparison ("X vs Y") | 1,000–2,000 | Highest AI citation *rate* of any page type — see §5 |
| How-to / tutorial | 1,000–2,000 | Steps expand it naturally; do not pad |
| Listicle / roundup | 1,200–2,500 | 19.6% of AI citations |
| Pillar / complete guide | 2,500–5,000 | Ranks on completeness; needs internal liftable blocks |
| Original research / data study | 1,500–3,000 | Length is whatever the data needs |

**Hard rule:** never pad to reach a range. `word-count-is-not-content-quality.md`
in this folder documents a real case where ranking pages by word count surfaced the
site's *worst* content as its best. Length answers "is there enough here to rank."
It does not answer "is this good."

---

## 2. Google's actual rules

### 2a. The helpful-content self-assessment — use it as a publishing gate

These are Google's own questions, quoted. Run a draft against them before it ships.
Any "no" is a rewrite, not a note-for-later.

**Content and quality**
- Does the content provide original information, reporting, research, or analysis?
- Does it provide a substantial, complete, or comprehensive description of the topic?
- Does it provide insightful analysis or interesting information beyond the obvious?
- If it draws on other sources, does it avoid simply copying or rewriting them, and
  instead provide substantial additional value and originality?
- Does the title provide a descriptive, helpful summary, and avoid exaggerating or
  being shocking?
- Is this the sort of page you'd want to bookmark, share, or recommend?
- Would you expect to see this content in or referenced by a printed magazine,
  encyclopedia, or book?
- Is the content produced well, or does it appear sloppy or hastily produced?

**Expertise**
- Is this written or reviewed by an expert or enthusiast who demonstrably knows the
  topic well?
- Does the content present information in a way that makes you want to trust it —
  clear sourcing, evidence of expertise?
- Does it have any easily-verified factual errors?

**The "Who / How / Why" test**
- **Who:** Is it self-evident who authored the content? Do pages carry a byline
  where one is expected? Do bylines lead to further information about the author?
- **How:** Is the use of automation, including AI-generation, self-evident to
  visitors? Are you providing background about how it was used, and why it was
  useful?
- **Why:** Was this created primarily to help people, or primarily to attract
  search engine visits? The second misaligns with Google's systems.

Google states that of E-E-A-T, **"trust is most important. The others contribute to
trust, but content doesn't necessarily have to demonstrate all of them."**

### 2b. The "avoid" list, in Google's words

- Content primarily made to attract visits from search engines
- Producing lots of content on many different topics hoping some performs
- Using extensive automation to produce content on many topics
- Mainly summarising what others say without adding much value
- Writing about things simply because they seem trending

### 2c. The spam policies that actually apply to blogging

From [Google's spam policies](https://developers.google.com/search/docs/essentials/spam-policies):

| Policy | Definition (Google's wording) | Where a blog trips it |
|---|---|---|
| **Scaled content abuse** | "when many pages are generated for the primary purpose of manipulating search rankings and not helping users" | Publishing AI-generated posts at volume. Note the test is *purpose and value*, not whether AI was used. |
| **Site reputation abuse** | hosting third-party content mainly to exploit the site's ranking authority | Accepting guest posts or sponsored content unrelated to the site's subject |
| **Keyword stuffing** | "filling a web page with keywords or numbers in an attempt to manipulate rankings" | Repeating the target term unnaturally; city/region blocks |
| **Link spam** | buying/selling links, excessive exchanges, automated link creation | Any paid link without `rel="sponsored"` |
| **Doorway abuse** | "sites or pages created to rank for specific, similar search queries" leading to intermediate pages | Near-duplicate posts per keyword variant |

**On AI specifically:** Google does not ban AI-assisted writing. It bans using
automation "to produce content for the primary purpose of manipulating search
rankings." The line is value and intent. But see §7 — for some brands the
positioning risk is separate from and larger than the ranking risk.

---

## 3. Writing to be cited — SEO and GEO

### 3a. What actually moves AI citation, ranked by measured effect

From **"GEO: Generative Engine Optimization"** (KDD 2024; Princeton, IIT Delhi,
Georgia Tech, Allen Institute). Nine tactics, **10,000 queries** (GEO-bench:
8,000 train / 1,000 val / 1,000 test), nine datasets, 25 domains.

> **Corrected 25 Aug 2026.** An earlier version of this table led with "Cite
> sources — up to +115.1%" and put quotations third. That ordering was wrong: the
> +115.1% is a narrow sub-result, not the headline. The table below is the paper's
> Table 1, re-read at source. Correct this if it has already gone to a client.

The paper's primary metric is **Position-Adjusted Word Count (PAWC)** — how much
of the generated answer your source accounts for, weighted by position. Baseline
is 19.5.

| Tactic | PAWC | vs baseline | What it means in practice |
|---|---|---|---|
| **Quotation addition** | 27.8 | **+41%** | Quote named authorities directly. The strongest single tactic |
| **Statistics addition** | 25.9 | **+33%** | Replace vague quantifiers with specific figures |
| **Fluency optimisation** | 25.1 | **+29%** | Clean, well-structured prose |
| **Cite sources** | 24.9 | **+28%** | Name and link sources inline |
| Technical terms | 23.1 | +18% | Domain vocabulary, used correctly |
| Easy-to-understand | 22.2 | +14% | Plain language |
| Authoritative voice | 21.8 | +12% | State findings plainly; stop hedging |
| Unique words | 20.7 | +6% | Marginal |
| **Keyword stuffing** | 17.8 | **−9%** | **Actively harmful.** SEO's oldest lever inverts here |

`Confirmed` — peer-reviewed, re-read at source 25 Aug 2026.
The paper's second metric, Subjective Impression, ranks the top four the same way
(quotations highest). Exact SI percentages are omitted here deliberately — two
readings of the table disagreed slightly, and the ordering is the robust part.

**What the +115.1% actually says.** In the paper's own words:

> "The Cite Sources method led to a substantial 115.1% increase in visibility for
> websites ranked fifth in SERP, while on average, the visibility of the
> top-ranked website decreased by 30.3%."

So it is a **redistribution, not a free gain** — citing sources pulls visibility
*down* the SERP toward mid-ranked pages. Good news if you rank fifth. Quoting the
+115.1% without the −30.3% is the kind of half-figure that gets caught.

### 3a-bis. The finding almost everyone misses: the winning tactic changes by domain

This is the paper's actual contribution (Table 3), and no open-source GEO tool
surveyed implements it. **Do not apply one template across a whole blog.**

| Tactic | Wins in |
|---|---|
| **Cite sources** | Law & Government, Facts, Statements |
| **Statistics addition** | Law & Government, Debate, Opinion |
| **Quotation addition** | People & Society, Explanation, History |
| **Authoritative voice** | Debate, History, Science |
| **Fluency optimisation** | Business, Science, Health |

Read: a legal or factual post earns citations by **sourcing**; a history or
society post by **quoting**; a business or health post by **being well written**;
a debate or opinion post by **taking a position and backing it with numbers**.
Classify the post's domain first, then pick the tactic.

**Limits to state honestly.** The study simulates a two-stage generative pipeline
rather than testing live ChatGPT or Perplexity, so external validity is limited.
Treat the *ranking* of tactics as robust, the exact percentages as directional,
and the domain split as the most useful part.

### 3b. The extractable-block spec

Every substantial page gets these. They are what an AI actually lifts.

1. **An answer block, 50–70 words**, immediately after the H1 or first H2.
   Self-contained: names its own subject, gives the verdict, needs no surrounding
   context. Opens with a definition pattern — "X is…", "X refers to…".
2. **A key-fact opener per major section**, 60–130 words, same rules.
3. **A facts table** where the subject allows: claim, value, source. Tables extract
   more reliably than prose.
4. **An FAQ** in question form, with answers 2–4 sentences, wired to `FAQPage`
   schema. **The schema text must match the visible text exactly** — a mismatch is
   a structured-data violation. Diff them programmatically before shipping.
5. **A sources list**, real and checkable.

### 3c. What Google says about optimising for AI features — read this before buying anything

From [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features):

> "There are no additional requirements to appear in AI Overviews or AI Mode, nor
> other special optimizations necessary."

> "You don't need to create new machine readable files, AI text files, or markup to
> appear in these features. There's also no special schema.org structured data that
> you need to add."

**This kills several popular claims.** `llms.txt` does **not** help a page appear in
Google's AI features — Google has said so explicitly. It may still be read by other
tools, and it costs almost nothing to maintain, so it is not *wrong* to have one.
But it must never be sold to a client as a Google AI ranking factor, and it should
not be presented as a competitive advantage without saying what it does and does
not do.

The two things that genuinely gate AI Overview eligibility:

- The page must be **indexed**
- The page must be **eligible to show with a snippet**

Which means `nosnippet`, `max-snippet:0` and `data-nosnippet` will exclude content
from AI features. Check these before diagnosing anything more exotic.

Traffic from AI features appears in Search Console under the standard "Web" search
type — it is not broken out separately.

### 3d. The off-site half — now with measurement behind it

On-page work makes a page *citable*. It does not make it *cited* for
recommendation-style queries ("best X", "who should I use for Y"). For those, an AI
looks for the same name appearing across independent sources.

**Upgraded 25 Aug 2026.** The ~30/70 on-site/off-site split was previously labelled
`Likely` — reasoned, not measured. Ahrefs has since published a **Spearman
correlation study across 75,000 brands** covering ChatGPT, AI Mode and AI Overviews,
and it supports the *direction* strongly:

| Factor | ChatGPT | AI Mode | AI Overviews |
|---|---|---|---|
| **YouTube mentions** | **0.737** | **0.740** | **0.712** |
| YouTube mention impressions | 0.717 | ~0.717 | ~0.717 |
| **Branded web mentions** | **0.664** | **0.709** | **0.656** |
| Branded anchors | 0.511 | 0.628 | 0.527 |
| Branded search volume | 0.352 | 0.466 | 0.392 |
| Ad traffic | 0.286 | 0.254 | 0.216 |
| Domain Rating | 0.266 | 0.285 | 0.326 |
| Branded traffic | 0.235 | 0.357 | 0.274 |
| Number of backlinks | weak — well below branded mentions on all three surfaces | | |

[Source](https://ahrefs.com/blog/ai-brand-visibility-correlations) · `Confirmed`
— read at source 25 Aug 2026.

**What this changes.** Being *talked about* correlates far more strongly with AI
visibility than being *linked to*. Domain Rating — the metric most agencies sell
against — sits at 0.27—0.33, below branded anchors and far below plain mentions.
YouTube is the single strongest correlate on every surface, which is not where most
blog budgets go.

**The caveat ships with the finding — always.** Ahrefs' own words:

> "correlation isn't causation. We've spotted patterns between search metrics and AI
> mentions, but that doesn't mean improving these metrics will automatically boost
> your AI visibility."

Do not promise causal lift from this table. It tells you where to look, not what to
guarantee. The **ratio** (30/70) remains `Likely` — a rule of thumb, not a
measurement. The **direction** is now `Confirmed`.

The practical consequence is unchanged and now better supported: budget real time
for getting mentioned elsewhere, and never promise AI citation from on-page work
alone.

---

## 4. The design system

Presentation is not decoration here — it changes whether the page gets read and
whether text can be extracted. Specs below were measured off well-typeset
long-form sites, not chosen by eye.

### 4a. Reference measurements

| Property | Measured reference | Use |
|---|---|---|
| Body size / leading | 17px / 1.6 | 17–18px, leading 1.6–1.7 |
| Body colour on dark | `#d0d6e0` on `#08090a` | ≥ 12:1 contrast |
| Line length | 73 characters | **66–75**, never above 80 |
| H1 | 48px, line-height 1.0, −0.022em | Tight leading, negative tracking |
| H2 lead-in space | 56px | 48–68px above each H2 |

### 4b. Non-negotiables

- **Contrast:** body ≥ 12:1, all text ≥ 4.5:1 (WCAG AA). Measure it, do not eyeball
  it — dim grey on near-black is the most common failure and it reads as "cheap."
- **Surfaces, not outlines.** Cards need a genuinely lighter background than the
  page. Hairline boxes drawn straight onto the ground look flat.
- **Text in HTML, never in SVG or images.** SVG `<text>` does not wrap or reflow, and
  neither search engines nor AI crawlers extract text from images. Build charts and
  timelines in HTML/CSS. See §4c.
- **Tables scroll inside their own `overflow-x:auto` container.** The page body must
  never scroll sideways.
- **Mobile first in practice, not slogan.** Check the real mobile share in Search
  Console — it is routinely 70%+ — and test at 375px, 490px and 768px.

### 4c. Two bugs that have already cost time in this workspace

**1. `ch` is not a character.**
`1ch` is the width of the "0" glyph, which is materially wider than the average
character. Measured on Inter: `1ch` = 12.6px while the average character is 9.56px.
So `max-width: 70ch` renders at roughly **92 characters**, well past readable.
**Set the measure in `rem` and verify by measuring rendered characters.**

**2. Grid gutters do not collapse when space runs out.**
A layout of `minmax(0,210px) | text | minmax(0,210px)` does *not* drop the gutters
first on a narrow screen. CSS Grid shrinks all three tracks **proportionally by
their max sizes**, so at ~490px the gutters still took ~90px each and the reading
column rendered at about half width — roughly 22 characters per line.
**Step the gutter down at breakpoints** (e.g. 210px → 64px → 0) rather than trusting
grid to do it. This is invisible on a desktop browser and only shows in the
400–1000px band: phones in landscape, small tablets, split-screen.

### 4d. Verify before shipping

Measure, do not eyeball. At minimum, at 375 / 490 / 768 / 1440px:

- rendered characters per line (target 66–75 desktop, 35–55 mobile)
- contrast ratio for every text role
- `document.documentElement.scrollWidth <= innerWidth` (no page-level overflow)
- no element wider than the viewport except tables inside their scroll container
- no grid child overflowing its own row

---

## 5. What to publish — content types that actually work

### 5a. AI citation share by page type

Across **25,337 citations** from ChatGPT, Perplexity, Gemini, AI Overviews and AI
Mode: articles **23.7%**, listicles **19.6%**, product pages **16.3%**.

The more useful number is *citation rate*, not share: **comparison pages earn 1.87
citations per retrieval — the highest of any page type.**

Platform differences are large and worth planning around:
- **ChatGPT** — 43% of its citations come from articles and listicles alone
- **AI Overviews** — listicle-dominant (46.3%)
- **Perplexity** — favours forums, community discussion, expert Q&A
- **UGC overall** — roughly 48% of AI search citations come from user-generated and
  community sources (Reddit, YouTube, LinkedIn)

`Confirmed` as published studies; note these are third-party samples and the figures
move. Re-check before quoting to a client.

### 5b. What earns links

Original research and data studies, "why" explainers, and comprehensive "what"
guides earn disproportionately more links than opinion pieces or standard how-tos.
The mechanism is simple: journalists and bloggers need something to cite, and
original data makes you the primary source.

### 5c. The publishing mix

Structure a plan across the funnel and research the split rather than assuming a
ratio.

| Type | Job | Funnel | Notes |
|---|---|---|---|
| **Pillar / complete guide** | Own the head term, anchor the cluster | TOFU | One per cluster; everything links back to it |
| **Definition / "what is X"** | Capture the definitional query | TOFU | Short, highly citable |
| **Comparison "X vs Y"** | Highest AI citation rate | MOFU | Include competitors honestly — see below |
| **Listicle / roundup** | AI Overview share | TOFU–MOFU | Needs a consistent evaluation framework per item |
| **Original research / data** | Links and authority | Any | The single best link-earning format |
| **How-to / tutorial** | Practical intent | MOFU | Each step: one action plus what goes wrong |
| **Case study** | Proof | BOFU | Lead with the result |
| **Glossary / FAQ hub** | Long tail, extractability | TOFU | Cheap; compounds |
| **Opinion / POV essay** | Brand voice, shareability | Any | Poor for links, good for being remembered |

**On comparison pages:** a page listing only your own offering is marketing, and AI
treats it as marketing. A page that honestly maps the landscape — competitors named —
is a *source*. You only get named alongside the alternatives if you name them first.
This will feel wrong to publish and it is still correct.

### 5d. What not to publish

- Near-duplicate posts per keyword variant — that is doorway abuse
- "Everything you need to know" pages with nothing the reader could not get elsewhere
- Trend posts with no angle of your own
- Anything where the honest answer to "does this provide substantial additional
  value over the sources it draws on?" is no

---

## 6. The pre-flight gate

A draft ships only when every line is true.

**Substance**
- [ ] Passes the §2a questions with no "no"
- [ ] Contains something no competitor page has: own data, own experience, a
      correction, a primary source others did not read
- [ ] Every number has a source; no invented figures, no soft quantifiers
- [ ] Facts spot-checked against the primary source, not a secondary blog

**Extractability**
- [ ] 50–70 word answer block, self-contained, definition pattern
- [ ] Key-fact opener on each major section
- [ ] FAQ present, schema text diffed against visible text and matching exactly
- [ ] Sources listed and links resolve

**Technical**
- [ ] Indexable, snippet-eligible — no `noindex`, `nosnippet`, `max-snippet:0`
- [ ] `Article` + `Person` author + `BreadcrumbList` (+ `FAQPage` if applicable)
- [ ] Author byline resolves to a real author page
- [ ] Canonical, title ≤ ~60 chars, description ~150–160
- [ ] 3–5 internal links; cluster pages link back to the pillar
- [ ] Added to sitemap; submitted to Search Console **and Bing Webmaster Tools**

**Presentation**
- [ ] 66–75 characters per line desktop, measured not estimated
- [ ] Contrast measured, all roles ≥ 4.5:1
- [ ] Verified at 375 / 490 / 768 / 1440px with no overflow
- [ ] All meaningful text is HTML text, not baked into an image or SVG

**Record**
- [ ] Logged in the brand changelog with a verify date
- [ ] Verify date set **8–16 weeks out** — new content does not rank sooner, and
      judging at four weeks produces a wrong conclusion

---

## 7. The AI-authorship question

Google permits AI-assisted content and judges it on value and intent (§2c). That is
the search answer. It is not the whole answer.

Two separate risks:

1. **Search risk** — low, provided the content is genuinely useful and not produced
   at scale to manipulate rankings.
2. **Positioning risk** — brand-specific and potentially total. Any brand whose
   public promise involves human craft, original authorship, or "no AI" cannot
   publish generated prose or generated imagery. One screenshot ends the claim.
   Check the brand's stated positioning before drafting, not after.

Where a named individual is the byline, drafted first-person passages are
placeholders, not copy. Mark them, list them, and get the person's real words before
publishing. Putting invented recollections in a real person's mouth is not a
style problem.

---

## Sources

1. Google — [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
2. Google — [Spam policies for Google web search](https://developers.google.com/search/docs/essentials/spam-policies)
3. Google — [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
4. Ahrefs — [Short vs. Long Content in AI Overviews](https://ahrefs.com/blog/short-vs-long-content-in-ai-overviews/) (174,048 pages, 560,346 AI Overviews)
5. Backlinko — [We Analyzed 11.8 Million Google Search Results](https://backlinko.com/search-engine-ranking) — top-10 average 1,447 words, **no** correlation with position
6. Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan, Deshpande — *GEO: Generative Engine Optimization*, KDD 2024 — [arXiv:2311.09735](https://arxiv.org/abs/2311.09735) · [full text](https://arxiv.org/html/2311.09735v3) (Table 1 and Table 3 re-read at source 25 Aug 2026)
7. AirOps / Delta V — page-type AI citation studies, 25,337 citations across five AI surfaces
8. Ahrefs — [AI brand visibility correlations](https://ahrefs.com/blog/ai-brand-visibility-correlations) (75,000 brands, Spearman, ChatGPT / AI Mode / AI Overviews)
9. Google — [US 11,354,342 B2, *Contextual estimation of link information gain*](https://patents.google.com/patent/US11354342B2/en) (filed 2018, granted **June 2022** — not 2024)
10. This folder — `word-count-is-not-content-quality.md`, `content-length-splits-by-ai-platform.md`

## Related notes in this folder

- `word-count-is-not-content-quality.md` — why length must never stand in for quality
- `content-length-splits-by-ai-platform.md` — why the length studies disagree, and
  why the answer is per-engine rather than a single number
- `common-crawl-proves-crawler-access.md` — proving crawler access properly
- `schema-script-blind-spots.md` — schema detection traps

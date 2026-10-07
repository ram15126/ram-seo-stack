# Technique 01: Information Gain Writing

## What It Is
Writing content that adds genuinely NEW information compared to what already ranks
for a keyword. The idea comes from Google's patent **US 11,354,342 B2 — "Contextual
estimation of link information gain"** (Victor Carbune, Pedro Gonnet Anders; Google
LLC), **filed 18 October 2018, granted 7 June 2022**.

> **Read `## Status` at the bottom before using this in client-facing work.** The
> technique is sound as a writing discipline. The claim that Google scores
> information gain in live ranking is **not established**, and this file previously
> asserted it as fact.

## Why It Works
The patent describes comparing a candidate document against documents **the user has
already been shown** in the same session. A document that repeats what the user just
read scores low; one that adds material they have not seen scores high. Note the
comparison set: it is *user-session-relative*, not "your page vs the top 10".

Whether Google runs this in production is unknown — see `## Status`. What survives
regardless is the writing discipline: a page that says only what the other results
say gives no reason to be read, ranked, or cited.

The May 2024 Content Warehouse API leak contains an `OriginalContentScore`
attribute. The name is suggestive, but the leak documents **attribute names and
types, not whether or how they are used in ranking**. Treat it as `Likely`
supporting context, not confirmation — and never present it to a client as proof.

**Algorithm reasoning:** If 10 pages all explain "how to do X" the same way, Google gains nothing by showing an 11th identical page. But if page 11 adds a case study, original data, or a contrarian perspective? That's information gain — value the user can only get from YOUR page.

## Step-by-Step Process

### Step 1: SERP Gap Analysis
1. Search the target keyword and read the top 10 results fully
2. Create a spreadsheet: rows = topics covered, columns = each competitor
3. Mark what each competitor covers and — critically — what they DON'T cover
4. Identify patterns: where do all 10 say the same thing? Where do they disagree?
5. Note the "missing angles": perspectives, data types, or use cases nobody addresses

### Step 2: Unique Value Identification
6. Ask: "What do I know about this topic that these 10 pages don't include?"
7. Sources of unique value:
   - **First-party data**: "We analyzed 500 customer accounts..."
   - **Original case studies**: "Client X tried this and here's what happened..."
   - **Expert interviews**: "I spoke with [Name], who said..."
   - **Contrarian perspective**: "Most guides say X. In our experience, Y works better because..."
   - **Process documentation**: "Here's the exact 9-step process we use internally..."
   - **Failure stories**: "We tried the common approach and it failed because..."
   - **Tool comparison**: "We tested 4 tools and measured actual results..."
8. Select 3-5 information gain elements to include

### Step 3: Content Architecture
9. Structure the article to lead with unique insights, not rehashed basics
10. Place information gain elements in the first 30% of the content (Google evaluates engagement early)
11. Use unique headings that signal novel content (not generic "What is X?" and "Benefits of X")
12. Plan specific data points, quotes, and examples for each section

### Step 4: Writing with Information Gain
13. Every section must answer: "What can the reader ONLY learn here?"
14. Replace generic statements with specific ones:
    - Bad: "Many companies have seen success with this approach"
    - Good: "We implemented this for 12 e-commerce clients in 2025. Average conversion improvement was 23%, but 3 clients saw no change — all in the B2B space"
15. Add "not found elsewhere" sections: edge cases, failure modes, advanced tips

## Hidden Tips & Tricks

- **The "So What?" test**: After every paragraph, ask "So what? Where can I ONLY read this?" If the answer is "anywhere," the paragraph has zero information gain.
- **Use your analytics**: Your GSC data, your customer data, your A/B test results — these are information gain goldmines that competitors literally cannot replicate.
- **Cite non-obvious sources**: Everyone cites HubSpot and Ahrefs. Cite academic papers, industry reports from niche organizations, or government data nobody else uses.
- **The 10-10-80 rule**: 10% covering basics (for context), 10% discussing what the competition says, 80% unique content. Most AI content is 80-10-10 — the opposite.

## Common Mistakes

1. **Thinking "more words" = information gain** — A 5,000-word article repeating the same points as competitors has zero information gain. A 1,500-word article with original data has high gain.
2. **Adding information gain at the end** — Google evaluates engagement early. Put unique insights in the first 500 words, not the conclusion.
3. **Fabricating data** — Never make up statistics for information gain. One fabricated stat that gets fact-checked destroys all credibility.
4. **Confusing "different format" with "different information"** — Putting the same information in a table instead of paragraphs isn't information gain.

## When to Use This Technique

- **Always** for competitive keywords (keyword difficulty > 30)
- For any content where you have access to unique data or experiences
- When updating content that lost rankings (likely lost due to competitors with higher information gain)
- Critical for pillar/hub content that anchors a topic cluster

## Status — what this patent does and does not establish

**What the patent actually says.** Verified against the primary source on
25 August 2026 — https://patents.google.com/patent/US11354342B2/en

> "An information gain score for a given document is indicative of additional
> information that is included in the given document beyond information contained
> in other documents that were already presented to the user."
> — US 11,354,342 B2, abstract

**Two claims removed from this file because they were wrong:**

1. **The grant date was given as June 2024.** It is **June 2022** (filed 2018).
   The 2024 date appears to come from conflating the patent with the May 2024 API
   leak. It is repeated widely in SEO writing; correct it if a client quotes it.

2. **A quotation was attributed to the patent that does not appear in it.** The
   sentence *"Information gain scores indicate how much more information one source
   may bring to a person who has seen other sources on the same topic. Pages with
   higher information gain scores may be ranked higher."* was presented here as
   something the patent "explicitly describes." It is a third-party paraphrase in
   circulation, not patent text. The real abstract is quoted above. Do not reuse the
   old sentence.

**What is genuinely uncertain:**

- Google has **never confirmed** this is in production. A granted patent is
  evidence of an idea Google thought worth protecting, not of a shipped system.
- The described mechanism is **session- and user-relative** — scored against
  documents *this user* already saw. The common SEO reading ("your page vs the top
  10") is a convenient proxy, not what the patent describes.
- The patent describes **two** applications: an automated assistant abbreviating
  what it reads aloud, and search-result ranking — the latter phrased as
  "in some implementations."

**The honest framing for a client:** this describes plausibly how an AI assistant
or search system decides which source to show *next*, to someone who has already
read something on the topic. That makes it a good model for the AI-citation era. It
is not a confirmed ranking factor and must not be sold as one.

**Label findings accordingly:** the writing technique is `Confirmed` useful. Any
claim that Google *scores* your page's information gain is `Unverified`.

**Tools Used:**
- keyword search — identify target keyword landscape
- competitor data — analyze who ranks for this topic
- opportunity detection — find keywords where we rank 4-20
- SERP feature detection — identify featured snippet / PAA opportunities
- page-level SEO data — analyze current page performance if updating

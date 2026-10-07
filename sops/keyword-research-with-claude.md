# Keyword research with Claude, on free tools

By Ramakrishnan S ([growwithram.in](https://growwithram.in)) · v1, 7 October 2026
The numbers below come from running this on my own site in September and October 2026.

**The idea:** keyword tools are expensive and most cap how many searches you can run. This is the system I
built to do the same job with Claude Code and Google's free tools. Claude does the sorting, matching and
drafting. **You** check it, because AI tools get things wrong, and this system is built around catching that.

## What it costs

| Part | Cost |
|---|---|
| Google Search Console | Free |
| Google Keyword Planner ("Get search volume") | Free with a Google Ads account, no ad spend needed. Without spend you get **ranges**, not exact numbers |
| Google Autocomplete | Free (unofficial endpoint, can rate-limit you) |
| Reddit thread titles, People Also Ask, competitor sitemaps | Free if you collect them by hand (see step 2) |
| Claude Code | **A paid plan.** The rest of the stack is free |
| Optional: scraping/search APIs, paid keyword tools | Not needed. A few scripts in `skills/seo/` can use them if you have keys |

No paid *keyword tool* is required. That is not the same as "everything is free", so I don't say that.

## The six steps

### 1. Start with what Google already shows your site for (Search Console)
Export **Performance → Queries and Pages** for the last 3 months. Use a **Domain property** if you can: it also
shows subdomains.
*Ask Claude:* "Read Queries.csv. List the searches this site already appears for, grouped by page. Flag any at
positions 2 to 15."

### 2. Listen to buyers in public
Read how real people phrase the problem. Three free sources:
- **Reddit thread titles.** Search Google for `site:reddit.com "your topic"` and copy the **titles** (and links).
- **People Also Ask.** Copy the questions from your own browser's results page.
- **Competitor page names.** Their `sitemap.xml` is public; the URL slugs show what each competitor decided deserves a page.

A thread title proves **at least one person phrased the problem that way**. It is **not search volume**: never report it as volume.
*Ask Claude:* "Group these titles by the problem being described. Quote the buyer's wording. Note where the top
answers contradict each other. Do not treat any of this as volume."
*What this found on my site:* 61 Reddit thread titles over 6 topics. 16 were the same question about pages Google
won't index, with contradicting answers. 18 showed buyers can't tell AEO, GEO and SEO apart.

### 3. Check what people actually type (Autocomplete)
`python skills/keyword-stack/scripts/autocomplete_expand.py --seeds "your seed" --gl in --out autocomplete.csv`
It tries seven shapes of each seed (`X`, `X for`, `X vs`, `is X`, `what is X`, `how to X`, `best X`) and writes a dated CSV.
Run it for each market you sell in and keep phrases that show up in both.
Google says predictions "reflect real searches". That proves a phrase **exists**, not that it is big.

### 4. Read how big each search is (Keyword Planner)
In Google Ads → Tools → Keyword Planner → **Get search volume**, paste your candidate list, set the location and
date range, and read the monthly **range** (10–100, 100–1K, 1K–10K, 10K–100K, 100K–1M) plus the 3-month and
year-on-year change. Read it on screen or download the CSV yourself.
- The "competition" column is about **advertisers**, not how hard it is to rank.
- **Date every reading.** A range belongs to the day you read it (see rule 1 below).
- *On my site:* 669 searches read. 24 were in the 1K–10K band, 90 in 100–1K, 319 in 10–100, 236 under 10 or no data. **None** reached 10K.

### 5. Score them
`python skills/keyword-stack/scripts/score_keywords.py keywords.csv --out scored.csv`
**Score = demand × 3 + fit × 3, out of 30.** Demand comes from the range band (1K–10K = 3, 100–1K = 2, 10–100 = 1 ...).
**Fit** is yours, 0 to 5, set after **reading the page the search would lead to**:
5 = a service you sell in a buyer's words · 4 = a problem you fix · 3 = wider knowledge your buyers read · 2 = off positioning.
- If most people mean something else by a word (a film, a place, a brand), mark it `mixed`: demand drops one step.
- **Report ties as ties.** Three keywords on 21 are three keywords on 21, not "first, second, third".

### 6. One main search per page, then draft the titles
Give each page **one** main search, and no two pages the same one. Leave pages that already rank near the top alone: change least
what is working. Ask Claude to draft a title and meta description per page (my house rule: titles of 60 characters or fewer),
then **you** read and tweak every one.
*On my site:* 10 of my 13 service pages were aimed at a smaller search than they needed to be. My free audit page targeted a
phrase with no data, while "free seo audit" reads 1K–10K. I rewrote titles and descriptions on 36 pages.

## The rules that came from mistakes

| What went wrong | The rule |
|---|---|
| A report line rested on a volume band that was two months old and a fresh reading contradicted it | **Date every range.** Re-read at the start of each round. If you already sent it, correct it the same day and say so |
| My own first report said to retitle a post for "how to rank in AI overviews", but the study behind the post measured Perplexity, not Google AI Overviews | **Never claim more than the evidence measured.** Check the claim against the source, then fix it the same day |
| Head terms that really meant a film, a place or a brand inflated demand | **The `mixed` flag.** Look at who ranks before you trust a head term |
| A fit score came from a product's name, and the product was something else | **Read the page before you score it** |
| The same kind of need scored 3 on one row and 4 on another | **Apply the rubric uniformly.** Re-read the whole column once |
| Pieces were written for searches of 10–100 a month | **Check the range before you write, not after** |
| Typed numbers in a report drifted from the data | **Generate every number from the data by script.** Never retype |
| A range turned into a traffic forecast | **Don't.** A range spans a factor of ten |

## Limits, stated plainly
- Free tools do **not** give exact volume, keyword difficulty or People Also Ask boxes at scale. Leave those columns blank; never guess.
- Autocomplete proves a phrase exists. A Reddit title proves one person said it. Neither is volume.
- This finds good *candidates*. It does not promise rankings, traffic or leads. Nothing here has been measured for outcomes yet beyond the first
  retitling round on one site, and one site isn't proof.
- Method credit: the demand-first, bottom-of-funnel approach follows Nathan Gotch's "My Complete SEO Keyword Research Process" (YouTube 9CajZ7SJQ_w).
  My graded notes on it are in [`keyword-research.md`](keyword-research.md). The method is his; the adaptation and checks are mine.

Want the audit done for you? [growwithram.in/free-seo-audit](https://growwithram.in/free-seo-audit)

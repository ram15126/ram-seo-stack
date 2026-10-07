# My SEO workflow with Claude Code, on free tools

By Ramakrishnan S, SEO and AI-search freelancer · [growwithram.in](https://growwithram.in)
Version 1 · 6 October 2026 · Google sources re-checked on 5 October 2026

This is the workflow I run for client sites and ran on my own site this week. It goes from "I know nothing about this site" to a 30-day plan, in five steps. Claude Code does the crawling, the number-crunching and the first drafts. Every finding has to pass the proof rules below before anyone sees it.

**No Ahrefs, no Semrush, no Screaming Frog, no paid SEO tool.**

---

## The stack and what it costs

| Tool | What I use it for | Cost |
|---|---|---|
| Google Search Console | What Google actually sees: queries, pages, indexing, AI Overview impressions | Free |
| Google Keyword Planner | Monthly search ranges for a list of searches | Free with a Google Ads account, no ad spend needed. Without spend you get ranges (100–1K, 1K–10K), not exact numbers |
| Google Autocomplete | Proof that real people search a phrase | Free |
| Google Trends | What is rising around a topic | Free |
| PageSpeed Insights | Speed and Core Web Vitals | Free |
| Bing Webmaster Tools | Bing's version of Search Console | Free |
| A private browser window | Who ranks on page 1 today | Free |
| Python and `curl` | Crawling every page and checking each finding | Free |
| Claude Code | Runs the crawl scripts, reads the exports, does the maths, drafts the reports | Paid subscription |

---

## The rule that runs every step: proof before claim

My first cold audit made with Claude had **8 wrong findings** in the draft. A second check caught all 8 before anything was sent. Every one came from the same slip: jumping from evidence to a conclusion. Two examples:

- The draft said meta descriptions over about 155 characters "get truncated". Google says: *"There's no limit on how long a meta description can be"* ([source](https://developers.google.com/search/docs/appearance/snippet)). Snippets are cut to fit the screen, which is a different thing.
- The draft said a server response time of about 0.55 seconds was slow, against a "200 ms target". web.dev puts a good TTFB at *"0.8 seconds or less"* ([source](https://web.dev/articles/ttfb)), and TTFB isn't a Core Web Vital.

So now a finding goes into a report only when all of this holds:

1. **There's command output for every number**, and the number was copied, not retyped.
2. **The scope is stated.** "All 202 pages in the sitemap" or "4 of the 8 pages we opened". Never an unstated "every".
3. **It's actually wrong.** Run a control first. Example: before calling a 404 a bug, request a made-up address like `/xyz-not-a-page`. If that behaves the same way, it's normal.
4. **Any rule quoted is quoted from Google or web.dev, word for word, with the link.** If no official source says it, label the line as your own judgement, or drop it.
5. **It's measured twice** if the client could re-measure it (timings, counts).
6. **Every finding ends with "Check it yourself"**: a URL to open or a one-line command, so the client can confirm it without trusting me.

Reports are made by a script that computes every number in the text. Typed numbers drift.

---

## Step 1: Outside-in audit (no access to the site needed)

Use it before a client signs, or on any site you're curious about.

**Claude Code does:**
- Crawls **every** URL in the sitemap, not a sample. For each page: status code, title, H1, meta description, canonical, word count, structured data, internal links.
- Checks the host variants: `http://`, `https://`, with and without `www`. Each should end on one address.
- Requests a made-up URL as a control.
- Opens 2 or 3 page types in a real browser, because some tags are added by JavaScript after the page loads.
- Runs PageSpeed Insights. If the free quota is used up, the report says "not measured". Never estimate Core Web Vitals.

**Check first, every time:** broken internal links, links going through a redirect, pages with no H1, duplicate titles and descriptions, missing or wrong canonicals. In my study of 44 sites audited from outside, these were the most common problems, and every one can be checked without access to the site.

**Rate each finding** Critical, High, Medium, Low or Working. Rate by impact, not by how easy it is to fix. When unsure between two ratings, pick the lower one. A finding the client disproves damages every other line in the report.

**Each finding is written as:** what it means in plain English, what we found (URLs and exact values), why it matters (the Google quote), how to fix it, and how to check it yourself.

**End with** what you could not check from outside: real indexing, rankings, traffic, backlinks. That's the natural next step: "give me Search Console access".

---

## Step 2: Search Console audit (once you have access)

- Use a **Domain property** if you can. It also shows subdomains, which is how a hacked staging subdomain turned up on one site.
- Read every report: Performance (queries, pages, countries, devices), Page indexing, Core Web Vitals, and the **Generative AI** performance report.
- **Inspect pages one by one with URL Inspection.** Reports can lag.

On my own site on 1 October, the indexing report said **28 pages** weren't indexed. It had last been updated 10 days earlier. Inspecting the pages one by one showed the real number was **12**.

- Some red flags aren't problems. "Page with redirect" on the bare domain that forwards to `www` is working as intended. Check before you "fix" it.
- Change nothing during the audit: no indexing requests, no validations. Read first.

---

## Step 3: Keyword research

**Collect the evidence (all free):**

| Source | What it proves | Limit |
|---|---|---|
| Search Console queries | People search it, and Google already shows the site for it | Positions are averages; many queries are hidden |
| Keyword Planner, "Get search volume" | A monthly search range, plus 3-month and year-on-year change | Ranges only without spend. The "competition" column is about advertisers, **not** how hard it is to rank |
| Google Autocomplete | Real people search the phrase. Google: *"autocomplete predictions reflect real searches that have been done on Google"* ([source](https://support.google.com/websearch/answer/7368877)) | Shows that a search exists, not how big it is |
| Autocomplete variants | Questions to answer as sections: `X for`, `X vs`, `is X`, `what is X`, `how to X`, `best X` | Not the "People also ask" box. Label it honestly |
| Page 1 today, in a private window | Whether forums and small sites rank, or only big publishers; whether the search means something else (a film, a place) | One person's view of Google, not a ranking tool |
| Reddit and Quora | The words customers actually use | Titles and snippets only |

**Read Keyword Planner in two passes.** First the head terms, one per topic. Then the longer questions from Autocomplete. In my runs, the head term carried the search volume and the long questions were small. So one article is built on the head term and answers the long questions as sections. Don't plan one article per question.

**Date every range.** A range belongs to the day you read it. One of my head terms read 1K–10K and, two months later, 100–1K.

**Score each keyword** on demand, intent, current position, relevance and how it fits the client's goal. Weight by the goal: impressions first, or sales first. Write the choice and the reason down. Leave blank what the free stack can't give you (exact volume, keyword difficulty) and say so. Never guess it.

**One main topic per page.** Variations go on the page that owns the main topic.

---

## Step 4: The 30-day plan and the titles file

**The plan, in this order:**
1. The 30 days in numbers, computed from the calendar.
2. What the client must hand over or approve before Day 1.
3. One theme per week, and why that order.
4. The calendar: one row per piece with the date, the main search, its monthly range, the page it leads to, and what it needs.
5. What could slow it down.
6. Check it yourself.

**Order:** week 1 publishes what's already written and fixes the page with the most unused impressions. Then one topic group per week, so new articles link to each other. A hub page goes last in its group, so it can link to everything.

**The titles file:** a new title and meta description for every page, built from the keyword research, with no duplicates.

On my own site this week: 683 searches put through Keyword Planner, 36 pages given new titles and descriptions, and a 30-day plan with 10 blog posts.

---

## Step 5: Measure, including AI search

- **Search Console, 28 days after a change against the 28 days before.** Same pages, same window.
- **The Generative AI performance report** shows impressions in AI Overviews and AI Mode by page, country, device and date ([source](https://support.google.com/webmasters/answer/16984139)). It shows no search terms. Google says it *"includes data from the Web search type in the Performance report"*, so AI impressions are already inside your normal totals. Don't add them twice.
- **Check AI crawler access**: make sure robots.txt and the firewall don't block the search bots of ChatGPT, Claude and Perplexity. That's a separate SOP.
- **If the client wants AI answers tracked, a fixed prompt panel** for ChatGPT, Perplexity, Gemini and Claude: the same 50 or so buyer questions, run on a fixed schedule. Record whether the brand is named, cited, and who else is. Compare medians over at least 3 runs; a single run is noise.

**Report three numbers separately:** classic search (clicks, positions), AI impressions from Search Console, and the prompt panel. A site can lose one while holding another.

---

## What this workflow can't do

- No exact search volumes or keyword difficulty. Paid tools estimate these; they don't observe them either.
- No click data from Google's AI features, at any price, as of October 2026.
- Nothing here has a guaranteed outcome. It's a careful process, not a promise of rankings.

---

Want me to run Step 1 on your site? Free audit: [growwithram.in/free-seo-audit](https://growwithram.in/free-seo-audit)

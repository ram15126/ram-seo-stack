---
name: keyword-stack
description: >
  Run a free-stack keyword research round for a site with Claude: Search Console queries, public
  customer-intent research (Reddit titles, People Also Ask, competitor sitemaps), Google Autocomplete,
  Keyword Planner ranges, scoring (demand x 3 + fit x 3), and a one-main-search-per-page plan with
  drafted titles. Use when the user asks for keyword research, "which search should this page target",
  retitling pages, or a keyword shortlist, and wants it without a paid keyword tool. Triggers on
  "keyword research", "keyword stack", "which keyword", "retitle my pages", "score these keywords".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
metadata:
  version: 1.0.0
---

# Keyword stack

A six-step keyword research round on free Google tools. You do the sorting, matching and drafting.
**The user checks every output.** Full write-up: `sops/keyword-research-with-claude.md` in the repo.

## Before you start (ask once, in one message, only for what is missing)
1. The site URL and what it sells, in a sentence.
2. The goal: impressions first, or sales.
3. A Search Console export (Queries and Pages, 3 months, Domain property if possible).
4. Access to Google Keyword Planner in the user's own Google Ads account (no ad spend needed).
5. The list of pages that will own a search.

## The six steps
1. **Search Console.** Read Queries.csv. List what the site already appears for, grouped by page. Flag positions 2 to 15.
2. **Public customer-intent research.** Reddit thread **titles** (Google `site:reddit.com "topic"`, collected by the user or via a search tool they already have), People Also Ask questions pasted from their browser, competitor sitemap slugs. Group by the problem described; quote the buyer's words; note contradictions. **Never present any of it as search volume.**
3. **Autocomplete.** `scripts/autocomplete_expand.py --seeds ... --gl <country>`; run per market; keep phrases seen in both.
4. **Keyword Planner ranges.** The user reads or downloads the ranges. Save them in `templates/keyword-sheet.csv` format with the **date, location and window** at the top.
5. **Score.** Set `fit` (0 to 5) only after **reading the page** each search would lead to. Flag `mixed` words (film, place, brand). Run `scripts/score_keywords.py`. **Report ties as ties.**
6. **Map and draft.** One main search per page; no two pages share one; change least what already ranks near the top. Draft a title and description per page (house rule: titles of 60 characters or fewer). Mark guesses as guesses.

## Gates (do not skip)
- **Date every range.** Re-read at the start of each round; never mix readings; correct a delivered report the same day and mark the correction.
- **Never claim more than the evidence measured.** Check each claim against its source.
- **Numbers come from the data by script.** Never retype a number.
- **No traffic forecast from ranges.** A range spans a factor of ten.
- **A thread title is not volume. Autocomplete is not volume.**
- Leave blank what the free stack cannot give (exact volume, keyword difficulty). Never guess it.
- End every report with a "Check it yourself" section: where to open each figure.
- Never use a client or prospect name in anything that will be published.

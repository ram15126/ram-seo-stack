# Claude SEO Stack

The SEO workflow I run with **Claude Code**: keyword research, audits, AI-search checks and content. It starts with Google's free tools, and every output gets checked by a human.

Built by **Ramakrishnan S**, an SEO and AI-search freelancer in Chennai ([growwithram.in](https://growwithram.in)). Built with Claude Code.

> I'm running SEO on my own site in public for 30 days. The write-ups are on [LinkedIn](https://linkedin.com/in/ramakrishnan15126). The keyword stack below is how I found out 10 of my 13 service pages were aimed at a smaller search than they needed to be.

## What's inside

| Folder | What it is |
|---|---|
| [`skills/keyword-stack/`](skills/keyword-stack/) | **The keyword research stack.** A Claude Code skill plus two small scripts (Google Autocomplete expander, keyword scorer) and a CSV template. Python standard library only |
| [`sops/keyword-research-with-claude.md`](sops/keyword-research-with-claude.md) | **Start here.** The six-step process in plain English, the rules that came from mistakes, and the limits |
| [`skills/seo/`](skills/seo/) | A router skill plus **39 playbooks**, **85 Python scripts** and **125 reference files**: audits, technical SEO, schema, GEO/AEO (AI search), content, local and e-commerce SEO. A merge of four open-source repos plus original work (see [`ATTRIBUTION.md`](ATTRIBUTION.md)) |
| [`skills/blog/`](skills/blog/) | Blog audit and building playbooks (10): topic clusters, information gain, slop gate, GEO citations |
| [`sops/`](sops/) | More SOPs: a free-stack SEO workflow, measuring AI-search visibility on free tools, AI crawler access control, and graded notes on Nathan Gotch's keyword method |
| [`process-notes/`](process-notes/) | 33 short, generic lessons from running audits with AI tools (false positives to watch for, script quirks). No client data |
| [`brands/_template/`](brands/_template/) | An empty per-brand folder layout the `seo` skill expects |

## The keyword stack in one minute

1. **Search Console:** what Google already shows your site for.
2. **Public threads:** Reddit thread titles, People Also Ask, competitor sitemap names, to see how buyers say it.
3. **Autocomplete:** what people type (`autocomplete_expand.py`).
4. **Keyword Planner:** a monthly *range* for every candidate.
5. **Score:** demand × 3 + fit × 3, out of 30 (`score_keywords.py`). Ties stay ties.
6. **One main search per page**, then draft titles. You read and tweak every one.

Full version: [`sops/keyword-research-with-claude.md`](sops/keyword-research-with-claude.md).

## Install

You need [Claude Code](https://claude.com/claude-code) and Python 3.

```bash
# the keyword stack (macOS / Linux)
cp -r skills/keyword-stack ~/.claude/skills/
# Windows PowerShell
Copy-Item -Recurse skills\keyword-stack $env:USERPROFILE\.claude\skills\
```

For the full `seo` + `blog` skills on Windows, run `.\install.ps1` (it links both skills into `~/.claude/skills` and installs `requests`, `beautifulsoup4`, `lxml`). It was written for my Windows setup and I have not tested it elsewhere; on macOS or Linux, copy `skills/seo` and `skills/blog` into `~/.claude/skills/` and install those three packages yourself.

Then ask Claude things like: *"Run the keyword stack for example.com. Here is my Search Console export."* or *"seo audit https://example.com"*.

## What's free and what isn't

| Part | Cost |
|---|---|
| Search Console, Keyword Planner (ranges only, no ad spend needed), Autocomplete, PageSpeed Insights | Free |
| **Claude Code** | **A paid plan** |
| `skills/seo` scripts that call DataForSEO, Mangools, Geoapify or similar | Need your own keys. You don't need them for the keyword stack |

So: **no paid keyword tool is required**. It is not "everything is free", and I won't say it is.

## Limits, stated plainly
- Keyword Planner without ad spend gives **ranges** (like 1K–10K), not exact volumes. Free tools don't give keyword difficulty.
- Autocomplete proves a phrase exists. A Reddit title proves one person said it. **Neither is search volume.**
- This produces good *candidates*. It does not promise rankings, traffic or leads. AI tools get things wrong with total confidence, which is why the process puts a human check at every step.
- Use it on sites you own or are hired to work on, and follow each site's and platform's terms.

## Credits and licences
- Original work here is **MIT-licensed** ([`LICENSE`](LICENSE)).
- `skills/seo/` merges four open-source repos (MIT ×3, Apache-2.0 ×1). Their licences, notices and the full list of changes are in [`ATTRIBUTION.md`](ATTRIBUTION.md) and [`licenses/`](licenses/). Please keep them if you fork.
- The keyword method follows Nathan Gotch's "My Complete SEO Keyword Research Process". The method is his; the adaptation and checks are mine.
- Other skills I use are listed, with links, in [`THIRD-PARTY.md`](THIRD-PARTY.md).

## Not included, on purpose
Client work, client folders and deliverables, prospect lists, and anything with personal or account data.

## Want it done for you?
Free audit: [growwithram.in/free-seo-audit](https://growwithram.in/free-seo-audit)

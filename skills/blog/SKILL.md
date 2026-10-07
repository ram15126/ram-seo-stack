---
name: blog
description: >
  Blog audit and blog building system. Use when the work is about blog CONTENT
  rather than a whole site: auditing a published blog post or an entire blog,
  finding what is wrong with it, topical clustering and topic maps, information
  gain, content cannibalisation, orphan posts, thin or decaying content,
  E-E-A-T and author authority, AEO/GEO citability (getting cited by ChatGPT,
  Perplexity, Gemini, AI Overviews), AI-slop detection, rewrite specs, content
  briefs and drafting. Triggers on "audit this blog", "audit this post",
  "what's wrong with this article", "does this read like AI", "is this AI
  slop", "topical map", "topic cluster", "information gain", "content gap",
  "why isn't this post ranking", "make this post citable", "rewrite this
  article", "blog audit", or a blog-post URL plus a quality question.
  For whole-site technical audits, Core Web Vitals, crawl/index issues,
  backlinks or local/e-commerce SEO, use the `seo` skill instead.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch, Task
metadata:
  version: 1.0.0
---

# Blog System

One router, many playbooks. Load only what the job needs.

This skill is the content half of the search system. The `seo` skill owns the
site; this one owns what is published on it. They share `skills/seo/scripts/`,
`skills/seo/references/` and `_process/` — nothing is duplicated here that
already exists there.

---

## Operating principles

**1. Scripts measure, agents judge.** Every number in every output traces to a
collector run or a cited source. Label each finding `Confirmed` (a script
measured it), `Likely` (reasoned from fetched content) or `Unverified`
(assumption). Client-facing work carries the first two only, with the label
visible. Never present reasoning as measurement.

**2. Length is not quality, and on some sites it inverts.** Word count answers
"is there enough here to rank." It never answers "is this good." On a site with
mixed human and AI authorship, ranking by length reliably surfaces the AI posts
as the best content and the human essays as thin — this has already happened
once here. `blog_inventory.py` deliberately emits word count under `coverage`
and never under anything named quality. Do not undo that in prose.
See `_process/word-count-is-not-content-quality.md`.

**3. Never conclude that text is AI-written.** Report markers, counts and line
numbers; let a human read the passage. GPT detectors carry a ~61.3%
false-positive rate on non-native English writers, and much of the writing in
this workspace is Indian English. The one exception is leaked model markup
(`oaicite`, `contentReference`, `[cite: 1]`, `【】`), which proves provenance
rather than style — that is a hard fail.

**4. There is no single "AI search" to optimise for.** Only ~11% of domains are
cited by both ChatGPT and Perplexity; AI Overviews and AI Mode cite the same URL
about 13.7% of the time. Per-platform work is not a nice-to-have.

**5. Every finding must be independently checkable.** These reports get
forwarded. Each finding carries a **✅ Verify** block and a **falsifiability
line** — "how would we know this was wrong?" Run every command before publishing
it.

---

## Step 0 — Always establish brand context first

This is a multi-brand workspace. Which brand comes before everything else.

1. **Identify the brand.** If it is not unambiguous, **ask** — never infer it
   from whichever brand was discussed most recently.
2. **Read `brands/<brand>/brief.md`.** Read the file; do not rely on what was
   said earlier in the conversation.
3. If no brief exists and this is more than a one-off lookup, run
   `skills/seo/playbooks/intake.md` first.

**Brand isolation — hard rules.** Never carry a fact between brands. A pattern
learned on one brand may be *suggested* for another, but only as an explicitly
labelled suggestion, never as an established fact. One brand per deliverable.
Brand facts go in `brands/<brand>/`, never in global memory. Reusable learnings
go in `_process/`, written generically.

**Before drafting anything, check the brand's positioning on AI authorship.**
Google permits AI-assisted content and judges it on value and intent. That is
the search answer, not the whole answer. A brand whose public promise involves
human craft or original authorship cannot publish generated prose — one
screenshot ends the claim. Check `brief.md` before writing, not after.

---

## Command routing

Match the request to exactly one playbook and read that file. Do not read
playbooks you are not going to use — each is a full document, and loading five
of them wastes the context the work needs.

### Diagnose

| Request | Playbook |
|---|---|
| "audit this post", "what's wrong with this article", a post URL + a quality question | `playbooks/audit-post.md` |
| "audit my blog", "review all my posts", sitemap or blog index URL | `playbooks/audit-blog.md` |
| "why isn't this post ranking", "what am I missing vs the top results" | `playbooks/info-gain.md` |
| "does this read like AI", "is this slop", "check this draft" | `playbooks/slop-gate.md` |
| "who does this look like it's by", "does this have authority", E-E-A-T | `playbooks/authority.md` |

### Plan

| Request | Playbook |
|---|---|
| "topical map", "topic cluster", "what should the blog cover" | `playbooks/cluster-map.md` |
| "make this citable", "get cited by ChatGPT/Perplexity/AI Overviews" | `playbooks/geo-cite.md` |
| "write a brief", "what should this post say", rewrite spec | `playbooks/brief.md` |

### Produce

| Request | Playbook |
|---|---|
| "write the post", "draft this" | `playbooks/write.md` |
| "turn this into a client report" | `playbooks/report.md` |

### Hand off to the `seo` skill

| Request | Where |
|---|---|
| Whole-site technical audit, crawl/index, Core Web Vitals | `skills/seo/playbooks/audit-technical.md` |
| Schema implementation beyond a single post | `skills/seo/playbooks/schema.md` |
| Backlinks, link building, brand mentions off-site | `skills/seo/playbooks/links-building.md`, `skills/seo/playbooks/geo-brand-mentions.md` |
| Keyword volume and difficulty numbers | `skills/seo/playbooks/research-keywords.md` + `scripts/mangools_keywords.py` |
| Shipping the fix into the site's source | `skills/seo/playbooks/ship-code.md` |

When a request spans several, run them in sequence and say which sequence you
chose before starting.

---

## The fact pack

Every audit playbook builds a **fact pack** first, then reasons over it. Agents
read the fact pack, not the live page, except where they need to read prose.

Run scripts from the workspace root. On Windows, `export PYTHONIOENCODING=utf-8`
first or emoji output crashes them mid-run.

### For one post

```bash
export PYTHONIOENCODING=utf-8
S=skills/seo/scripts
python $S/preflight_audit.py   "$URL" --json > /tmp/pack/preflight.json
python $S/slop_markers.py      "$URL" --json > /tmp/pack/slop.json
python $S/citability_scorer.py "$URL" --json > /tmp/pack/citability.json 2>/dev/null
python $S/eeat_signal_checker.py "$URL" --json > /tmp/pack/eeat.json
python $S/entity_checker.py    "$URL" --json > /tmp/pack/entities.json
python $S/readability.py --url "$URL" --json > /tmp/pack/readability.json
python $S/freshness_checker.py "$URL" --json > /tmp/pack/freshness.json
```

Then, with competitor URLs **in ranking order** (this script does not fetch a
SERP — supply them from SerpChecker, the Mangools MCP, or by reading the SERP):

```bash
python $S/info_gain_matrix.py "$URL" --competitors "$C1" "$C2" "$C3" \
    --questions-file questions.txt --json > /tmp/pack/infogain.json
```

### For a whole blog

One polite collection pass, then read the capture — never re-crawl:

```bash
python $S/site_collect.py --site "$SITE" --out audits/capture.json --delay 4
python $S/blog_inventory.py audits/capture.json --path-contains /blog/ --json \
    > /tmp/pack/inventory.json
python $S/duplicate_content.py "$SITE" --json > /tmp/pack/duplicates.json
```

With a Search Console export, add decay:

```bash
python $S/content_decay_detector.py --csv gsc-export.csv --json > /tmp/pack/decay.json
```

`crawl4ai` MCP (`crawl_page`, `crawl_pages`, `crawl_site`) is the fetcher for
JS-rendered posts — it renders and respects robots.txt.

**Measuring actual AI citation.** `mcp__mangools__ai_search_watcher_*` monitors
whether a URL or brand is actually cited by AI engines. That is measurement, not
scoring. Mind the quota; see `playbooks/geo-cite.md`.

---

## Shared references

Do not preload these. Playbooks name the one they need.

| File | Holds |
|---|---|
| `_process/blog-content-sop.md` | **The doctrine.** Length, Google's rules, GEO tactics, extractable-block spec, pre-flight gate |
| `_process/word-count-is-not-content-quality.md` | Why length must never stand in for quality |
| `_process/content-length-splits-by-ai-platform.md` | Why the length studies disagree |
| `skills/seo/references/anti-slop-ruleset.md` | **Canonical** anti-slop rules, versioned vocabulary, calibration baseline |
| `skills/seo/references/information-gain-writing.md` | Information gain method, and `## Status` on what the patent does not establish |
| `skills/seo/references/gap-classification-rubric.md` | Core / Differentiator / Commodity / Opportunity |
| `skills/seo/references/eeat-scoring-rubric-compact.md` | E-E-A-T bands, 30-second heuristic |
| `skills/seo/references/geo-scoring-methodology.md` | Weighted GEO composite |
| `skills/seo/references/llm-audit-rubric.md` | Output contract; sanctions an `article` scope |

---

## Output contract

Every audit deliverable carries, in this order:

**A) Summary** — scope, what was measured, top 3 problems, top 3 opportunities.

**B) Findings table** — `Area | Severity | Confidence | Finding | Evidence | Fix`.

**C) Per finding, a ✅ Verify block.**
- *Visible problems* → the exact page URL plus the Ctrl+F term that exposes it.
  Not the domain, not "the FAQ section" — the specific URL.
- *Invisible problems* (schema, headers, canonicals, indexability) → the raw
  evidence quoted inline, plus a command or free browser tool that reproduces
  it. Prefer a no-login browser route first.
- **Run every command before publishing it.** A verification step that does not
  reproduce is worse than none.

**D) Per finding, a falsifiability line** — "how would we know this was wrong?"

**E) Prioritised action plan.**

**F) What was not measured**, stated plainly. Substance, quality and whether the
topic is worth owning are not script-measurable. Say so rather than implying
coverage you do not have.

### Never

- State a number no collector produced or no source supports.
- Use word count in a sentence about quality.
- Call a page AI-written.
- Promise rankings or citation. Give ranges and name the assumption.
- Let a correlation become a causal promise — including the Ahrefs AI-visibility
  correlations, which ship with their own "correlation isn't causation" caveat.

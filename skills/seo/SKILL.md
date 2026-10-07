---
name: seo
description: >
  Complete SEO + AEO + GEO system for client brand sites. Use for any search
  work: audits, technical SEO, Core Web Vitals, crawl/index issues, schema and
  structured data, keyword research, topic clusters, semantic gap analysis,
  content briefs, writing and improving content, E-E-A-T, backlinks and link
  building, local SEO, e-commerce SEO, programmatic SEO, international/hreflang,
  and AI search work (GEO, AEO, llms.txt, AI crawler access, citability, AI
  Overviews, ChatGPT/Perplexity/Claude/Gemini citations, brand mentions). Also
  use for client deliverables: audit reports, PDF reports, proposals, and
  month-over-month progress comparisons. Triggers on "seo", "audit my site",
  "why am I not ranking", "traffic dropped", "optimize for AI search", "get
  cited by ChatGPT", "schema markup", "keyword research", "content brief",
  "write a blog post for <brand>", or any bare URL plus an SEO-shaped question.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch, Task
metadata:
  version: 1.0.0
---

# SEO System

One router, many playbooks. You load only what the job needs.

**Operating principle: evidence over opinion.** Anyone can assert that a page is
slow or thin. This system runs scripts that measure, then labels every finding
`Confirmed` (script evidence), `Likely` (reasoning from fetched content), or
`Unverified` (assumption). Client-facing findings must be `Confirmed` or
`Likely`, and the label must appear in the report. Never present reasoning as
measurement.

**Second principle: most target sites are code, not WordPress.** These are
custom sites, frequently built with Claude Code (Next.js, Astro, Vite, plain
static). Do not recommend plugins. The fix is an edit to the source — and you
can make it. An audit that ends in a list of recommendations is half-finished
work; see `playbooks/ship-code.md`.

---

## Step 0 — Always establish brand context first

This is a multi-brand workspace. Establishing *which* brand comes before
everything else.

1. **Identify the brand.** If it is not unambiguous from the request, **ask** —
   do not infer it from whichever brand was discussed most recently.
2. **Read `brands/<brand>/brief.md`.** Read the file; do not rely on what was
   said earlier in the conversation.
3. If you are inside the site's own repo, also check
   `.agents/product-marketing.md`, `.claude/product-marketing.md`, `CLAUDE.md`
   or `README.md`.
4. If no brief exists and the task is more than a one-off lookup, run
   `playbooks/intake.md` to create one. Once per brand; every later job reads it
   instead of re-asking.

Never ask the user questions the brief already answers.

### Brand isolation — hard rules

- **Never carry a fact between brands.** Competitors, keywords, stack, voice,
  findings and scores are brand-specific. A pattern learned on one brand may be
  *suggested* for another, but must be labelled a suggestion, never stated as
  fact.
- **Never write brand facts to global memory.** They go in `brands/<brand>/`.
  Test: *"would this still be true if this client left tomorrow?"* If no, it
  belongs in the brand folder.
- **One brand per deliverable.** No document references two brands — these get
  sent to clients.
- Genuinely reusable, client-neutral learnings go in `_process/`.

---

## Command routing

Match the request to exactly one playbook and read that file. Do not read
playbooks you are not going to use — each one is a full document, and loading
five of them wastes the context you need for the actual work.

### Diagnose

| Request | Playbook |
|---|---|
| Full site audit, "audit my site", health check | `playbooks/audit-full.md` |
| One page, "why doesn't this page rank" | `playbooks/audit-page.md` |
| Crawl/index, robots, canonicals, redirects, CWV | `playbooks/audit-technical.md` |
| Content quality, thin content, decay | `playbooks/audit-content.md` |
| Images, alt text, weight, formats | `playbooks/audit-images.md` |
| Backlink profile, anchor text, link health | `playbooks/audit-links.md` |
| Sitemap structure and coverage | `playbooks/audit-sitemap.md` |
| hreflang, international targeting | `playbooks/audit-hreflang.md` |

### AI search (GEO / AEO)

| Request | Playbook |
|---|---|
| "Will AI cite this?", citability scoring | `playbooks/geo-citability.md` |
| AI crawler access, GPTBot/ClaudeBot/PerplexityBot in robots.txt | `playbooks/geo-crawlers.md` |
| llms.txt — analyze or generate | `playbooks/geo-llmstxt.md` |
| Per-platform tuning (ChatGPT, Perplexity, AI Overviews) | `playbooks/geo-platforms.md` |
| "Is our brand mentioned in AI answers?" | `playbooks/geo-brand-mentions.md` |
| Featured snippets, People Also Ask | `playbooks/aeo-snippets.md` |
| Answer-engine structure, direct-answer formatting | `playbooks/aeo-answers.md` |

### Research

| Request | Playbook |
|---|---|
| Keyword research, difficulty, intent | `playbooks/research-keywords.md` |
| Topic clusters, pillar/spoke architecture | `playbooks/research-clusters.md` |
| "We rank #7, what's missing?" | `playbooks/research-semantic-gap.md` |
| "Who are my competitors?", competitor keywords, "what should we copy from them", keyword gap | `playbooks/research-competitor-mining.md` |
| Competitor and alternatives pages ("X vs Y", comparison pages) | `playbooks/research-competitors.md` |
| Quarterly strategy, where to invest | `playbooks/plan.md` |

### Produce

| Request | Playbook |
|---|---|
| Content brief for a writer | `playbooks/content-brief.md` |
| Write the post | `playbooks/content-write.md` |
| Improve an existing post | `playbooks/content-improve.md` |
| E-E-A-T signals, author authority, YMYL | `playbooks/content-eeat.md` |
| Source real expertise to beat AI-generic content | `playbooks/content-expert-interview.md` |
| Schema / structured data | `playbooks/schema.md` |
| Link building and outreach | `playbooks/links-building.md` |

### Ship

| Request | Playbook |
|---|---|
| **Implement the fixes in the site's code** | `playbooks/ship-code.md` |
| Pages at scale from a dataset | `playbooks/niche-programmatic.md` |

### Niche verticals

| Request | Playbook |
|---|---|
| Local business, Google Business Profile, maps | `playbooks/niche-local.md` |
| E-commerce, product/collection pages | `playbooks/niche-ecommerce.md` |

### Deliver

| Request | Playbook |
|---|---|
| Client-ready written report | `playbooks/report-client.md` |
| Prep to walk a client through the audit on a call | `playbooks/call-prep.md` |
| PDF report with scores and charts | `playbooks/report-pdf.md` |
| Proposal / pitch from audit findings | `playbooks/proposal.md` |
| "Did we improve?" month-over-month | `playbooks/compare-monthly.md` |
| Log what shipped, so results are attributable | `playbooks/changelog.md` |

When a request spans several (e.g. "audit and fix"), run them in sequence and
say which sequence you chose before starting.

---

## Evidence scripts

`scripts/` holds 83 Python collectors. They are the difference between an
audit and an opinion. Run them; do not simulate their output.

**Read `scripts/INDEX.md` before invoking any script.** Calling conventions are
not uniform across the set — some take a positional URL, others `--url` — and
the index lists the real usage line for each. Guessing wastes a call.

**On Windows, always export `PYTHONIOENCODING=utf-8` first.** Several scripts
print emoji status icons, and the default `cp1252` console encoding crashes on
them mid-output — losing findings that were already collected.

```bash
export PYTHONIOENCODING=utf-8
python "skills/seo/scripts/ai_crawler_policy_matrix.py" https://example.com
python "skills/seo/scripts/audit_runner.py" --help
```

First run only, install the three dependencies:

```bash
python -m pip install requests beautifulsoup4 lxml
```

High-value collectors:

| Script | Answers |
|---|---|
| `audit_runner.py` | Orchestrates a full evidence pass |
| `crawl_audit.py` | Site crawl: status codes, depth, orphans |
| `robots_checker.py` / `robots_path_tester.py` | Is Google actually allowed in? |
| `ai_crawler_policy_matrix.py` | Which AI crawlers are allowed or blocked |
| `citability_scorer.py` | Passage-level AI citation score |
| `citation_readiness.py` / `answer_block_scanner.py` | Extractable answer blocks |
| `llms_txt_checker.py` / `llms_txt_generator.py` | llms.txt audit and generation |
| `validate_schema.py` / `schema_required_props.py` | Schema validity and gaps |
| `pagespeed.py` / `lcp_subparts.py` / `critical_request_chain.py` | Core Web Vitals |
| `indexability_matrix.py` / `canonical_checker.py` | Index eligibility per URL |
| `internal_links.py` / `orphan_pages_from_sitemap.py` | Internal link equity |
| `content_decay_detector.py` / `freshness_checker.py` | What to refresh |
| `eeat_signal_checker.py` | Author, citation, and trust signals |
| `javascript_render_audit.py` | Content that only exists after JS runs |

**Schema caveat that matters on these sites.** `WebFetch` and `curl` strip
`<script>` tags, so JSON-LD frequently appears missing when it is present.
Confirm with `validate_schema.py`, the browser tool
(`document.querySelectorAll('script[type="application/ld+json"]')`), or Google's
Rich Results Test before reporting "no schema found". On JS-rendered sites also
run `javascript_render_audit.py` — reporting a false negative to a client costs
more credibility than the finding was worth.

Scripts needing Playwright (`capture_screenshot.py`, `analyze_visual.py`,
`mobile_render_checker.py`, `visual_regression_snapshot.py`) are optional; skip
them and label the affected findings `Likely` rather than blocking.

---

## References

`references/` holds the rubrics the playbooks cite — `llm-audit-rubric.md`
(evidence standards and severity), `geo-scoring-methodology.md`,
`eeat-framework.md`, `cwv-thresholds.md`, `schema-types.md`, `quality-gates.md`,
plus per-topic material and `references/agents/` role definitions for parallel
specialist passes on large audits.

---

## Self-verification — run this before anything leaves

Mandatory between finishing the analysis and writing the deliverable. Findings
have failed re-testing before; a false alarm in front of a client costs more
than a missed issue.

Take your own findings and **try to disprove them**:

1. **Re-run the evidence.** Every command or script that produced a `Confirmed`
   label, run again. A finding that does not reproduce is not a finding.
2. **Check it against `_process/`.** The false-positive register exists because
   these traps have already been paid for once — parser artefacts, soft 200s,
   truncated crawls, `curl -L` masking a redirect. If a finding matches a known
   pattern there, treat it as a false positive until proven otherwise.
3. **Prove absence properly.** "X is missing" is the easiest claim to get wrong.
   `WebFetch` and `curl` strip `<script>`; headless browsers cannot see
   lazy-loaded content; an HTTP 200 does not prove a file exists. Confirm the
   fetch actually measured what you are claiming.
4. **Demote what you cannot re-prove.** `Confirmed` → `Likely`, or cut it.
   Never carry a label you could not reproduce five minutes ago.
5. **Run every ✅ Verify command** exactly as written, against the live site.
   If it does not reproduce for you, it will not reproduce for the client.

Say in the report that this pass was run. It is the reason the findings can be
trusted.

## Output discipline

Client-facing deliverables follow `references/client-report-style.md` — the
house format: severity-ordered sections, a prose executive summary that leads
with what is already right, and every finding as
*In plain terms → Detail → Recommended fix → ✅ Check it yourself*.

Every deliverable, without exception:

1. **Severity-ordered**, never chronological. Critical → High → Medium → Low.
   A client should be able to stop reading after Critical and still have gotten
   the value.
2. **Every finding carries** a confidence label, the evidence (script output,
   quoted HTML, URL), the specific fix, and where the fix goes.
3. **Effort marked** — S / M / L — so the user can negotiate scope.
4. **No invented numbers.** If you did not measure traffic, keyword volume, or
   rank, do not state it. "Estimated" is not a license to make it up; either
   pull it from a real source or omit it and say what tool would supply it.
5. **Write to disk** under `brands/<brand>/`, don't only print to chat. These
   are deliverables the user re-reads and sends on.

## Timeline honesty

SEO results lag 4–12 weeks, and AI-search citations move on their own schedule.
When asked to predict, give a range and name the assumption. Do not promise
rankings. When something shipped, log it in `changelog.md` with the date — a
change you cannot date is a change you can never claim credit for.

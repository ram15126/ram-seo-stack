# Attribution

This system is a curated merge of four open-source SEO skill repositories plus
original work. Nothing here was written from scratch that already existed in
good form upstream — the value added is selection, deduplication, path
rewiring, and the connective tissue that none of them provide.

Full license texts are in `licenses/`.

| Upstream | License | What was taken |
|---|---|---|
| [Bhanunamikaze/Agentic-SEO-Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill) | MIT | 76 evidence-collector scripts, the technical/audit playbooks, the LLM audit rubric, CWV thresholds, schema types, specialist agent definitions |
| [zubair-trabzada/geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) | MIT | GEO playbooks (citability, AI crawlers, llms.txt, platform tuning, brand mentions), scoring methodology, client report/proposal/comparison playbooks, schema templates |
| [inhouseseo/superseo-skills](https://github.com/inhouseseo/superseo-skills) | Apache-2.0 | Strategy and content playbooks (page audit, semantic gap, keyword deep-dive, topic clusters, content brief, write/improve, E-E-A-T, expert interview, featured snippets, link building) and their reference material |
| [AgricIDaniel/claude-seo](https://github.com/AgricIDaniel/claude-seo) | MIT | Local SEO and e-commerce SEO vertical playbooks |

## Modifications made to upstream files

Required disclosure under Apache-2.0 §4(b), and stated here for the MIT sources
as well:

- `SKILL.md` files were relocated to `skills/seo/playbooks/` and renamed by job
  (e.g. `superseo/skills/page-audit/SKILL.md` → `playbooks/audit-page.md`) so
  that one router skill dispatches them instead of ~34 skills competing to
  auto-trigger.
- Internal paths were rewritten to the merged layout: `resources/references/` →
  `references/`, `resources/templates/` → `references/industry-templates/`,
  `resources/skills/` → `playbooks/`, `../seo/references/` → `references/`.
- Reference files from all four repos were merged into a single
  `skills/seo/references/` tree. Where filenames collided with differing
  content (`cwv-thresholds.md`, `eeat-framework.md`, `quality-gates.md`,
  `schema-types.md`), the Agentic-SEO-Skill version was kept because the
  playbooks that cite them came from that repo.
- The GitHub-repository-SEO script family (`github_*.py`, `repo_*.py`) was
  removed as out of scope for client brand sites.
- **Factual corrections to reference files (25 August 2026).** Verified against
  primary sources; the upstream originals are available from the upstream repositories
  linked above, for diffing.
  - `references/information-gain-writing.md` (from superseo-skills) stated the
    Google Information Gain patent was "granted June 2024" and quoted a sentence
    it attributed to the patent. The patent is **US 11,354,342 B2, filed 18 Oct
    2018, granted 7 June 2022**, and the quoted sentence **does not appear in
    it** — it is a third-party paraphrase in circulation. Both were corrected,
    the real abstract substituted, and a `## Status` section added recording that
    Google has never confirmed the mechanism ships and that it is session- and
    user-relative rather than page-vs-SERP.
  - `references/serp-driven-writing.md` carried the same wrong grant date; fixed,
    with an `Unverified` label added to distinguish it from the genuinely
    leak-confirmed signals listed beside it.
  - `references/anti-slop-ruleset.md` was extended with vocabulary-drift windows,
    machine-checkable markers, a markup-leakage hard fail, citation-integrity
    checks, and a caveat on detector false-positive rates. It also absorbed the
    rules formerly duplicated in the separate `blog-writer` skill, which now
    points here. Additions are original work; upstream content is unchanged.
- File contents are otherwise unmodified.

## Original work in this repo

Not derived from any upstream:

- `skills/seo/SKILL.md` — the router, evidence/confidence discipline, and
  output rules
- `skills/seo/playbooks/ship-code.md` — implementing fixes in Next.js / Astro /
  Vite / static codebases
- `skills/seo/playbooks/intake.md` — brand brief and baseline capture
- `skills/seo/playbooks/changelog.md` — change attribution
- `brands/_template/` — per-brand workflow
- `install.ps1`, `README.md`, this file

## Used alongside, not merged — claude-blog

| Upstream | License | Version | Status |
|---|---|---|---|
| [AgricIDaniel/claude-blog](https://github.com/AgricIDaniel/claude-blog) | MIT | **v2.1.1** (pinned, cloned 2026-08-04) | Standalone skill suite |

**Deliberately not merged into `skills/seo/`.** claude-blog is a self-contained
suite — 32 skill directories, 5 subagents, 17 Python scripts, its own `/blog`
command namespace and a 5-gate delivery contract that expects its own file
layout. Flattening it into the seo router the way the four SEO repos were merged
would break the contract runner and the agent invocations. The two systems have
no command collision: `seo` diagnoses and ships site-level fixes, `/blog` plans
and produces posts.

Verified before adoption (2026-08-04): MIT, `pushed_at` 2026-07-23, 1.6k stars,
not archived. Files unmodified.

**Rejected candidate, recorded so it is not re-evaluated:**
[TheCraigHewitt/seomachine](https://github.com/TheCraigHewitt/seomachine) — MIT,
7.3k stars, and genuinely good on headline variants and the GSC impressions/CTR
loop. **Last code push 2026-04-10, 23 commits, 20 open issues.** The recent
`updated_at` is star metadata, not development. Same staleness class as the
`react-snap` recommendation withdrawn on 2026-08-01. Its two good ideas —
headline variant generation and a CTR feedback loop — are worth reimplementing
as original playbooks rather than vendoring a stalled dependency.

## Also referenced, not vendored

- [multivmlabs/aeo.js](https://github.com/multivmlabs/aeo.js) (MIT) — used via
  `npx aeo.js` in `ship-code.md` for build-time `llms.txt` / `ai-index.json`
  generation. Not copied in; it is an npm dependency of the client site, not of
  this skill.
- [Auriti-Labs/geo-optimizer-skill](https://github.com/Auriti-Labs/geo-optimizer-skill)
  (MIT) — optional, for real AI-citation tracking. Needs a Perplexity API key.

## Added in this public repository

Original work by Ramakrishnan S (growwithram.in), MIT-licensed:

- `skills/keyword-stack/` and `sops/keyword-research-with-claude.md` — the keyword research stack
- `sops/seo-workflow-free-stack.md`, `sops/measurement-free-stack.md`,
  `sops/ai-crawler-access-control.md` — SOPs
- `sops/keyword-research.md` — a graded write-up of Nathan Gotch's keyword method
  ("My Complete SEO Keyword Research Process", YouTube 9CajZ7SJQ_w); the method is his, the grading and
  adaptation are mine
- `process-notes/` — generic lessons from running audits with AI tools (no client data)

Not included on purpose: client folders, client deliverables and anything containing client or prospect data.

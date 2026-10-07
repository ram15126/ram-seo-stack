---
name: audit-post
description: >
  Audit one published blog post across every dimension that decides whether it
  ranks and whether it gets cited. Produces a flaw list and a rewrite spec. Use
  when the user shares a blog post URL and asks what is wrong with it, why it
  isn't ranking, or how to make it better.
---

# Audit one blog post

The user hands over a URL. You return: what is wrong, what is already right, and
what would have to change.

**Read `_process/blog-content-sop.md` before starting.** It is the doctrine this
playbook executes. Do not re-derive its numbers, and do not contradict them
without saying so.

---

## Step 1 — Scope and context

1. Establish the brand (SKILL.md Step 0) and read `brands/<brand>/brief.md`.
2. Ask for, or infer and state, the **target query** this post is meant to win.
   An audit without a target query can assess citability and craft but cannot
   assess intent match or information gain. If the user does not know, say which
   findings are therefore unavailable rather than inventing a target.
3. Ask whether they want competitor comparison. If yes, you need the top 3
   ranking URLs **in order** — no free, ToS-clean, no-key route to Google
   results exists, so get them from the Mangools MCP (`serpchecker_get_serp`),
   or ask the user to paste the SERP. Never fabricate a ranking order.

---

## Step 2 — Build the fact pack

Run the single-post collector set from SKILL.md. Every one writes JSON; you read
the JSON, not the live page, except where you need to read prose.

Then **read the post itself** — at least 500 words of it, and the opening and
closing sections in full. This is not optional. Several dimensions below cannot
be judged from collector output, and the one time an audit in this workspace
skipped the reading step it reported a site's AI-generated posts as its
strongest content.

---

## Step 3 — The eight dimensions

Work through all eight. Each produces findings with a confidence label, a
✅ Verify block and a falsifiability line.

### 1. Citability gate — is it even eligible?

From `preflight.json`. Google states the only requirements for AI features are
that a page is **indexed** and **eligible to show with a snippet**.

- `noindex` → nothing else matters until it is removed. Lead with it.
- `nosnippet`, `max-snippet:0`, `data-nosnippet` → excluded from AI features.
- Canonical pointing elsewhere → the post is not the ranking candidate.

If any of these fail, say plainly that the remaining findings are moot until
fixed, and still report them so the fix list is complete.

### 2. Intent and SERP match

Does the format match what ranks? A how-to page cannot win a comparison query.
Use `content_intent_matcher.py` and the actual SERP if you have it.
Classify: informational / commercial / transactional / navigational, and say
whether the post's format matches.

### 3. Information gain — the reason to rank at all

From `infogain.json`. The deliverable is the **claim diff**, not the cosine
number:

- **Claims only this post makes** — this is the information gain. If the list is
  short or generic, the post has no reason to outrank the incumbents, and that
  is the headline finding.
- **Claims competitors make that this post does not** — the add list.
- **Coverage matrix** — Core gaps must be added, Differentiator gaps if scope
  allows, Commodity gaps get one sentence, Opportunity gaps are the angle to own.

Target the 10-10-80 split from `information-gain-writing.md`: 10% basics, 10%
what competitors say, 80% unique. Most weak content is 80-10-10.

**Say this plainly when it applies:** information gain as a live Google ranking
factor is `Unverified` — a granted patent is not a shipped system. The reason to
chase it is that a page saying only what the other results say gives no reader a
reason to choose it. That holds regardless of what Google runs.

### 4. Topical fit and cannibalisation

Needs corpus context. If a `blog_inventory.py` capture exists, use it: which
cluster does this post sit in, is it an orphan, does another post compete with
it? If not, note that cluster findings need `playbooks/audit-blog.md` first
rather than guessing.

### 5. Authority and E-E-A-T

From `eeat.json` and `entities.json`, plus reading.

The 30-second heuristic from `eeat-scoring-rubric-compact.md`: **count specific,
datable, first-person observations** — a number with a year, a named client, an
error message, a mistake that got fixed. Three or more and Experience is
probably strong. Zero or one and Experience is absent no matter how long the bio
is.

Also check: byline resolves to a real author page, `Person` schema with
`sameAs`, sources that are checkable.

### 6. AEO/GEO citability

From `citability.json` and `preflight.json`, against the SOP §3b
extractable-block spec:

- 50–70 word answer block after the H1, self-contained, definition pattern
- key-fact opener per major section
- facts table where the subject allows
- FAQ with **schema text matching visible text exactly**
- real, checkable sources list

Then pick tactics **by domain**, per SOP §3a-bis — this is the part almost
everyone misses:

| Post's domain | Lead tactic |
|---|---|
| Law, government, factual, statements | Cite sources |
| Debate, opinion | Authoritative voice + statistics |
| History, people & society, explanation | Quotation addition |
| Business, health, science | Fluency optimisation |
| Any | **Never keyword stuffing — measured at −9%** |

### 7. Anti-slop

From `slop.json`, plus reading 300 words. Follow
`skills/seo/references/anti-slop-ruleset.md`.

**Report markers, never a verdict.** The calibration table in that file shows
em-dash density does not separate human from machine writing at all — human
posts ranged 0.00–4.51 per 1,000 words and the slop control sat at 4.88, inside
the range. Sentence-length standard deviation is the clean separator. Vocabulary
hits, banned phrases and vague attribution had zero false positives on real
human posts, so those are safe to act on.

Leaked model markup is the only conclusive signal, and it is a hard fail.

### 8. Structure and presentation

Headings form a real outline, tables scroll in their own container, text is HTML
rather than baked into images or SVG (neither search engines nor AI crawlers
extract text from images). Full presentation checks need a real viewport — say
so rather than implying you measured contrast and line length from HTML.

---

## Step 4 — Self-verify before writing anything up

Take each `Confirmed` finding and try to **disprove** it. Re-run the check.
Open the page and look. Four findings in this workspace once passed an audit and
failed re-testing; false alarms cost the user's credibility, not yours.

Specifically re-check anything where a script said "absent" or "zero" — a
headless fetch cannot prove a lazy-loaded element is missing, and a helper that
strips scripts will report "no schema" on a page that has it.

Downgrade anything that does not survive.

---

## Step 5 — Record what is already right

List what the post does well, with the same evidence discipline. This prevents
regressions when someone rewrites it, and it is why the rest of the report gets
believed.

---

## Step 6 — Output

Follow the SKILL.md output contract. Then add the rewrite spec:

### Rewrite spec

- **Keep** — the passages carrying the information gain, quoted.
- **Cut** — with the reason.
- **Add** — Core and Differentiator gaps, each with the source that shows the
  competitor covers it.
- **The answer block** — write it, 50–70 words, ready to paste.
- **The FAQ** — questions from real sources (People Also Ask, Stack Exchange,
  the brand's own inbox), answers 2–4 sentences.
- **The angle to own** — the Opportunity gap, if there is one.
- **What only the author can supply** — the first-person material. Mark it
  clearly. Never invent a recollection and put it in a real person's mouth.

Save to `brands/<brand>/audits/<date>-<slug>-post-audit.md`. One brand per
document.

---

## Common failure modes for this playbook

- **Reporting length as a quality judgement.** Say "coverage" and mean it.
- **Quoting the +115.1% cite-sources figure without its −30.3% counterpart.** It
  is a redistribution toward mid-ranked pages, not a free gain.
- **Treating information gain as a confirmed ranking factor.** It is not.
- **Calling the post AI-written.** Report markers and let the human read.
- **Auditing without reading.** The collectors cannot see the thing that matters
  most.

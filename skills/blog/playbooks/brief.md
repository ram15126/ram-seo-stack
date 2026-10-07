---
name: brief
description: >
  Produce a writer-ready brief for a new post, or a rewrite spec for an existing
  one. Use when the user wants to know what a post should say before it gets
  written, or wants the fix list from an audit turned into something a writer
  can execute.
---

# Brief / rewrite spec

For the SERP-research method — reading the top 10, classifying intent, mapping
the gap, picking the content type — `seo/playbooks/content-brief.md` already has
it and is good. **Read that and use it.**

This playbook covers what it does not: turning audit output into a spec, and the
blocks that decide whether the finished post gets cited.

---

## Which mode

- **New post** → run `seo/playbooks/content-brief.md`, then add sections 3–6 below.
- **Rewrite** → start from `playbooks/audit-post.md` output, then all of below.

---

## 1. What this post is for

One sentence: the query it wins, the reader it serves, the action it should
produce. If you cannot write that sentence, the brief is not ready.

## 2. Length

Give a **range from `_process/blog-content-sop.md` §1**, and label it a starting
range rather than a target. Then say the operating rule out loud, because writers
default to padding:

> Match total length to the intent. Put short, self-contained, liftable blocks
> *inside* long pages.

Never state a word-count target as a requirement. Google's own guidance says
there is no preferred word count, and the studies disagree by platform. **Never
pad to reach a range.**

## 3. The information gain — the part that makes it worth publishing

From `playbooks/info-gain.md`. This section is the brief's reason to exist.

- **What this post will contain that no competitor page has.** Be specific: the
  dataset, the case, the correction, the primary source others did not read.
- **Where it goes** — in the first 30%. A unique insight in the conclusion is one
  nobody read.
- **The 10-10-80 split** — 10% basics, 10% what competitors say, 80% unique.
- **What only the author can supply**, listed as questions to answer. Mark these
  clearly. They are the parts that cannot be researched, only extracted.

If this section is thin, say so and stop. A brief with no information gain is a
brief for a post that should not be written.

## 4. The extractable blocks — write them, do not describe them

Hand the writer finished text, not instructions:

- **The answer block**, 50–70 words, self-contained, opening "X is…". Written out.
- **A key-fact opener** per major section, 60–130 words. At least the first one
  written out.
- **The FAQ** — 4–6 questions taken from real sources (Stack Exchange, the
  brand's inbox, the SERP), each with a 2–4 sentence answer. Written out.
  Note that the `FAQPage` schema text must match the visible text **exactly**.
- **The facts table**, where the subject allows: claim, value, source.

## 5. The citation tactic

From `playbooks/geo-cite.md` — classify the post's domain and name the lead
tactic, because it changes by domain:

| Domain | Lead with |
|---|---|
| Law, government, factual | Cite sources |
| Debate, opinion | Authoritative voice + statistics |
| History, people & society | Quotation |
| Business, health, science | Fluency |

And, for every domain: **no keyword stuffing.** It measured −9% in generative
engines. Say it in the brief, because it is the habit writers arrive with.

## 6. Structure and wiring

- Outline with the H2s, and which one targets the featured snippet.
- Cluster placement: which hub this links to, and the **first contextual body
  link** goes there.
- 3–5 internal links, named.
- Title ≤ ~60 chars, description ~150–160.
- Schema: `Article` + `Person` author + `BreadcrumbList`, plus `FAQPage` if there
  is an FAQ.
- Sources to cite, with URLs. Real ones — every link must resolve.

## 7. Voice and constraints

From `brands/<brand>/brief.md`: tone, never-say list, claims needing approval.

**Check the brand's position on AI authorship before anything is drafted.** A
brand whose promise involves human craft cannot publish generated prose,
regardless of what Google permits. That is a positioning risk, separate from and
larger than the search risk.

Point the writer at `skills/seo/references/anti-slop-ruleset.md`.

## 8. Verify date

Set it **8–16 weeks out**. New content does not rank sooner, and judging at four
weeks produces a wrong conclusion. Log it in `brands/<brand>/changelog.md`.

---

## Output

Save to `brands/<brand>/content/<date>-<slug>-brief.md`. One brand per document.

Include a **"what we do not know"** section — the assumptions the brief rests on
and what would change it. A brief that hides its uncertainty produces a writer
who cannot tell which parts are load-bearing.

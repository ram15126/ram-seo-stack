---
name: write
description: >
  Draft a post from an approved brief, then put it through the delivery gate
  before it ships. Use when the user asks for the post to actually be written or
  rewritten, and a brief already exists.
---

# Write the post

**Do not start without a brief.** If there isn't one, run `playbooks/brief.md`
first. Drafting straight from a keyword is how the padded, sourceless,
says-nothing post gets made.

For the writing craft itself — voice, rhythm, show-don't-state, the 23 content
type templates — `seo/playbooks/content-write.md` has it. Read that. This
playbook is the wrapper: what happens before drafting, and the gate afterwards.

---

## Before drafting

**1. Check the brand's AI-authorship position.** From `brands/<brand>/brief.md`.
Google permits AI-assisted content and judges it on value and intent — that is
the search answer, and the search risk is low. It is not the whole answer. A
brand whose public promise involves human craft or original authorship cannot
publish generated prose or generated imagery; one screenshot ends the claim.
Check before drafting, not after.

**2. Extract what cannot be researched.** The brief lists what only the author
can supply. Get it now — one question at a time, not as a form. Good openers:
*"What do most people get wrong about this?"*, *"Who should NOT follow this
advice?"*, *"What did you try that didn't work?"*

If the author is unavailable, draft the first-person passages as **clearly
marked placeholders**, list them at the end, and say the post cannot publish
until they are replaced. Putting invented recollections in a real person's mouth
is not a style problem.

**3. Confirm the content type** and load its template from
`seo/references/content-types/`.

---

## While drafting

- **The gain goes in the first 30%.** Lead with what only this page has, not
  with a definition everyone already has.
- **Write the extractable blocks as written in the brief** — the answer block,
  key-fact openers and FAQ are not paraphrase targets.
- **Every number gets a source.** No soft quantifiers. If the figure does not
  exist, write around it or mark `[to confirm]` — never invent one.
- **Asymmetric coverage is human.** Spend 500 words on the interesting part and
  50 on the boring-but-necessary part. Even coverage across every subheading is
  a machine habit.
- **No keyword stuffing.** Measured at −9% in generative engines. It is the one
  classic SEO lever that actively inverts.
- Match length to intent. Never pad to hit a range.

---

## The delivery gate

A draft ships only when every gate passes. **Rewrite to pass — never flag and
move on.** Auto-iterate up to three times, then stop and escalate to the user
with what is still failing rather than shipping something that half-passes.

### Gate 1 — Substance

- Passes Google's helpful-content self-assessment with no "no". Any "no" is a
  rewrite, not a note for later.
- Contains something no competitor page has: own data, own experience, a
  correction, a primary source others did not read.
- Every number has a source. Facts spot-checked against the primary source, not
  a secondary blog.
- **The Horoscope Test** on every paragraph: could this have been written by
  anyone, for anyone, about anything? If yes, it fails whatever else it passes.

### Gate 2 — Anti-slop

Run `playbooks/slop-gate.md`. Hard fail on leaked model markup. Read the markers
against the brand's calibrated baseline, not against absolute thresholds — and
remember em-dash density separates nothing.

### Gate 3 — Extractability

- Answer block 50–70 words, self-contained, definition pattern, no pronoun
  opening.
- Key-fact opener on each major section.
- FAQ present, and **schema text diffed against visible text programmatically**,
  not by eye.
- Sources listed, and **every link opened and confirmed to resolve**. A broken
  citation is a fabrication tell.

### Gate 4 — Technical

```bash
export PYTHONIOENCODING=utf-8
python skills/seo/scripts/preflight_audit.py "$URL_OR_FILE" --check-links --json
```

Indexable, snippet-eligible, `Article` + `Person` + `BreadcrumbList` schema,
byline resolving, canonical, title and description lengths, 3–5 internal links
with the first contextual one pointing at the hub.

### Gate 5 — Presentation

Needs a real viewport, so check it in one at 375 / 490 / 768 / 1440px:
characters per line 66–75 desktop, contrast measured not eyeballed, no page-level
horizontal overflow, tables scrolling inside their own container, and **all
meaningful text as HTML text** — never baked into an image or SVG, because
neither search engines nor AI crawlers extract text from images.

---

## After shipping

- Log it in `brands/<brand>/changelog.md`: what changed, why, the evidence, and
  the expected effect.
- **Set the verify date 8–16 weeks out.** Judging at four weeks produces a wrong
  conclusion.
- Record the result at that date — including "no change", which is a real result.

---

## Output

The draft, in the brand's CMS format. Plus, separately:

- **Placeholders still needing the author's real words**, listed.
- **Anything marked `[to confirm]`**, listed.
- Which gates passed, and any that needed more than one rewrite pass — that is a
  signal about the brief, not just the draft.

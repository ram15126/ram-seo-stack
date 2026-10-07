---
name: authority
description: >
  Score a post and its author on E-E-A-T, and say exactly what to add. Use when
  the user asks about authority, expertise, trust signals, author pages, or why
  a factually correct post still is not trusted or ranked.
---

# Authority and E-E-A-T

Scoring rubric: `skills/seo/references/eeat-scoring-rubric-compact.md`.
Do not restate it here — read it.

Google's own position: of the four, **"trust is most important. The others
contribute to trust, but content doesn't necessarily have to demonstrate all of
them."**

---

## Step 1 — The 30-second heuristic, first

Before any script: **count the specific, datable, first-person observations.**
A number with a year. A named client. A timestamped screenshot. An error message.
A mistake that got fixed.

- **Three or more** → Experience is probably strong.
- **Zero or one** → Experience is absent, no matter how long the bio is.

This one count predicts the rest of the audit better than any collector output,
and it takes half a minute.

## Step 2 — Run the collectors

```bash
export PYTHONIOENCODING=utf-8
python skills/seo/scripts/eeat_signal_checker.py "$URL" --json
python skills/seo/scripts/entity_checker.py "$URL" --json
python skills/seo/scripts/preflight_audit.py "$URL" --json   # byline + Person schema
```

`entity_checker.py` looks for Wikidata/Wikipedia presence and `sameAs` links —
whether the author and brand exist as entities anywhere an engine can resolve.

## Step 3 — The four dimensions

**Experience** — did the author do the thing? First-person, specific, datable.
This is the dimension AI-assisted drafts fail hardest and the one that cannot be
researched, only extracted. See `seo/playbooks/content-expert-interview.md`.

**Expertise** — do they demonstrably know the subject? Depth, correct use of
domain terms, awareness of the edge cases and the exceptions.

**Authoritativeness** — does anyone else say so? Byline resolving to a real
author page, `Person` schema with `sameAs`, citations from elsewhere. This is
mostly off-site, and mostly not fixable on the page.

**Trust** — the one that matters most. Sourcing that checks out, no
easily-verified factual errors, transparency about who made this and why,
contact and ownership information, and dates.

## Step 4 — Google's Who / How / Why test

Quoted from the helpful-content guidance, and worth running literally:

- **Who** — Is it self-evident who wrote this? Does the byline lead to further
  information about the author?
- **How** — Is the use of automation, including AI generation, self-evident to
  visitors? Is there background on how it was used and why it was useful?
- **Why** — Was this created primarily to help people, or primarily to attract
  search visits?

The **How** question is the one most sites fail silently, and it is worth
raising with the brand rather than deciding for them.

## Step 5 — The off-site reality

Authority is largely earned elsewhere. The Ahrefs 75,000-brand correlation study
found **branded web mentions (0.664 ChatGPT / 0.709 AI Mode) correlate far more
strongly with AI visibility than backlinks**, with Domain Rating at 0.266–0.326.
YouTube mentions correlate highest of all (~0.71–0.74).

Ship the caveat with the finding: *correlation isn't causation*, in Ahrefs' own
words. Do not promise that getting mentions will raise visibility.

Practical: an author with no resolvable presence anywhere cannot be made
authoritative by on-page markup. Say that plainly instead of recommending more
schema.

## Step 6 — YMYL

If the topic touches health, finance, safety or legal, the bar is higher and the
rubric changes — use `references/ymyl-scoring-rubric.md`. Do not apply the
standard bands to YMYL content.

---

## Output

- The first-person observation count, with the observations quoted.
- Per-dimension score and band, with the specific markers found and missing.
- **The fastest wins first** — byline linking to a real author page, `Person`
  schema with `sameAs`, and dates are usually hours of work.
- What requires the author's own material, marked clearly. Drafted first-person
  passages are placeholders, not copy: list them and get the person's real words
  before publishing. **Putting invented recollections in a real person's mouth is
  not a style problem.**
- What cannot be fixed on-page, said plainly.

---
name: info-gain
description: >
  Score one post's information gain against the pages that outrank it, as a
  claim-level diff rather than a similarity number, and classify every gap.
  Use when a post is not ranking despite covering the topic, or when the user
  asks what the top results have that theirs does not.
---

# Information gain

**Read `skills/seo/references/information-gain-writing.md`, including its
`## Status` section, before using this with a client.**

---

## What this actually is, and what it is not

Google holds **US 11,354,342 B2, "Contextual estimation of link information
gain"** (Carbune & Gonnet Anders), filed 2018, **granted June 2022**. Its
abstract:

> "An information gain score for a given document is indicative of additional
> information that is included in the given document beyond information
> contained in other documents that were already presented to the user."

Three things to keep straight, because the SEO literature gets all three wrong:

1. **The date.** Not June 2024. That figure comes from conflating the patent
   with the May 2024 API leak, and it is repeated everywhere.
2. **The comparison set.** It is **session- and user-relative** — scored against
   documents *this user already saw*. "Your page vs the top 10" is a convenient
   proxy, not what the patent describes.
3. **Its status.** Google has never confirmed it runs in production. A granted
   patent is evidence of an idea worth protecting, not of a shipped system. Do
   not sell it as a ranking factor.

Also beware a widely circulated sentence — *"Information gain scores indicate
how much more information one source may bring to a person who has seen other
sources on the same topic…"* — presented as a quotation from the patent. **It is
not in the patent.** It was in this workspace's own reference file until 25 Aug
2026. Do not reuse it.

**What survives all of that**, and why the technique is still right: a page that
says only what the other results say gives no reader a reason to choose it, and
no engine a reason to surface it. That holds regardless of what Google runs.

---

## Step 1 — Get the ranking set, honestly

`info_gain_matrix.py` **does not fetch a SERP.** There is no free, ToS-clean,
no-key route to Google results, and pretending otherwise would put a fabricated
ranking order into a client deliverable.

Get the top 3–5 URLs **in order** from:
- `mcp__mangools__serpchecker_get_serp` (real data, mind the quota), or
- the user pasting the SERP.

If the order is wrong, the Differentiator classification is wrong with it. Say
where the order came from in the report.

## Step 2 — Gather real questions

The Opportunity bucket needs external signal, otherwise a topic nobody covers is
indistinguishable from a topic nobody wants. Free, sanctioned sources:

- **Stack Exchange API** — 300 requests/day without a key, 10,000 with a free
  one. High-signal real questions.
- **Wikipedia / Wikidata** — no key, no registration, fully sanctioned. Best
  free source for the entity set a topic should cover.
- **The brand's own inbox and sales calls** — the best source, and nobody else
  has it.
- Google Suggest works but is undocumented and ToS-grey; use sparingly with a
  real user agent.

Known dead or unusable, so do not plan around them: pytrends (archived April
2025), Pushshift, Reddit's free tier for commercial use (prohibited),
DuckDuckGo autocomplete scraping (against ToS), and any free route to People
Also Ask.

Put one question per line in a file.

## Step 3 — Run the diff

```bash
export PYTHONIOENCODING=utf-8
python skills/seo/scripts/info_gain_matrix.py "$TARGET" \
    --competitors "$C1" "$C2" "$C3" \
    --questions-file questions.txt --json
```

## Step 4 — Read the claim diff, not the cosine

The script reports a `novelty_score` of `1 − max(cosine)`. **It is a coarse
gate.** The patent describes a trained model over document embeddings, not
cosine over TF-IDF; the commonly cited ">0.5 = meaningfully different" threshold
has no published validation. Use it to sanity-check, never as the finding.

The deliverable is the claim diff:

- **`claims_only_on_target`** — the actual information gain. If this list is
  short or generic, that is the headline finding of the whole audit. There is no
  amount of on-page optimisation that fixes having nothing to say.
- **`claims_missing_from_target`** — the add list, each traceable to the
  competitor that makes it.

Claim extraction is heuristic — sentences carrying numbers, named entities,
definitions or comparisons. It misses vaguely phrased claims and admits some
non-claims. **Read the lists** before putting them in a report.

## Step 5 — Work the coverage matrix

Buckets follow `references/gap-classification-rubric.md`:

| Bucket | Means | Action |
|---|---|---|
| **Core** | All top results treat it as part of the answer | Must add. No depth elsewhere compensates |
| **Differentiator** | Covered by some, and the ones covering it rank higher | Add if scope allows — it is pulling weight |
| **Commodity** | Everyone mentions it once, nobody expands | One sentence. Do not build a section |
| **Opportunity (candidate)** | Nobody covers it, and a real question asks for it | **The angle to own.** Often the lead section |

Opportunity gaps arrive as *candidates* deliberately: the script cannot confirm
relevance, only absence. Confirm each one is genuinely what a reader wants
before building on it.

## Step 6 — Turn gaps into gain

Missing claims are the floor, not the goal. Copying competitors' claims makes
the page complete, not novel. The gain has to come from somewhere they cannot
reach:

- **First-party data** — the brand's own analytics, support tickets, test results
- **Original case studies** — a named client and what actually happened
- **Expert interview** — see `seo/playbooks/content-expert-interview.md`
- **A contrarian position**, with the reasoning
- **Process documentation** — the real steps, including the ugly ones
- **Failure stories** — what was tried that did not work, and why
- **Tool tests** — measured, not summarised

Target the **10-10-80 split**: 10% basics for context, 10% what competitors say,
80% what only this page has. Weak content is 80-10-10.

Put the gain in the **first 30%** of the page. A unique insight in the
conclusion is a unique insight nobody read.

## Step 7 — Re-score on a cadence

Gain decays as competitors copy you. Re-run against the live top 10 at the
post's verify date rather than treating the score as permanent.

---

## Output

- Where the ranking order came from, named.
- The claim diff, both directions, quoted.
- The coverage matrix with buckets.
- A ranked add list: Core first, then Differentiator, then the Opportunity angle.
- **What only the author can supply**, marked clearly — never invent first-person
  material.
- The `Unverified` label on any statement about Google scoring information gain.

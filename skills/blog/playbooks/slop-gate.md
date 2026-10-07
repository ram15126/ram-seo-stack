---
name: slop-gate
description: >
  Run the anti-slop gate over a draft or a published post. Reports measurable
  markers with locations, never an authorship verdict, and rewrites to pass
  rather than flagging and moving on. Use when the user asks whether something
  reads like AI, wants a draft checked before publishing, or says a post feels
  generic.
---

# The anti-slop gate

**Read `skills/seo/references/anti-slop-ruleset.md` first.** It is canonical.
This playbook is how to run it, not a second copy of the rules — the rules used
to live in two files and drifted apart, which is how one said 1 em dash per 150
words and the other said 1 per 500.

---

## The rule that governs everything else

**Report evidence. Never conclude that AI wrote the text.**

This is a correctness constraint, not a style preference. Stanford tested seven
GPT detectors against 91 TOEFL essays by non-native English speakers: **61.3%
average false-positive rate**, over 91% flagged by at least one detector, while
native-speaker writing classified correctly. The same study showed light
rewriting pushes genuinely AI-generated text back under the threshold. OpenAI
withdrew its own classifier in July 2023 at ~26% accuracy.

Much of the writing in this workspace is by and for Indian English speakers. A
verdict-producing detector would flag the good human work. A marker linter will
not, because it reports what it found rather than what it concluded.

Say: *"seven uncited numerals at lines 42, 88 and 133; sentence-length SD 4.4
against a house baseline of 14–26."*
Never: *"this reads as AI-generated."*

---

## Step 1 — Run it

```bash
export PYTHONIOENCODING=utf-8
python skills/seo/scripts/slop_markers.py "$SOURCE" --json
```

Accepts a URL, an HTML file, a markdown file, or `-` for stdin.

## Step 2 — Hard fail first

If `hard_fail` is true, leaked model markup is in the text — `oaicite`,
`contentReference`, `turn0search0`, `[cite: 1]`, `【】`, `ppl-ai-file-upload`.

This is the one conclusive check in the whole system, and what it proves is
**provenance, not quality**: the text was pasted out of a chat interface without
being read. Fix it before anything else, and check the rest of the site for the
same strings — where there is one, there are usually more.

## Step 3 — Read the markers against a baseline, not an absolute

The calibration run in the ruleset, four hand-written posts versus a slop
control:

| Marker | Human range | Slop control | Verdict |
|---|---|---|---|
| Vocabulary (weighted) | 0–1 | 32 | **Acts on it. Zero false positives.** |
| Banned phrases | 0 | 7 | **Acts on it. Zero false positives.** |
| Vague attribution | 0 | 4 | **Acts on it. Zero false positives.** |
| Sentence-length SD | 14.5–26.1 | 4.4 | **Cleanest single separator.** Under ~10, read the passage |
| Em-dash per 1k words | 0.00–4.51 | 4.88 | **Separates nothing.** Context only, never evidence |
| Uncited numerals | 3–15 | 1 | Sourcing to-do list, not a slop signal |

Two consequences worth stating to a client if it comes up:

- The em-dash rule that circulates everywhere as "the #1 AI tell" did not
  survive testing here. It is not evidence on its own.
- **One or two markers are inconclusive.** You need clustering. Wikipedia's
  WikiProject AI Cleanup, which built the taxonomy from thousands of flagged
  articles, says so explicitly.

## Step 4 — Weight the vocabulary by its date

The banned-word clusters rot roughly annually. The versioning table in the
ruleset:

- 2023–mid-2024: *delve, tapestry, testament, meticulous, intricacies…*
- mid-2024–mid-2025: *align with, fostering, showcasing, bolstered…*
- **mid-2025 onward: *emphasizing, enhance, highlighting, showcasing***

A hit from the current cluster is a real signal. A "delve" in 2026 more likely
means the writer likes the word. `slop_markers.py` weights them 3/2/1
accordingly and reports `current_window_hits` separately — use that number, not
the raw total.

Human writing is also increasingly influenced by model patterns post-2024, so
the base rates drift underneath you. Re-check the table every six months.

## Step 5 — The Horoscope Test

For each paragraph: *could this have been written by anyone, for anyone, about
anything?* If yes, it fails regardless of passing every phrase check. Every
paragraph needs at least one element specific to this topic, this audience, this
moment.

This catches the content that avoids every banned word and still says nothing —
which no linter can detect.

## Step 6 — Rewrite to pass

**Rewrite, do not flag.** A gate that produces a list of notes is not a gate.

For each marker: quote the text, name the pattern, rewrite it, apply the
rewrite. Then **re-run the linter** — first-pass rewrites reliably reintroduce
the model's natural tendencies, and the second pass catches copula swaps and
recycled transitions that crept back.

Do not over-correct. Making every sentence a fragment is its own signature.

## Step 7 — Calibrate before gating a new brand

Before this gate blocks anything for a brand you have not run it on, run it over
**three human-written posts in that brand's voice** and record the baseline in
`brands/<brand>/brief.md`. If good human writing trips a threshold, the
threshold is wrong for that brand. Given the 61.3% figure above, this step is
not optional.

---

## Output

- Hard fail status, with locations.
- Marker table: measured value, brand baseline, whether it is inside range.
- Paragraphs failing the Horoscope Test, quoted.
- The rewritten text.
- Explicitly: **this is not an authorship judgement**, and the thresholds are
  advisory and calibrated per brand.

# Topic clustering: stripping site-wide terms fixes one false positive and creates another

**Class:** false positive in corpus-level content analysis
**Written:** 25 August 2026

## Both failures, in order

**Failure 1 — the byline becomes the topic.**
Clustering blog posts by title/heading token overlap on a real 8-post capture put
three unrelated posts in one cluster whose only shared terms were the author's first
and last name. The site puts `<author name>` in every `<title>`, so every post
overlapped with every other post on exactly those two tokens.

Any site-wide string does this: brand name, tagline, `| Blog`, a category prefix.
The cluster looks real in the output and is pure boilerplate.

**Failure 2 — the fix eats the subject.**
The obvious correction is to drop terms appearing in most posts, the way IDF would.
Set too loosely — "drop anything in ≥50% of posts, minimum 2 posts" — it removed
`sourdough` and `starter` from a four-post sourdough blog, and then reported **zero
cannibalisation between two near-duplicate sourdough guides** that were plainly
competing. The check that was supposed to find overlap had deleted the overlap.

## The principle

> On a single-topic blog, a term shared by most posts **is the topic**, not
> boilerplate. On a multi-topic blog, a term shared by *every* post is boilerplate.

Corpus size is what distinguishes them, and small corpora cannot distinguish them at
all — with four posts, "in half of them" is two, which is meaningless.

## Rule

1. Only strip high-frequency terms once the corpus is large enough for frequency to
   mean something. **Six posts minimum**; below that, strip nothing.
2. Set the share threshold near-universal — **~80%**, not 50% — with an absolute
   floor of 3 posts.
3. **Always report which terms were stripped.** A cluster report that silently
   discarded the subject is unfalsifiable. One disclosure line makes both failure
   modes visible to whoever reads the output.
4. Sanity-check the result against a case you already know the answer to. Two posts
   titled "The Complete Guide to X" and "The Ultimate X Guide" must come back as
   cannibalisation. If they do not, the tokeniser ate something.

## Related

- `word-count-is-not-content-quality.md` — the other content-audit proxy that
  inverts
- `compare-only-like-for-like-extraction.md` — same family: the measurement changed
  the thing being measured

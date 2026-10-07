# Content length and AI citation — the studies disagree, and the disagreement is the finding

**Class:** conflicting evidence / false resolution risk
**Written:** 25 August 2026. **Re-check:** February 2027, with `blog-content-sop.md`.

## The problem

Two credible-looking bodies of evidence give opposite answers to "how long should a
post be to get cited by AI," and both circulate as settled fact.

**Camp A — short wins.** Ahrefs, 174,048 pages across 560,346 **AI Overviews**:
53.4% of citations go to pages under 1,000 words; mean cited page 1,282 words;
Spearman correlation between word count and citation position **0.04** — effectively
zero. `Confirmed` (in `blog-content-sop.md` §1).

**Camp B — long wins.** Authoritas: AI-cited pages average **2,290 words**, ~3× a
typical web page, and **78% exceed 1,000 words**. SE Ranking: pages over 2,900 words
earned **59% more ChatGPT citations** than pages under 800.
`Likely` — read from search-result summaries, not the source reports. **Verify at
source before quoting to a client.**

## Why both are right

They measured different engines.

| Surface | What the data says about length |
|---|---|
| **Google AI Overviews** | Effectively length-neutral. Short pages cited heavily |
| **ChatGPT** | Favours longer pages |
| **Cross-platform averages** | Dominated by whichever engine the sample over-weights |

This is consistent with the wider finding that the engines barely overlap: only
~11% of domains are cited by both ChatGPT and Perplexity, and AI Overviews and AI
Mode cite the same URL only ~13.7% of the time. **There is no single "AI search" to
optimise for, and therefore no single correct length.**

## The trap

The trap is not picking the wrong camp. It is **quoting a cross-platform average as
if it were a target**. "AI-cited content averages 2,290 words" is true and useless:
it is an average across surfaces that disagree, and it says nothing causal. Longer
pages are also more likely to be comprehensive, well-linked and from established
sites — word count is plausibly a proxy for something else entirely.

Note that Camp B is *correlational* in exactly the way `blog-content-sop.md` §3d
warns about, and none of these studies control for domain authority.

## Rule

1. **Never state a word-count target.** Google's own position stands: "Are you
   writing to a particular word count because you've heard or read that Google has a
   preferred word count? (No, we don't.)"
2. **If a length claim must be made, name the surface it came from.** "Pages cited
   in AI Overviews skew short" is defensible. "AI prefers short content" is not.
3. **Report the conflict rather than resolving it.** A report that says "two studies
   disagree, here is why" survives a client checking the sources. One that picks a
   side does not.
4. The operating rule from the SOP is unaffected and is the actual answer: **match
   total length to intent, and put short, self-contained, liftable blocks inside
   long pages.** That serves both camps simultaneously.

## Sources

- Ahrefs — [Short vs. Long Content in AI Overviews](https://ahrefs.com/blog/short-vs-long-content-in-ai-overviews/) `Confirmed`
- Passionfruit — [AI citation rate by content length](https://www.getpassionfruit.com/blog/ai-citation-rate-by-content-length-does-longer-content-get-cited-more) `Likely`
- PushLeads — [How long should content be to get cited by AI](https://pushleads.com/how-long-should-your-content-be-to-get-cited-by-ai-search-in-2026/) `Likely`
- Google — [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

## Related

- `blog-content-sop.md` §1 — the length section this qualifies
- `word-count-is-not-content-quality.md` — the separate, larger trap: length as a
  *quality* proxy inverts on mixed-authorship sites

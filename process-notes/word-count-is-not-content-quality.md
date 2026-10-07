# Word count is not content quality — and it inverts on AI-written pages

**Class:** false positive in content auditing
**First hit:** a site where the audit ranked pages by rendered word count and
reported the three longest as *"the three strongest pages on the site"* and
*"the best content is hidden"*. On reading them, those three were the only
AI-generated posts on the site. The genuinely good house-voice essays were the
three *shortest* pages and had been scored as thin.

## Why it happens

Content-quality collectors mostly proxy quality with length, heading count and
reading time, because those are cheap to measure. On a site with mixed authorship
that proxy does not just fail, it **inverts**:

- AI-generated posts are long by construction — padded intros, nickname
  listicles, "everything you need to know" structure, restated summaries.
- Human expert posts are often short, because the writer removed the padding.

So sorting by word count reliably surfaces the worst content as the best.

## The tell — read before you rank

Open the two longest and two shortest pages and read 300 words of each. Generic
long-form has a fingerprint that is fast to spot:

- Uncited statistics with soft quantifiers — "research shows … up to 40%"
- Invented time/effort breakdowns — "you spend 30% writing, 50% debugging"
- Rhetorical tics — "Here's the thing —", "The real magic?", "The result?"
- Structure announcements — "this guide is going to cover everything"
- Nickname padding in comparisons — "The GOAT", "The Speed Demon"
- Named model/tool versions used as a selling point (dates the page)
- Zero reference to the site owner's own projects, even where the owner has a
  case study on that exact topic

That last one is the strongest signal. A studio writing about the thing it
literally built, without mentioning that it built it, did not write the post.

## Rule

Never let a word-count ranking reach a client-facing sentence about content
*quality*. Word count answers "is there enough here to rank", which is a
different question from "is this good". Report them separately, and read a
sample before using either word.

## Related

- `spa-soft-200-false-positives.md` — the other case where a collector's cheap
  proxy produced a confident wrong answer

# Two crawlers on identical bytes disagree — never compare across extraction methods

**Type:** measurement trap / false positive
**Cost when missed:** would have reported invented content growth and phantom title rewrites

## What happened

A re-audit compared a fresh `site_collect.py` pass against the previous audit's
`crawl_audit.py` output. It appeared to show, in one twelve-day window with no site changes:

- **41 of 43 pages gained content** (word counts up 1–13%)
- **14 page titles had been rewritten**

Both were artefacts. Nothing on the site had changed.

**The titles.** Every single "change" was `&` becoming `&amp;`. One script decodes HTML
entities, the other does not. `Ragi & Veldt Grape Atta` vs `Ragi &amp; Veldt Grape Atta` is
the same title.

**The word counts.** Proved directly. For one page, saved HTML existed from both dates and
the visible text was byte-identical (same MD5, same 678 words by a single consistent method).
The two scripts reported **675** and **678** words for those identical bytes. The 1–3% drift
across every page was pure method difference.

The same trap inflated a meta description from 160 to 165 characters — the extra five
characters were `&#039;` left un-decoded instead of rendered as `'`.

## The rule

**A metric is only comparable to itself measured the same way.**

Before reporting any delta between two audits:

1. **Was the same script, same version, same flags used on both dates?** If not, the delta is
   not evidence of anything until proven otherwise.
2. **Re-measure the old date with the new method.** Keep raw HTML from every audit precisely
   so this is possible — it is the only way to settle these disputes.
3. **Suspect any change that is uniform across every page.** Real edits are lumpy; a +1–3%
   shift on all 43 pages is a method signature, not an editorial programme.
4. **Normalise before comparing text:** decode HTML entities, collapse whitespace, strip
   `<script>`/`<style>` on both sides.
5. **Compare hashes of normalised visible text**, not word counts, to answer "did this page
   change?" It is binary and cannot drift.

## Related

Follows the same shape as the earlier `grep -c "lorem ipsum"` trap, where a raw count rose
from 16 to 24 because new JSON-LD had been added — the visible text was unchanged. Whole-HTML
counts and visible-text counts are different metrics wearing the same name. See also
[[word-count-is-not-content-quality]] and [[pagespeed-caches-identical-results]].

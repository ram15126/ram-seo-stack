# Vendored reference files carry fabricated citations — verify before building on them

**Class:** inherited false claim / credibility risk
**First hit:** 25 August 2026, `references/information-gain-writing.md`

## What happened

A reference file merged from an upstream open-source SEO skill repo made two claims
about Google's Information Gain patent:

1. That it was **"granted June 2024."** It was granted **7 June 2022** (filed 18
   October 2018). US 11,354,342 B2.
2. That the patent **"explicitly describes"** a specific quoted sentence:
   *"Information gain scores indicate how much more information one source may bring
   to a person who has seen other sources on the same topic. Pages with higher
   information gain scores may be ranked higher."*
   **That sentence does not appear in the patent.** It is a third-party paraphrase
   circulating in SEO writing, presented as primary-source quotation.

The real abstract says something narrower and materially different: gain is measured
against documents *"already presented to the user"* — session- and user-relative,
not "your page vs the top 10."

Both claims had propagated into four files across the merged tree.

## Why it matters more than a normal error

A wrong date is embarrassing. **A fabricated quotation attributed to a primary
source is unrecoverable in front of a client** — it is exactly the failure the
✅ Verify discipline exists to prevent, and it arrived pre-installed rather than
being generated during the work.

It also sat in a file whose job is to instruct writing. Anyone following it would
repeat the claim in good faith.

## Why it happens

Skill repos are assembled fast from blog posts. SEO writing quotes SEO writing;
paraphrases get quotation marks somewhere along the chain and then look primary. The
"June 2024" date is likely contamination from the May 2024 Content Warehouse API
leak, which is a different event entirely.

Merging a repo imports its citation hygiene along with its methodology.

## Rule

1. **Before a vendored reference informs client-facing work, verify its primary-source
   claims at the primary source.** Patents, Google documentation and academic papers
   are all one fetch away.
2. **Treat any quotation attributed to a patent, a Google statement or a paper as
   unverified until fetched.** Search the source text for the exact sentence. If it is
   not there, delete it — do not paraphrase around it.
3. **A granted patent is not a shipped system.** "Google patented X" means Google
   thought X worth protecting. It does not mean X ranks anything. Label accordingly:
   the writing *technique* can be `Confirmed` useful while the *mechanism* stays
   `Unverified`.
4. **Record corrections in the modification disclosure**, not just in the file. The
   upstream copy under `upstream/` stays pristine so the diff remains meaningful.

## Where to look next

Other vendored references make claims of the same shape and have not been checked:
anything citing the Content Warehouse API leak, the antitrust-trial testimony, or a
named Google patent. Scan for quotation marks near "patent", "leak", "confirmed" and
"Google says".

## Related

- `blog-content-sop.md` — corrected the same day for a different sourcing error
  (a GEO tactic ranking that did not match the paper's own table)

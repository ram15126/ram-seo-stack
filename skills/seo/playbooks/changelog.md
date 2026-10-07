---
name: changelog
description: Log every shipped SEO change with a date so results become attributable. Use after shipping any fix, and read before interpreting any traffic change.
---

# Change Log

The cheapest playbook here and the one that decides whether the work can be
proven. SEO results lag 4–12 weeks. Without a dated record of what changed,
every future traffic movement is unexplainable — you cannot tell a client which
change earned the lift, and you cannot tell yourself which tactic to repeat.

## Format

Append to `brands/<brand>/changelog.md`. Newest entry at the top.

```markdown
## 2026-07-31 — Canonical tags + Article schema on /blog

**Type:** Technical · Schema
**Scope:** 47 blog post routes
**Files:** app/blog/[slug]/page.tsx, app/layout.tsx
**Commit:** abc1234

**Problem (evidence):** canonical_checker.py — 47/47 posts had no canonical.
indexability_matrix.py — 12 posts competing with their own /amp variant.

**Change:** Added self-referencing canonical via generateMetadata. Added
Article JSON-LD generated from the post object.

**Expected effect:** De-duplicate the 12 competing pairs; make posts eligible
for article rich results. Expect movement in 3–6 weeks.

**Verify on:** 2026-09-11 — re-run canonical_checker.py, check GSC duplicate
coverage report, check rich result impressions.
```

## Rules that make it useful

- **Log the evidence, not just the change.** "Added canonicals" is a note.
  "47/47 posts had no canonical, per `canonical_checker.py`" is a baseline you
  can measure against later.
- **One entry per shipped change**, not per work session. Group by what a
  reader would consider one intervention.
- **Always set a verify date.** An entry with no follow-up date never gets
  checked, and unchecked work is indistinguishable from work that didn't help.
- **Log the failures too.** A change that produced nothing is genuinely
  valuable information — it stops you and every future client from paying for
  the same tactic twice.
- **Never edit history to look better.** The log's only value is that it is
  true.

## Reading it

Before answering "did our SEO work?", read the log first, then align dates
against the traffic curve. If three changes shipped in one week you cannot
attribute the result to one of them — say so plainly rather than picking the
flattering explanation. Space changes out when attribution matters more than
speed, and say which tradeoff you are making.

Feeds `playbooks/compare-monthly.md` and `playbooks/report-client.md`.

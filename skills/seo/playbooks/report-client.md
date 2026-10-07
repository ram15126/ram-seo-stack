---
name: report-client
description: >
  Assemble finished audit evidence into the client-facing report — the document
  that gets sent, read by a business owner, and forwarded. Use after the audit
  and GEO passes have produced evidence.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write
metadata:
  version: 2.0.0
---

# Client report

Turns collected evidence into the deliverable. This is the document that leaves
the building — assume it will be forwarded to someone who was not on any call
with you, and who will spot-check a claim.

**Format is not optional here.** Follow `references/client-report-style.md`
exactly: it is the house format, derived from what has actually been shipped.
This playbook covers *assembly and scoring*; the style guide covers *how each
finding is written*. Read both.

**Output:** `brands/<brand>/reports/<Brand>-SEO-Audit-<YYYY-MM-DD>.md`
Mark it `-CLIENT` if an internal variant exists alongside.

---

## Before you write a word

1. **Run the self-verification pass** in `SKILL.md`. Every `Confirmed` finding
   re-tested, every finding checked against `_process/`, every ✅ Verify command
   run against the live site. Demote anything that does not reproduce.
2. **Read `brands/<brand>/brief.md`** — the business, the audience, and what
   they actually care about. A finding's severity depends on their business, not
   on a generic rubric. A broken form is catastrophic for a lead-gen site and
   irrelevant for a brochure page with a phone number.
3. **Gather the evidence files** already produced in `brands/<brand>/audits/`.
   Do not re-run the audit inside this playbook. If evidence is missing for an
   area, either collect it or leave the area out — do not fill the gap with
   reasoning presented as measurement.

---

## Inputs

Whatever exists. The report covers what was measured, not a fixed set.

| Source | Contributes |
|---|---|
| `audit-full` / `audit-technical` | crawlability, canonicals, redirects, headers, CWV |
| `audit-content` | thin content, decay, E-E-A-T, readability |
| `audit-images` | weight, formats, alt text |
| `audit-sitemap` | coverage and quality |
| `schema` | structured data present, valid, and matching visible content |
| `geo-citability` / `geo-crawlers` / `geo-llmstxt` / `geo-platforms` | AI-search readiness |
| `geo-brand-mentions` | brand and entity presence |

Areas with no evidence are simply absent from the report. Say so in the
"unknowns" close rather than implying they passed.

---

## Scoring

Two scores, only where the evidence supports them.

### Site score (0–100)

Weights are defined in `SKILL.md` Step 7 — read them there, do not copy them
here. Present per-area sub-scores in a table so the total is auditable.

### GEO readiness (0–100), when the GEO passes were run

| Component | Weight |
|---|---|
| AI platform readiness | 25% |
| Content quality and E-E-A-T | 25% |
| Technical foundation | 20% |
| Schema and structured data | 15% |
| Brand authority and entity presence | 15% |

Round to an integer, cap at 100.

**A score is a summary of findings, never a substitute for them.** If a
component had no evidence collected, drop it and re-weight the rest — do not
score it from impression. Say in the report which components were measured.

### Bands

| Range | Label |
|---|---|
| 85–100 | Excellent |
| 70–84 | Good |
| 55–69 | Moderate |
| 40–54 | Below average |
| 0–39 | Needs attention |

Describe the band factually — what is and is not in place. Do not tell a client
that competitors are "capturing traffic your brand should own" unless you have
measured that. It is a sales line, and it is the kind of claim that gets checked.

---

## Assembly order

1. **Header block** — prepared for, site, date, pages reviewed.
2. **Score table** + finding counts by severity.
3. **Executive summary** — prose. Leads with what is already right. Names the
   single most serious finding and its cause. Closes on effort framing.
4. **How to read this report** — severity order, the `[Technical]` / `[Content]`
   tags, what the confidence labels mean, and that every verification command
   was run against the live site before issuing.
5. **What is already right — keep it.** Its own section. Non-negotiable.
6. **Findings**, severity-ordered, each in the house block:
   *In plain terms → Detail → Recommended fix → ✅ Check it yourself.*
7. **Prioritised action plan** — immediate blockers, then quick wins, then
   strategic. Carry the S/M/L effort marks through so scope is negotiable.
8. **Unknowns and follow-ups** — what would move a `Likely` to `Confirmed`, and
   what only the client can answer.

---

## Hard rules

These are the ones that cost credibility when broken.

- **No invented numbers.** No traffic, volume, ranking or revenue figure without
  a named source. Do not project "an estimated X% traffic increase" or a monthly
  rupee/dollar value — you have not measured it. Where a client will want a
  figure, name the tool that would supply it and offer to run it.
- **Never promise rankings.** Ranges, with the assumption named. Results lag
  4–12 weeks; AI-search citation moves on its own schedule.
- **`Confirmed` or `Likely` only.** No `Unverified` finding appears in a client
  report. `Confirmed` means fetched and read.
- **Every finding carries a ✅ Check it yourself block**, and every command in it
  was run before the report was issued.
- **Plain language in the headline and the "in plain terms" section.** Jargon is
  allowed in Detail and nowhere else.
- **No plugin recommendations.** These are code sites; the fix is a commit, and
  `ship-code.md` can make it.
- **One brand per document.** Never mention another client, by name or
  description.

---

## After issuing

- Note the delivery in `brands/<brand>/changelog.md` with the date.
- If the client disputes a finding, re-verify before defending it. Re-testing
  costs less than being wrong twice.
- `call-prep.md` turns this document into something you can talk from.

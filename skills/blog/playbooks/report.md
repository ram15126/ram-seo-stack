---
name: report
description: >
  Turn audit output into a client-facing deliverable. Use when the user wants
  the findings written up for a client, or says the report is going to be
  forwarded.
---

# Client report

These get forwarded. Someone the user has never met will read a finding, try to
check it, and form a view of the user's competence from whether it holds up.

That is the whole design constraint.

---

## Hard rules

**One brand per document.** No report references two brands. Not as a
comparison, not as an example, not in a footnote.

**`Confirmed` or `Likely` only.** `Unverified` findings do not go to a client.
If something matters and is unverified, either verify it or leave it out and say
what tool would settle it.

**No invented numbers.** No traffic, volume or ranking figures without a source.
Where a number would help and does not exist, name the tool that would supply it
rather than estimating.

**Never promise rankings or citations.** Give ranges and name the assumption the
range rests on.

**Correlation is not causation, and the caveat ships with the table.** This
applies specifically to the Ahrefs AI-visibility correlations, which carry their
own published caveat. Quote it.

---

## Structure

**1. Summary** — scope, what was measured, top 3 problems, top 3 opportunities.
Written for a business reader, not an SEO.

**2. What is already right.** Before the problems. It prevents regressions when
someone else edits the site, and it is the reason the rest of the report gets
believed. A report that is entirely bad news reads as a sales document.

**3. Findings table** — `Area | Severity | Confidence | Finding | Evidence | Fix`.

**4. Each finding, expanded**, with:

**✅ Verify** — the reader must be able to check it themselves.
- *Visible problems* → the exact page URL plus the Ctrl+F term or section that
  exposes it. Not the domain. Not "the FAQ page". The specific URL.
- *Invisible problems* (schema, headers, canonicals, sitemap contents,
  indexability) → the raw evidence quoted inline, plus a command or free online
  tool that reproduces it. **Prefer a browser, no-login route first** — most
  clients will not run a shell command.
- **Run every command before publishing it.** A verification step that does not
  reproduce is worse than no verification step at all.

**How would we know this was wrong?** — one line per finding. It signals the
finding is a claim rather than an assertion, and it makes the report auditable.

**5. Prioritised action plan** — effort against impact, sequenced.

**6. What was not measured.** Say it plainly:
- Content quality, if only scripts ran.
- Traffic, rankings and decay, without a Search Console export.
- Near-duplicate content below byte-identical, without shingling.
- Whether the topics are worth owning.
- Presentation, if no real viewport was used.

A report that quietly omits its own gaps is the one that gets caught.

---

## Before sending — verify your own work

Take every `Confirmed` finding and try to **disprove** it. Re-run the check, open
the page, look with your own eyes.

Four findings in this workspace once passed an audit and failed re-testing. False
alarms cost the user's credibility, not the tool's.

Pay particular attention to anything a script reported as **absent or zero**:

- A headless fetch cannot prove a lazy-loaded element is missing.
- A helper that strips `<script>` tags reports "no schema" on a page that has it.
- An HTTP 200 is not proof a file exists — SPAs return 200 with an HTML shell for
  any path.
- A sitemap "404" is often the checker probing filenames that were never meant to
  exist.
- Counting alt attributes without checking for `alt=""` produced 1,182 false
  "missing alt" findings once.

See `_process/` for the full false-positive register, and read it before
reporting any tool warning as a finding.

---

## Output

Markdown, to `brands/<brand>/reports/<date>-<scope>.md`.

No artifacts, no HTML, no PDF unless the user asks. If they want a PDF, use
`seo/playbooks/report-pdf.md`.

Log the deliverable in `brands/<brand>/changelog.md` with its verify date.

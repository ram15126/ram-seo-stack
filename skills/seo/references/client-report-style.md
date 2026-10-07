# Client report style — the house format

The format actually shipped to clients from this workspace. Derived from the
audits already delivered; it supersedes the generic findings-table contract in
`llm-audit-rubric.md` §7 for anything **client-facing**.

The rubric governs *how findings are judged*. This governs *how they are
written*. Use both.

Client-facing means: the client will read this file, and may forward it. Write
for a business owner or marketing lead, not a developer.

---

## 1. Document skeleton

```
# <Brand> — <Website Audit | SEO & AI-Search Audit>

**Prepared for:** <brand>
**Site:** <url>
**Date:** <D Month YYYY>
**Pages reviewed:** <n>

---

## Overall score: NN / 100
<per-area score table>
**N findings:** n critical · n high · n medium · n low

---

## Executive summary          ← prose, not bullets
## How to read this report    ← the contract with the reader
---

# CRITICAL
# HIGH
# MEDIUM
# LOW
```

Order findings **by severity, not by topic**. State that explicitly, so a reader
who stops after the Critical section knows they got the important part.

Number findings so they can be referenced in a call: `1.1` / `C1` / `H2`.
Either scheme is fine — be consistent inside one document.

---

## 2. The executive summary

Prose. Four to eight sentences, no bullet list. It must contain:

1. **What was reviewed** — pages, and how they were fetched. Say if each page was
   fetched twice (crawler view and fully-rendered view); it tells the reader the
   review was thorough and pre-empts "did you see the real site?"
2. **What is already good.** Before the bad news, in its own sentence. This is
   not politeness — it is why the reader trusts the rest of the report.
3. **The single most serious finding, bolded**, in plain language, with its
   cause. If the most serious problem is not a search problem, say so outright.
4. **The cluster of smaller issues**, and what they add up to *for the reader's
   business* — how it reads to a prospect comparing suppliers, not "this hurts
   SEO."
5. **Effort framing.** Which fixes are small, which need separate scoping.

Then a `### What is already right — keep it` section, or fold it into the
summary. Never ship an audit that is only a list of faults.

---

## 3. The finding block

Every finding, without exception:

````
## <n>. <A full sentence naming the consequence, not the mechanism>

**[Technical]** or **[Content]** · <Confirmed|Likely> · Effort: <S|M|L>

### In plain terms
Two to four sentences. No jargon at all. What is happening and what it costs.

### Detail
The mechanism, the numbers, the affected URLs. Jargon allowed here.

### Recommended fix
What to change, and the scope — "a short piece of work, not a rebuild."
Name the file or the pattern where you can. No plugin recommendations.

### ✅ Check it yourself
<see §4 — mandatory>
````

**Headline rule.** Write the consequence, not the diagnosis:

- Wrong: *Canonical tag misconfiguration on article templates*
- Right: *Four articles tell Google to index a page that does not exist*
- Wrong: *Missing SSR / client-side rendering detected*
- Right: *Content only exists after JavaScript runs; AI crawlers receive an empty page*

**Tag every finding `[Technical]` or `[Content]`** so the right person picks up
the right items — say in "How to read" that the content fixes need no engineer.

**Confidence is per-finding and may be split.** A real shipped example:
`Confirmed that the claims are unsourced / Unverified whether they are accurate`.
That precision is the point. `Confirmed (lab data)` for CWV is likewise better
than bare `Confirmed`.

Add a one-line editorial flag where it earns its place — `Fix today`,
`Decision needed from you`, `Highest-leverage structural fix`,
`Best ratio of value to effort in this audit`, `Strategic, not a bug`.

---

## 4. The ✅ Check it yourself block — mandatory

The single non-negotiable element of the house format, and the reason these
reports survive being forwarded.

**Visible problems** → the exact page URL plus the Ctrl+F term or the section
that exposes it. Not the domain. Not "the FAQ page."

**Invisible problems** (schema, headers, canonicals, sitemap contents,
indexability, form endpoints) → the raw evidence quoted inline, plus a command
or free online tool that reproduces it. Prefer a browser or no-login route
first; give the command as the fallback.

Rules:

- **Run every command against the live site before issuing the report.** State
  in "How to read" that you did. A verification step that does not reproduce is
  worse than no verification step.
- **State the expected output**, so the reader knows whether they reproduced it:
  *"The first returns `405`; the second returns `200`."*
- **Give a contrast where one exists.** One command showing the fault and one
  showing a working equivalent proves the fault is specific, not site-wide.
  This is what converts a claim into proof.
- **Reassure on side effects** when a command looks like it writes:
  *"Nothing is submitted and no data is sent."*
- Close with `**Worth asking internally:** <question>` where a business fact
  would confirm the finding — e.g. *"when did you last receive an enquiry
  through the website form?"*

---

## 5. Prohibitions

- **No invented numbers.** No traffic, volume, ranking or revenue figures
  without a named source. Do not write "could increase AI-driven traffic by an
  estimated XX%, approximately $X,XXX/month" — say what tool would supply the
  figure instead.
- **Never promise rankings.** Ranges, with the assumption named.
- **No `Unverified` findings in a client report.** `Confirmed` or `Likely` only.
  `Confirmed` means *fetched and read*, never an inference that looks certain.
- **No plugin recommendations.** These are code sites; the fix is a commit.
- **One brand per document.** Never reference another client.
- Anything the client cannot check themselves does not go in.

---

## 6. Sibling deliverables

Same voice and same evidence rules apply to:
`ACTION-CHECKLIST` · `CALL-PREP` / call brief · `30-DAY-PLAN` ·
`COMPETITOR-GAP-ANALYSIS` · topical map and blog plan · proposal ·
month-over-month comparison.

Naming: `<TYPE>-<YYYY-MM-DD>.md` or `<YYYY-MM-DD>-<type>.md`, in
`brands/<brand>/reports/`. Mark the client-facing one `-CLIENT` where an
internal variant exists alongside it.

# Call prep — walking a client through an audit

Turns a finished audit into a document you can talk from. The audit proves the
findings; this decides what to say out loud, in what order, and what not to say.

**Run after** `report-client.md`. Never instead of it.

**Output:** `brands/<brand>/reports/CALL-PREP-<YYYY-MM-DD>.md` (internal — this
one is not sent to the client).

---

## Before you start

Read the finished report and `brands/<brand>/brief.md`. Everything here comes
from those two files. Do not introduce a finding that is not in the report — if
it was not good enough to write down, it is not good enough to say on a call.

---

## Structure

### 1. Open with this

Two or three sentences, written to be said aloud. It must lead with something
true and positive about their site, then name the single most serious finding
in plain language.

Getting a client defensive in the first minute costs the rest of the call. Open
on what they did right, and they will hear the rest.

### 2. The one thing to get right

One finding. The one that changes their decision. Write what it is, why it
matters to their business, and the sentence you will use to introduce it.

If the most serious problem is not a search problem — a broken form, a wrong
phone number — say so explicitly. It builds more trust than any ranking claim.

### 3. Order to walk the call

Numbered, with a rough minute budget. Severity order from the report is usually
right, with one exception: if a finding needs a **decision from them**, put it
early while attention is high.

### 4. Plain-language translations

A two-column list. Left: what the report calls it. Right: what you say out loud.

| In the report | On the call |
|---|---|
| Canonical tag points to a non-existent URL | Four of your articles are telling Google to ignore them |
| No SSR; content renders client-side | AI assistants can't read your site |
| Soft 404 | Pages that don't exist still load as normal pages |

Never say canonical, render-blocking, SSR, schema, crawl budget or Core Web
Vitals unless the client used the word first.

### 5. The moment to use deliberately

Most audits have one finding that lands hardest when *shown* rather than
described — a slow page loading on their phone while you wait, a search result
with a truncated title, a form that returns an error. Name it, say when in the
call to use it, and what to say while it happens.

Use one. Two feels like a pile-on.

### 6. Questions they will ask — and the answers

Anticipate five to eight. Always include:

- *How long until we see results?* — 4–12 weeks, name the assumption, promise
  nothing about rankings.
- *How much of this can you do?* — separate what you can ship from what needs
  their developer or a decision.
- *Why didn't our last agency catch this?* — answer without disparaging anyone.
- *Is this going to be expensive?* — map to the S/M/L effort marks already in
  the report.

### 7. Things that are genuinely good — say these

Pull from the report's "what is already right" section. Have three ready. This
is what stops the call reading as a teardown, and it is why they believe the
critical findings.

### 8. Numbers you may quote, and their source

Every figure you plan to say, with where it came from. If a number has no
source next to it here, it does not get said.

### 9. Numbers you must NOT quote

Explicit. Traffic estimates, revenue projections, ranking promises, competitor
figures you did not measure, anything from a tool you have not run for them.

Writing the prohibited list down is what stops it coming out under pressure
when a client asks "so how much more traffic?"

### 10. Things NOT to say

Beyond numbers. Anything that:

- criticises a named person or a previous agency
- touches a sensitive commercial or legal point (write the careful phrasing
  instead — e.g. image rights, third-party photographs, testimonial claims)
- commits to a timeline you have not scoped
- mentions another client, by name or by description

### 11. The asks to close on

One or two, concrete, with a date. "Send us access to X by Friday" beats "let
us know your thoughts."

### 12. If they ask "what would you do first?"

Have the answer pre-written. It is the most common closing question and the
worst one to improvise.

### 13. Open questions you still need answered

Things only the client can tell you — traffic history, what changed and when,
who maintains the site, what the form used to do. These become brief.md updates
after the call.

---

## After the call

1. Update `brands/<brand>/brief.md` with what you learned — especially anything
   that was marked `[confirm with client]`.
2. Log agreed work in `changelog.md` as planned, with the date.
3. If a finding was disputed, re-verify it before defending it. The client is
   sometimes right, and re-testing costs less than being wrong twice.

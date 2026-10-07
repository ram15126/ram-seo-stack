# Use Common Crawl to prove crawler-access findings, not user-agent tests

## The problem with UA tests

"I sent a request with `User-Agent: GPTBot` and got `403`, therefore GPTBot is
blocked" is **not a valid finding**, and it is one of the easiest ways to put
something unrecoverable in front of a client.

A spoofed crawler UA arriving from an unverified IP *should* be challenged. That is
correct firewall behaviour. It tells you nothing about what the real crawler,
arriving from its own verified IP range, receives. Report it as-is and the client's
developer will refute it in one reply.

## The fix: Common Crawl's public index

Common Crawl runs **CCBot** from its own infrastructure and publishes every crawl
attempt — URL, timestamp, and **the HTTP status the server returned**. It is free,
needs no login, and it is third-party evidence the client can verify themselves.

```bash
# list available crawl cycles
curl -sS "https://index.commoncrawl.org/collinfo.json" | head

# query one cycle for a domain
curl -sS "https://index.commoncrawl.org/CC-MAIN-2026-30-index?url=example.com%2F*&output=json"
```

Each line is JSON with a `status` field. What to read:

| What you see | What it means |
|---|---|
| Many records, `"status": "200"` | CCBot crawls the site fine. Any "AI crawlers are blocked" claim is dead — drop it. |
| Only `/robots.txt` records, `4xx`/`5xx` | The crawler never got past robots.txt. **This is the finding**, and it is airtight. |
| No records at all | Inconclusive on its own — could be a low-value domain CC never picked. Needs the control below. |

## Always run the control

A query returning nothing is ambiguous between "blocked" and "my query is wrong".
Run the identical query against a **competitor in the same niche** — ideally one the
client names on their own comparison page, which makes the result land harder:

```
clientsite.com  records= 2   statuses={'429': 2}                      HTTP-200 pages =  0
competitor.com  records=63   statuses={'200': 51, '308': 7, '404': 5} HTTP-200 pages = 51
```

Same index, same cycle, same query. That contrast is the finding, and it survives
any developer pushback.

## Walk it backwards to date the problem

Query 10–14 consecutive cycles. This converts a snapshot into a timeline and
answers the first question the client will ask — *when did this start?* Observed on
one audit: `429` on every cycle back to the earliest checked, which reframed the
finding from "a recent regression" to "this has never worked", and changed the
remediation conversation entirely.

## What it still cannot tell you

CCBot is the only crawler Common Crawl reports on. It says nothing directly about
GPTBot, ClaudeBot or PerplexityBot from their own IPs. Say so explicitly and scope
the claim: direct evidence for CCBot, pattern-inference for the rest, and name
server access logs as the check that would settle it.

One partial exception worth using: if a fetch by your own tooling's real
infrastructure (not a spoofed UA) is refused, that is a second genuine data point
from a different network — weaker than Common Crawl, but real.

## Also: this is a zero-load test

It queries Common Crawl's servers, not the client's. No rate limiting, no crawl
budget, nothing to pace — unlike the UA matrix, which can poison a bulk crawl
(see [[ua-matrix-poisons-the-bulk-crawl]]). **Run the Common Crawl check first**,
before touching the client's origin at all. If it comes back with hundreds of
`200`s, there is no crawler-access finding and you have saved the whole
investigation.

## And it doubles as a baseline metric

"Pages in the Common Crawl corpus" is a clean, externally-verifiable number to
record before any fix and re-check at 90 days. Unlike rankings, nobody can argue
with it.

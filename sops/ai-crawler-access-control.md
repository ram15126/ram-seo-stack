# AI Crawler Access Control
Status: ACTIVE | Last verified: 2026-09-07 against vendor docs | Review by: 2026-12

Verified directly from vendor documentation [T1]. Do **not** update this file from
SEO blog aggregations — user-agent strings and product names change, and blog lists
are routinely wrong or stale. Re-verify at the URLs below before any client deployment.

## The distinction that matters most

**Training crawlers and search crawlers are separate, and the controls are independent.**

Blocking a training bot does **not** remove you from that assistant's search answers.
Blocking a search bot **does**. Agencies get this backwards constantly — either
reassuring a client that "we blocked the AI bots so we're protected" (they are still
being cited, via a different bot), or blanket-blocking everything and silently
destroying the client's ChatGPT visibility.

**Audit this on every new client before anything else.** A site that blocked AI
crawlers during the 2023–24 panic and never revisited it has a hard ceiling on AI
visibility that no amount of content work will lift. It is the single most common
silent killer, and it is free to find.

## OpenAI [T1 — developers.openai.com/api/docs/bots]

| User agent | Purpose | Blocking effect |
|---|---|---|
| **OAI-SearchBot** | **Search.** Surfaces sites in ChatGPT search features. | Site **will not be shown in ChatGPT search answers** (may still appear as a navigational link). **Allow this one.** |
| **GPTBot** | Crawls content that may be used for **training** foundation models. | Content not used for training. **No effect on search visibility.** |
| **ChatGPT-User** | User-triggered fetches when someone asks ChatGPT to visit a page, plus GPT Actions. Not automatic crawling. | Note: because these are user-initiated, **robots.txt rules may not apply**. Not used to determine Search appearance. |
| **OAI-AdsBot** | Validates safety of landing pages submitted as **ads** on ChatGPT; may also assess relevance. Only visits submitted ad pages. Data **not** used for model training. | Relevant only if running ChatGPT ads. |

Verbatim from OpenAI: a webmaster can "allow OAI-SearchBot in order to appear in
search results while disallowing GPTBot to indicate that crawled content should not
be used for training." If both are allowed, OpenAI may use one crawl for both purposes.

**Operational notes:**
- robots.txt changes take **~24 hours** to propagate to search behaviour.
- Published IP ranges for verification: `openai.com/searchbot.json`,
  `openai.com/gptbot.json`, `openai.com/chatgpt-user.json`, `openai.com/adsbot.json`.
- OpenAI may append a `robots.txt` marker to the UA string when fetching robots.txt —
  useful for log analysis when paths aren't logged.

## Anthropic [T1 — support.claude.com article 8896518]

| User agent | Purpose | Blocking effect |
|---|---|---|
| **ClaudeBot** | **Training** — model training and development. | Future material excluded from training datasets. |
| **Claude-User** | **User-triggered retrieval** when a user asks Claude a question. | Prevents retrieval of your content in response to user queries. |
| **Claude-SearchBot** | **Search indexing.** | Prevents indexing of your content for search. |

Control via robots.txt (`User-agent: ClaudeBot` / `Disallow: /`); `Crawl-delay` supported.
IP verification list: `claude.com/crawling/bots.json`.

**Anthropic's own warning:** blocking by IP alone does **not** work reliably — it
stops the bots reading your robots.txt, so your actual instructions never land.
Control via robots.txt, verify via IP.

## Others in the landscape
Verify each at source before deployment — these are **[T4] aggregated** and included
only as a checklist of what to look for in logs:
PerplexityBot (search — now verified, see the note below), Google-Extended (Gemini training
opt-out; does **not** affect Search or AI Overviews eligibility), CCBot (Common Crawl), plus
bots operated by Apple, Amazon and Meta.

> **PerplexityBot — verified at source 2026-09-20 [T1 — docs.perplexity.ai/guides/bots].**
> Fetched during `research/ai-citation-research.md`. Verbatim: *"PerplexityBot is designed to
> surface and link websites in search results on Perplexity. It is not used to crawl content for
> AI foundation models."* The page adds that to appear in results Perplexity recommends allowing
> PerplexityBot in robots.txt **and** permitting its published IP ranges, and that settings can
> take up to 24 hours to take effect. So Perplexity follows the same search-vs-training split as
> OpenAI and Anthropic. Re-verify at the URL before a client deployment — this note is a record of
> one fetch on one date, not a standing guarantee.

**Google is the important exception:** AI Overviews and AI Mode eligibility is
controlled by **normal Googlebot access plus the Search Console generative-AI
exclusion toggle** — not by Google-Extended. Blocking Google-Extended does not remove
you from AI Overviews. See knowledge/delivery/measurement-free-stack.md.

## The standing caveat
robots.txt is a **norm, not an enforcement mechanism**. Some crawlers have historically
ignored it, and a user-agent string can be spoofed by anyone. Verify real crawler
traffic against the published IP ranges before drawing conclusions from logs, and
never present robots.txt as a security control to a client.

## Recommended default posture for agency clients
Unless the client has a specific reason to withhold training data:

```
User-agent: OAI-SearchBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /
```

Training bots (GPTBot, ClaudeBot, CCBot, Google-Extended) are a **business decision,
not an SEO one** — blocking them costs no search visibility. Put the choice to the
client explicitly; do not decide it for them, and do not let a developer decide it
by accident.

# Brand folder

Copy this folder to `brands/<brand-name>/` for each new client.

```
brands/<brand>/
├── brief.md          ← who they are, what matters, the baseline. Written once.
├── changelog.md      ← dated log of everything shipped. Append forever.
├── audits/           ← FULL-AUDIT-REPORT.md, ACTION-PLAN.md, geo-audit.json
├── research/         ← keywords, clusters, competitor and semantic-gap analyses
├── content/          ← briefs and drafts
└── reports/          ← client-facing deliverables and PDFs
```

## The order

1. `seo intake` — fill `brief.md`, capture the baseline **before touching anything**
2. `seo audit <url>` — evidence pass → `audits/`
3. `seo geo citability <url>` + `seo geo crawlers <url>` — AI-search baseline
4. `seo plan` — decide what's worth doing, in what order
5. `seo ship` — implement in the site's code, on a branch
6. Log it in `changelog.md` with a verify date
7. `seo compare` at 30/60/90 days — against the baseline from step 1

Step 1 is the one that's tempting to skip and the only one that can't be done
retroactively.

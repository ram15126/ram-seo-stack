---
name: intake
description: Create the one-time brand brief that every other playbook reads. Run once per new client brand, before the first audit.
---

# Brand Intake

Run this once per brand. Everything downstream reads the output instead of
re-interrogating the user, so it pays for itself by the second job.

## Gather it yourself first

Do not open with a questionnaire. Fetch the site and answer what you can from
evidence, then ask only about what you genuinely cannot observe: business
goals, constraints, and access.

```bash
python "skills/seo/scripts/fetch_page.py" --url https://example.com
python "skills/seo/scripts/robots_checker.py" --url https://example.com
python "skills/seo/scripts/sitemap_checker.py" --url https://example.com
```

From that you can usually infer the niche, the offer, the rough page inventory,
the stack, and whether anyone has done SEO here before.

## Then ask only these

1. **Goal** — what does this site need to do more of? (leads, sales, signups,
   bookings, calls) And is there a number attached?
2. **Money pages** — which 3–5 URLs actually matter commercially?
3. **Competitors** — name 3 they lose to. Real rivals, not aspirational ones.
4. **Access** — Search Console? Analytics? The site's repo? Deploy rights?
5. **Constraints** — anything off-limits: brand voice rules, legal review,
   claims they cannot make, pages that cannot change.
6. **History** — any traffic drop, migration, or penalty in the last year?

Six questions. If they can only answer three, start anyway and fill in the rest
from the audit.

## Write the brief

Save to `brands/<brand>/brief.md`:

```markdown
# <Brand> — Brand Brief
Created: YYYY-MM-DD · Last updated: YYYY-MM-DD

## Business
- Site: https://…
- Niche / category:
- What they sell, in one sentence:
- Primary conversion:
- Target customer:

## Commercial priorities
| Priority | Page | Why it matters |
|---|---|---|

## Competitors
| Competitor | URL | Where they beat us |
|---|---|---|

## Stack
- Framework: (Next.js / Astro / static / …)
- Repo path or URL:
- Deploy: (Vercel / Netlify / …)
- CMS or content source:

## Voice and constraints
- Tone:
- Never say:
- Approval needed for:

## Access
- Search Console: yes/no
- Analytics: yes/no
- Repo write access: yes/no

## Baseline (as of YYYY-MM-DD)
- Indexed pages:
- Known rankings:
- SEO health score:
- GEO score:
```

## Record the baseline before changing anything

This is the step people skip and regret. Run a full audit
(`playbooks/audit-full.md`) and a GEO pass (`playbooks/geo-citability.md`,
`playbooks/geo-crawlers.md`) **before** the first fix, and save the scores into
the brief. Without a dated baseline you can never demonstrate improvement, and
"trust me, it's better" is not a renewal argument.

Then start `brands/<brand>/changelog.md` — see `playbooks/changelog.md`.

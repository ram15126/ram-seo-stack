---
name: audit-blog
description: >
  Audit a whole blog as a body of work: inventory, topic clusters, hub gaps,
  orphan posts, cannibalisation, duplicates, decay and coverage. Use when the
  user gives a blog URL, sitemap or index page and wants the blog reviewed
  rather than one post.
---

# Audit a whole blog

Cannibalisation, orphaning, cluster gaps and decay do not exist at page level.
They only appear across the corpus, which is why this playbook exists separately
from `audit-post.md`.

---

## Step 1 — Collect once, and only once

**One polite pass.** Re-crawling a site because the first pass did not capture
everything has already cost real time here.

```bash
export PYTHONIOENCODING=utf-8
python skills/seo/scripts/site_collect.py \
    --site "$SITE" --out brands/<brand>/audits/<date>-capture.json --delay 4
```

Notes that matter:
- It probes the host once and paces itself. Leave `--delay` at 4 unless the
  probe says otherwise.
- It uses a real browser UA by default. **Never** use `--ua-matrix` for the bulk
  crawl — spoofing Googlebot gets 429s from some hosts and poisons the capture.
  Use it only for a deliberate spot-check of a handful of URLs.
- It writes incrementally and supports `--resume`. A timeout is not a restart.

Then build the inventory:

```bash
python skills/seo/scripts/blog_inventory.py \
    brands/<brand>/audits/<date>-capture.json --path-contains /blog/ --json \
    > /tmp/pack/inventory.json
```

If the post-detection heuristic misses (it looks for Article schema or
`/blog|/articles|/posts|/insights|/news|/journal` in the path), pass
`--path-contains` explicitly rather than accepting a wrong post count.

---

## Step 2 — Read the inventory, then check its own working

`blog_inventory.py` reports `boilerplate_terms_ignored` — the site-wide terms it
stripped before clustering. **Read that line first.**

- If it stripped the brand or author name, good — those are in every title and
  would otherwise manufacture one giant false cluster.
- If it stripped the blog's actual subject, the clusters are wrong. This happens
  on small single-topic blogs. Re-run with a higher `--cluster-threshold` or
  judge the clusters by hand, and say in the report that you did.
- Sanity test: two posts titled "The Complete Guide to X" and "The Ultimate X
  Guide" must come back as cannibalisation. If they do not, the tokeniser ate
  something. See `_process/topic-clustering-term-stripping-cuts-both-ways.md`.

---

## Step 3 — The corpus questions

### Clusters and hubs

For each cluster of 3+ posts: is there a clear hub, and do the spokes link to
it? The script picks the hub as the member the rest of the cluster links to
most — **not the longest post**, because length would just elect the wordiest
one.

A cluster with no clear hub is the most common reason a topic underperforms:
the spokes are competing with each other instead of pointing at a pillar.

### Orphans

Posts nothing links to. The script counts inbound links from the whole capture,
not just from other posts, so a post linked from a service page is correctly not
an orphan.

An orphan that is also the best post on the blog is the highest-value fix
available — and you will only know it is the best post by reading it.

### Cannibalisation

Pairs above ~0.55 topic similarity. Read both before recommending a merge. The
right answer is usually consolidate-and-redirect, occasionally differentiate-
the-intent, and rarely delete.

### Duplicates

`main_hash` catches byte-identical bodies. For near-duplicates run
`duplicate_content.py`, which does shingling — the inventory does not.

### Decay

Needs a Search Console export; there is no way around that. With one:

```bash
python skills/seo/scripts/content_decay_detector.py --csv gsc-export.csv --json
```

Without one, say that decay was not assessed. Do not infer traffic from
anything.

### Coverage

What does the blog not cover that it should? That is a research question, not a
crawl question — hand to `playbooks/cluster-map.md`.

---

## Step 4 — The landmine check, every time

**Do not rank posts by word count, and do not let a length ranking reach a
sentence about quality.**

Instead: open the **two longest and two shortest** posts and read 300 words of
each. On a mixed-authorship site the ranking inverts — AI posts are long by
construction (padded intros, "everything you need to know" structure, restated
summaries) and human expert posts are often short because the writer removed the
padding.

Run `slop_markers.py` over a sample and read the markers, but remember the
calibration: vocabulary hits, banned phrases and vague attribution separate
cleanly; em-dash density does not separate at all.

The strongest single tell from the workspace record: **a site writing about the
thing it built, without mentioning that it built it, did not write the post.**

---

## Step 5 — Self-verify

Try to disprove each finding. Re-check every "absent" or "zero" — those are
where collectors fail silently. Downgrade what does not survive.

---

## Step 6 — Output

Follow the SKILL.md output contract, plus:

- **Inventory table** — post, cluster, coverage (word count, clearly labelled as
  coverage), inbound links, date, schema types.
- **Cluster map** — clusters, hubs, orphans, and the link edges that are missing.
- **Consolidation plan** — which posts merge, which redirect, which stay.
- **What is already right.**
- **What was not measured** — quality, near-duplicates below byte-identical,
  traffic, and whether the topics are worth owning.

Save to `brands/<brand>/audits/<date>-blog-audit.md`.

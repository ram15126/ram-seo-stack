---
name: cluster-map
description: >
  Build or repair a blog's topical map: hub and spokes, the internal link
  graph, publishing order, and what the blog should cover next. Use when the
  user asks for a topical map, topic clusters, a content plan, or what to write
  about next.
---

# Topical map

Two entry points. Say which one you are in before starting.

- **Repair** — the blog exists. Start from `blog_inventory.py` output.
- **Build** — new topic area. Start from research.

For the underlying hub-and-spoke method, `seo/playbooks/research-clusters.md`
already has it: hub selection, spoke mapping, the link graph, and the publishing
order. Do not duplicate it here. This playbook adds what that one lacks — the
corpus-repair path, and honesty about which parts of topical-authority theory
are testable.

---

## What is testable, and what is guru-talk

Topical authority as popularised has no academic backing and no published
replication. It is a coherent practitioner heuristic. Encode the parts that
produce measurable outcomes and drop the rest:

| Worth encoding | Skip |
|---|---|
| Question-as-heading with a short direct answer underneath — measurable via snippet and citation capture | "Semantic content network" as a mystical whole |
| Entity coverage measured against a Wikidata/Wikipedia entity set — countable | "Historical data" or "trust" as levers you can pull |
| Publishing core topics before peripheral ones — testable at site level | Precise attribute-ordering prescriptions |
| Internal link density within a cluster — measurable | Claims about specific Google internals |

Do not present the framework to a client as established fact. Present the
mechanics, which stand on their own.

---

## Repair path

1. Run `playbooks/audit-blog.md` first if you have not. You need the inventory.
2. **Check `boilerplate_terms_ignored` before trusting any cluster.** If the
   blog's actual subject was stripped, the clusters are wrong — see
   `_process/topic-clustering-term-stripping-cuts-both-ways.md`.
3. For each cluster of 3+ posts:
   - Is there a clear hub? The inventory picks the post the cluster links to
     most, **not the longest** — length would elect the wordiest post.
   - **No clear hub is the most common reason a cluster underperforms.** The
     spokes are competing with each other instead of pointing at a pillar.
   - Fix by promoting an existing post to hub, or writing one, and wiring the
     spokes' **first contextual body link** to it.
4. Orphans: adopt into a cluster, or retire.
5. Cannibalisation pairs: consolidate and redirect, or differentiate the intent.
   Read both posts before deciding.

## Build path

1. Establish the central topic and the intent behind it.
2. **Entity coverage.** Pull the entity set for the topic from Wikipedia and
   Wikidata — free, no key, fully sanctioned, and the best available proxy for
   "what a domain expert would expect to see covered." Compare against what the
   blog has.
3. **Real questions.** Stack Exchange API (300/day free, 10,000 with a key),
   forums, and the brand's own inbox. These become spokes and FAQ entries.
   Do not plan around pytrends, Pushshift, Reddit's free tier, or any free
   People-Also-Ask route — all dead or ToS-hostile.
4. **Real numbers, if needed.** `mangools_keywords.py` or the Mangools MCP.
   Never state a volume or difficulty figure without one of those behind it; say
   which tool would supply it instead.
5. Hub, then 8–15 spokes, each owning one sub-topic and one query.
6. **Publishing order: 3–4 spokes first, then the hub, then the rest.** A hub
   published first is an orphan pillar with nothing pointing at it.
7. Split across the funnel and research the split rather than assuming a ratio.

---

## The link graph

- Every spoke links to the hub. The **first contextual body link** is the
  weighted one — put it there, not in a footer block.
- The hub links to every spoke.
- Spokes link sideways only where genuinely relevant.
- Anchors describe the destination. Do not repeat the same exact anchor
  site-wide.

---

## Output

- Cluster table: hub, spokes, the query each owns, current status.
- The missing link edges, as a specific list of "add a link from A to B".
- Publishing sequence with reasoning.
- Entity coverage: covered / missing, sourced from Wikidata.
- Consolidation decisions for cannibalising pairs.
- **What was assumed** — anything not backed by a tool or a source, labelled.

Save to `brands/<brand>/research/<date>-topical-map.md`.

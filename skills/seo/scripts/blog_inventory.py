#!/usr/bin/env python3
"""Turn a site_collect.py capture into a blog inventory: clusters, orphans, overlap.

site_collect.py already captures titles, headings, word counts, JSON-LD, content
hashes and internal link targets in one polite pass. Nothing consumed it for content
work, so this does: it reads that JSON and answers the questions that only exist at
corpus level and cannot be seen one URL at a time --

  * which posts form a topic cluster, and which cluster has no hub
  * which posts nothing links to (orphans)
  * which posts compete with each other for the same topic (cannibalisation)
  * which posts are byte-identical or near-identical
  * where the internal link graph is thin

DELIBERATE DESIGN CONSTRAINT: word count is emitted under `coverage`, never under
anything named quality, and no ranking in this script sorts by it. On a site with
mixed human and AI authorship, ranking by length surfaces the AI posts as the best
content and the human essays as thin -- that has already happened once in this
workspace. See _process/word-count-is-not-content-quality.md.

Usage:
    python site_collect.py --site https://example.com --out capture.json
    python blog_inventory.py capture.json --json
    python blog_inventory.py capture.json --path-contains /blog/ --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "best", "but", "by", "can", "do",
    "does", "for", "from", "guide", "has", "have", "how", "in", "is", "it", "its",
    "of", "on", "or", "that", "the", "their", "them", "there", "these", "they",
    "this", "to", "top", "was", "were", "what", "when", "where", "which", "who",
    "why", "will", "with", "you", "your", "we", "our", "us", "if", "not", "no",
    "so", "than", "then", "into", "about", "more", "most", "other", "some", "such",
    "only", "same", "too", "very", "just", "also", "here", "all", "any", "each",
    "vs", "versus", "com", "www", "html", "index", "blog", "post", "posts",
}

ARTICLE_TYPES = {"Article", "BlogPosting", "NewsArticle", "TechArticle", "Report"}
DATE_KEYS = ("datePublished", "dateModified", "dateCreated")


def toks(text: str) -> set:
    return {w for w in re.findall(r"[a-z][a-z0-9'-]+", (text or "").lower())
            if w not in STOPWORDS and len(w) > 2}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def path_of(url: str) -> str:
    try:
        p = urlparse(url).path or "/"
    except ValueError:
        return url
    return p.rstrip("/") or "/"


# --------------------------------------------------------------------------

def is_post(rec: dict, path_contains: str | None) -> bool:
    if rec.get("status") != 200:
        return False
    if path_contains:
        return path_contains in (rec.get("url") or "")
    if set(rec.get("jsonld_types") or []) & ARTICLE_TYPES:
        return True
    return bool(re.search(r"/(blog|articles?|posts?|insights?|news|journal)/[^/]+",
                          rec.get("url") or "", re.I))


def dates_from_jsonld(rec: dict) -> dict:
    found = {}
    stack = list(rec.get("jsonld") or [])
    while stack:
        node = stack.pop()
        if isinstance(node, list):
            stack.extend(node)
        elif isinstance(node, dict):
            for k in DATE_KEYS:
                if k in node and isinstance(node[k], str) and k not in found:
                    found[k] = node[k][:10]
            stack.extend(v for v in node.values() if isinstance(v, (dict, list)))
    return found


def build_rows(records: list, path_contains: str | None) -> list[dict]:
    rows = []
    for rec in records:
        if not is_post(rec, path_contains):
            continue
        headings = rec.get("headings") or {}
        h1 = (headings.get("h1") or [None])[0]
        h2s = headings.get("h2") or []
        topic = toks(rec.get("title")) | toks(h1) | toks(" ".join(h2s[:12]))
        rows.append({
            "url": rec.get("url"),
            "path": path_of(rec.get("url") or ""),
            "title": rec.get("title"),
            "h1": h1,
            "h2_count": len(h2s),
            "h2": h2s[:20],
            "dates": dates_from_jsonld(rec),
            "schema_types": rec.get("jsonld_types") or [],
            # Coverage, NOT quality. See the module docstring.
            "coverage": {
                "word_count": rec.get("main_word_count") or rec.get("word_count") or 0,
                "heading_total": rec.get("heading_total") or 0,
                "note": "Answers 'is there enough here to rank', never 'is this good'.",
            },
            "content_hash": rec.get("main_hash"),
            "canonical": rec.get("canonical"),
            "canonical_is_self": rec.get("canonical_is_self"),
            "robots_meta": rec.get("robots_meta") or [],
            "outbound_internal": rec.get("internal_paths") or [],
            "outbound_internal_count": rec.get("internal_link_count") or 0,
            "_topic": topic,
        })
    return rows


def link_graph(rows: list[dict], all_records: list) -> dict:
    """Inbound link counts. Count links from the WHOLE site, not just from posts --
    a post linked only from the blog index is still effectively orphaned, but a post
    linked from a service page is not, and counting posts only would miss that."""
    by_path = {r["path"]: r for r in rows}
    inbound = defaultdict(set)
    for rec in all_records:
        src = path_of(rec.get("url") or "")
        for target in rec.get("internal_paths") or []:
            tgt = path_of(target)
            if tgt in by_path and tgt != src:
                inbound[tgt].add(src)
    return {p: sorted(s) for p, s in inbound.items()}


MIN_POSTS_FOR_BOILERPLATE = 6
BOILERPLATE_SHARE = 0.8


def drop_boilerplate_terms(rows: list[dict],
                           max_share: float = BOILERPLATE_SHARE) -> list[str]:
    """Remove terms that appear in nearly every post -- they carry no topical signal.

    Brand names and author bylines sit in every <title> on a lot of sites. Left in,
    they dominate the token overlap and manufacture one giant false cluster whose
    "shared terms" are just the author's name. Observed on a real capture: all eight
    clusters shared exactly the two tokens of the author's name and nothing else.

    The thresholds are deliberately conservative. An earlier version used a 50% share
    with a floor of 2 posts, which on a small niche blog stripped the subject itself:
    across four sourdough posts it discarded "sourdough" and "starter" and then
    reported zero cannibalisation between two near-identical guides. A term shared by
    most posts on a single-topic blog is the topic, not boilerplate. Only strip at
    ~80% and only once there are enough posts for that to mean anything.
    """
    if len(rows) < MIN_POSTS_FOR_BOILERPLATE:
        return []
    df = Counter()
    for r in rows:
        df.update(r["_topic"])
    cutoff = max(3, int(round(len(rows) * max_share)))
    common = [t for t, c in df.items() if c >= cutoff]
    for r in rows:
        r["_topic"] = r["_topic"] - set(common)
    return sorted(common)


def cluster(rows: list[dict], threshold: float) -> list[list[int]]:
    """Greedy agglomeration on topic-token overlap. Deterministic: seeded in the
    input order so two runs over the same capture give the same clusters."""
    unassigned = list(range(len(rows)))
    clusters = []
    while unassigned:
        seed = unassigned.pop(0)
        group = [seed]
        changed = True
        while changed:
            changed = False
            for idx in list(unassigned):
                if any(jaccard(rows[idx]["_topic"], rows[m]["_topic"]) >= threshold
                       for m in group):
                    group.append(idx)
                    unassigned.remove(idx)
                    changed = True
        clusters.append(group)
    return clusters


def analyse(records: list, path_contains: str | None, threshold: float) -> dict:
    rows = build_rows(records, path_contains)
    if not rows:
        return {"error": "No blog posts identified.",
                "hint": "Pass --path-contains /blog/ if the URLs do not match the "
                        "default patterns and the pages carry no Article schema."}

    boilerplate = drop_boilerplate_terms(rows)
    inbound = link_graph(rows, records)
    for r in rows:
        r["inbound_internal"] = inbound.get(r["path"], [])
        r["inbound_count"] = len(r["inbound_internal"])

    groups = cluster(rows, threshold)
    clusters = []
    for gi, group in enumerate(groups):
        members = [rows[i] for i in group]
        # The hub is the member the rest of the cluster links to most, not the
        # longest one. Length would just re-elect the wordiest post.
        member_paths = {m["path"] for m in members}
        internal_pull = {
            m["path"]: len([s for s in m["inbound_internal"] if s in member_paths])
            for m in members
        }
        # A hub only means something once a cluster has spokes to anchor.
        hub = (max(members, key=lambda m: internal_pull[m["path"]])
               if len(members) >= 3 else None)
        has_hub = bool(hub and internal_pull[hub["path"]] >= max(1, len(members) - 2))
        clusters.append({
            "cluster_id": gi,
            "size": len(members),
            "shared_terms": sorted(set.intersection(*[m["_topic"] for m in members]))[:10]
                            if len(members) > 1 else sorted(members[0]["_topic"])[:10],
            "members": [m["path"] for m in members],
            "hub_candidate": hub["path"] if hub else None,
            "hub_inbound_from_cluster": internal_pull.get(hub["path"], 0) if hub else 0,
            "has_clear_hub": has_hub,
            "note": "" if has_hub or len(members) < 3 else
                    "No member is the clear hub: spokes are not linking to a pillar. "
                    "This is the most common reason a cluster underperforms.",
        })
        for i in group:
            rows[i]["cluster_id"] = gi

    orphans = [{"path": r["path"], "title": r["title"]}
               for r in rows if r["inbound_count"] == 0]
    thin_links = [{"path": r["path"], "outbound": r["outbound_internal_count"]}
                  for r in rows if r["outbound_internal_count"] < 3]

    # Exact duplicates by content hash.
    by_hash = defaultdict(list)
    for r in rows:
        if r["content_hash"]:
            by_hash[r["content_hash"]].append(r["path"])
    exact_dupes = [{"hash": h, "paths": p} for h, p in by_hash.items() if len(p) > 1]

    # Cannibalisation: distinct posts whose topics overlap heavily.
    cannibal = []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            sim = jaccard(rows[i]["_topic"], rows[j]["_topic"])
            if sim >= 0.55:
                cannibal.append({
                    "similarity": round(sim, 2),
                    "a": {"path": rows[i]["path"], "title": rows[i]["title"]},
                    "b": {"path": rows[j]["path"], "title": rows[j]["title"]},
                })
    cannibal.sort(key=lambda c: -c["similarity"])

    noindex = [r["path"] for r in rows
               if any("noindex" in d.lower() for d in r["robots_meta"])]
    bad_canonical = [{"path": r["path"], "canonical": r["canonical"]}
                     for r in rows if r["canonical"] and not r["canonical_is_self"]]
    undated = [r["path"] for r in rows if not r["dates"]]

    for r in rows:
        r.pop("_topic", None)

    return {
        "posts": len(rows),
        "boilerplate_terms_ignored": boilerplate,
        "clusters": clusters,
        "issues": {
            "orphans": orphans,
            "thin_outbound_linking": thin_links,
            "cannibalisation_candidates": cannibal[:25],
            "exact_duplicates": exact_dupes,
            "noindexed_posts": noindex,
            "canonical_points_elsewhere": bad_canonical,
            "no_date_in_schema": undated,
        },
        "inventory": rows,
        "not_measured": [
            "Content quality. This script reports coverage (word count, heading "
            "count) and structure only. Read the posts.",
            "Near-duplicate content below byte-identical. Use duplicate_content.py, "
            "which does shingling.",
            "Traffic, rankings and decay. Those need Search Console; see "
            "content_decay_detector.py with a GSC export.",
            "Whether a cluster's topic is worth owning. That is a research question, "
            "not a crawl question.",
        ],
    }


def summarise(r: dict) -> list[str]:
    if "error" in r:
        return [r["error"], r.get("hint", "")]
    i = r["issues"]
    lines = [f"Posts: {r['posts']}   Clusters: {len(r['clusters'])}"]
    if r.get("boilerplate_terms_ignored"):
        lines.append("Site-wide terms ignored when clustering (brand/author boilerplate): "
                     + ", ".join(r["boilerplate_terms_ignored"][:12]))
    lines.append("")
    lines.append("CLUSTERS")
    for c in sorted(r["clusters"], key=lambda c: -c["size"]):
        flag = "" if c["has_clear_hub"] or c["size"] < 3 else "   <-- NO CLEAR HUB"
        lines.append(f"  [{c['size']:>2} posts] {', '.join(c['shared_terms'][:5]) or '(no shared terms)'}{flag}")
        if c["hub_candidate"]:
            lines.append(f"           hub candidate: {c['hub_candidate']}")
        else:
            for m in c["members"]:
                lines.append(f"           {m}")
    lines += ["", "ISSUES"]
    lines.append(f"  Orphans (nothing links to them):     {len(i['orphans'])}")
    for o in i["orphans"][:8]:
        lines.append(f"      {o['path']}")
    lines.append(f"  Thin outbound linking (<3 links):    {len(i['thin_outbound_linking'])}")
    lines.append(f"  Cannibalisation candidates:          {len(i['cannibalisation_candidates'])}")
    for c in i["cannibalisation_candidates"][:5]:
        lines.append(f"      {c['similarity']}  {c['a']['path']}  vs  {c['b']['path']}")
    lines.append(f"  Exact duplicate content:             {len(i['exact_duplicates'])}")
    lines.append(f"  Noindexed posts:                     {len(i['noindexed_posts'])}")
    lines.append(f"  Canonical points elsewhere:          {len(i['canonical_points_elsewhere'])}")
    lines.append(f"  No date in schema:                   {len(i['no_date_in_schema'])}")
    lines += ["", "Not measured by this script:"]
    for n in r["not_measured"]:
        lines.append(f"  - {n}")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a blog inventory from a site_collect.py capture.")
    parser.add_argument("capture", help="JSON file written by site_collect.py --out")
    parser.add_argument("--path-contains",
                        help="Only treat URLs containing this substring as posts (e.g. /blog/)")
    parser.add_argument("--cluster-threshold", type=float, default=0.28,
                        help="Topic-token Jaccard threshold for clustering (default 0.28)")
    parser.add_argument("--json", "-j", action="store_true")
    args = parser.parse_args()

    with open(args.capture, "r", encoding="utf-8") as fh:
        records = json.load(fh)
    if isinstance(records, dict):
        records = records.get("pages") or records.get("results") or []

    result = analyse(records, args.path_contains, args.cluster_threshold)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n".join(summarise(result)))


if __name__ == "__main__":
    main()

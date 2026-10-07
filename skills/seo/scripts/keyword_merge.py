#!/usr/bin/env python3
"""
Competitor Keyword Merge & Triage

Deterministic stage of the competitor-mining pipeline. Takes the raw JSON each
miner agent wrote, plus our own site's coverage, and produces one deduplicated,
scored, labelled keyword table.

This is a script and not an agent on purpose: deduplication is string
normalisation, and a model doing it silently drops rows and invents merges.

No API keys, no network. Free-mode scoring only -- it never emits a search
volume or a keyword difficulty score, because nothing here measures either.
Priority is a tier derived from named, checkable evidence.

Input directory layout (see playbooks/research-competitor-mining.md):

    <staging>/mined/<competitor>.json    one per miner agent
    <staging>/ours/site.json             our own coverage (optional)

Usage:
    python skills/seo/scripts/keyword_merge.py <staging_dir>
    python skills/seo/scripts/keyword_merge.py <staging_dir> --json
    python skills/seo/scripts/keyword_merge.py <staging_dir> --min-competitors 2
"""

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

# Evidence strength. A term in a title tag is a far stronger statement of
# targeting than the same words appearing in an anchor somewhere.
EVIDENCE_WEIGHT = {
    "title": 5,
    "h1": 5,
    "slug": 4,
    "h2": 3,
    "nav": 3,
    "anchor": 2,
    "meta": 2,
    "h3": 1,
    "body": 1,
    # Query-source evidence: these came from a real search surface, not from
    # the competitor's own phrasing, so they prove the query exists.
    "autocomplete": 4,
    "paa": 4,
    "related_search": 3,
}

QUERY_SOURCED = {"autocomplete", "paa", "related_search"}

# Only stripped at the edges of a term, never from the middle -- stripping
# inside changes intent ("tools for x" is not "tools x").
EDGE_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "for", "in", "on", "at",
    "is", "are", "your", "my", "our", "with", "by",
}

YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
PUNCT_RE = re.compile(r"[^\w\s-]", re.UNICODE)
WS_RE = re.compile(r"\s+")


# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------

def normalize(term):
    """Conservative normalisation: enough to dedupe, not enough to merge two
    different intents into one row."""
    t = unicodedata.normalize("NFKD", term or "")
    t = t.casefold()
    t = t.replace("&", " and ")
    t = PUNCT_RE.sub(" ", t)
    t = YEAR_RE.sub(" ", t)
    t = WS_RE.sub(" ", t).strip()

    words = t.split()
    while words and words[0] in EDGE_STOPWORDS:
        words.pop(0)
    while words and words[-1] in EDGE_STOPWORDS:
        words.pop()
    return " ".join(words)


def brand_tokens(domain):
    """Brand words implied by a domain, for brand-term detection.
    blog.example.com -> {'example'}"""
    host = re.sub(r"^https?://", "", (domain or "")).split("/")[0]
    host = re.sub(r"^www\.", "", host)
    parts = host.split(".")
    generic = {"com", "co", "in", "net", "org", "io", "app", "dev", "blog",
               "shop", "store", "www", "uk", "us", "au", "ai", "me"}
    return {p for p in parts if p and p not in generic and len(p) > 2}


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_mined(staging):
    mined_dir = staging / "mined"
    if not mined_dir.is_dir():
        sys.exit("Error: no mined/ directory in %s. Miner agents write one "
                 "JSON per competitor there." % staging)
    files = sorted(mined_dir.glob("*.json"))
    if not files:
        sys.exit("Error: %s is empty. Nothing to merge." % mined_dir)

    docs = []
    for f in files:
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print("  ! skipped %s: invalid JSON (%s)" % (f.name, e),
                  file=sys.stderr)
            continue
        doc.setdefault("competitor", f.stem)
        doc.setdefault("candidates", [])
        docs.append(doc)
    if not docs:
        sys.exit("Error: every file in mined/ failed to parse.")
    return docs


def load_ours(staging):
    """Returns (covered_terms, our_brand_tokens, our_urls_by_term)."""
    path = staging / "ours" / "site.json"
    if not path.is_file():
        return set(), set(), {}
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print("  ! ours/site.json is invalid JSON (%s); treating our coverage "
              "as unknown" % e, file=sys.stderr)
        return set(), set(), {}

    covered, urls = set(), {}
    for item in doc.get("candidates", []) or []:
        key = normalize(item.get("term", ""))
        if not key:
            continue
        covered.add(key)
        if item.get("url") and key not in urls:
            urls[key] = item["url"]
    return covered, brand_tokens(doc.get("domain", "")), urls


# ---------------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------------

def merge(docs):
    rows = defaultdict(lambda: {
        "display": None,
        "competitors": set(),
        "evidence": set(),
        "urls": [],
        "hub_hits": 0,
        "inbound_max": 0,
        "intents": [],
        "clusters": [],
        "query_sourced": False,
        "display_counts": defaultdict(int),
    })

    for doc in docs:
        comp = doc["competitor"]
        for c in doc.get("candidates", []) or []:
            raw = (c.get("term") or "").strip()
            key = normalize(raw)
            if not key or len(key) < 3:
                continue

            r = rows[key]
            r["competitors"].add(comp)
            r["display_counts"][raw] += 1

            ev = (c.get("evidence") or "body").strip().lower()
            r["evidence"].add(ev)
            if ev in QUERY_SOURCED:
                r["query_sourced"] = True

            url = c.get("url")
            if url and url not in r["urls"]:
                r["urls"].append(url)

            if c.get("hub"):
                r["hub_hits"] += 1
            try:
                r["inbound_max"] = max(
                    r["inbound_max"], int(c.get("inbound_internal_links") or 0))
            except (TypeError, ValueError):
                pass

            if c.get("intent_guess"):
                r["intents"].append(c["intent_guess"])
            if c.get("cluster_hint"):
                r["clusters"].append(c["cluster_hint"])

    for key, r in rows.items():
        # Display form = the phrasing most competitors actually used.
        r["display"] = max(r["display_counts"].items(),
                           key=lambda kv: (kv[1], -len(kv[0])))[0]
        del r["display_counts"]
    return rows


def score(r, is_brand):
    """Returns (score, tier). Deliberately not a volume estimate."""
    comp_n = len(r["competitors"])

    # Demand proxy: how many independent competitors bet on this topic.
    s = {0: 0, 1: 10}.get(comp_n, 10 + (comp_n - 1) * 18)

    # Strongest evidence type seen anywhere.
    s += max((EVIDENCE_WEIGHT.get(e, 1) for e in r["evidence"]), default=1) * 3

    # They point their own internal links at it -> they believe it earns.
    # Only counted when the term also has EDITORIAL evidence. A global-nav
    # label sits on every page, so its inbound count is structural, not a
    # statement of intent -- without this guard, site furniture ("our
    # philosophy", "cold pressed oil") outranks real target keywords.
    editorial = r["evidence"] & {"title", "h1", "h2", "h3", "slug", "meta"}
    if editorial:
        s += min(r["hub_hits"], 3) * 8
        s += min(r["inbound_max"], 20)

    # Proven to be a real query, not just their phrasing.
    if r["query_sourced"]:
        s += 15

    if is_brand:
        s -= 60

    if s >= 65:
        tier = "A"
    elif s >= 38:
        tier = "B"
    else:
        tier = "C"
    return s, tier


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Merge, dedupe and tier competitor keyword candidates.")
    ap.add_argument("staging",
                    help="Staging directory containing mined/ and ours/")
    ap.add_argument("--min-competitors", type=int, default=1,
                    help="Drop terms targeted by fewer than N competitors "
                         "(default 1)")
    ap.add_argument("--drop-brand-terms", action="store_true",
                    help="Remove competitor brand terms entirely "
                         "(default: keep but flag)")
    ap.add_argument("--json", action="store_true",
                    help="Print JSON summary to stdout")
    args = ap.parse_args()

    staging = Path(args.staging)
    if not staging.is_dir():
        sys.exit("Error: %s is not a directory." % staging)

    docs = load_mined(staging)
    covered, our_brand, our_urls = load_ours(staging)

    all_brand = set()
    for d in docs:
        all_brand |= brand_tokens(d.get("domain") or d["competitor"])

    rows = merge(docs)

    out = []
    for key, r in rows.items():
        if len(r["competitors"]) < args.min_competitors:
            continue

        words = set(key.split())
        # Token match catches "acme login". The de-spaced check also
        # catches a brand written as two words ("acme labs" vs the domain
        # token "acmelabs"), which a token match alone silently misses.
        squashed = key.replace(" ", "")
        is_brand = bool(words & all_brand) or any(
            b in squashed for b in all_brand if len(b) >= 6)
        if is_brand and args.drop_brand_terms:
            continue

        s, tier = score(r, is_brand)
        we_cover = key in covered

        if we_cover:
            bucket = "re-optimize"
        elif is_brand:
            bucket = "competitor-brand"
        else:
            bucket = "new"

        # The claim being made determines the label. That a competitor page
        # targets this term is Confirmed -- a page was fetched and read. That
        # it is an opportunity for us is inference: Likely.
        if r["urls"] and (r["evidence"] & {"title", "h1", "slug"}):
            claim, label = "targeted-by-competitor", "Confirmed"
        elif r["query_sourced"]:
            claim, label = "query-exists", "Confirmed"
        else:
            claim, label = "inferred-target", "Likely"

        intents = sorted(set(r["intents"]))
        clusters = sorted(set(r["clusters"]))

        out.append({
            "term": r["display"],
            "normalized": key,
            "priority_tier": tier,
            "score": s,
            "bucket": bucket,
            "competitor_count": len(r["competitors"]),
            "competitors": ",".join(sorted(r["competitors"])),
            "best_evidence": max(r["evidence"],
                                 key=lambda e: EVIDENCE_WEIGHT.get(e, 1)),
            "all_evidence": ",".join(sorted(r["evidence"])),
            "query_sourced": r["query_sourced"],
            "hub_signal": r["hub_hits"] > 0,
            "max_inbound_internal_links": r["inbound_max"],
            "intent_guess": ",".join(intents),
            "cluster_hint": clusters[0] if clusters else "",
            "we_cover": we_cover,
            "our_url": our_urls.get(key, ""),
            "claim": claim,
            "label": label,
            "verify_url": r["urls"][0] if r["urls"] else "",
            "all_urls": " ".join(r["urls"][:5]),
        })

    out.sort(key=lambda x: (-x["score"], x["term"]))

    merged_dir = staging / "merged"
    merged_dir.mkdir(parents=True, exist_ok=True)
    csv_path = merged_dir / "keywords-master.csv"

    if out:
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
            w.writeheader()
            w.writerows(out)

    summary = {
        "staging": str(staging),
        "competitors_merged": [d["competitor"] for d in docs],
        "raw_candidates": sum(len(d.get("candidates") or []) for d in docs),
        "unique_terms": len(rows),
        "after_filters": len(out),
        "tier_a": sum(1 for r in out if r["priority_tier"] == "A"),
        "tier_b": sum(1 for r in out if r["priority_tier"] == "B"),
        "tier_c": sum(1 for r in out if r["priority_tier"] == "C"),
        "new": sum(1 for r in out if r["bucket"] == "new"),
        "re_optimize": sum(1 for r in out if r["bucket"] == "re-optimize"),
        "competitor_brand": sum(1 for r in out
                                if r["bucket"] == "competitor-brand"),
        "confirmed": sum(1 for r in out if r["label"] == "Confirmed"),
        "likely": sum(1 for r in out if r["label"] == "Likely"),
        "our_coverage_known": bool(covered),
        "output_csv": str(csv_path) if out else None,
        "note": "No search volume or KD in this table. Nothing here "
                "measures either.",
    }
    (merged_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(summary, indent=2))
        return

    print("Merged %d competitor file(s)" % len(docs))
    print("  raw candidates    : %d" % summary["raw_candidates"])
    print("  unique terms      : %d" % summary["unique_terms"])
    print("  after filters     : %d" % summary["after_filters"])
    print("  tiers A/B/C       : %d/%d/%d" % (summary["tier_a"],
                                              summary["tier_b"],
                                              summary["tier_c"]))
    print("  new / re-optimize : %d / %d" % (summary["new"],
                                             summary["re_optimize"]))
    print("  competitor brand  : %d (flagged)" % summary["competitor_brand"])
    print("  Confirmed / Likely: %d / %d" % (summary["confirmed"],
                                             summary["likely"]))
    if not covered:
        print("  ! ours/site.json missing -- 'we already cover this' is "
              "unknown,")
        print("    so every term is bucketed 'new'. Collect our site first.")
    if out:
        print("\nWrote %s" % csv_path)


if __name__ == "__main__":
    main()

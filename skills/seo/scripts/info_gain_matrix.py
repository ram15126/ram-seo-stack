#!/usr/bin/env python3
"""Claim-level information-gain diff between a target page and the pages that outrank it.

Produces the SERP gap matrix that references/information-gain-writing.md describes as
a manual step, and classifies each gap with references/gap-classification-rubric.md.

The deliverable is a CLAIM DIFF, not a similarity number:

  * claims the competitors make that the target does not  -> what to add
  * claims only the target makes                          -> the actual information gain
  * topic coverage matrix, with depth, in rank order      -> Core / Differentiator /
                                                             Commodity / Opportunity

A cosine similarity is also reported, but only as a coarse gate. The patent describes
a trained model, not cosine over TF-IDF, so treat `1 - max(cos)` as a rough novelty
indicator and the claim diff as the thing you act on.

IMPORTANT, and not a limitation to hide from a client: this script does NOT fetch a
SERP. There is no free, ToS-clean, no-key route to Google results. You supply the
competitor URLs in ranking order (position 1 first) from whatever SERP source you
trust -- SerpChecker, the Mangools MCP, or reading the SERP yourself.

Usage:
    python info_gain_matrix.py TARGET_URL --competitors URL1 URL2 URL3 --json
    python info_gain_matrix.py target.html --competitor-file serp.txt --json
    python info_gain_matrix.py TARGET --competitors U1 U2 U3 --questions-file paa.txt
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter

try:
    from seo_common import load_html, parse_html
except ImportError:  # pragma: no cover
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from seo_common import load_html, parse_html


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "can", "do", "does",
    "for", "from", "has", "have", "how", "in", "is", "it", "its", "of", "on", "or",
    "that", "the", "their", "them", "there", "these", "they", "this", "to", "was",
    "were", "what", "when", "where", "which", "who", "why", "will", "with", "you",
    "your", "we", "our", "us", "i", "if", "not", "no", "so", "than", "then", "into",
    "about", "more", "most", "other", "some", "such", "only", "own", "same", "too",
    "very", "just", "also", "here", "all", "any", "each", "few", "up", "out", "over",
}

# A claim is a sentence carrying something checkable. Vague prose is not a claim.
HAS_NUMBER = re.compile(r"\d")
HAS_PROPER_NOUN = re.compile(r"\b[A-Z][a-z]{2,}\b")
IS_DEFINITION = re.compile(r"\b(is|are|refers to|means|stands for|describes)\b", re.I)
IS_COMPARATIVE = re.compile(
    r"\b(faster|slower|cheaper|better|worse|larger|smaller|higher|lower|more|less|"
    r"unlike|compared to|versus|vs\.?|instead of|rather than|outperform\w*)\b", re.I
)
BOILERPLATE = re.compile(
    r"\b(cookie|privacy policy|terms of service|subscribe|newsletter|all rights "
    r"reserved|sign up|log in|share this|read more|related posts)\b", re.I
)


# --------------------------------------------------------------------------
# Extraction
# --------------------------------------------------------------------------

def tokens(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z][a-z'-]+", (text or "").lower())
            if w not in STOPWORDS and len(w) > 2]


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(\[])", text or "")
    return [p.strip() for p in parts if 4 <= len(p.split()) <= 80]


def prose_blocks(soup) -> list[str]:
    """Text of block-level prose elements, separately.

    Do not run claim extraction over one flattened body_text string: parse_html joins
    every element with a space, so a heading runs straight into the paragraph beneath
    it and the first "sentence" of the page becomes 'Title Title Heading The actual
    claim...'. Extracting per block keeps sentence boundaries real.
    """
    blocks = []
    for el in soup.find_all(["p", "li", "td", "blockquote", "dd"]):
        text = el.get_text(" ", strip=True)
        if text:
            blocks.append(re.sub(r"\s+", " ", text))
    return blocks


def extract_claims(blocks: list[str], cap: int = 400) -> list[str]:
    """Sentences that assert something specific enough to be checked or contradicted."""
    out = []
    sentences = [s for block in blocks for s in split_sentences(block)]
    for sentence in sentences:
        if BOILERPLATE.search(sentence):
            continue
        signals = sum([
            bool(HAS_NUMBER.search(sentence)),
            bool(HAS_PROPER_NOUN.search(sentence)),
            bool(IS_DEFINITION.search(sentence)),
            bool(IS_COMPARATIVE.search(sentence)),
        ])
        if signals >= 2:
            out.append(re.sub(r"\s+", " ", sentence).strip())
        if len(out) >= cap:
            break
    return out


def extract_sections(soup) -> list[dict]:
    """Headings plus the word count beneath each -- depth is what the rubric needs."""
    sections = []
    headings = soup.find_all(["h2", "h3"])
    for i, h in enumerate(headings):
        title = h.get_text(" ", strip=True)
        if not title or len(title) > 140:
            continue
        words = 0
        node = h
        while True:
            node = node.find_next()
            if node is None or node in headings[i + 1:i + 2]:
                break
            if getattr(node, "name", None) in ("h2", "h3"):
                break
            if getattr(node, "name", None) in ("p", "li", "td", "blockquote"):
                words += len(node.get_text(" ", strip=True).split())
        sections.append({
            "title": title,
            "level": h.name,
            "words": words,
            "tokens": set(tokens(title)),
        })
    return sections


def load_page(source: str, timeout: int) -> dict:
    fetch_error = None
    if os.path.exists(source):
        with open(source, "r", encoding="utf-8", errors="replace") as fh:
            html = fh.read()
        url = ""
    else:
        html, url, fetched = load_html(source, timeout=timeout)
        status = fetched.get("status")
        if fetched.get("error"):
            fetch_error = str(fetched["error"])
        elif status is not None and status >= 400:
            fetch_error = "HTTP %s" % status

    parsed = parse_html(html, url)
    body = parsed.get("body_text") or ""
    blocks = prose_blocks(parsed["soup"])

    # A page that failed to load contributes zero claims and zero sections, which
    # silently reads as "this competitor covers nothing" -- inflating the target's
    # apparent information gain and hiding real gaps. Surface it instead.
    if fetch_error is None and not os.path.exists(source) and len(body.split()) < 150:
        fetch_error = ("only %d words retrieved -- likely client-rendered; re-fetch "
                       "with a JS-rendering client" % len(body.split()))

    return {
        "source": source,
        "url": url or source,
        "fetch_error": fetch_error,
        "title": parsed.get("title"),
        "word_count": len(body.split()),
        "sections": extract_sections(parsed["soup"]),
        "claims": extract_claims(blocks),
        "tokens": tokens(body),
    }


# --------------------------------------------------------------------------
# Similarity (coarse gate only)
# --------------------------------------------------------------------------

def tfidf_cosine(docs: list[list[str]]) -> list[list[float]]:
    n = len(docs)
    df = Counter()
    for d in docs:
        df.update(set(d))
    vectors = []
    for d in docs:
        tf = Counter(d)
        total = sum(tf.values()) or 1
        vec = {t: (c / total) * math.log((n + 1) / (df[t] + 1)) + 1e-9
               for t, c in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        vectors.append({t: v / norm for t, v in vec.items()})
    out = []
    for a in vectors:
        row = []
        for b in vectors:
            shared = set(a) & set(b)
            row.append(round(sum(a[t] * b[t] for t in shared), 4))
        out.append(row)
    return out


def claim_similarity(a: str, b: str) -> float:
    ta, tb = set(tokens(a)), set(tokens(b))
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def dedupe_claims(claims: list[str], threshold: float = 0.6) -> list[str]:
    kept: list[str] = []
    for c in claims:
        if not any(claim_similarity(c, k) >= threshold for k in kept):
            kept.append(c)
    return kept


# --------------------------------------------------------------------------
# Gap classification (references/gap-classification-rubric.md)
# --------------------------------------------------------------------------

def topic_matches(a: set, b: set) -> bool:
    if not a or not b:
        return False
    if a <= b or b <= a:
        return True
    return len(a & b) / len(a | b) >= 0.5


def build_matrix(target: dict, competitors: list[dict], questions: list[str]) -> list[dict]:
    """One row per competitor topic, with per-competitor depth and a rubric bucket."""
    top3 = competitors[:3]
    rows: list[dict] = []

    for comp_index, comp in enumerate(competitors):
        for section in comp["sections"]:
            if any(topic_matches(section["tokens"], r["tokens"]) for r in rows):
                continue

            coverage = []
            for i, other in enumerate(competitors):
                match = next((s for s in other["sections"]
                              if topic_matches(section["tokens"], s["tokens"])), None)
                coverage.append({
                    "position": i + 1,
                    "covered": match is not None,
                    "words": match["words"] if match else 0,
                })

            target_match = next((s for s in target["sections"]
                                 if topic_matches(section["tokens"], s["tokens"])), None)

            in_top3 = sum(1 for c in coverage[:3] if c["covered"])
            # "Material" in the rubric means a real H2 section or multi-paragraph
            # treatment, not a sentence in passing. 80 words is about two paragraphs.
            material = sum(1 for c in coverage[:3] if c["words"] >= 80)
            shallow_everywhere = (
                in_top3 == len(top3) and all(0 < c["words"] < 60 for c in coverage[:3])
            )
            # Position correlation: covered by the higher-ranked pages but not the lower.
            covering = [c["position"] for c in coverage[:3] if c["covered"]]
            not_covering = [c["position"] for c in coverage[:3] if not c["covered"]]
            correlates = bool(covering and not_covering
                              and max(covering) < min(not_covering))

            if target_match:
                bucket, action = "covered", "Already covered on the target page."
            elif in_top3 == len(top3) and material >= 2:
                bucket, action = "Core", "Must add. Google treats this as part of the answer."
            elif shallow_everywhere:
                bucket, action = "Commodity", "Add one sentence. Do not build a section."
            elif 1 <= in_top3 < len(top3) and correlates:
                bucket, action = "Differentiator", "Add if scope allows; it correlates with position."
            elif in_top3 == len(top3):
                # Covered by everyone at real depth, but under the "material" bar in
                # 2+ of them. Still a Core gap: every result treats it as part of the
                # answer. Without this branch such topics fell through to Commodity,
                # which told the writer to add one sentence about the main subject.
                bucket, action = "Core", "Must add. Every top result treats this as part of the answer."
            elif 1 <= in_top3 < len(top3):
                bucket, action = "Differentiator (weak)", "Covered by some, no clear position signal."
            else:
                bucket, action = "Commodity", "Low priority."

            rows.append({
                "topic": section["title"],
                "tokens": section["tokens"],
                "first_seen_at_position": comp_index + 1,
                "covered_in_top3": f"{in_top3}/{len(top3)}",
                "coverage": coverage,
                "on_target_page": bool(target_match),
                "target_words": target_match["words"] if target_match else 0,
                "bucket": bucket,
                "action": action,
            })

    # Opportunity gaps: topics NOTHING in the SERP covers, surfaced from the supplied
    # question list. Without external signal these cannot be distinguished from noise,
    # so they are candidates until a human confirms.
    for q in questions:
        qt = set(tokens(q))
        if not qt:
            continue
        anywhere = any(topic_matches(qt, s["tokens"])
                       for page in competitors + [target] for s in page["sections"])
        if not anywhere:
            rows.append({
                "topic": q,
                "tokens": qt,
                "first_seen_at_position": None,
                "covered_in_top3": "0/%d" % len(top3),
                "coverage": [],
                "on_target_page": False,
                "target_words": 0,
                "bucket": "Opportunity (candidate)",
                "action": "Nobody in the SERP covers this and a real question asks it. "
                          "Confirm it is genuinely relevant, then consider leading with it.",
            })

    for r in rows:
        r.pop("tokens", None)
    return rows


# --------------------------------------------------------------------------

def analyse(target_src: str, competitor_srcs: list[str], questions: list[str],
            timeout: int) -> dict:
    target = load_page(target_src, timeout)
    competitors = [load_page(u, timeout) for u in competitor_srcs]

    failed = [{"url": p["url"], "error": p["fetch_error"]}
              for p in [target] + competitors if p["fetch_error"]]
    if target["fetch_error"]:
        return {
            "error": "The target page could not be read: %s" % target["fetch_error"],
            "fix": "Re-fetch before analysing. Nothing below can be measured from an "
                   "empty document, and reporting gaps from one would describe the "
                   "fetch failure, not the page.",
            "failed_fetches": failed,
        }
    # Drop unreadable competitors rather than counting them as covering nothing --
    # that would inflate the target's apparent information gain.
    usable = [c for c in competitors if not c["fetch_error"]]

    competitors = usable
    if not competitors:
        return {
            "error": "No competitor page could be read.",
            "failed_fetches": failed,
        }
    sims = tfidf_cosine([target["tokens"]] + [c["tokens"] for c in competitors])
    to_comp = sims[0][1:]
    max_sim = max(to_comp) if to_comp else 0.0

    # Claims present in competitors but absent from the target.
    target_claims = target["claims"]
    missing = []
    for i, comp in enumerate(competitors):
        for claim in comp["claims"]:
            if not any(claim_similarity(claim, t) >= 0.45 for t in target_claims):
                missing.append({"position": i + 1, "url": comp["url"], "claim": claim})

    # Claims only the target makes -- the actual information gain.
    all_competitor_claims = [c for comp in competitors for c in comp["claims"]]
    unique = [t for t in target_claims
              if not any(claim_similarity(t, c) >= 0.45 for c in all_competitor_claims)]

    matrix = build_matrix(target, competitors, questions)
    buckets = Counter(r["bucket"] for r in matrix)

    return {
        "target": {"url": target["url"], "title": target["title"],
                   "word_count": target["word_count"],
                   "sections": len(target["sections"]), "claims": len(target_claims)},
        "competitors": [{"position": i + 1, "url": c["url"], "title": c["title"],
                         "word_count": c["word_count"], "sections": len(c["sections"]),
                         "claims": len(c["claims"])}
                        for i, c in enumerate(competitors)],
        "novelty_gate": {
            "cosine_to_each_competitor": [round(s, 3) for s in to_comp],
            "max_cosine": round(max_sim, 3),
            "novelty_score": round(1 - max_sim, 3),
            "note": (
                "Coarse gate only. The patent describes a trained model over document "
                "embeddings, not cosine over TF-IDF, so this is a proxy and nothing "
                "more. A commonly cited practitioner threshold is >0.5 = meaningfully "
                "different; it has no published validation. Act on the claim diff."
            ),
        },
        "information_gain": {
            "claims_only_on_target": dedupe_claims(unique)[:40],
            "count": len(unique),
            "note": (
                "These are the passages a reader can get ONLY here. If this list is "
                "short or generic, the page has no reason to outrank the incumbents. "
                "The 10-10-80 target in information-gain-writing.md means most of the "
                "page should be in this list."
            ),
        },
        "gaps": {
            "claims_missing_from_target": dedupe_claims(
                [m["claim"] for m in missing])[:40],
            "count": len(missing),
        },
        "coverage_matrix": matrix,
        "bucket_summary": dict(buckets),
        "failed_fetches": failed,
        "method_limits": [
            "No SERP was fetched. Competitor URLs and their order were supplied by "
            "the caller; if that order is wrong, the Differentiator classification is "
            "wrong with it.",
            "Claim extraction is heuristic (sentences carrying numbers, named "
            "entities, definitions or comparisons). It will miss claims phrased "
            "vaguely and will admit some non-claims. Read the lists.",
            "Opportunity gaps need external signal (People Also Ask, forum threads, "
            "Stack Exchange). Supply them with --questions-file; without it the "
            "opportunity bucket stays empty rather than guessing.",
            "Information gain as a live Google ranking factor is Unverified. See "
            "references/information-gain-writing.md -> ## Status.",
        ],
    }


def summarise(r: dict) -> list[str]:
    if "error" in r:
        out = [r["error"]]
        if r.get("fix"):
            out.append(r["fix"])
        for f in r.get("failed_fetches", []):
            out.append("  FAILED  %s  -- %s" % (f["url"][:70], f["error"]))
        return out
    t = r["target"]
    lines = [
        f"Target: {t['url']}",
        f"  {t['word_count']} words, {t['sections']} sections, {t['claims']} claims",
        "",
        "Competitors (in supplied rank order):",
    ]
    for c in r["competitors"]:
        lines.append(f"  {c['position']}. {c['word_count']:>6} words, "
                     f"{c['claims']:>3} claims  {c['url'][:70]}")
    ng = r["novelty_gate"]
    lines += [
        "",
        f"Novelty gate: max cosine {ng['max_cosine']} -> novelty {ng['novelty_score']} "
        f"(proxy only)",
        "",
        f"INFORMATION GAIN - claims only the target makes ({r['information_gain']['count']}):",
    ]
    for c in r["information_gain"]["claims_only_on_target"][:8]:
        lines.append(f"  + {c[:150]}")
    lines += ["", f"GAPS - claims competitors make that the target does not "
                  f"({r['gaps']['count']}):"]
    for c in r["gaps"]["claims_missing_from_target"][:8]:
        lines.append(f"  - {c[:150]}")

    lines += ["", "COVERAGE MATRIX (topics not on the target page):"]
    for row in r["coverage_matrix"]:
        if row["on_target_page"]:
            continue
        lines.append(f"  [{row['bucket']:<22}] {row['covered_in_top3']}  {row['topic'][:70]}")
    if r.get("failed_fetches"):
        lines += ["", "COMPETITORS DROPPED (could not be read - NOT counted as covering nothing):"]
        for f in r["failed_fetches"]:
            lines.append("  %s  -- %s" % (f["url"][:66], f["error"]))
    lines += ["", "Buckets: " + json.dumps(r["bucket_summary"]), "", "Method limits:"]
    for lim in r["method_limits"]:
        lines.append(f"  - {lim}")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Claim-level information-gain diff against the pages that outrank you.")
    parser.add_argument("target", help="Target URL or local HTML file")
    parser.add_argument("--competitors", nargs="*", default=[],
                        help="Competitor URLs IN RANKING ORDER (position 1 first)")
    parser.add_argument("--competitor-file",
                        help="File of competitor URLs, one per line, in ranking order")
    parser.add_argument("--questions-file",
                        help="File of real questions (PAA, Stack Exchange, forums), one "
                             "per line. Required for the Opportunity bucket.")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--json", "-j", action="store_true")
    args = parser.parse_args()

    comps = list(args.competitors)
    if args.competitor_file:
        with open(args.competitor_file, "r", encoding="utf-8") as fh:
            comps += [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    if not comps:
        parser.error("no competitors supplied. This script does not fetch a SERP -- "
                     "pass --competitors or --competitor-file in ranking order.")

    questions = []
    if args.questions_file:
        with open(args.questions_file, "r", encoding="utf-8") as fh:
            questions = [l.strip() for l in fh if l.strip() and not l.startswith("#")]

    result = analyse(args.target, comps, questions, args.timeout)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n".join(summarise(result)))


if __name__ == "__main__":
    main()

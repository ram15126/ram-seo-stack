#!/usr/bin/env python3
"""Report measurable AI-writing markers in a page or draft.

This reports EVIDENCE, never a verdict. It does not estimate whether a human or a
model wrote the text, and its output must never be presented as an authorship
judgement. GPT detectors carry a ~61.3% false-positive rate on non-native English
writers (Liang et al., Patterns 2023), which is why this script counts markers and
prints their locations instead of producing a probability.

Marker taxonomy follows Wikipedia's "Signs of AI writing" (WikiProject AI Cleanup)
and the workspace ruleset at references/anti-slop-ruleset.md. Lexical-richness
measures are included because they are the signals that generalised across models
and domains in arXiv 2606.04177; most other proposed indicators did not.

Thresholds are ADVISORY and unsourced. Calibrate against three human-written posts
in the brand's own voice before letting any of them gate a draft.

Usage:
    python slop_markers.py https://example.com/post --json
    python slop_markers.py draft.md --json
    python slop_markers.py page.html
    cat draft.md | python slop_markers.py -
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import sys

try:
    from seo_common import load_html, parse_html
except ImportError:  # pragma: no cover - direct execution from another cwd
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from seo_common import load_html, parse_html


# --------------------------------------------------------------------------
# Marker definitions
# --------------------------------------------------------------------------

# Leaked chat-interface markup. A hit is conclusive PROVENANCE evidence -- text was
# pasted out of a model UI unedited -- and is the one check here that is not a
# stylistic judgement.
MARKUP_LEAKAGE = {
    "chatgpt": [
        r"contentReference",
        r"oaicite",
        r"oai_citation",
        r"turn\d+search\d+",
        r"attributableIndex",
    ],
    "gemini": [r"\[cite:\s*\d+\]", r"\[span_\d+\]\(start_span\)"],
    "grok": [r"grok_card", r"grok_render_citation_card_json"],
    "deepseek": [r"[【】]", r"†"],
    "perplexity": [r"attached_file", r"ppl-ai-file-upload"],
    "generic": [r":::writing", r"\{\{\s*[a-z_]+\s*\}\}"],
}

# Vocabulary clusters, dated. These rot roughly annually: a term from the 2023 window
# is weak evidence in 2026 because human writing has absorbed the same patterns.
# See references/anti-slop-ruleset.md -> "Vocabulary versioning". Review Feb 2027.
VOCAB_WINDOWS = {
    "current_2025_on": {
        "weight": 3,
        "first_seen": "2025-06",
        "still_current": True,
        "terms": ["emphasizing", "enhance", "highlighting", "showcasing"],
    },
    "mid2024_mid2025": {
        "weight": 2,
        "first_seen": "2024-06",
        "still_current": False,
        "terms": [
            "align with", "bolstered", "crucial", "enduring", "fostering",
            "pivotal", "underscore", "vibrant",
        ],
    },
    "2023_mid2024": {
        "weight": 1,
        "first_seen": "2023-01",
        "still_current": False,
        "terms": [
            "additionally", "boasts", "delve", "garner", "intricacies",
            "interplay", "meticulous", "tapestry", "testament", "valuable",
            "multifaceted", "realm", "cutting-edge", "leverage", "harness",
            "embark", "seamless", "robust", "transformative", "facilitate",
            "utilize", "commence", "paramount", "plethora", "myriad",
            "culminate", "spearhead", "unlock", "supercharge", "elevate",
            "revolutionize",
        ],
    },
}

BANNED_PHRASES = [
    "it's worth noting that", "in today's fast-paced", "let's dive in",
    "without further ado", "in conclusion", "in summary", "in essence",
    "it's important to note", "stands as a testament to", "in the realm of",
    "it goes without saying", "buckle up", "the landscape is ever-evolving",
    "when it comes to", "the world of", "at the end of the day",
    "navigate the landscape", "game-changer",
]

# Copula avoidance: models substitute these for plain "is"/"are".
COPULA_SUBSTITUTES = [
    r"\bserves as\b", r"\bstands as\b", r"\bfunctions as\b", r"\boperates as\b",
    r"\brepresents\b", r"\bmarks\b", r"\bboasts\b", r"\bfeatures\b",
    r"\bexemplifies\b",
]

NEGATIVE_PARALLELISM = [
    (r"\bnot just\b[^.!?]{2,80}?\bbut\b", "not just X, but Y"),
    (r"\bnot only\b[^.!?]{2,80}?\bbut\b", "not only X, but Y"),
    (r"\bit's not\b[^.!?]{2,60}?,\s*it's\b", "it's not X, it's Y"),
    (r"\bisn't just\b[^.!?]{2,80}?\bit's\b", "isn't just X, it's Y"),
    (r"\brather than\b", "X rather than Y"),
]

VAGUE_ATTRIBUTION = [
    r"\bindustry reports?\b", r"\bobservers have (?:cited|noted)\b",
    r"\bexperts (?:argue|say|agree|believe)\b", r"\bsome critics argue\b",
    r"\bseveral sources\b", r"\bstudies show\b", r"\bresearch shows\b",
    r"\bit is widely (?:believed|accepted)\b", r"\bmany believe\b",
]

# Trailing participial clause: "..., highlighting the importance of X."
PARTICIPIAL_TACKON = re.compile(
    r",\s+(highlight|underscor|emphasiz|ensur|reflect|contribut|cultivat|"
    r"showcas|demonstrat|solidify|cement)\w*ing\b",
    re.I,
)

# Three comma-separated items ending in "and"/"or" -- the rule-of-three tell.
TRICOLON = re.compile(
    r"\b([\w'-]+(?:\s+[\w'-]+){0,2}),\s+([\w'-]+(?:\s+[\w'-]+){0,2}),\s+"
    r"(?:and|or)\s+([\w'-]+(?:\s+[\w'-]+){0,2})\b"
)

NUMERAL = re.compile(r"(?<![\w/])(\d[\d,]*\.?\d*\s?%|\d[\d,]{2,}|\d+\.\d+)(?![\w/])")
# Bare years are not uncited statistics. Without this exclusion any history or
# timeline piece reports dozens of false hits -- observed on four real posts.
YEAR_ONLY = re.compile(r"^(?:1[0-9]{3}|20[0-9]{2}|2100)$")
# Pixel dimensions, ranges and version strings are not statistics either.
NOT_A_STATISTIC = re.compile(
    r"\d+\s?[x×]\s?\d+|\bv?\d+\.\d+\.\d+\b|\b\d{3,4}\s?px\b", re.I
)
CITATION_NEAR = re.compile(
    r"https?://|\[\d+\]|\(\d{4}\)|\bsources?\b|\baccording to\b|\bcited in\b|"
    r"\breported by\b|\bper\s+[A-Z]|\bvia\s+[A-Z]|[A-Z][a-z]+\s+et al",
    re.I,
)
# A named authority in the same paragraph counts as attribution. Without this, every
# markdown table row that carries its source in an adjacent column is flagged --
# observed repeatedly on real research posts.
NAMED_SOURCE = re.compile(r"\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})+\b")


# --------------------------------------------------------------------------
# Text handling
# --------------------------------------------------------------------------

def _strip_markdown(text: str) -> str:
    """Remove markdown syntax that would skew punctuation and word counts."""
    # YAML front matter is config, not prose. Leaving it in flagged `target_length:
    # 2200-2600` as an uncited statistic on real posts.
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s+", "", text, flags=re.M)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.M)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)
    return text


def load_text(source: str, timeout: int) -> tuple[str, str, str]:
    """Return (raw_source_text, analysis_text, resolved_url).

    raw_source_text keeps markup so leakage checks can see it.
    analysis_text is prose only.
    """
    if source == "-":
        raw = sys.stdin.read()
        return raw, _strip_markdown(raw), ""

    if os.path.exists(source):
        with open(source, "r", encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
        if source.lower().endswith((".md", ".markdown", ".txt")):
            return raw, _strip_markdown(raw), ""
        html = raw
        url = ""
    else:
        html, url, _fetched = load_html(source, timeout=timeout)
        raw = html

    parsed = parse_html(html, url)
    soup = parsed["soup"]
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "noscript"]):
        tag.decompose()
    body = soup.find("article") or soup.find("main") or soup.body or soup
    return raw, body.get_text("\n", strip=True), url


SENTINEL = chr(0)


def split_sentences(text: str) -> list[str]:
    protected = re.sub(
        r"\b(Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|etc|e\.g|i\.e|Inc|Ltd|Co|No)\.",
        lambda m: m.group(0).replace(".", SENTINEL),
        text,
    )
    parts = re.split(r"(?<=[.!?])[\"')\]]*\s+(?=[A-Z\"'(\[])", protected)
    out = []
    for part in parts:
        cleaned = part.replace(SENTINEL, ".").strip()
        if len(cleaned.split()) >= 2:
            out.append(cleaned)
    return out


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]*", text)


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _hits(text: str, pattern: str, label: str, cap: int = 25) -> list[dict]:
    out = []
    for m in re.finditer(pattern, text, re.I):
        out.append({
            "match": m.group(0)[:90],
            "line": line_of(text, m.start()),
            "label": label,
        })
        if len(out) >= cap:
            break
    return out


# --------------------------------------------------------------------------
# Lexical richness
# --------------------------------------------------------------------------

def mtld(tokens: list[str], threshold: float = 0.72) -> float | None:
    """Measure of Textual Lexical Diversity (McCarthy & Jarvis), bidirectional mean.

    Length-robust, unlike raw type-token ratio. Higher = more varied vocabulary.
    """
    if len(tokens) < 50:
        return None

    def one_pass(seq: list[str]) -> float:
        factors, types, count = 0.0, set(), 0
        for tok in seq:
            types.add(tok)
            count += 1
            if count and len(types) / count <= threshold:
                factors += 1
                types, count = set(), 0
        if count:
            ttr = len(types) / count
            denom = 1 - threshold
            if denom:
                factors += (1 - ttr) / denom
        return len(seq) / factors if factors else float(len(seq))

    lowered = [t.lower() for t in tokens]
    return round((one_pass(lowered) + one_pass(lowered[::-1])) / 2, 2)


# --------------------------------------------------------------------------
# Analysis
# --------------------------------------------------------------------------

def analyse(raw: str, text: str, url: str) -> dict:
    toks = words(text)
    wc = len(toks)
    per_k = (lambda n: round(n * 1000 / wc, 2)) if wc else (lambda n: None)

    # --- Hard fail: leaked model markup -----------------------------------
    leakage = []
    for engine, patterns in MARKUP_LEAKAGE.items():
        for pat in patterns:
            for m in re.finditer(pat, raw):
                leakage.append({
                    "engine": engine,
                    "match": m.group(0)[:60],
                    "line": line_of(raw, m.start()),
                })
                break  # one example per pattern is enough
    hard_fail = bool(leakage)

    # --- Sentence rhythm ---------------------------------------------------
    sentences = split_sentences(text)
    lengths = [len(s.split()) for s in sentences]
    sd = round(statistics.pstdev(lengths), 2) if len(lengths) > 1 else None
    uniform_runs = []
    for i in range(len(lengths) - 2):
        window = lengths[i:i + 3]
        if max(window) - min(window) <= 3:
            uniform_runs.append({"sentence_index": i + 1, "lengths": window})

    # --- Em dashes ---------------------------------------------------------
    em_positions = [m.start() for m in re.finditer(r"—", text)]
    back_to_back = 0
    for i in range(len(sentences) - 1):
        if "—" in sentences[i] and "—" in sentences[i + 1]:
            back_to_back += 1

    # --- Copula ------------------------------------------------------------
    copula_count = len(re.findall(r"\b(?:is|are|was|were)\b", text, re.I))
    substitutes = []
    for pat in COPULA_SUBSTITUTES:
        substitutes.extend(_hits(text, pat, "copula substitute", cap=10))

    # --- Vocabulary --------------------------------------------------------
    vocab_hits, vocab_weighted = [], 0
    for window, meta in VOCAB_WINDOWS.items():
        for term in meta["terms"]:
            found = _hits(text, r"\b" + re.escape(term) + r"\w{0,3}\b", term, cap=6)
            for f in found:
                f.update({
                    "window": window,
                    "weight": meta["weight"],
                    "still_current": meta["still_current"],
                })
            if found:
                vocab_hits.extend(found)
                vocab_weighted += meta["weight"] * len(found)

    phrase_hits = []
    for phrase in BANNED_PHRASES:
        phrase_hits.extend(_hits(text, re.escape(phrase), phrase, cap=5))

    # --- Structural --------------------------------------------------------
    neg_par = []
    for pat, label in NEGATIVE_PARALLELISM:
        neg_par.extend(_hits(text, pat, label, cap=10))
    tricolons = _hits(text, TRICOLON.pattern, "rule of three", cap=15)
    participials = _hits(text, PARTICIPIAL_TACKON.pattern, "participial tack-on", cap=15)

    vague = []
    for pat in VAGUE_ATTRIBUTION:
        vague.extend(_hits(text, pat, "vague attribution", cap=10))

    # --- Uncited numerals (per paragraph) ----------------------------------
    uncited = []
    offset = 0
    for para in text.split("\n"):
        attributed = CITATION_NEAR.search(para) or (
            "|" in para and NAMED_SOURCE.search(para)
        )
        if para.strip() and not attributed:
            for m in NUMERAL.finditer(para):
                token = m.group(0).replace(",", "").strip()
                if YEAR_ONLY.match(token):
                    continue  # a date is not an uncited statistic
                window = para[max(0, m.start() - 12):m.end() + 12]
                if NOT_A_STATISTIC.search(window):
                    continue  # image dimensions, version strings
                uncited.append({
                    "match": m.group(0),
                    "line": line_of(text, offset + m.start()),
                    "paragraph": para.strip()[:120],
                })
        offset += len(para) + 1
    uncited_total = len(uncited)

    # --- Citation integrity ------------------------------------------------
    utm_links = _hits(raw, r"https?://[^\s\"'<>)]*utm_source=[^\s\"'<>)]*", "utm_source in source URL", cap=10)

    return {
        "url": url or None,
        "word_count": wc,
        "sentence_count": len(sentences),
        "hard_fail": hard_fail,
        "markup_leakage": leakage,
        "markers": {
            "em_dash": {
                "count": len(em_positions),
                "per_1000_words": per_k(len(em_positions)),
                "back_to_back_sentences": back_to_back,
                "advisory_flag_above_per_1000": 6.7,
            },
            "sentence_rhythm": {
                "length_stdev": sd,
                "advisory_floor_stdev": 5,
                "uniform_runs_of_3": len(uniform_runs),
                "examples": uniform_runs[:5],
            },
            "copula": {
                "is_are_was_were_per_1000": per_k(copula_count),
                "substitute_hits": len(substitutes),
                "examples": substitutes[:8],
            },
            "vocabulary": {
                "weighted_score": vocab_weighted,
                "hits": len(vocab_hits),
                "current_window_hits": sum(1 for h in vocab_hits if h["still_current"]),
                "examples": vocab_hits[:20],
            },
            "banned_phrases": {"count": len(phrase_hits), "examples": phrase_hits[:10]},
            "negative_parallelism": {"count": len(neg_par), "examples": neg_par[:8]},
            "tricolon": {"count": len(tricolons), "examples": tricolons[:6]},
            "participial_tackons": {"count": len(participials), "examples": participials[:8]},
            "vague_attribution": {"count": len(vague), "examples": vague[:8]},
            "uncited_numerals": {
                "count": uncited_total,
                "examples": uncited[:12],
                "note": (
                    "A client-work sourcing check, NOT an AI marker -- a human writer "
                    "quoting an unsourced figure trips it too, and should. Bare years, "
                    "image dimensions and version strings are excluded, and a named "
                    "authority in the same paragraph counts as attribution. A residual "
                    "false-positive rate remains on research-heavy and table-heavy "
                    "content (measured: 13-19 hits on four hand-written posts, most of "
                    "them figures attributed in an adjacent table column). Read the "
                    "examples before reporting a count."
                ),
            },
            "lexical_richness": {
                "mtld": mtld(toks),
                "type_token_ratio": round(len(set(t.lower() for t in toks)) / wc, 3) if wc else None,
                "note": (
                    "MTLD is the signal that generalised across 27 LLMs and 10 domains "
                    "(arXiv 2606.04177). No absolute threshold exists -- compare against "
                    "the brand's own baseline at a similar length. Raw type-token ratio "
                    "falls as length rises, so never compare TTR between texts of "
                    "different sizes; MTLD is length-robust but unstable below ~300 words."
                ),
            },
            "citation_integrity": {"utm_source_leftovers": len(utm_links), "examples": utm_links[:5]},
        },
        "interpretation": {
            "is_authorship_verdict": False,
            "disclaimer": (
                "These are markers, not a conclusion. Do not report this output as "
                "evidence that AI wrote the text. GPT detectors show a ~61.3% "
                "false-positive rate on non-native English writers (Liang et al., "
                "Patterns 2023); a verdict would misclassify good human writing."
            ),
            "thresholds": (
                "Advisory and unsourced. Calibrate against three human-written posts "
                "in the brand's voice before gating anything on them."
            ),
            "conclusive_check": (
                "Only markup_leakage is conclusive, and it proves provenance "
                "(text pasted from a model UI), not quality."
            ),
        },
    }


def summarise(r: dict) -> list[str]:
    m = r["markers"]
    lines = [
        f"Words: {r['word_count']}  Sentences: {r['sentence_count']}",
        "",
    ]
    if r["hard_fail"]:
        lines.append("HARD FAIL - leaked model markup found:")
        for hit in r["markup_leakage"][:6]:
            lines.append(f"  line {hit['line']}: [{hit['engine']}] {hit['match']}")
        lines.append("")
    lines += [
        f"Em dashes           {m['em_dash']['count']} ({m['em_dash']['per_1000_words']}/1k words), "
        f"{m['em_dash']['back_to_back_sentences']} back-to-back",
        f"Sentence length SD  {m['sentence_rhythm']['length_stdev']} "
        f"({m['sentence_rhythm']['uniform_runs_of_3']} uniform runs of 3)",
        f"Copula per 1k       {m['copula']['is_are_was_were_per_1000']} "
        f"({m['copula']['substitute_hits']} substitutes)",
        f"Vocabulary          {m['vocabulary']['hits']} hits, "
        f"{m['vocabulary']['current_window_hits']} in the current cluster "
        f"(weighted {m['vocabulary']['weighted_score']})",
        f"Banned phrases      {m['banned_phrases']['count']}",
        f"Negative parallel   {m['negative_parallelism']['count']}",
        f"Rule of three       {m['tricolon']['count']}",
        f"Participial tack-on {m['participial_tackons']['count']}",
        f"Vague attribution   {m['vague_attribution']['count']}",
        f"Uncited numerals    {m['uncited_numerals']['count']}",
        f"Lexical MTLD        {m['lexical_richness']['mtld']} "
        f"(TTR {m['lexical_richness']['type_token_ratio']})",
        f"utm_source left in  {m['citation_integrity']['utm_source_leftovers']}",
        "",
        "Evidence only - this is not an authorship verdict. Thresholds are advisory;",
        "calibrate against human-written posts in the brand's voice first.",
    ]
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Report measurable AI-writing markers. Evidence only, never a verdict.",
    )
    parser.add_argument("source", help="URL, local HTML/markdown file, or - for stdin")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON")
    args = parser.parse_args()

    raw, text, url = load_text(args.source, args.timeout)
    if not text.strip():
        print(json.dumps({"error": "no extractable text"}) if args.json else "No extractable text.")
        sys.exit(1)

    result = analyse(raw, text, url)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n".join(summarise(result)))


if __name__ == "__main__":
    main()

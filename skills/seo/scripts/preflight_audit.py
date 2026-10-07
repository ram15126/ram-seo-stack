#!/usr/bin/env python3
"""Run the blog pre-flight gate backwards against a published page.

_process/blog-content-sop.md section 6 is a gate for content about to ship. This
runs the same checks against something already live, so an audit and a publishing
decision use one standard instead of two.

Checks, grouped as the SOP groups them:

  Extractability  answer block (50-70 words, self-contained, definition pattern),
                  key-fact openers per section, FAQ present, FAQPage schema text
                  diffed against the VISIBLE text, sources list
  Technical       indexable and snippet-eligible (noindex / nosnippet /
                  max-snippet:0 / data-nosnippet), Article + Person +
                  BreadcrumbList schema, byline resolves, canonical, title and
                  description length, internal link count

Substance (SOP 2a) is deliberately absent: "does this provide original information"
cannot be measured by a script, and pretending otherwise is how word count ends up
standing in for quality. See _process/word-count-is-not-content-quality.md.

Usage:
    python preflight_audit.py https://example.com/post --json
    python preflight_audit.py post.html --json
    python preflight_audit.py https://example.com/post --check-links
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from difflib import SequenceMatcher
from urllib.parse import urljoin, urlparse

try:
    from seo_common import load_html, parse_html, same_host
    from lib.safe_http import safe_get
except ImportError:  # pragma: no cover
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from seo_common import load_html, parse_html, same_host
    from lib.safe_http import safe_get


# The SOP's own numbers. Ranges, not targets.
ANSWER_BLOCK_WORDS = (50, 70)
KEY_FACT_WORDS = (60, 130)
TITLE_MAX = 60
DESC_RANGE = (150, 160)
INTERNAL_LINKS_MIN = 3

DEFINITION_PATTERN = re.compile(
    r"^\s*(?:the\s+)?[A-Z][\w'’\- ]{1,60}\s+(?:is|are|refers to|means|describes)\b",
    re.I,
)
# A block that opens with a pronoun cannot stand alone once lifted out of the page.
DANGLING_OPENER = re.compile(r"^\s*(it|this|that|they|these|those|he|she)\b", re.I)


def _words(text: str) -> int:
    return len(re.findall(r"\b[\w'’-]+\b", text or ""))


def _norm(text: str) -> str:
    """Normalise for comparison: collapse whitespace, unify quotes and dashes."""
    text = text or ""
    for a, b in (
        ("\u2019", "'"), ("\u2018", "'"),          # curly single quotes
        ("\u201c", '"'), ("\u201d", '"'),          # curly double quotes
        ("\u2014", "-"), ("\u2013", "-"),          # em / en dash
        ("\u00a0", " "), ("\u2009", " "), ("\u202f", " "),  # nbsp, thin, narrow nbsp
    ):
        text = text.replace(a, b)
    return re.sub(r"\s+", " ", text).strip().lower()


def _despace(text: str) -> str:
    """Whitespace-free form, for presence tests only.

    BeautifulSoup's get_text(" ") inserts a separator at every inline-element
    boundary, so a page rendering `<em>Kapadapuram</em>.` yields "Kapadapuram ."
    while the schema string holds "Kapadapuram." Comparing with whitespace intact
    reports a structured-data violation that does not exist -- observed on two of
    three flagged FAQ entries on a real post, where the only differences were a
    space before a semicolon and a space before a full stop.

    Whitespace differences are not schema mismatches. Wording differences are.
    """
    return re.sub(r"\s+", "", _norm(text))


def _finding(check: str, status: str, detail: str, evidence: str = "", fix: str = "") -> dict:
    """status: pass | fail | warn | info"""
    return {
        "check": check,
        "status": status,
        "detail": detail,
        "evidence": evidence[:400],
        "fix": fix,
    }


# --------------------------------------------------------------------------
# Schema
# --------------------------------------------------------------------------

def collect_jsonld(parsed: dict) -> list:
    """Flatten the JSON-LD that parse_html already extracted.

    Do NOT re-scan parsed["soup"] for script tags: parse_html decomposes every
    script, style, noscript and template element before returning, so a search for
    application/ld+json there finds nothing and silently reports "no schema".
    See _process/schema-script-blind-spots.md.
    """
    blocks = []
    for entry in parsed.get("schema") or []:
        if isinstance(entry, list):
            blocks.extend(entry)
        else:
            blocks.append(entry)

    flat = []
    for b in blocks:
        if isinstance(b, dict) and "@graph" in b and isinstance(b["@graph"], list):
            flat.extend(b["@graph"])
        else:
            flat.append(b)
    return flat


def types_of(node) -> list[str]:
    if not isinstance(node, dict):
        return []
    t = node.get("@type") or []
    return [str(x) for x in (t if isinstance(t, list) else [t])]


def find_faq_pairs(nodes: list) -> list[dict]:
    pairs = []
    for node in nodes:
        if "FAQPage" not in types_of(node):
            continue
        entities = node.get("mainEntity") or []
        if isinstance(entities, dict):
            entities = [entities]
        for q in entities:
            if not isinstance(q, dict):
                continue
            answer = q.get("acceptedAnswer") or {}
            if isinstance(answer, list):
                answer = answer[0] if answer else {}
            pairs.append({
                "question": (q.get("name") or "").strip(),
                "answer": re.sub(r"<[^>]+>", " ", str(answer.get("text") or "")).strip(),
            })
    return pairs


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check_fetch(fetched: dict, parsed: dict, soup) -> tuple[list[dict], bool]:
    """Is there actually a page here? Returns (findings, keep_going).

    Three ways this script would otherwise produce a confident, entirely wrong audit:

    0. The fetch never happened. seo_common.fetch_url returns status=None plus an
       `error` string when it fails -- DNS, timeout, or the SSRF guard rejecting a
       NAT64 address as "private". The HTML is then EMPTY, and every content check
       reports its subject as missing. Observed live: an SSRF-guard block produced a
       nine-finding audit of a zero-byte document, including a confident "page
       carries a noindex directive". This is the most dangerous of the three because
       the output looks exactly like a real audit of a badly built page.
    1. A 4xx/5xx, or a soft 404 -- a report about the error page's markup, not the
       article.
    2. A client-rendered page. A raw fetch gets the app shell, so every absence is an
       artifact of not running JavaScript. Never report "missing" from a shell.
    """
    status = fetched.get("status")
    error = fetched.get("error")

    if error or (status is None and fetched.get("input_url")):
        return [_finding(
            "fetch", "fail",
            f"The page was never retrieved, so nothing below could be measured. "
            f"Fetch error: {error or 'no response'}",
            evidence=f"status={status} error={error}",
            fix="Re-fetch before auditing. If the error mentions a private or "
                "internal IP for a public site, that is the SSRF guard mis-reading a "
                "NAT64/IPv6 address -- see _process/ssrf-guard-dns-resolver-mismatch.md. "
                "Use the crawl4ai MCP (crawl_page) instead and audit that output. "
                "Report NOTHING as missing from this run.",
        )], False

    if status is not None and status >= 400:
        return [_finding(
            "page_exists", "fail",
            f"HTTP {status}. There is no page here to audit.",
            evidence=f"status={status} url={fetched.get('url')}",
            fix="Check the URL. If the post is unpublished or moved, audit the live "
                "URL instead; if this is the intended URL, the 404 is the finding.",
        )], False

    text = parsed.get("body_text") or ""
    words = len(text.split())
    headings = sum(len(v) for v in (parsed.get("headings") or {}).values())
    error_shell = re.search(r"\b(404|page (could )?not be found|page not found)\b",
                            text[:600], re.I)

    if status == 200 and error_shell and words < 400:
        return [_finding(
            "page_exists", "fail",
            "HTTP 200 but the page renders a not-found message -- a soft 404.",
            evidence=text[:200],
            fix="A soft 404 should return a real 404 status. Until then search "
                "engines may index the error page.",
        )], False

    # Applies to local files too (status None): a saved SPA shell is still a shell.
    if words < 150 and headings == 0:
        return [_finding(
            "rendering", "fail",
            "Almost no text and no headings in the raw HTML. This is very likely a "
            "client-rendered page, so every 'missing' finding below would be an "
            "artifact of not running JavaScript.",
            evidence=f"{words} words, {headings} headings in raw HTML",
            fix="Re-fetch with a JavaScript-rendering client (the crawl4ai MCP "
                "crawl_page with wait_seconds=6) and audit that. Do NOT report "
                "anything as absent from this result.",
        )], False

    return [], True


def check_indexability(soup, headers: dict) -> list[dict]:
    out = []
    directives = []
    for tag in soup.find_all("meta"):
        name = (tag.get("name") or "").lower()
        if name in ("robots", "googlebot"):
            directives.append((name, (tag.get("content") or "").lower()))
    header_robots = ""
    for key, value in (headers or {}).items():
        if key.lower() == "x-robots-tag":
            header_robots = str(value).lower()
            directives.append(("x-robots-tag", header_robots))

    joined = " ".join(v for _, v in directives)

    if "noindex" in joined:
        out.append(_finding(
            "indexable", "fail",
            "Page carries a noindex directive. It cannot appear in search or in AI "
            "Overviews at all -- every other finding is moot until this is removed.",
            evidence=str(directives),
            fix="Remove noindex from the meta robots tag / X-Robots-Tag header.",
        ))
    else:
        out.append(_finding("indexable", "pass", "No noindex directive found.",
                            evidence=str(directives) or "no robots directives"))

    blockers = [d for d in ("nosnippet", "max-snippet:0") if d in joined]
    nosnippet_attrs = soup.find_all(attrs={"data-nosnippet": True})
    if blockers or nosnippet_attrs:
        out.append(_finding(
            "snippet_eligible", "fail",
            "Snippet suppression present. Google states the only requirements for AI "
            "features are that a page is indexed and eligible to show with a snippet; "
            "this disqualifies it.",
            evidence=f"directives={blockers} data-nosnippet elements={len(nosnippet_attrs)}",
            fix="Remove nosnippet / max-snippet:0 / data-nosnippet from the content region.",
        ))
    else:
        out.append(_finding("snippet_eligible", "pass",
                            "No snippet suppression found."))
    return out


def check_answer_block(soup) -> list[dict]:
    out = []
    h1 = soup.find("h1")
    anchor = h1 or soup.find("h2")
    if not anchor:
        return [_finding("answer_block", "fail", "No H1 or H2 found; cannot locate an answer block.",
                         fix="Add an H1, then a 50-70 word answer block directly beneath it.")]

    # Prefer an explicitly labelled summary section. Without this the scan grabs the
    # standfirst -- the short dek many templates render above the byline, often just
    # the meta description -- and then reports a 28-word answer block and "no
    # definition pattern" on a page whose real 72-word answer block two elements
    # later is textbook. Observed on three real posts.
    block = None
    # The label is not always a heading -- templates also use an eyebrow span or a
    # bolded lead-in, so match on any small element whose whole text is the label.
    SUMMARY_LABEL = re.compile(
        r"^\s*(in short|summary|tl;?dr|quick answer|the short version|key facts?)\s*[:—-]?\s*$",
        re.I,
    )
    summary_h = soup.find(
        ["h2", "h3", "h4", "span", "strong", "b", "p"], string=SUMMARY_LABEL
    )
    if summary_h:
        node = summary_h
        for _ in range(4):
            node = node.find_next(["p", "ul", "blockquote", "h2", "h3"])
            if node is None or node.name in ("h2", "h3"):
                break
            text = node.get_text(" ", strip=True)
            if _words(text) >= 20:
                block = text
                break

    if block is None:
        node = anchor
        for _ in range(8):
            node = node.find_next(["p", "div", "blockquote", "h2", "h3"])
            if node is None:
                break
            if node.name in ("h2", "h3"):
                continue
            text = node.get_text(" ", strip=True)
            if _words(text) >= 20:
                block = text
                break

    if not block:
        return [_finding(
            "answer_block", "fail",
            "No substantive paragraph found near the top of the page.",
            fix="Add a self-contained 50-70 word answer directly after the H1.",
        )]

    wc = _words(block)
    lo, hi = ANSWER_BLOCK_WORDS
    if lo <= wc <= hi:
        out.append(_finding("answer_block_length", "pass", f"Opening block is {wc} words.",
                            evidence=block[:200]))
    else:
        out.append(_finding(
            "answer_block_length", "warn",
            f"Opening block is {wc} words; the SOP range is {lo}-{hi}.",
            evidence=block[:200],
            fix="Tighten or expand to a self-contained answer in the 50-70 word band.",
        ))

    if DANGLING_OPENER.match(block):
        out.append(_finding(
            "answer_block_self_contained", "fail",
            "Opening block starts with a pronoun, so it does not stand alone when lifted.",
            evidence=block[:160],
            fix="Open by naming the subject: 'X is...' rather than 'It is...'.",
        ))
    elif DEFINITION_PATTERN.match(block):
        out.append(_finding("answer_block_self_contained", "pass",
                            "Opens with a definition pattern and names its own subject.",
                            evidence=block[:160]))
    else:
        out.append(_finding(
            "answer_block_self_contained", "warn",
            "Opening block does not use a definition pattern ('X is...', 'X refers to...').",
            evidence=block[:160],
            fix="Rewrite the first sentence so the block names its subject and gives the verdict.",
        ))
    return out


def check_key_fact_openers(soup) -> list[dict]:
    lo, hi = KEY_FACT_WORDS
    sections, weak = 0, []
    for h2 in soup.find_all("h2"):
        # A heading inside a nav, aside or footer labels a component, not a prose
        # section. Counting a table-of-contents "Contents" heading as a section
        # that needs a 60-130 word opener is a false positive, and it inflates the
        # denominator on every page that has one.
        if h2.find_parent(["nav", "aside", "footer", "header"]):
            continue
        node = h2.find_next(["p", "ul", "ol", "table", "h2"])
        if node is None or node.name == "h2":
            weak.append({"section": h2.get_text(" ", strip=True)[:70], "opener_words": 0})
            sections += 1
            continue
        wc = _words(node.get_text(" ", strip=True))
        sections += 1
        if not (lo <= wc <= hi):
            weak.append({"section": h2.get_text(" ", strip=True)[:70], "opener_words": wc})

    if sections == 0:
        return [_finding("key_fact_openers", "warn", "No H2 sections found.",
                         fix="Structure the page with H2 sections, each opening with a 60-130 word key fact.")]
    status = "pass" if len(weak) <= sections // 3 else "warn"
    return [_finding(
        "key_fact_openers", status,
        f"{sections - len(weak)}/{sections} H2 sections open with a {lo}-{hi} word block.",
        evidence=json.dumps(weak[:6]),
        fix="Give each major section a self-contained opener an AI can lift on its own.",
    )]


def check_faq_schema_diff(soup, nodes: list, body_text: str) -> list[dict]:
    """The check almost nobody runs: FAQPage schema text must match visible text."""
    pairs = find_faq_pairs(nodes)
    if not pairs:
        headings = [h.get_text(" ", strip=True) for h in soup.find_all(["h2", "h3"])]
        has_visible_faq = any(re.search(r"\bFAQ|frequently asked", h, re.I) for h in headings)
        if has_visible_faq:
            return [_finding(
                "faq_schema", "fail",
                "A visible FAQ section exists but no FAQPage schema was found.",
                evidence=str([h for h in headings if re.search(r'FAQ|frequently asked', h, re.I)][:3]),
                fix="Add FAQPage JSON-LD whose text matches the visible Q&As exactly.",
            )]
        return [_finding("faq_schema", "info", "No FAQ section and no FAQPage schema.",
                         fix="An FAQ is one of the most reliably extracted blocks; consider adding one.")]

    raw_visible = body_text or soup.get_text(" ", strip=True)
    visible = _norm(raw_visible)
    visible_despaced = _despace(raw_visible)
    mismatches = []
    for pair in pairs:
        for field in ("question", "answer"):
            value = _norm(pair[field])
            if not value:
                continue
            # Whitespace-insensitive presence test: see _despace.
            if value in visible or _despace(pair[field]) in visible_despaced:
                continue
            # Near-miss: find the closest visible run to report a useful diff.
            ratio = SequenceMatcher(None, value, visible[:20000]).quick_ratio()
            mismatches.append({
                "field": field,
                "schema_text": pair[field][:180],
                "found_verbatim_on_page": False,
                "rough_similarity": round(ratio, 2),
            })

    if mismatches:
        return [_finding(
            "faq_schema_matches_visible", "fail",
            f"{len(mismatches)} of {len(pairs) * 2} FAQ schema strings do not appear "
            f"verbatim in the visible page text. Google treats schema text that is not "
            f"present on the page as a structured-data violation.",
            evidence=json.dumps(mismatches[:4], ensure_ascii=False),
            fix="Make the JSON-LD question and answer text identical to the rendered text.",
        )]
    return [_finding("faq_schema_matches_visible", "pass",
                     f"All {len(pairs)} FAQ pairs appear verbatim in the visible text.")]


def check_schema_types(nodes: list) -> list[dict]:
    present = {t for node in nodes for t in types_of(node)}
    out = []
    article_like = {"Article", "BlogPosting", "NewsArticle", "TechArticle"}
    if present & article_like:
        out.append(_finding("schema_article", "pass", f"Found {sorted(present & article_like)}."))
    else:
        out.append(_finding("schema_article", "fail", "No Article/BlogPosting schema.",
                            evidence=str(sorted(present)),
                            fix="Add Article or BlogPosting JSON-LD."))

    # Index Person nodes by @id so author references resolve. JSON-LD idiomatically
    # writes `author: {"@id": "...#person"}` pointing at a sibling Person node --
    # the better-formed pattern. Requiring an inline Person failed those pages.
    persons_by_id = {
        n.get("@id"): n for n in nodes
        if isinstance(n, dict) and "Person" in types_of(n) and n.get("@id")
    }
    author_ok = False
    for node in nodes:
        if not isinstance(node, dict):
            continue
        author = node.get("author")
        authors = author if isinstance(author, list) else [author]
        for a in authors:
            if not isinstance(a, dict):
                continue
            if "Person" in types_of(a) and a.get("name"):
                author_ok = True
            elif a.get("@id") and a["@id"] in persons_by_id:
                author_ok = True
    out.append(_finding(
        "schema_author_person", "pass" if author_ok else "fail",
        "Author is a named Person node." if author_ok
        else "No Person author found in schema.",
        fix="" if author_ok else "Add author as a Person node with name and url.",
    ))

    out.append(_finding(
        "schema_breadcrumb", "pass" if "BreadcrumbList" in present else "warn",
        "BreadcrumbList present." if "BreadcrumbList" in present else "No BreadcrumbList schema.",
        fix="" if "BreadcrumbList" in present else "Add BreadcrumbList JSON-LD.",
    ))

    errors = [n for n in nodes if isinstance(n, dict) and n.get("error") == "invalid_json"]
    if errors:
        out.append(_finding("schema_parses", "fail", f"{len(errors)} JSON-LD block(s) failed to parse.",
                            evidence=str(errors[0])[:200],
                            fix="Fix the malformed JSON-LD; invalid blocks are ignored entirely."))
    return out


def check_head(parsed: dict) -> list[dict]:
    out = []
    title = parsed.get("title") or ""
    # parse_html returns `meta_description`, NOT a `meta` dict. Reading the wrong
    # key made this report "No meta description" on every page that had one.
    desc = parsed.get("meta_description") or ""

    if not title:
        out.append(_finding("title", "fail", "No <title>.", fix="Add a title."))
    elif len(title) > TITLE_MAX:
        out.append(_finding("title", "warn", f"Title is {len(title)} chars (guide: <= {TITLE_MAX}).",
                            evidence=title, fix="Shorten so it is not truncated in the SERP."))
    else:
        out.append(_finding("title", "pass", f"Title is {len(title)} chars.", evidence=title))

    lo, hi = DESC_RANGE
    if not desc:
        out.append(_finding("meta_description", "fail", "No meta description.",
                            fix=f"Add one, roughly {lo}-{hi} characters."))
    elif lo <= len(desc) <= hi:
        out.append(_finding("meta_description", "pass", f"Description is {len(desc)} chars."))
    else:
        out.append(_finding("meta_description", "warn",
                            f"Description is {len(desc)} chars (guide: {lo}-{hi}).",
                            evidence=desc))

    canonical = parsed.get("canonical")
    out.append(_finding("canonical", "pass" if canonical else "warn",
                        f"Canonical: {canonical}" if canonical else "No canonical link.",
                        fix="" if canonical else "Add a self-referencing canonical."))
    return out


def check_links(soup, base_url: str, check_http: bool, timeout: int) -> list[dict]:
    out = []
    if not re.match(r"^https?://", base_url or ""):
        # Local file: without a real origin, relative hrefs cannot be classified and
        # internal links get silently reported as zero. Fall back to the canonical.
        return [_finding(
            "internal_links", "info",
            "Cannot classify internal vs external links: no base URL. Audit the live "
            "URL, or add a canonical tag to the file.",
        )]
    internal, external = [], []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        full = urljoin(base_url, href) if base_url else href
        if base_url and same_host(full, base_url):
            internal.append(full)
        elif re.match(r"^https?://", full):
            external.append(full)

    unique_internal = sorted(set(internal))
    out.append(_finding(
        "internal_links",
        "pass" if len(unique_internal) >= INTERNAL_LINKS_MIN else "warn",
        f"{len(unique_internal)} unique internal links (SOP guide: {INTERNAL_LINKS_MIN}-5).",
        evidence=str(unique_internal[:8]),
        fix="" if len(unique_internal) >= INTERNAL_LINKS_MIN
            else "Add contextual internal links; cluster pages should link back to the pillar.",
    ))

    out.append(_finding(
        "sources_listed", "pass" if external else "warn",
        f"{len(set(external))} unique external links (source citations).",
        evidence=str(sorted(set(external))[:8]),
        fix="" if external else
            "Cite sources inline. Measured at +28% visibility in the GEO study, and the "
            "highest-leverage tactic for Law/Government and factual content.",
    ))

    if check_http and external:
        broken = []
        for url in sorted(set(external))[:25]:
            try:
                resp = safe_get(url, timeout=timeout, allow_redirects=True)
                if resp.status_code >= 400:
                    broken.append({"url": url, "status": resp.status_code})
            except Exception as exc:  # network, DNS, SSRF guard
                broken.append({"url": url, "status": f"error: {type(exc).__name__}"})
        out.append(_finding(
            "external_links_resolve", "fail" if broken else "pass",
            f"{len(broken)} of {min(len(set(external)), 25)} checked external links failed."
            if broken else "All checked external links resolved.",
            evidence=json.dumps(broken[:6]),
            fix="Fix or remove dead citations. A broken source link is a fabrication tell." if broken else "",
        ))

    utm = [u for u in external if "utm_source=" in u]
    if utm:
        out.append(_finding(
            "citation_hygiene", "warn",
            f"{len(utm)} source link(s) still carry utm_source tracking parameters.",
            evidence=str(utm[:4]),
            fix="Strip tracking parameters from cited URLs.",
        ))
    return out


def check_byline(soup, nodes: list, base_url: str) -> list[dict]:
    persons_by_id = {
        n.get("@id"): n for n in nodes
        if isinstance(n, dict) and "Person" in types_of(n) and n.get("@id")
    }
    author_url = None
    for node in nodes:
        if not isinstance(node, dict):
            continue
        author = node.get("author")
        authors = author if isinstance(author, list) else [author]
        for a in authors:
            if not isinstance(a, dict):
                continue
            if a.get("url"):
                author_url = a["url"]
            elif a.get("@id") in persons_by_id:
                ref = persons_by_id[a["@id"]]
                author_url = ref.get("url") or a["@id"].split("#")[0]

    visible = soup.find(attrs={"rel": "author"}) or soup.find(class_=re.compile(r"author|byline", re.I))
    if not visible and not author_url:
        return [_finding(
            "byline", "fail", "No visible byline and no author URL in schema.",
            fix="Add a byline linking to a real author page. Google's Who/How/Why test asks "
                "whether bylines lead to further information about the author.",
        )]
    if author_url:
        return [_finding("byline", "pass", f"Author URL present in schema: {author_url}")]
    return [_finding(
        "byline", "warn", "Visible byline found but it does not resolve to an author page.",
        evidence=visible.get_text(" ", strip=True)[:120] if visible else "",
        fix="Link the byline to an author page and add url to the Person node.",
    )]


# --------------------------------------------------------------------------

def audit(source: str, timeout: int = 20, check_http: bool = False) -> dict:
    if os.path.exists(source):
        with open(source, "r", encoding="utf-8", errors="replace") as fh:
            html = fh.read()
        url, fetched = "", {"headers": {}}
    else:
        html, url, fetched = load_html(source, timeout=timeout)

    parsed = parse_html(html, url)
    soup = parsed["soup"]
    nodes = collect_jsonld(parsed)

    findings: list[dict] = []

    # Establish there is a real, server-rendered page before auditing its contents.
    gate, keep_going = check_fetch(fetched, parsed, soup)
    findings += gate
    if not keep_going:
        return {
            "url": url or source,
            "summary": {"pass": 0, "fail": len(gate), "warn": 0, "info": 0},
            "blocking": gate,
            "findings": gate,
            "not_checked": [
                "Everything. The audit stopped at the fetch gate above -- reporting "
                "content findings from this response would describe an error page or "
                "an unrendered shell, not the article.",
            ],
        }

    findings += check_indexability(soup, fetched.get("headers") or {})
    findings += check_answer_block(soup)
    findings += check_key_fact_openers(soup)
    findings += check_faq_schema_diff(soup, nodes, parsed.get("body_text") or "")
    findings += check_schema_types(nodes)
    findings += check_byline(soup, nodes, url)
    findings += check_head(parsed)
    # A local file has no origin of its own; the canonical is the page's own claim
    # about where it lives, which is the correct base for classifying its links.
    link_base = url or parsed.get("canonical") or ""
    findings += check_links(soup, link_base, check_http, timeout)

    tally = {s: sum(1 for f in findings if f["status"] == s)
             for s in ("pass", "fail", "warn", "info")}

    return {
        "url": url or source,
        "summary": tally,
        "blocking": [f for f in findings if f["status"] == "fail"],
        "findings": findings,
        "not_checked": [
            "Substance (SOP 2a: original information, insight beyond the obvious). "
            "Not measurable by script -- requires reading the page.",
            "Presentation (SOP 4: characters per line, contrast, responsive overflow). "
            "Requires a real viewport; see the Playwright-based scripts.",
            "Whether the content is actually good. Word count answers 'is there enough "
            "here to rank', never 'is this good'.",
        ],
    }


def summarise(r: dict) -> list[str]:
    icon = {"pass": "PASS", "fail": "FAIL", "warn": "WARN", "info": "INFO"}
    lines = [f"Pre-flight audit: {r['url']}", ""]
    for f in r["findings"]:
        lines.append(f"[{icon[f['status']]}] {f['check']}: {f['detail']}")
        if f["status"] in ("fail", "warn") and f["fix"]:
            lines.append(f"        fix: {f['fix']}")
    s = r["summary"]
    lines += ["", f"{s['pass']} pass / {s['fail']} fail / {s['warn']} warn / {s['info']} info", ""]
    lines.append("Not checked by this script:")
    for item in r["not_checked"]:
        lines.append(f"  - {item}")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the blog pre-flight gate against a published page.")
    parser.add_argument("source", help="URL or local HTML file")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--check-links", action="store_true",
                        help="Also HTTP-check external source links (slower, makes requests)")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON")
    args = parser.parse_args()

    result = audit(args.source, args.timeout, args.check_links)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n".join(summarise(result)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Expand seed searches with Google Autocomplete. Free, no API key, standard library only.

Why: Google says autocomplete predictions "reflect real searches that have been done on Google"
(support.google.com/websearch/answer/7368877). That proves a phrase EXISTS. It does not tell you how
big it is: read the size in Keyword Planner afterwards.

Usage:
  python autocomplete_expand.py --seeds "seo audit" "seo consultant" --gl in --out autocomplete.csv
  python autocomplete_expand.py --seeds-file seeds.txt --gl us --sleep 1.5

Notes:
- The endpoint is unofficial and can rate-limit you (HTTP 429). Keep --sleep at 1 second or more.
- Run it for each market you care about (--gl in, --gl us) and keep phrases that appear in both.
- Every row records the date, language and country, because a reading belongs to the day it was taken.
"""
import argparse
import csv
import datetime
import json
import sys
import time
import urllib.parse
import urllib.request

ENDPOINT = "https://suggestqueries.google.com/complete/search"
# The seven shapes that surface questions and comparisons for a seed X.
SHAPES = ["{}", "{} for", "{} vs", "is {}", "what is {}", "how to {}", "best {}"]


def suggest(query: str, hl: str, gl: str, retries: int = 2) -> list:
    url = ENDPOINT + "?" + urllib.parse.urlencode({"client": "firefox", "q": query, "hl": hl, "gl": gl})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (keyword-stack; polite)"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
            return [s for s in data[1] if isinstance(s, str)]
        except Exception as e:  # network error, 429, bad JSON
            if attempt == retries:
                print(f"[skip] {query!r}: {e}", file=sys.stderr)
                return []
            time.sleep(2 * (attempt + 1))
    return []


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seeds", nargs="*", default=[], help="seed searches, e.g. 'seo audit'")
    ap.add_argument("--seeds-file", help="text file, one seed per line")
    ap.add_argument("--hl", default="en", help="interface language (default en)")
    ap.add_argument("--gl", default="in", help="country code: in, us, uk ... (default in)")
    ap.add_argument("--sleep", type=float, default=1.0, help="seconds between requests (default 1.0)")
    ap.add_argument("--shapes", type=int, default=len(SHAPES), help="use only the first N shapes (default all 7)")
    ap.add_argument("--out", default="autocomplete.csv")
    a = ap.parse_args()

    seeds = list(a.seeds)
    if a.seeds_file:
        seeds += [l.strip() for l in open(a.seeds_file, encoding="utf-8") if l.strip() and not l.startswith("#")]
    if not seeds:
        ap.error("give --seeds or --seeds-file")

    today = datetime.date.today().isoformat()
    seen, rows = set(), []
    for seed in seeds:
        for shape in SHAPES[: a.shapes]:
            q = shape.format(seed)
            for s in suggest(q, a.hl, a.gl):
                key = s.lower().strip()
                if key not in seen:
                    seen.add(key)
                    rows.append({"seed": seed, "asked": q, "suggestion": s, "gl": a.gl, "hl": a.hl, "date": today})
            time.sleep(a.sleep)

    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["seed", "asked", "suggestion", "gl", "hl", "date"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} unique suggestions from {len(seeds)} seed(s) -> {a.out}")
    print("Reminder: this proves phrases exist, not how big they are. Read sizes in Keyword Planner next.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

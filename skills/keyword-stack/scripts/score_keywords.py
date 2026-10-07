#!/usr/bin/env python3
"""Score keywords: demand x 3 + fit x 3, out of 30. Standard library only.

Input CSV columns (extra columns are kept):
  keyword   the search
  range     Keyword Planner band: 100K-1M, 10K-100K, 1K-10K, 100-1K, 10-100, <10 or none
  fit       0-5, set by you after reading the page it would lead to:
            5 = a service/product you sell, in a buyer's words
            4 = a problem you fix        3 = wider knowledge your buyers read
            2 = off your positioning     0-1 = not for you
  mixed     optional, yes/no: most people mean something else by this word (a film, a place, a brand).
            "yes" steps demand down by one.
  page      optional: the page that would own the search
  note      optional

Demand: 100K-1M = 5, 10K-100K = 4, 1K-10K = 3, 100-1K = 2, 10-100 = 1, under 10 or none = 0.

Rules built in (each came from a mistake):
- Report ties as ties. An alphabetical cut inside a tie is not a ranking.
- A range spans a factor of ten. Never turn it into a traffic forecast.
- A range belongs to the day you read it: put the date and location in a '#' comment line at the top.

Usage:  python score_keywords.py keywords.csv --out scored.csv
"""
import argparse
import csv
import sys
from collections import Counter

DEMAND = {"100k-1m": 5, "10k-100k": 4, "1k-10k": 3, "100-1k": 2, "10-100": 1, "<10": 0, "0-10": 0, "none": 0, "nodata": 0, "": 0}


def norm_range(s: str) -> str:
    s = (s or "").strip().lower().replace("–", "-").replace("—", "-").replace(" to ", "-").replace(" ", "")
    return s.replace("under10", "<10")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_in")
    ap.add_argument("--out", default="scored.csv")
    a = ap.parse_args()

    lines = [l for l in open(a.csv_in, encoding="utf-8-sig") if l.strip() and not l.lstrip().startswith("#")]
    rows = list(csv.DictReader(lines))
    need = {"keyword", "range", "fit"}
    if not rows or not need <= set(rows[0].keys()):
        print(f"CSV needs the columns: {', '.join(sorted(need))}", file=sys.stderr)
        return 2

    out, problems = [], []
    for i, r in enumerate(rows, start=2):
        rng = norm_range(r.get("range", ""))
        if rng not in DEMAND:
            problems.append(f"row {i} ({r['keyword']!r}): unknown range {r.get('range')!r}")
            continue
        try:
            fit = int(str(r["fit"]).strip())
            assert 0 <= fit <= 5
        except Exception:
            problems.append(f"row {i} ({r['keyword']!r}): fit must be a whole number 0-5, got {r.get('fit')!r}")
            continue
        demand = DEMAND[rng]
        mixed = str(r.get("mixed", "")).strip().lower() == "yes"
        if mixed:
            demand = max(0, demand - 1)
        r2 = dict(r)
        r2.update({"demand": demand, "score": demand * 3 + fit * 3, "mixed": "yes" if mixed else "no"})
        out.append(r2)

    out.sort(key=lambda r: (-r["score"], -r["demand"], r["keyword"].lower()))
    # the same score is the same tier
    tiers = {s: n for n, s in enumerate(sorted({r["score"] for r in out}, reverse=True), start=1)}
    for r in out:
        r["tier"] = tiers[r["score"]]
    cols = ["tier", "keyword", "range", "demand", "fit", "mixed", "score", "page", "note"]
    extra = [c for c in (rows[0].keys() if rows else []) if c not in cols]
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols + extra, extrasaction="ignore")
        w.writeheader()
        w.writerows(out)

    counts = Counter(r["score"] for r in out)
    print(f"{len(out)} scored -> {a.out}")
    for s in sorted(counts, reverse=True):
        print(f"  score {s:>2}: {counts[s]} keyword(s)" + ("  <- tied, report them as tied" if counts[s] > 1 else ""))
    if problems:
        print("\nSkipped:", *problems, sep="\n  ", file=sys.stderr)
    print("\nReminder: ranges are bands, not exact volumes. Do not forecast traffic from them.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Mangools keyword collector: search volume, difficulty and volume trend.

Supplies the numbers this system otherwise refuses to state. Every figure it
prints comes from the Mangools API; nothing is estimated or inferred. Keywords
the API has no data for are reported as null, never as zero.

Auth: set MANGOOLS_API_TOKEN in the environment. Never pass the token on the
command line -- it lands in shell history.

    export MANGOOLS_API_TOKEN=...            # bash / git-bash
    $env:MANGOOLS_API_TOKEN = '...'          # PowerShell

Usage:
    python mangools_keywords.py locations Chennai
    python mangools_keywords.py keywords "website cost india,web design chennai" --location India
    python mangools_keywords.py keywords --file kws.txt --location India --json
    python mangools_keywords.py related "website development cost in india" --location India

Notes:
    * `seo` in the API response is keyword difficulty (0-100). Mangools KD is
      largely link-based -- it does not model local-pack, review or Google
      Business Profile competition, so local commercial terms are harder than
      their KD implies. See references/ before acting on a local term.
    * Trend compares the last 12 months against the 12 before it. A term can
      have healthy volume and a collapsing trend; both matter.
"""

import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)

API_BASE = "https://api.mangools.com/v3"
DEFAULT_LANGUAGE_ID = 1000  # English
KD_BANDS = [(15, "very easy"), (30, "easy"), (50, "possible"), (70, "hard")]


def get_token() -> str:
    """Read the API token from the environment, or exit with guidance."""
    token = os.environ.get("MANGOOLS_API_TOKEN", "").strip()
    if not token:
        print(
            "Error: MANGOOLS_API_TOKEN is not set.\n"
            "  bash:       export MANGOOLS_API_TOKEN=your_token\n"
            "  PowerShell: $env:MANGOOLS_API_TOKEN = 'your_token'\n"
            "Get a token at https://mangools.com/api-token",
            file=sys.stderr,
        )
        sys.exit(2)
    return token


def call(method: str, path: str, token: str, timeout: int = 45, **kwargs) -> dict:
    """Make an authenticated API call and return parsed JSON."""
    url = f"{API_BASE}{path}"
    headers = {"x-access-token": token, "Content-Type": "application/json"}
    try:
        resp = requests.request(method, url, headers=headers, timeout=timeout, **kwargs)
    except requests.RequestException as exc:
        return {"error": f"request failed: {exc}"}

    if resp.status_code == 401:
        return {"error": "401 unauthorized -- token rejected or lacks API access"}
    if resp.status_code == 429:
        return {"error": "429 rate limited -- quota exhausted, retry later"}
    if resp.status_code >= 400:
        return {"error": f"HTTP {resp.status_code}: {resp.text[:200]}"}
    try:
        return resp.json()
    except ValueError:
        return {"error": "response was not JSON"}


def resolve_location(name: str, token: str) -> dict | None:
    """Resolve a location name to its Mangools location record."""
    data = call("GET", "/mangools/locations", token, params={"query": name})
    if isinstance(data, dict) and data.get("error"):
        print(f"Error: {data['error']}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, list) or not data:
        return None
    # Prefer an exact case-insensitive name match, else the first result.
    for row in data:
        if row.get("name", "").lower() == name.lower():
            return row
    return data[0]


def trend(msv: list | None) -> dict:
    """
    Compare the last 12 months of volume against the 12 before it.

    Returns nulls rather than guesses when there is not enough history.
    """
    if not msv or len(msv) < 24:
        return {"recent_12m_avg": None, "prior_12m_avg": None, "change_pct": None}
    # msv rows are [year, month_index, volume]; sort chronologically before slicing.
    vols = [row[2] for row in sorted(msv, key=lambda r: (r[0], r[1]))]
    recent = sum(vols[-12:]) / 12
    prior = sum(vols[-24:-12]) / 12
    change = ((recent - prior) / prior * 100) if prior else None
    return {
        "recent_12m_avg": round(recent),
        "prior_12m_avg": round(prior),
        "change_pct": round(change, 1) if change is not None else None,
    }


def kd_band(kd) -> str | None:
    """Map a 0-100 difficulty score to a readable band."""
    if kd is None:
        return None
    for ceiling, label in KD_BANDS:
        if kd < ceiling:
            return label
    return "very hard"


def normalise(raw: list) -> list:
    """Reduce API keyword records to the fields this system reports on."""
    out = []
    for k in raw:
        kd = k.get("seo")
        out.append(
            {
                "keyword": k.get("kw"),
                "volume": k.get("sv"),
                "difficulty": kd,
                "difficulty_band": kd_band(kd),
                "cpc": k.get("cpc"),
                "ppc": k.get("ppc"),
                "trend": trend(k.get("msv")),
            }
        )
    return out


def print_table(rows: list, location_label: str) -> None:
    """Print a severity-free, volume-sorted table. Nulls print as '-'."""
    def cell(v):
        return "-" if v is None else str(v)

    print(f"\nLocation: {location_label}    Keywords: {len(rows)}")
    print(f"{'keyword':<46}{'vol':>7}{'KD':>5}  {'band':<11}{'12m trend':>18}")
    print("-" * 88)
    for r in sorted(rows, key=lambda x: -(x["volume"] or 0)):
        t = r["trend"]
        if t["change_pct"] is None:
            tr = "-"
        else:
            tr = f"{t['recent_12m_avg']} ({t['change_pct']:+.0f}%)"
        print(
            f"{(r['keyword'] or '')[:45]:<46}"
            f"{cell(r['volume']):>7}{cell(r['difficulty']):>5}  "
            f"{cell(r['difficulty_band']):<11}{tr:>18}"
        )

    no_data = [r["keyword"] for r in rows if r["volume"] is None]
    if no_data:
        print(
            f"\n{len(no_data)} keyword(s) returned no volume data. "
            "That is an absence of measurement, not a volume of zero -- "
            "long-tail buyer questions routinely have no recorded volume and "
            "can still be worth writing."
        )
        for kw in no_data:
            print(f"  - {kw}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch Mangools keyword volume, difficulty and trend."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_loc = sub.add_parser("locations", help="Resolve a location name to an id")
    p_loc.add_argument("query")

    p_kw = sub.add_parser("keywords", help="Metrics for a specific keyword set")
    p_kw.add_argument("keywords", nargs="?", help="Comma-separated keywords")
    p_kw.add_argument("--file", help="File with one keyword per line")

    p_rel = sub.add_parser("related", help="Related keyword ideas for a seed")
    p_rel.add_argument("seed")

    for p in (p_kw, p_rel):
        p.add_argument("--location", default="India", help="Location name (default: India)")
        p.add_argument("--language-id", type=int, default=DEFAULT_LANGUAGE_ID)
    for p in (p_loc, p_kw, p_rel):
        p.add_argument("--json", action="store_true", help="Emit raw JSON")

    args = parser.parse_args()
    token = get_token()

    if args.command == "locations":
        data = call("GET", "/mangools/locations", token, params={"query": args.query})
        if isinstance(data, dict) and data.get("error"):
            print(f"Error: {data['error']}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(data, indent=2))
            return
        for row in data[:25]:
            print(f"{row.get('_id'):>10}  {row.get('target_type','?'):<10} {row.get('canonical_name')}")
        return

    location = resolve_location(args.location, token)
    if not location:
        print(f"Error: no location matched '{args.location}'", file=sys.stderr)
        sys.exit(1)

    if args.command == "keywords":
        if args.file:
            with open(args.file, encoding="utf-8") as fh:
                kws = [ln.strip() for ln in fh if ln.strip()]
        elif args.keywords:
            kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
        else:
            print("Error: pass keywords or --file", file=sys.stderr)
            sys.exit(2)
        if len(kws) > 700:
            print(f"Error: {len(kws)} keywords exceeds the 700 per-request limit", file=sys.stderr)
            sys.exit(2)
        payload = {
            "keywords": kws,
            "location_id": location["_id"],
            "language_id": args.language_id,
        }
        data = call("POST", "/kwfinder/keyword-imports", token, json=payload)
    else:
        data = call(
            "GET",
            "/kwfinder/related-keywords",
            token,
            params={
                "kw": args.seed,
                "location_id": location["_id"],
                "language_id": args.language_id,
            },
        )

    if isinstance(data, dict) and data.get("error"):
        print(f"Error: {data['error']}", file=sys.stderr)
        sys.exit(1)

    rows = normalise(data.get("keywords", []))
    if args.json:
        print(json.dumps(
            {"location": location.get("canonical_name"), "keywords": rows},
            indent=2,
        ))
    else:
        print_table(rows, location.get("canonical_name", args.location))


if __name__ == "__main__":
    main()

# Product schema: "missing price" is often a false positive

`product_schema_checker.py` reports these as **errors**:

```
error: Offer is missing price or lowPrice
error: Offer is missing priceCurrency
```

It checks for `offers.price` and `offers.priceCurrency` as **direct** properties of the
Offer node. Schema.org allows the price to live one level deeper instead, inside
`offers.priceSpecification`:

```json
"offers": [{
  "@type": "Offer",
  "priceSpecification": [{
    "@type": "UnitPriceSpecification",
    "price": "240.00",
    "priceCurrency": "INR",
    "valueAddedTaxIncluded": false
  }],
  "availability": "http://schema.org/InStock"
}]
```

That is valid, and the script flags it anyway. Several WooCommerce and Shopify schema
generators emit this nested form by default, so it will recur.

**Reporting "your products have no price in structured data" when the price is right
there is the kind of error that costs a client relationship.** It is trivially
disprovable by the client in ten seconds with View Source.

## Verify before reporting

```bash
python - <<'PY'
import urllib.request, re, json
hdr = {'User-Agent': 'Mozilla/5.0 (compatible; SEOAudit/1.0)'}
u = 'https://example.com/product/thing/'
h = urllib.request.urlopen(urllib.request.Request(u, headers=hdr), timeout=40).read().decode('utf-8', 'replace')
for b in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S | re.I):
    d = json.loads(b)
    def walk(o):
        if isinstance(o, dict):
            if o.get('@type') == 'Product':
                print(json.dumps(o, indent=1, ensure_ascii=False))
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(d)
PY
```

## What to report instead

The finding is real but much smaller than the script implies. Downgrade it:

> Price is present via `priceSpecification`, which is valid. The flatter
> `offers.price` + `offers.priceCurrency` form is better supported across Google's
> tooling — emitting both is safest. **Severity: Medium, not Critical.**

## Real issues to look for in the same node while you are there

These are frequently present and genuinely worth reporting:

- **Double-encoded entities** — `"name": "Atta - Ragi &amp;amp; Veldt Grape"`. The
  `&amp;amp;` renders literally as `&amp;` in rich results. Grep the raw HTML for
  `&amp;amp;`.
- **Missing `brand`** — required for Google merchant listings.
- **No `aggregateRating` / `review` anywhere** — this, not the price, is usually the
  reason a store shows no stars in the SERP. Highest commercial value item.
- `availability` using `http://schema.org/...` instead of `https://`.
- `sku` emitted as a number rather than a string.
- `valueAddedTaxIncluded: false` on a store whose displayed prices are tax-inclusive —
  misrepresents the price to Google Shopping.

## Related

Same lesson as `spa-soft-200-false-positives.md`: **a script's error string is a
hypothesis, not a measurement.** Confirm against raw source before it reaches a client
deliverable.

## A second pattern worth naming: stale llms.txt

`llms_txt_checker.py` returning "found" can be a true positive and still be misleading.
A file can be genuinely present (`text/plain`, valid markdown) while listing URLs that
have since 404'd — generator plugins snapshot the site and are rarely re-run after pages
are deleted.

Check the file's *contents* against live status, not just its existence. The finding
"llms.txt is stale and points AI crawlers at N dead URLs" is more useful and more
accurate than either "present" or "missing".

**Corollary for sequencing:** on any site getting a cleanup pass, regenerate llms.txt
**last**. Regenerating before the deletions and redirects land just re-freezes the mess.
</content>

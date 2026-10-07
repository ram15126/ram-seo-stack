# Grepping for a schema type name gives false positives

`grep -c "FAQPage"` on a page with **no structured data at all** returned `1`.

The hit was not schema. It was a platform feature-flag name inside a JavaScript
config blob:

```
"specs.thunderbolt.deduplicateFAQPageStructuredData":true
```

That is Wix/Thunderbolt, but the class of problem is not Wix-specific. Page
bundles routinely embed framework config, A/B flags, analytics schemas and
i18n keys containing strings like `Product`, `Review`, `Breadcrumb`,
`FAQPage`, `Organization`, `AggregateRating`.

## Why it matters more than a normal tool bug

This one nearly shipped **inside a client deliverable, as the verification step**.
The finding itself was correct — the page genuinely had zero JSON-LD. But the
command published next to it returned `1`, so the client running it would have
concluded the finding was wrong. A verify block that contradicts its own finding
is worse than no verify block: it costs the credibility of every *other* finding
in the document.

## Match on the property, not the value

```bash
# Wrong — substring match anywhere in the bundle
curl -s "$URL" | grep -c "FAQPage"

# Right — only matches an actual JSON-LD @type declaration
curl -s "$URL" | grep -o '"@type"[[:space:]]*:[[:space:]]*"FAQPage"' | wc -l

# Better still — confirm whether any JSON-LD exists at all first
curl -s "$URL" | grep -o 'application/ld+json' | wc -l
```

Note `[[:space:]]*` on both sides of the colon — minified JSON has no spaces,
pretty-printed JSON does, and some generators emit `"@type" : "X"`.

## Always sanity-check the pattern in the positive direction

A precise pattern that returns `0` is indistinguishable from a *broken* pattern
that returns `0`. Prove the pattern can find something before trusting its
absence:

```bash
# same pattern, on a page that definitely HAS the type
curl -s "$PRODUCT_URL" | grep -o '"@type"[[:space:]]*:[[:space:]]*"Product"' | wc -l   # → 1
```

If the positive control also returns `0`, the pattern is wrong, not the page.

## Generalises to

- `grep -c "noindex"` — matches JS strings, comments, and CMS UI labels as often
  as a real `<meta name="robots">`. Match the tag.
- `grep -c "canonical"` — matches `rel=canonical`, but also `canonicalUrl` keys
  in embedded app state. Match `rel=["']canonical["']`.
- `grep -c "hreflang"` — matches config arrays of available locales.
- Any check for `AggregateRating` on a store — review-app bundles ship the string
  whether or not any rating is rendered.

## Related

Same root lesson as `schema-nested-price-false-positive.md` and
`spa-soft-200-false-positives.md`: **a string match is a hypothesis, not a
measurement.** Parse the JSON, or read the rendered DOM, before it reaches a
client. And run every command you publish — this was caught only because the
pre-send checklist requires it.

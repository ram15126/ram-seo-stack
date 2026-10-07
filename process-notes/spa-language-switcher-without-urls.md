# Client-side language switchers hide complete translations from search

## What happened
A client-rendered site shipped a header dropdown offering five languages. It was
not a stub: selecting a language swapped the full page copy, the `<title>` and
the `<html lang>` attribute into real, human-quality translation.

The URL never changed. All five languages lived on `/`, and the site carried no
`hreflang` markup at all.

## Why it matters
A search engine can only index a URL. Four of the five language versions did not
exist as far as any crawler was concerned — despite the translation already being
written, reviewed and paid for. It is usually the cheapest large win available on
a site, because the content cost is already sunk.

## How to check it
1. Use the switcher in the browser and watch the address bar. If the path does
   not change, the translations are invisible.
2. Count `hreflang` tags: `document.querySelectorAll('link[rel=alternate]').length`

## Trap to avoid
If the switcher is a `<select>`, clicking the `<option>` element from automation
does nothing — no `change` event fires, and it looks like a broken feature.
Set the value through the native setter and dispatch `change` before concluding
anything:

```js
const nat = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set;
nat.call(sel, 'fr');
sel.dispatchEvent(new Event('change', { bubbles: true }));
```

Reporting a working translation system as broken is far more damaging than
missing the finding.

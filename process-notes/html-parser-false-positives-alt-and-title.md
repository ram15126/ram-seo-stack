# Two HTML-parsing false positives: valueless `alt` and SVG `<title>`

Both encountered in a single audit of a WordPress + page-builder site. Both would
have shipped as confident, wrong, client-facing findings. Both are properties of
*how HTML is parsed*, not of the site — so they will recur on any stack.

---

## 1. "N images missing alt text" — when the alt attribute is valueless

**The warning:** a collector reported **1,182 of 5,372 images missing alt text**
across 177 pages. On the worst single page, 46 of 192.

**What was actually in the HTML:**

```html
<img id="image-861-1714" alt src="data:image/svg+xml,…" class="…perfmatters-lazy"
     data-src="https://example.com/wp-content/uploads/network-security.svg" />
```

Note `alt` with **no `=` and no value**. Per the HTML spec this is an empty
attribute, semantically identical to `alt=""` — the correct, intentional markup
for a decorative image. Screen readers skip it exactly as intended.

**Why the tooling gets it wrong:** Python's `html.parser` yields `('alt', None)`
for a valueless attribute, and BeautifulSoup preserves that `None`. So the common
check `img.get('alt') is None` counts *correct decorative markup* as missing alt.
A naive regex (`\balt\s*=`) fails the same way, for a different reason — there is
no `=` to match. Two independent methods agreeing on "46 missing" gave false
confidence that the number was real.

**How to check properly** — separate three cases, not two:

```python
imgs    = re.findall(r'<img\b[^>]*>', html)
no_attr = [t for t in imgs if not re.search(r'\balt\b', t)]              # genuine defect
bare    = [t for t in imgs if re.search(r'\balt(?![\w-])(?!\s*=)', t)]   # == alt="" : fine
empty   = [t for t in imgs if re.search(r'\balt\s*=\s*["\']\s*["\']', t)]# alt=""    : fine
```

Only `no_attr` is a finding. In the audit above it was **zero** — the site's alt
handling was fully correct, and the headline number was pure noise.

**Extra trap in the same markup:** the `src` is a `data:image/svg+xml` placeholder
with `viewBox='0 0 0 0'` and the real file is in `data-src`. That is a lazy-loader
(Perfmatters here, but WP Rocket / a3 / native loaders all do it). Any check that
reads `src` to judge image weight, format or dimensions is reading a 0×0 blank,
not the image. Read `data-src` / `data-lazy-src` too.

---

## 2. "Every page has multiple `<title>` tags"

**The warning:** *100% of pages have more than one `<title>`* — with sample values
like `star`, `map-marker`, `phone`, `facebook`, `envelope`, `cross`.

**What it actually was:** an inline SVG icon sprite in the page body.

```html
<svg aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden">
  <defs><symbol id="FontAwesomeicon-star" viewBox="0 0 26 28">
    <title>star</title>
```

`<title>` inside `<svg>` is the SVG **accessible-name** element — the correct way
to label an icon. It is a different element in a different namespace from the
HTML `<head><title>`, and it has no SEO meaning whatsoever.

**How to check properly:** count only within `<head>`.

```python
head = html[:html.lower().find('</head>')]
len(re.findall(r'<title[^>]*>', head))   # the only count that matters
```

On the audited page: **1** in `<head>`, 16 in the document, 79 `<svg>` elements.

**Where this shows up:** FontAwesome/Iconify/Feather sprites, Oxygen and Elementor
icon sets, and any `<use href="#icon">` sprite system. That is most modern sites,
so expect this one often.

---

## The general rule

Both false positives share a shape: **a tool counted a DOM element without
checking which context it sits in.** Namespace (`svg:title` vs `html:title`) and
attribute-presence-vs-value are exactly the distinctions a quick count discards.

Before reporting any count-based finding, open the raw HTML and read three actual
instances of the thing being counted. If they are not what the label says they
are, the count is measuring something else.

A `Confirmed` label means *I fetched it and read it* — reading the tool's summary
of it does not qualify, even when two tools agree.

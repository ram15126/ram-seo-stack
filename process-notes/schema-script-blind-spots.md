# Schema scripts: five blind spots that silently mislead

Found while validating a two-block JSON-LD setup. All five are reproducible on
any site; none are site-specific. Three produce **false positives**, two produce
**false negatives** — the false negatives are the dangerous ones, because a
clean "0 errors" reads as proof.

---

## 1. `schema_required_props.py` — every array or object is "placeholder text"

```
[warning] Organization property 'sameAs' appears to contain placeholder text
[warning] ContactPoint property 'availableLanguage' appears to contain placeholder text
[warning] OfferCatalog property 'itemListElement' appears to contain placeholder text
```

Cause:

```python
PLACEHOLDER_MARKERS = ("[", "REPLACE", "TODO", "INSERT", "example.com")
...
text = json.dumps(value) if not isinstance(value, str) else value
```

Non-string values get `json.dumps`'d, so **every list serialises with a `[`**
and matches the `"["` marker. Nested objects containing any list do too.

**Consequence:** a perfectly clean block reports 6+ "placeholder" warnings.
Never pass these through to a client — they read as "your schema has unfinished
template text in it," which is a specific and alarming claim.

**Triage rule:** a placeholder warning is only real if the offending value is a
*string* and you can see the bracket in it. Check the value before repeating the
warning.

---

## 2. Type matching is exact-string — subtypes are invisible

`schema_required_props.py`, `local_seo_checker.py` and `entity_checker.py` all
match `@type` by literal string.

`REQUIRED_PROPS` has a `LocalBusiness` entry but no entry for any of its ~80
subtypes (`ProfessionalService`, `Dentist`, `Restaurant`, `HomeAndConstruction
Business`, `LegalService`, …). A node typed with a subtype therefore:

- has **no** required properties looked up → `Errors: 0`
- is invisible to `local_seo_checker.py` → `LocalBusiness nodes: 0` →
  `[warning] No LocalBusiness JSON-LD found`, on a page that has one

Observed on a live page with a `ProfessionalService` node missing `address`
(which Google documents as required for LocalBusiness):

```
schema_required_props.py  → Nodes checked: 15  Errors: 0  Warnings: 6
local_seo_checker.py      → LocalBusiness nodes: 0  Phones: 0
entity_checker.py         → Entities in Schema: 1     (missed the second node)
```

Three scripts, three clean-looking outputs, one genuine missing required
property. **`Errors: 0` from these scripts is not evidence the schema is
correct.** Read the actual `@type` values yourself:

```bash
curl -s "$URL" | grep -oE '"@type"[[:space:]]*:[[:space:]]*"[A-Za-z]+"' | sort | uniq -c
```

That one command is worth more than all three scripts on a schema pass — it
inventories exactly what types exist and, by absence, what does not.

---

## 3. `local_seo_checker.py` reads body text, so JSON-LD-only phones are "0 phones"

```python
phones = sorted(set(m.group(1) for m in PHONE_RE.finditer(body_text)))
...
if node.get("telephone") and phones and <mismatch>:
    issues.append("Schema telephone does not visibly match page phone text")
```

The NAP-mismatch check is guarded by `and phones` — so when the page is a JS
shell (or the number lives only in schema / a widget config), `phones` is empty
and **the mismatch check never runs at all**. It cannot report a NAP conflict;
it silently skips.

To actually find conflicting numbers, grep all three surfaces:

```bash
curl -s "$URL"        | grep -o '"telephone"[[:space:]]*:[[:space:]]*"[^"]*"'
curl -s "$BUNDLE_JS"  | grep -oE 'wa\.me/[0-9]+'      | sort | uniq -c
curl -s "$BUNDLE_JS"  | grep -oE 'tel:\+?[0-9]+'      | sort | uniq -c
```

---

## 4. `validate_schema.py` crashes on a multi-type node

```json
{"@type": ["Organization", "ProfessionalService"]}
```

```
TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
  at  if schema_type in deprecated:
```

Multi-typing is valid JSON-LD and is the standard way to merge two entities into
one node. The script assumes `@type` is a string. Exit code is 1 (crash), not 2
(block), so as a pre-commit hook it fails *open* — the edit goes through with no
validation performed and only a traceback in the log.

Until it is fixed, validate multi-type blocks with `python -m json.tool` plus a
manual read, and do not treat a passing hook as coverage.

---

## 5. Two stale "recommended property" warnings

| Warning | Why it is wrong |
|---|---|
| `WebSite is missing recommended property 'potentialAction'` | `potentialAction`/`SearchAction` existed for the sitelinks search box. Google removed that feature and archived the docs. Recommending it now adds markup that renders nothing — and only makes sense at all if the site has a real search endpoint. |
| `BreadcrumbList is missing recommended property 'name' / 'position' / 'item'` | Those belong on each `ListItem`, not on the `BreadcrumbList` node. A correct breadcrumb block triggers all three warnings. |

---

## The pattern behind all five

Same root lesson as `schema-grep-false-positives.md` and
`schema-nested-price-false-positive.md`, with one addition:

- A script's **error** string is a hypothesis, not a measurement.
- A script's **silence** is also a hypothesis. `Errors: 0` on a type the script
  has never heard of is not a pass — it is a skip wearing a pass's clothes.

Before writing "your schema validates cleanly", confirm the tool actually
*looked* at every node: compare its `Nodes checked:` count and the types it
names against your own `@type` inventory.

## Two external checks worth running instead

Both are free, no-login, and reproduce for the reader:

- `https://validator.schema.org/#url=<urlencoded-page-url>` — deep link
  auto-runs and lists every node. Validates **vocabulary only**: it will show
  `0 ERRORS` on markup that Google considers incomplete. Say so when you quote
  it, or the client will use it to "disprove" a correct finding.
- `https://search.google.com/test/rich-results?url=<urlencoded-page-url>` —
  deep link auto-runs, no sign-in needed. This is the one that reflects Google's
  own requirements. Note that it grades missing *required* properties as
  "non-critical issues" rather than errors, so calibrate severity to what the
  client will actually see on screen, not to what the docs say.

---

## Blind spot: `parse_html()` returns a soup with every script already removed

**Added 25 August 2026.** Found while building a new collector.

`seo_common.parse_html()` extracts JSON-LD into the returned `schema` key and then
runs:

```python
for element in soup(["script", "style", "noscript", "template"]):
    element.decompose()
```

before returning. So `parsed["soup"]` has **no script tags at all**. Any new script
that does the natural thing —

```python
soup = parse_html(html, url)["soup"]
soup.find_all("script", attrs={"type": "application/ld+json"})   # always []
```

— finds nothing and reports **"no structured data found"** on a page that has
perfectly good JSON-LD. The failure is silent: no exception, no warning, just a
confident false negative in a client-facing audit.

Observed live: a new pre-flight checker reported "A visible FAQ section exists but no
FAQPage schema was found" against a test page whose FAQPage schema was correct and
right there in the head.

**Rule**

- Read structured data from **`parsed["schema"]`**, never by re-scanning
  `parsed["soup"]`.
- `parse_html` marks unparseable blocks as `{"error": "invalid_json", "snippet": ...}`
  — check for that key rather than assuming every entry is a valid node.
- `parsed["body_text"]` is computed *after* the decompose, which makes it the correct
  input for any visible-text comparison (e.g. diffing FAQ schema against rendered
  text). Using `soup.get_text()` on a page whose scripts had *not* been stripped would
  silently include JSON-LD content in the "visible" text and mask a mismatch.
- The general form: **when reusing a shared parser, check what it mutates before
  trusting a negative result.** A zero count from a helper is a claim about the
  helper as much as about the page.

---

## Four more false positives from the same family (25 Aug 2026)

Found by running a new checker against real, well-built pages and refusing to
believe a result that contradicted a handover document. All four were the
*checker's* fault, not the pages'.

1. **Reading a key the parser does not return.** The head check read
   `parsed["meta"]["description"]`. `parse_html` returns **`meta_description`**,
   a flat key. `parsed.get("meta")` is always `None`, so it reported *"No meta
   description"* on every page that had one.

2. **Refusing the better JSON-LD pattern.** The author check required an inline
   `{"@type": "Person", "name": ...}` under `author`. Well-formed pages write
   `author: {"@id": "...#person"}` referencing a sibling `Person` node. The
   idiomatic form was reported as *"No Person author found in schema"*.
   **Resolve `@id` references before concluding a node is absent.**

3. **Comparing schema text to visible text with whitespace intact.**
   BeautifulSoup's `get_text(" ")` inserts a separator at every inline-element
   boundary, so `<em>Kapadapuram</em>.` renders as `Kapadapuram .` Two of three
   flagged FAQ "mismatches" differed only by a space before a semicolon and a
   space before a full stop. **Compare whitespace-insensitively** — whitespace
   differences are not structured-data violations.

4. **Grabbing the standfirst instead of the answer block.** The scan took the
   first paragraph over 20 words after the H1. On templates with a dek above the
   byline that is the dek — often just the meta description. It reported a
   *28-word answer block with no definition pattern* on pages whose real 72-word
   answer block, two elements later, opened *"X, also called Y, is a…"*.
   **Look for the labelled summary block first** — and note the label may be a
   `<span class="eyebrow">`, not a heading.

**The pattern across all four:** the checker was right that it could not find the
thing, and wrong that the thing was missing. Also note #3 and #4 only surfaced
because a handover document asserted the opposite and was trusted enough to check
against. **Keep something to disagree with.**

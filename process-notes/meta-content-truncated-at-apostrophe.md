# Meta content truncated at the first apostrophe — a live bug in `site_collect.py`

Found during a routine site audit. The collector reported three meta descriptions
and one `og:title` as catastrophically truncated:

```
description: 'If you'   (len 6)
description: 'It'       (len 2)
og:title   : 'Ravi Kumar'
```

That looked like a serious CMS templating defect and was one edit away from
shipping as a `Confirmed`, High-severity, client-facing finding: *"your meta
descriptions are being cut to two characters."*

**The tags were completely fine.** Raw HTML:

```html
<meta name="description" content="It's interesting how most things are digital these days — even solar. A look at one provider…">
<meta property="og:title" content="Ravi Kumar's three markets on a train — Author Name">
```

A literal `'` inside a double-quoted attribute is valid HTML and needs no
escaping. The site was correct; **our own collector was wrong.**

---

## The bug

`skills/seo/scripts/site_collect.py` line 100 (and 102, 103):

```python
descs = all_matches(html, r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']')
#                                                                          ^^^^^^        ^^^^^^
```

The closing delimiter is the character class `["\']`, which matches **either**
quote character — with no requirement that it matches the one that opened the
attribute. So `(.*?)`, being non-greedy, stops at the first `"` *or* `'` it
finds. In `content="It's …"` that is the apostrophe in `It's`, four characters in.

Any value containing an apostrophe is silently truncated at it. In English prose
— which is what meta descriptions are — that is extremely common: `it's`,
`you've`, `don't`, `business's`, and every possessive.

Reproduce:

```python
import re
html  = '''<meta name="description" content="It's interesting how most things are digital.">'''
buggy = r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']'
re.findall(buggy, html)     # -> ['It']
```

## The fix

Capture the opening quote and require the same character to close it, via a
backreference:

```python
fixed = r'<meta[^>]+name=["\']description["\'][^>]+content=(["\'])(.*?)\1'
[m[1] for m in re.findall(fixed, html)]
# -> ["It's interesting how most things are digital."]
```

The captured value moves to group 2, so callers indexing group 1 must be updated.
The same pattern-shape bug is present on the `robots` line (102) and the `og:`
line (103) of the same file; both need the same treatment.

Better still: parse meta tags with BeautifulSoup (`soup.find('meta', attrs=...)
.get('content')`), which handles quoting correctly and has no equivalent failure
mode. The regex exists for speed on a bulk pass — if it stays, it must at least
be quote-balanced.

## Why it went unnoticed

The truncation is *plausible*. "Meta description is 6 characters" reads like a
real CMS bug, not like a tooling artifact — unlike a parse error, which announces
itself. And because the same collector produces `description`, `description_len`
and `og:*` from the same broken pattern, **every derived field agreed with every
other**, which felt like corroboration. It was one bug counted four times.

## The general rule

This is the third false positive in this workspace with an identical shape: a
regex or a count that measures the *markup's syntax* rather than the page's
meaning. The prior two are in `html-parser-false-positives-alt-and-title.md`.

The check that catches all of them is cheap and non-negotiable:

> Before reporting any extracted *value* as defective, `curl` the page and read
> that exact tag in the raw bytes.

A `Confirmed` label means *I fetched it and read it*. Reading the collector's
summary does not qualify — especially when the collector's fields all agree,
because they are usually all derived from the same parse.

**Corollary specific to truncation findings:** a value that looks cut off mid-word
is a tooling suspect first and a site defect second. Real CMS truncation almost
always lands on a length boundary (155, 160, 60 chars) or a word boundary — not
in the middle of `It's`.

# Calling a form broken: the four structural checks that survive any environment

A previous learning in this workspace
(`lazy-loaded-widgets-need-a-real-viewport.md`) says: **never report an
interactive feature as broken from automation alone.** That rule stands. This
note is the other half — how to legitimately confirm a form is dead when it
genuinely is, without a browser and without risking a repeat of that mistake.

The distinction is **visibility-dependent vs structurally-dependent evidence.**

- The false positive that cost a report was visibility-dependent: a widget that
  *would* mount given a real viewport. Absence in headless proved nothing.
- A form with no `action`, no field names, and its submit button outside the
  `<form>` element is broken in the served bytes. No amount of rendering,
  scrolling or intersection changes that.

## The four checks

Run all four against `curl`-fetched HTML. If **all four** fail, the form cannot
submit, and that holds in every browser.

```bash
URL="https://site.com/contact.html"

# 1. Does the form have a destination?
curl -s "$URL" | grep -oE '<form[^>]*>'
#    Look for action= and method=. Bare <form> posts to itself.

# 2. Is the submit control INSIDE the form element?
curl -s "$URL" | grep -n -A2 "</form>"
#    A <button> appearing AFTER </form> is outside it and submits nothing.

# 3. Do the inputs have name attributes?
curl -s "$URL" | grep -oE '<input[^>]*>' | grep -c 'name='
#    0 means no data would be transmitted even on a successful submit.

# 4. Is there ANY JS that could intercept submission?
curl -s "$URL" | grep -oE '<script[^>]*src="[^"]*"|onsubmit=|addEventListener|fetch\(|formspree|emailjs|web3forms|getform|netlify'
#    Only jquery/bootstrap/carousel libs = no handler. This is the check that
#    separates "broken" from "handled by JS you cannot see".
```

Check 4 is the one that matters most. It is the direct analogue of the missed
`grep` for the Turnstile site key in the earlier failure: **verify the premise,
not just the symptom.** The symptom is "nothing happens on click"; the premise is
"no code exists that could make something happen". Only check 4 tests the
premise.

## Byte offsets beat eyeballing

For the button-outside-form case, prove it numerically rather than by reading
indentation — nested markup makes visual inspection unreliable:

```python
h = open('page.html').read()
fs, fe = h.find('<form'), h.find('</form>')
for m in re.finditer(r'<button[^>]*>', h):
    print(m.start(), "inside_form =", fs < m.start() < fe)
```

An offset 13 characters past `</form>` is not a judgement call.

## Still do this

Even with all four confirmed, give the reader a **10-second manual check** as the
first verification step ("fill a field, click submit, watch nothing happen").
Structural proof convinces you; the manual check convinces the client, and it
costs them no tools. If the manual check ever contradicts the four structural
checks, the structural reading was wrong — trust the browser.

## Where this generalises

The same split applies beyond forms:

| Safe to call broken from curl | Needs a real browser |
|---|---|
| Missing `action` / `name` / handler | Lazy-loaded widget absent |
| Button outside its form | Captcha not appearing |
| `href="#"` links with no JS router | Scroll-triggered content empty |
| Missing meta/schema/canonical tags | Hover or tab-revealed content |
| Redirects, status codes, headers | Anything intersection-gated |

Left column: report it. Right column: ask the user, or say "could not verify in
an automated browser".

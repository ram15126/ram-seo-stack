# A headless browser cannot prove a lazy-loaded widget is absent

**The false positive.** An audit reported a client's contact form as completely
broken — "the SEND button is permanently disabled, no visitor can submit an
enquiry" — and put it at the top of a client-ready report as an URGENT finding.

**The form worked perfectly.** The client opened it in a normal browser: the
Cloudflare Turnstile widget rendered, showed "Success!", the button enabled, the
message sent.

## Why the automated check was wrong

The widget is lazy-loaded:

```js
// Only mounts when an IntersectionObserver says the container is near the viewport
const Turnstile = dynamic(() => import('...').then(m => m.Turnstile), {ssr: false})
new IntersectionObserver(([e]) => e.isIntersecting && setShow(true),
                         {rootMargin: '200px 0px'})
// And the widget itself only renders if the site key is configured:
{siteKey && <Turnstile … />}
```

In the automated browser the component never mounted. Every signal agreed, and
every signal was misleading:

| Observation | Wrong conclusion drawn | Actual meaning |
|---|---|---|
| No Turnstile container in the DOM | "`siteKey` must be falsy" | The component never mounted |
| No network request to Cloudflare | "The site never tries to load it" | Nothing had mounted to trigger the load |
| `window.turnstile` undefined | "The script is absent" | Same |
| Button disabled with valid fields | "Permanently broken" | Correct gating, waiting on a token that never came |

**The root cause: the browser pane was not compositing frames.**
`IntersectionObserver` does not fire reliably when the page is not actually being
painted. Programmatic `scrollIntoView()` moves `scrollY` without necessarily
producing a real intersection event in a non-rendering tab.

## The clue that was missed

The screenshot tool had already said it, verbatim:

```
screenshot failed: the Browser pane is not displayed,
so the page is not compositing frames.
```

That message was treated as a minor tooling annoyance. It was in fact a direct
statement that **anything gated on rendering, visibility or intersection would not
work in that session** — which is exactly what was then tested and reported.

**Rule: if the screenshot tool says the page is not compositing, every
visibility-dependent finding from that session is void.**

## The check that would have caught it in seconds

Search the JS bundle for the key before concluding it is missing:

```bash
grep -oE '0x4AAAA[A-Za-z0-9_-]+' chunk.js     # Turnstile site keys start 0x4AAAA
grep -oE '6L[A-Za-z0-9_-]{30,}'  chunk.js     # reCAPTCHA site keys start 6L
```

It was there: `0x4AAAAAADmT2u0yj2IMaZ9O`. One grep against the claim's central
premise — "the site key is missing" — would have killed the finding before it ever
reached a document.

## Standing rules

1. **Never report an interactive feature as broken from automation alone.** Ask
   the user to try it, or state it as "could not verify in an automated browser"
   and move on. The asymmetry is brutal: telling a client their site works when it
   doesn't is a missed finding; telling them it is broken when it works destroys
   trust in the entire report.
2. **Absence of evidence in a headless browser is not evidence of absence** for
   anything lazy-loaded, deferred, intersection-gated, hover-triggered, or
   consent-gated.
3. **Verify the premise, not just the symptom.** The claim rested on "the site key
   is missing." That was directly checkable and was never checked.
4. **Prefer environment-independent methods.** Findings that survive a plain
   `curl` of the served HTML are safe. In the same audit, "no analytics installed"
   was confirmed by grepping the raw HTML of all 8 pages for GA4/GTM/Pixel/Clarity
   — it needed no browser and it held up. Same audit, same session: one method
   robust, the other not.
5. **Anything gated on real rendering needs a real browser.** Lazy images below
   the fold, infinite scroll, animation triggers, sticky headers, cookie banners,
   captchas — all of it.

## Where this bites in SEO audits specifically

- Below-the-fold images with `loading="lazy"` — may look "never loaded"
- Third-party embeds behind consent banners — look absent, are merely deferred
- Sticky navigation and scroll-triggered CTAs
- Any captcha or bot-protection widget
- Content revealed by hover, tab, or accordion interaction

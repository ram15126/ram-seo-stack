# A hidden browser tab suppresses entrance animations — don't call the page blank

**Class:** false positive · **Cost if shipped:** a fabricated Critical finding
**First hit:** 2026-08-07, on a Next.js site using Framer Motion

---

## The trap

Modern marketing sites commonly ship above-the-fold elements with inline
`opacity:0` and fade them in after hydration:

```html
<h1 id="hero-heading" style="opacity:0;transform:translateY(28px)">…</h1>
```

Query that element from an automated browser and you get the alarming result:

```js
getComputedStyle(document.querySelector('h1')).opacity  // "0"
```

Sample it repeatedly over several seconds and it *stays* `0`. On one site, 96 of
98 animated elements were still at `opacity: 0` three seconds after load.

The obvious conclusion — "the hero never renders, the page is blank for users,
this is Critical" — is **wrong**.

## Why it happens

Animation libraries (Framer Motion, GSAP ScrollTrigger, AOS, most
IntersectionObserver-based reveals) drive frames with `requestAnimationFrame`.
A browser tab that is not being composited does not fire `rAF`. So the
animation never starts and the initial `opacity:0` persists forever.

This happens whenever the automation surface isn't painting: a hidden pane, a
backgrounded tab, some headless configurations.

## The tell

```js
document.visibilityState   // "hidden"  ← everything below this is unreliable
```

Check it **before** reporting anything derived from computed styles, element
geometry, or visibility. `document.hidden`, `getBoundingClientRect()` returning
zeros, and "element not in viewport" all fail the same way.

A second tell: a screenshot attempt errors with something like *"the page is not
compositing frames."* That error is diagnostic information, not an obstacle —
it is telling you the visibility state is wrong.

## What to do instead

1. **Check `document.visibilityState` first.** If it is `hidden`, do not report
   any visibility, layout or animation finding from that session.
2. **Prove hydration separately from animation.** Clicking a button and seeing
   the DOM change proves JS ran. If interaction works but animations don't, the
   problem is compositing, not the site.
3. **Cross-check with a renderer you don't control.** Lighthouse / PageSpeed
   Insights runs a real, painting Chrome. If it reports a plausible LCP, the
   content painted for a real user.
4. **Fall back to `Likely`** and say why, rather than dropping the observation
   entirely.

## What survives — the finding underneath is still real

Do not over-correct into reporting nothing. The pattern itself is a genuine and
common **LCP problem**, and it is measurable without any visibility check:

- Count the elements shipped hidden:
  `curl -s <url> | grep -o "opacity:0" | wc -l`
- Compare **FCP vs LCP** from PageSpeed. A large gap — e.g. FCP 0.9 s against
  LCP 5.1–5.8 s — is the signature of a largest element that cannot paint until
  the JS bundle downloads, hydrates and animates.

So the honest finding is *"above-fold content is gated behind client-side
animation, and here is the LCP cost"* — **not** *"the hero is invisible."*

Label the measurement `Confirmed` and the mechanism `Likely` unless you have
isolated the LCP element directly.

## Related

- `lazy-loaded-widgets-need-a-real-viewport.md` — same root cause, different symptom
- `form-broken-verify-structurally-not-visually.md` — the general rule: never
  conclude "broken" from automation alone

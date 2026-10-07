# `next dev` and `next build` share `.next` — never run both

**Class:** self-inflicted, wastes 5–10 minutes and looks like a real bug
**First hit:** 2026-08-07, verifying a design change on a Next.js client site

---

## What happens

Leave a dev server running, run `npm run build` in another shell to verify a
change, then `next start` — and the production server returns **HTTP 500** on
every route, with no useful error in the response body.

The build itself reports success. That is what makes it confusing: you go
looking for a bug in the code you just wrote.

## Why

`next dev` and `next build` both write to the same `.next` directory, and
`next dev` keeps writing while it runs. The build's output gets interleaved with
dev-mode artefacts, and `next start` then reads a directory that is a mix of
both.

## The fix

```bash
# stop every node process holding .next (Windows)
taskkill //F //IM node.exe //T
rm -rf .next
npm run build
npx next start -p <port>
```

## The rule

**One server at a time.** Pick the one that matches the question:

| Question | Use |
|---|---|
| Does it *look* right? Iterating on design? | `next dev` — hot reload |
| Is the HTML/schema/sitemap right? Perf numbers? | `next build` + `next start` |

SEO verification must use the production build. Dev mode does not preload fonts
the same way, does not minify, does not apply the same image optimisation, and
its performance numbers are meaningless. Any claim about served HTML, font
loading, or Core Web Vitals made against `next dev` is unreliable.

If you need both, build to a separate directory (`distDir` in `next.config`) or
just stop the dev server first — it takes seconds.

## Tell

`next start` returning 500 on *every* route, including static ones, right after
a build that printed `✓ Compiled successfully`. If the build passed and every
route 500s, suspect the directory, not the code.

## Related

- `run-scripts-from-workspace-root.md` — the other "it's the environment, not the code" trap

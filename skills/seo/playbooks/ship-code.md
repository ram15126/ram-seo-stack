---
name: ship-code
description: Implement SEO/GEO fixes directly in a code-built site (Next.js, Astro, Vite, SvelteKit, Nuxt, plain static). Use after an audit, when the user says "fix it", "implement these", "apply the changes", or when the site has no CMS to configure.
---

# Ship the Fix in Code

Most SEO advice assumes a CMS with a plugin panel. These sites have neither.
The fix is a commit. This playbook turns audit findings into that commit.

## Why this playbook exists

An audit that ends in recommendations transfers the work to someone else. On a
code-built site you have file access, so the honest deliverable is the change
itself. This is also where most of the durable wins live: metadata generated
from a template applies to every page ever added, while a hand-edited title tag
applies to one.

---

## Step 1 — Identify the stack before touching anything

```bash
ls package.json next.config.* astro.config.* nuxt.config.* svelte.config.* vite.config.* 2>/dev/null
cat package.json | head -40
```

| Signal | Stack | Where metadata lives |
|---|---|---|
| `next.config.*`, `app/` | Next.js App Router | `export const metadata` / `generateMetadata()` per route |
| `next.config.*`, `pages/` | Next.js Pages Router | `next/head` per page, or a shared `<Seo>` component |
| `astro.config.*` | Astro | Frontmatter + a layout `<head>` |
| `nuxt.config.*` | Nuxt | `useHead()` / `definePageMeta` |
| `svelte.config.*` | SvelteKit | `<svelte:head>` |
| `vite.config.*`, no framework | Vite/SPA | `index.html` + prerender; **check indexability first** |
| plain `.html` | Static | Edit `<head>` directly, or generate |

If it's a client-rendered SPA with no prerendering, stop and check whether
Google is indexing anything at all (`javascript_render_audit.py`). Metadata
work on an unindexable site is wasted effort — fix rendering first.

## Step 2 — Read before you write

Find what already exists. Do not add a second competing source of truth for
metadata; that is how sites end up with two `<title>` tags.

```bash
grep -rn "generateMetadata\|export const metadata\|<title>\|useHead\|svelte:head\|application/ld\+json" --include=*.{ts,tsx,js,jsx,astro,svelte,vue,html} . | head -40
```

Identify: the shared layout, any existing SEO component, the sitemap route, and
`robots.txt` / `robots.ts`.

---

## Step 3 — Fix in this order

Order matters. Each step is worthless if the one above it is broken.

### 1. Indexability — can Google and AI crawlers reach it?

- `robots.txt`: confirm no blanket `Disallow: /`, and that AI crawlers are
  handled deliberately (see `playbooks/geo-crawlers.md` — this is a business
  decision the client makes, not a default you apply silently).
- No stray `noindex` in layouts or on staging-derived routes.
- Canonical tags present, absolute, self-referencing by default.

### 2. Metadata — templated, not hand-typed

Set it at the layout level with a per-page override so every future page
inherits correct defaults. Next.js App Router:

```ts
// app/layout.tsx
export const metadata = {
  metadataBase: new URL('https://example.com'),
  title: { default: 'Brand — Primary Value Prop', template: '%s | Brand' },
  description: '...',
  openGraph: { type: 'website', siteName: 'Brand', images: ['/og.png'] },
  twitter: { card: 'summary_large_image' },
  alternates: { canonical: '/' },
}
```

```ts
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }) {
  const post = await getPost(params.slug)
  return {
    title: post.title,
    description: post.excerpt,
    alternates: { canonical: `/blog/${post.slug}` },
    openGraph: { type: 'article', publishedTime: post.date, authors: [post.author] },
  }
}
```

Titles: unique per page, primary term early, ~50–60 chars. Descriptions written
to earn the click, ~150–160 chars. One `<h1>` per page.

### 3. Structured data — generated from the same data as the page

Emit JSON-LD from the object that already renders the page, so it can never
drift out of sync with what users see (contradicting the visible page is a
manual-action risk, not just a wasted opportunity).

```tsx
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    datePublished: post.date,
    dateModified: post.updated,
    author: { '@type': 'Person', name: post.author, url: post.authorUrl },
  })}}
/>
```

Templates live in `schema/`. Pick types via `references/schema-types.md`, then
validate with `scripts/validate_schema.py` and `scripts/schema_required_props.py`.

### 4. Sitemap and robots — as code, so they never go stale

```ts
// app/sitemap.ts
export default async function sitemap() {
  const posts = await getAllPosts()
  return [
    { url: 'https://example.com', lastModified: new Date(), priority: 1 },
    ...posts.map(p => ({
      url: `https://example.com/blog/${p.slug}`,
      lastModified: new Date(p.updated),
    })),
  ]
}
```

A hand-maintained `sitemap.xml` is wrong within a month. Generate it.

### 5. AI-readable surfaces — the AEO layer

This is where code-built sites can beat WordPress competitors outright, because
it is trivial for you and awkward for them.

- `llms.txt` and `llms-full.txt` — generate with
  `scripts/llms_txt_generator.py`, or at build time with
  [`aeo.js`](https://github.com/multivmlabs/aeo.js)
  (`npx aeo.js generate`), which also emits `ai-index.json` and per-page
  markdown. Prefer a build step over a committed static file so it stays current.
- Serve a clean markdown twin of each page where cheap — LLM fetchers parse it
  far more reliably than a JS-heavy DOM.
- Structure content for extraction per `playbooks/geo-citability.md`:
  answer-first sections, self-contained passages, specific figures with dates.

### 6. Performance — only what actually moves LCP

Check `scripts/lcp_subparts.py` before optimizing. Usually: the hero image
(`next/image`, correct `sizes`, `priority` on the LCP element only), fonts
(`next/font` or `font-display: swap`, self-hosted), and third-party scripts
(`scripts/third_party_script_audit.py` — a chat widget is often the whole
problem). Do not refactor rendering for a 40ms gain.

### 7. Internal linking — the most under-used lever you control

Run `scripts/internal_links.py` and `scripts/orphan_pages_from_sitemap.py`.
Orphan pages and thin cross-linking are common on component-built sites because
links are written by hand. Where a content collection exists, generate related
links from tags/cluster metadata rather than hardcoding them.

---

## Step 4 — Verify, don't assume

Re-run the collectors that produced the original findings and diff the result.
A fix is not shipped because you edited a file; it is shipped when the
measurement changes.

```bash
python "skills/seo/scripts/audit_runner.py" --url https://example.com
```

Then build the site and confirm the metadata is in the **rendered HTML**, not
just the source:

```bash
npm run build && npx serve out   # or the project's own preview command
curl -s localhost:3000 | grep -i "<title>\|canonical\|application/ld+json"
```

## Step 5 — Log it

Append to `brands/<brand>/changelog.md` — date, files changed, what was fixed,
what you expect it to move. Without this, the next month's traffic change is
uninterpretable. See `playbooks/changelog.md`.

---

## Guardrails

- **Branch, don't push to main.** Show the diff and let the user approve before
  anything is deployed. This is someone's live business.
- **One concern per commit** (`seo: add canonical tags to blog routes`), so a
  regression can be traced and reverted precisely.
- **Never mass-rewrite content for keyword density.** It reads as spam to
  readers and to Google, and it damages the E-E-A-T signals you are also
  trying to build.
- **Redirects before URL changes.** Changing a slug without a 301 discards
  every link and ranking that URL earned.
- **Respect the client's stack.** Do not migrate frameworks, add a CMS, or pull
  in a dependency to solve a metadata problem.

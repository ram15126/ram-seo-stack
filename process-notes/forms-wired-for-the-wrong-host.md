# Check the form's submit target against the actual host

Static-host form services (Netlify Forms, and to a lesser extent Cloudflare
Pages / Vercel equivalents) work by having the **platform** intercept a POST.
Move the same codebase to a different host and the markup still looks perfect —
the attributes, the honeypot, the hidden detection form are all intact — but
nothing intercepts the request and every submission dies.

This survives redesigns and migrations silently because there is no visual tell:
the form renders, validates, and shows a state on submit.

## What to look for

Netlify's convention, in HTML and in the bundle:

```html
<form name="contact" data-netlify="true" data-netlify-honeypot="bot-field">
<!-- plus a hidden duplicate <form netlify> for build-time detection -->
```

```js
fetch("/", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ "form-name": "contact", ...values }).toString()
})
```

`fetch("/")` with a `form-name` field **is** the Netlify Forms signature. If the
response headers do not say Netlify, the form is dead.

## The check — three commands, no data submitted

```bash
# 1. Who actually serves this site?
curl -sI https://site.com/ | grep -i -E "server|x-nf-request-id|x-vercel-id"

# 2. Does the form's target accept POST at all?
curl -s -o /dev/null -X POST -w "%{http_code}\n" "https://site.com/"

# 3. Control: does POST work anywhere on this host?
curl -s -o /dev/null -X POST -w "%{http_code}\n" "https://site.com/api/<known-endpoint>"
```

Step 3 is what makes the finding airtight. A 405 on step 2 alone could be a
platform-wide POST rule. A 405 on step 2 **and** a 200 on step 3 proves the
rejection is specific to the form's target.

Send **no body**. A bare POST establishes the method-level verdict, and it puts
zero fake lead data into a client's inbox or CRM.

## Do not submit a test lead to prove it

Tempting, and wrong. If the form turns out to work, you have injected a fake
enquiry into a client's pipeline — an outward-facing side effect you did not have
permission for. The method-level 405 is sufficient evidence. If a stakeholder
wants an end-to-end test, that is their call to make and their inbox to check.

## Also grep for the alternatives before concluding

Confirm there is no *other* submit path before writing it up:

```bash
grep -oE 'fetch\("[^"]+"' bundle.js | sort -u
grep -oE '"/\.netlify/functions/[^"]*"|"/api/[^"]*"' bundle.js | sort -u
```

A React `onSubmit` can post anywhere. Only report the form broken once you have
enumerated every `fetch` in the bundle and none of them reach a live endpoint.

## Severity

Report it above every SEO finding on the page. Rankings that deliver traffic to a
form that discards it are worth nothing, and this is usually a small fix — one
serverless function plus a changed URL.

Related: `never-report-broken-from-automation.md` — the inverse failure, where a
working feature was called dead. The discipline is the same: prove the mechanism,
not the appearance.

# SSRF guards: validate through the same resolver the fetch will actually use

**Class:** security-relevant bug caught by live-network testing, not mocks
**First hit:** 2026-08-07, building a public URL-audit tool for a client site

---

## The trap

Building an SSRF guard for an endpoint that fetches user-supplied URLs, the
obvious move in Node is `dns.resolve4`/`dns.resolve6` — they return exactly
the IP addresses a hostname resolves to, easy to check against a private-IP
blocklist.

```js
const [v4, v6] = await Promise.allSettled([dns.resolve4(host), dns.resolve6(host)]);
```

This is a real gap, not just a style choice: `dns.resolve4`/`resolve6` make a
**direct DNS-protocol query** (via c-ares), while `fetch()` — the thing that
actually connects — resolves via `dns.lookup`, which uses the **OS resolver**
(`getaddrinfo`, honouring `/etc/hosts` and NSS configuration). These are two
different resolution paths that are not guaranteed to agree. A guard built on
one path is validating a different lookup than the one the connection will
actually use.

## Why mocked tests don't catch it

A test suite that mocks `dns.resolve4`/`resolve6` to return controlled values
proves the *blocking logic* works — the private-IP-range check, the redirect
re-validation, the IPv6 parsing. It cannot catch a resolver-choice mismatch,
because the mock is written against the same function the code calls. The
test and the implementation agree with each other by construction; neither is
checked against what a real connection does.

This one was only caught by running the actual code against real network
traffic — `dns.resolve4('example.com')` failed outright in the sandbox this
was built in (`ECONNREFUSED`, no direct DNS-protocol access), while
`dns.lookup('example.com')` succeeded immediately. A guard that fails on a
domain as canonical as `example.com` is impossible to miss once you run it
for real — and impossible to see if you never do.

## The fix

Use `dns.lookup(hostname, { all: true })` instead of `resolve4`/`resolve6`:

```js
const results = await dns.lookup(hostname, { all: true });
const addresses = results.map(r => r.address);
```

This is strictly better on two axes, not just a workaround for one
environment:
- It's the **same resolution path `fetch()`/undici uses internally** to
  connect, so the guard validates what will actually happen.
- `{ all: true }` still returns every address the resolver has, so a
  multi-answer response hiding a private IP behind a public-looking first
  result is still caught — the protection doesn't regress by switching APIs.

## The broader lesson

**Test SSRF/security-boundary code against real network calls at least once,
not only against mocks.** Mocks validate internal logic; they cannot reveal
that the logic is checking the wrong thing entirely. For a guard whose whole
job is "does this match what will really happen at connect time," a live run
against a known-good and a known-bad target (a public domain, `127.0.0.1`, the
cloud metadata address `169.254.169.254`) is cheap and catches a class of bug
mocks structurally cannot.

Related: `run-scripts-from-workspace-root.md` — same family of "the mock
agrees with itself, reality doesn't" failure.

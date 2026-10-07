# Connecting Search Console (service account) — the repeatable setup

**Why bother:** GSC is the only source of *actually measured* numbers in this
workspace. Impressions, clicks, CTR and average position, per query and per
page, free and exact. Everything else we use — volume, difficulty, competitor
traffic — is modeled. This is what lets a client report carry a number with a
source instead of a hedge.

`gsc_checker.py` authenticates with a **service account only**. Its docstring
mentions OAuth2, but `build_service()` calls
`service_account.Credentials.from_service_account_file`, so an OAuth client
JSON will fail. Do not spend time on the OAuth flow.

Service account is also the right choice here regardless: no browser step, no
refresh token to expire, and it works unattended in a script.

---

## One-time, per Google account

### 1. Google Cloud side

1. [Google Cloud Console](https://console.cloud.google.com/) → create a project
   (or reuse one). Note the project id.
2. **APIs & Services → Library** → enable **Google Search Console API**
   (`searchconsole.googleapis.com`). There are similarly-named entries; this is
   the one.
3. **IAM & Admin → Service Accounts → Create service account.** Give it a name.
   **Skip the "grant this service account access to the project" step** — GCP
   IAM roles are irrelevant here. The permission that matters is granted inside
   Search Console, not in Cloud.
4. Open the new service account → **Keys → Add key → Create new key → JSON**.
   A file downloads.
5. Copy the service account **email**, which looks like
   `something@project-id.iam.gserviceaccount.com`. You need it in step 7.

### 2. Search Console side

6. Open the property in [Search Console](https://search.google.com/search-console).
7. **Settings → Users and permissions → Add user** → paste the service account
   email → permission **Full**.

   *Restricted* is enough to read performance data, but blocks parts of the URL
   Inspection API. Use Full unless the client objects.

### 3. Workspace side

8. Move the downloaded JSON into `.secrets/` (already gitignored — the
   directory is ignored wholesale, so the filename does not matter).
9. Set the path in `.env`:

   ```
   GSC_CREDENTIALS_PATH=.secrets/<the-file>.json
   ```

10. Test, from the workspace root:

    ```bash
    PYTHONIOENCODING=utf-8 python skills/seo/scripts/gsc_checker.py sc-domain:example.com --days 28
    ```

---

## Gotchas that cost real time

- **Use a Domain property, and pass it as `sc-domain:example.com`.** The
  script's `--help` shows `https://example.com`, which is the *URL-prefix*
  form. A URL-prefix property silently reports only that exact
  scheme+host — miss `www` or `https` and the data looks catastrophically wrong
  rather than erroring. A domain property covers every subdomain and protocol.
- **A domain property is also a security check.** It reports subdomains you did
  not know were indexed. Scan the Pages tab for stray hostnames on every first
  pull — see `gsc-domain-property-reveals-hacked-subdomains.md`. This has found
  a live compromise before.
- **Run from the workspace root.** `env_loader` looks for `.env` in the cwd; from
  anywhere else `GSC_CREDENTIALS_PATH` silently resolves empty. Same trap as
  `run-scripts-from-workspace-root.md`.
- **`PYTHONIOENCODING=utf-8` on Windows.** The report printer emits emoji and
  crashes mid-run without it.
- **Data is delayed ~2-3 days** and the API caps at 16 months of history. A
  "missing" recent week is normal, not a bug.
- **Permission propagation is not instant.** A 403 immediately after adding the
  service account usually resolves within a few minutes.
- **Each brand is a separate property**, but they can share one service account
  — add the same email as a user on each property. Do **not** create a
  service account per client; do add each property separately, and keep the
  brand→property mapping in `brands/<brand>/brief.md`.

## Dependencies

Installed 2026-09-06: `google-api-python-client` 2.200.0, `google-auth` 2.57.1,
`google-auth-oauthlib` 1.4.1.

```bash
pip install google-api-python-client google-auth-oauthlib
```

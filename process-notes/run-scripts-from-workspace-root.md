# Run every `seo` script from the workspace root, or `.env` never loads

**The rule:** `cd` to the workspace root and call the script by its full path.
Never `cd` into the `scripts/` directory first.

```bash
# ✅ correct — .env is found
cd "<workspace root>"
export PYTHONIOENCODING=utf-8
python "<workspace root>/skills/seo/scripts/pagespeed.py" --strategy mobile https://example.com

# ❌ wrong — .env is invisible, every key silently missing
cd "<workspace root>/skills/seo/scripts"
python pagespeed.py https://example.com
```

## Why

`env_loader.py` searches for `.env` in exactly three places, in order:

1. `Path.cwd()/.env` — **the directory you invoked the script from**
2. `SKILL_DIR/.env` — i.e. `~/.claude/skills/seo/.env`
3. `$HOME/.agentic-seo/.env`

The workspace `.env` lives at the **workspace root**, which matches only
candidate 1. Locations 2 and 3 do not exist in this setup. So the moment you
`cd` into `scripts/`, the loader finds nothing and every key comes back empty.

## The failure is silent and misleading

`pagespeed.py` without a key does not say "no key found". It says:

```
[pagespeed] Rate limited by API. Retrying in 3s...
Error: Rate limited by Google API. Wait a few minutes or add an API key.
```

That message describes a *quota* problem and invites you to wait it out.
Waiting does nothing, because the anonymous quota is per-IP and effectively
zero. Retrying and concluding "PSI is unavailable today" is the trap — the key
was present in `.env` the whole time.

**Cost when this happened:** an entire audit was written with Core Web Vitals in
the "Not measured" column, and a Critical finding was drafted on the inference
that a 10 MB hero video must be destroying LCP. Re-run correctly, the site
scored **99/100 on mobile with every CWV passing**. The finding had to be
rewritten and downgraded in a file that had already been presented.

## Check before you conclude a key is missing

```bash
cd "<workspace root>"
python -c "
import sys; sys.path.insert(0,'<workspace root>/skills/seo/scripts')
from env_loader import load_env, get_env
print('loaded from:', load_env() or 'NOTHING')
k = get_env('PAGESPEED_API_KEY','GOOGLE_API_KEY')
print('key:', (k[:4]+'…'+str(len(k))+' chars') if k else 'NONE')
"
```

`loaded from: NOTHING` means you are in the wrong directory — not that the key
is absent.

## Make it not happen again

Drop a copy of `.env` at `$HOME/.agentic-seo/.env` (candidate 3). That path is
checked regardless of working directory, so the key resolves from anywhere.
Keep it out of version control.

## The general lesson

A tool's error message describes the symptom it can see, not the cause. "Rate
limited" was true — the request really was unauthenticated and really was
throttled — but the *reason* was three directories up. When a script reports a
quota, credential or network problem, verify the input actually reached it
before writing the limitation into a deliverable.

Related: `.env` currently defines `PAGESPEED_API_KEY` (set),
`GSC_CREDENTIALS_PATH` (empty) and `GOOGLE_KG_API_KEY` (empty). The latter two
will fail the same silent way when a playbook needs them.

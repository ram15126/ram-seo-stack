# Run the verification command, and check it measures the claim

## What happened
An audit reported that a JS-rendered site serves AI crawlers "7 words of body
content", and published this as the reader's verification step:

```bash
curl -s -A "...GPTBot..." https://example.com/ | wc -w
```

The finding was correct. The command was not: `wc -w` counts the entire HTML
response, `<head>` markup included, so it returned **123** — a number that
appears to contradict the finding it was supposed to prove.

Caught only because every published command was re-run before shipping.

## The rule
A verification step must reproduce *the specific number in the finding*, not a
loosely related one. Running the command is necessary but not sufficient — read
its output and confirm it matches what the finding claims.

## The corrected form
```bash
curl -s -A "...GPTBot..." https://example.com/ \
  | sed -n '/<body/,/<\/body>/p' | sed 's/<[^>]*>//g' | tr -s ' \n' ' ' | wc -w
```

## Why it matters
A reader who runs a published command and gets a contradicting number does not
conclude the command was sloppy. They conclude the finding was invented — and
then they distrust the rest of the report.

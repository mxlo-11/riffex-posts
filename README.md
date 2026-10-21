# riffex-posts

Images, generator and auto poster for @riffexapp's daily Instagram post.

- `kit/RULES.md`: what to post each day, the look, caption rules, banned words. The daily task reads it every run.
- `kit/render2.py` + `kit/brand/wordmark.svg`: turns a JSON spec into 1080x1080 slides (examples in `kit/examples/`). Setup: `cd kit && npm i` (fonts + playwright), then `python3 render2.py spec.json out/`. Spec image paths are relative to `kit/` (put downloads in `kit/assets/`, which is git ignored).
- `POSTED_LOG.md`: every post so far, with sources. Append one line per post.
- `queue/YYYY-MM-DD/`: JPEG slides `1.jpg, 2.jpg, ...` plus `caption.txt`. Pushing a folder starts `.github/workflows/post.yml`, which posts past days right away and today's from 5 PM New York time, then writes `posted.json`.
- The Instagram token lives only in the repo secret `IG_TOKEN` (Settings > Secrets and variables > Actions). It lasts 60 days; regenerate it on the Riffex Meta app (Use cases > Instagram API > API setup with Instagram login > Generate token) and replace the secret.
- Manual test: Actions > Post to Instagram > Run workflow, mode `check` (reads the profile, posts nothing).

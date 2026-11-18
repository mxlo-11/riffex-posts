# riffex-posts

Images, generator and auto poster for @riffexapp's daily Instagram post.

- `kit/RULES.md`: what to post each day, the look, words, tagging, and account safety rules. The daily task reads it every run.
- `kit/render4.py` (v4, the Riffex Home screen look, 1080x1440 carousels) + `kit/brand/wordmark.svg` + `kit/brand/app_home.jpg`: turns a JSON spec into slides (one of each slide type in `kit/examples/types.json`). Setup: `cd kit && npm i` (fonts + playwright), then `python3 render4.py spec.json out/`. Spec image paths are relative to `kit/` (downloads go in `kit/assets/`, git ignored). `render2.py` is the old square look, kept for reference only.
- `POSTED_LOG.md`: every post so far, with sources. Append one line per post.
- `queue/YYYY-MM-DD/`: JPEG slides `1.jpg, 2.jpg, ...`, `caption.txt`, optional `tags.json`. Pushing a folder starts `.github/workflows/post.yml`, which posts today's folder from 5 PM New York time through Instagram's official API (one post per run, never more), then writes `posted.json`.
- `preview/YYYY-MM-DD/`: same layout, never posted. Used to check a post before it goes live.
- The Instagram token lives only in the repo secret `IG_TOKEN` (Settings > Secrets and variables > Actions). It lasts 60 days; regenerate it on the Riffex Meta app (Use cases > Instagram API > API setup with Instagram login > Generate token) and replace the secret.
- Manual test: Actions > Post to Instagram > Run workflow, mode `check` (reads the profile, posts nothing).

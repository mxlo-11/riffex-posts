# riffex-posts

Images and the auto-poster for @riffexapp's daily Instagram post.

- The daily Claude task renders the post and commits it to `queue/YYYY-MM-DD/` (JPEG slides `1.jpg`, `2.jpg`, ... plus `caption.txt`).
- `.github/workflows/post.yml` publishes today's folder at 5 PM New York time through the Instagram API, then commits `posted.json`.
- The Instagram token lives only in the repo secret `IG_TOKEN` (Settings > Secrets and variables > Actions). It lasts 60 days; regenerate it on the Riffex Meta app (Use cases > Instagram API > API setup with Instagram login > Generate token) and replace the secret.
- Manual test: Actions > Post to Instagram > Run workflow, mode `check` (reads the profile, posts nothing).

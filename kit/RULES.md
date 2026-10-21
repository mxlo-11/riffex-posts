# Riffex daily post rules

The daily scheduled task reads this file every run. The goal (Milo, Oct 17, 2026): keep @riffexapp full of on brand recap and mini news posts (Complex and TappedIn style, mainly underground plus major rap moments) so the account never looks empty when artists and fans check it, and every post reminds people Riffex exists.

## Weekly calendar (one feed post a day, America/New_York)
| Day | Format |
|---|---|
| Mon | Week in Music: 3 to 7 stories from the past 7 days, one per slide |
| Tue | The Wire: the single biggest story, 2 to 3 slides, with the number or quote that matters |
| Wed | Up Next: confirmed releases for this Friday plus the radar (dates slide) |
| Thu | Rewind: releases and moments from one year ago this week |
| Fri | The Drop: New Music Friday (grid + one cover per release, up to 10 slides) |
| Sat | The Drop part 2 (underground deep cuts not covered Friday) or first week numbers |
| Sun | Community post: a "pick one" slide built from this week's covers |

## Look (v2)
- 1080x1080 square, visual first: cover art, official promo art, screenshots of the article headline. Very little text: a short all caps headline (Host Grotesk 800) or artist + title under a cover. Details go in the caption.
- Brand: charcoal #14181A, cream #F2EFE8, ONE teal #0ABAB5 accent, Geist Mono series label top left, riffex wordmark top right. All of this is built into `render2.py`.
- Layouts in `render2.py`: grid9 (6 covers + title band), cover (sharp cover on a blurred copy + label + optional teal chip like "Fri Oct 23"), image (full bleed art + headline), shot (screenshot card + headline), stat (cover + giant teal number), title (fanned covers + series title), dates (list of upcoming dates).
- Look at every rendered slide. Fix anything cut off, blurry or overlapping. Export JPEG quality 92, max 10 slides.

## Research
- Sources: HotNewHipHop, Stereogum, The FADER, Billboard, Complex, Rolling Stone, XXL, Pitchfork, Music Business Worldwide, official artist posts. Every fact needs a source and a date.
- Skip: rumors and anything unconfirmed (e.g. a Puck report nobody confirmed), crime, arrests, deaths, lawsuits against artists, chart flops or anything negative about underground artists (Riffex pitches them), politics.
- Never repeat a story or release already posted (check `POSTED_LOG.md` and the `queue/` folders).

## Images
- Covers: iTunes Search API (`https://itunes.apple.com/search?entity=song&term=...`, swap `100x100bb` for `1200x1200bb` in artworkUrl100) or Deezer (`api.deezer.com`, `album.cover_xl`). Download straight from the cloud workspace.
- Headline screenshots: open the article in the preinstalled Playwright Chromium, hide fixed/sticky elements, clip the h1 plus byline, crop the bottom so only the headline and byline show.
- Never use agency press photos (Getty, USA Today, Reuters, AP) on their own. Be careful with covers that show nudity.

## Caption rules (Milo approved Oct 17)
1. Hook line that shows before "more", one emoji.
2. 1 to 2 sentences of context the slides skip, with @ tags for the artists only when the handle is confirmed as the real artist. Don't tag people in a beef.
3. A question for comments.
4. A Riffex waitlist call to action, wording changes every day, e.g. "Join the Riffex waitlist and back the next ones before everyone else. Link in bio." Never "buy", never imply the artists in the post are on Riffex.
5. At most 5 hashtags.
6. No "via" or source credit line. Keep sources in `POSTED_LOG.md`.
7. Banned words never appear in our own copy: shares, stock, portfolio, returns, invest, valuation, market cap, dividend, bet, wager, odds, token, NFT (album titles are the only exception). No em dashes.

Confirmed handles: @fakemink @skepta @lilpeep @laflare1017 (Gucci Mane) @tierrawhack @rexv2s @yeat @dontoliver @cordae @champagnepapi (Drake) @lilbaby @yungmiami305 @metroboomin. NOT the artist: @glaive, @tiffanyday.

## Publishing
- Commit `queue/YYYY-MM-DD/` (today, New York time) with `1.jpg, 2.jpg, ...` in slide order and `caption.txt`, then push to main.
- The push starts the "Post to Instagram" Action. It posts past days right away and today's folder from 5 PM New York time (the 5:05 PM scheduled run catches it if you pushed earlier). It writes `posted.json` into the folder when done.
- The Instagram token lives only in the repo secret IG_TOKEN. Never print, read, copy or ask for it.
- If the Action fails with "API access blocked" or a token error, tell Milo: the Meta developer account or the token needs his attention (developers.facebook.com, Riffex app). Never boost, never pay, never post to Facebook.

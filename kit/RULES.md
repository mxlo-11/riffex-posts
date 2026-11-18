# Riffex daily post rules (v4, Nov 18, 2026)

The daily scheduled task reads this file every run. Goal (Milo): keep @riffexapp full of on brand music news and culture posts so the account never looks empty, put small and rising artists in front of people next to the big names, and remind people Riffex exists. Posts are content first, not app ads.

## Weekly calendar (one post a day, America/New_York). Every post is a carousel (2 to 10 slides).
| Day | Format | Main slide types |
|---|---|---|
| Mon | The week in music: 3 to 5 stories from the past 7 days | ranked, then one slide per story (hero or number) |
| Tue | The Wire: the one story that matters most | hero, then number or ranked for the details |
| Wed | Up next: confirmed releases for this Friday and the next few weeks | calendar, then hero for the biggest one |
| Thu | Rewind: releases and moments from one year ago this week | carousel (one album per slide) |
| Fri | The Drop: New Music Friday | carousel (one album per slide, up to 10) |
| Sat | Rising: small artists worth knowing (underground drops from the week, deep cuts) | carousel, then question |
| Sun | Pick one: a vote built from this week's covers, then a fan question | pick, then question |
About once a week, swap a slot for "Inside Riffex" (inside type, then one product slide) or a "Live" moment (live type) when a real one happened. Vary the slide mix so two days in a row never look the same.

## Artists: big AND small, every post
- Riffex is about finding artists early, so every post includes at least one underground or rising artist, and across the week about half the artists featured should be small or rising. Pair them with the big names people already search for.
- Sources for small and rising artists: The FADER, Pigeons & Planes, Lyrical Lemonade, Our Generation Music, Kerrang/Alternative Press for rock, SoundCloud and Spotify discovery charts (Fresh Finds, Radar), Bandcamp Daily, plus the artists' own posts. Big names: HotNewHipHop, Complex, Billboard, Rolling Stone, XXL, Pitchfork, Stereogum, Music Business Worldwide.
- Every fact needs a source and a date (keep them in POSTED_LOG.md, not in the caption).
- Skip: rumors, crime, arrests, deaths, lawsuits, beef, politics, and anything negative about small artists.
- Never repeat a story or release already posted (check POSTED_LOG.md and queue/).

## The look (v4, render4.py): the Riffex Home screen
- 1080x1440 (3:4). Header on every slide: riffex wordmark left, category pill and the pick shaped slide counter right. Big bold Host Grotesk titles, rounded cover cards, blue (#3DD6CD) kicker lines, a full width blue pill at the bottom with the hook. Near black background. All of this is built into render4.py; never hand edit colors or fonts.
- Slide types: carousel, calendar, ranked, hero, pick, number, question, live, inside. Examples of each: kit/examples/types.json.
- Carousels must read like a real scroll: in a carousel post, give every slide the same items list and set "index" to 0, 1, 2... First slide shows the card left with the next one peeking right; the last shows the card right with the previous one peeking left. render4.py does this from "index".
- Look at every rendered slide. Fix anything cut off, overlapping, blurry or too long. Export JPEG quality 92.

## Words (Milo, Nov 18): plain and natural
- Write like a fan talking to a friend, not a label or a press release. Short, specific, warm. Bad: "Out on Warp", "Out the same day as Stardust". Good: "His first album since getting sober", "Same Friday, totally different vibe".
- Titles are short (2 to 6 words). Kicker lines are 2 to 4 words ("New today", "A year ago this week"). Each item line is one plain sentence, under 45 characters.
- The bottom pill is a question or nudge people actually answer ("What are you playing first?", "Who found them first?").
- No em dashes or hyphens. Banned words in our own copy: shares, stock, portfolio, returns, invest, valuation, market cap, dividend, bet, wager, odds, profit, gains, token, NFT (album titles are the only exception).

## Images
- Covers: Deezer (api.deezer.com/search/album, cover_xl) or iTunes Search (swap 100x100bb for 1200x1200bb). Official single or album art only.
- Headline screenshots of articles are fine on a hero or ranked slide; crop to the headline and byline.
- Never use agency or wire press photos (Getty, AP, Reuters, USA Today). Never AI generated people. Careful with covers that show nudity.
- Never put a real artist next to Riff prices or credits, and never imply any real artist is on Riffex or endorses it.

## Tagging artists (tags.json)
- Tag the artists featured, on the slide that shows them: queue/<date>/tags.json like {"2": ["handle"], "3": ["handle2"]} (slide numbers start at 1).
- Only the artist's real, verified account (check the profile: verified badge or linked from their official site or Spotify). If you can't confirm the handle, don't tag.
- Max 5 tags per post. Never tag the same small artist more than once every 14 days (check POSTED_LOG.md). Never tag in negative or beef stories.
- Also @mention the main artist once in the caption, only with a confirmed handle.
Confirmed handles so far: @fakemink @skepta @lilpeep @laflare1017 (Gucci Mane) @tierrawhack @rexv2s @yeat @dontoliver @cordae @champagnepapi (Drake) @lilbaby @yungmiami305 @metroboomin. NOT the artist: @glaive, @tiffanyday.

## Caption
1. A hook line that shows before "more", at most one emoji.
2. One or two plain sentences of context the slides skip.
3. A question for the comments.
4. A call to action that changes every day: the Riffex beta (link in bio) or the waitlist at riffex.app. Never "buy", never imply the artists in the post are on Riffex.
5. At most 5 hashtags. No source credits in the caption.

## Publishing and account safety (most important)
- Commit queue/YYYY-MM-DD/ (today, New York time): 1.jpg, 2.jpg ... in slide order, caption.txt, and tags.json if tagging. Then push to main. The "Post to Instagram" Action posts it from 5 PM New York time through Instagram's official publishing API.
- One post per day, never more. If today's folder already exists or POSTED_LOG.md has today, stop.
- The only thing that touches Instagram is that Action. Never open Instagram in a browser, never log in, never DM, comment, like, follow, unfollow, reply, or change settings. Never boost or pay. Never post to Facebook.
- The token lives only in the repo secret IG_TOKEN. Never print, read, copy or ask for it.
- If the Action reports any error, limit, block, "API access blocked", or token problem: stop, queue nothing new, and tell Milo exactly what it said. Do not retry over and over.

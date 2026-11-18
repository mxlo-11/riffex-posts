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
- 1080x1440 (3:4). Header on every slide: riffex wordmark left, category pill and the pick shaped slide counter right. Big bold Host Grotesk titles, rounded cover cards, blue (#3DD6CD) kicker lines, a full width blue pill at the bottom with the hook. Background: a blurred, glowing color wash made from the slide's main artwork (like the Spotify player), fading to near black at the bottom; frosted glass panels and pills. render4.py picks the image automatically (the card in focus, the hero image, the first row or item); set "bg" on a slide to choose a different one. All of this is built into render4.py; never hand edit colors or fonts.
- Slide types: carousel, calendar, ranked, hero, pick, number, question, live, inside. Examples of each: kit/examples/types.json.
- Carousels must read like a real scroll: in a carousel post, give every slide the same items list and set "index" to 0, 1, 2... First slide shows the card left with the next one peeking right; the last shows the card right with the previous one peeking left. render4.py does this from "index".
- Look at every rendered slide. Fix anything cut off, overlapping, blurry or too long. Export JPEG quality 92.

## Words (Milo, Nov 18): plain and natural
- Write like a fan talking to a friend, not a label or a press release. Short, specific, warm.
- Titles are short (2 to 6 words). Kicker lines are 2 to 4 words ("This Friday", "A year ago this week").
- Lines under a release (calendar rows, carousel cards) are app style details, not sentences: "meta" like "Album · 11 songs" or "Single · prod. Conductor Williams", plus "play" with the song that's already out (shows as a play chip). The design says what it means; never write it out ("X is the first taste", "11 songs, X is already out").
- A sentence (hero "line", number "sub") only when it gives a fan a real reason to care: who's on it, who the artist is if they're small, a big moment around it (a tour, SNL, a first album in years). Never trivia about how it was made ("made alone in her home studio", "he produced all of it himself"), and never a flat fact the slide already shows.
  Bad: "He recorded and produced all of it himself." Good: "Three Wu Tang legends and, somehow, the Goo Goo Dolls." / "The voice behind Computer Magic, back with 12 songs of cosmic synth pop." / "The first song off Nitrous. He plays SNL the night after it drops."
- The bottom pill is a question people actually answer and fits that slide ("Which feature are you skipping to?", "Who remembers Computer Magic?"). Don't repeat the caption's question word for word.
- No em dashes or hyphens (write "Wu Tang"). Banned words in our own copy: shares, stock, portfolio, returns, invest, valuation, market cap, dividend, bet, wager, odds, profit, gains, token, NFT (album titles are the only exception).

## Structure
- After an overview slide (calendar, ranked), give each item its own slide in the same order as the overview, small artists included. Never skip one.
- Show full titles: render4.py wraps long album titles; never shorten a title with "…" yourself.
- On a number slide, "imgs" takes two different images; with one image it shows one card. Never use the same cover twice on a slide.

## Images
- Covers: Deezer (api.deezer.com/search/album, cover_xl) or iTunes Search (swap 100x100bb for 1200x1200bb; upcoming albums are often on iTunes before Deezer). Official single or album art only.
- Label art correctly. If an album's cover isn't out yet, use the lead single's art and make that slide about the single by name (headline = the song, kicker = when the album drops). Never put a single's cover under the album's name as if it were the album art.
- Headline screenshots of articles are fine on a hero or ranked slide; crop to the headline and byline.
- Never use agency or wire press photos (Getty, AP, Reuters, USA Today). Never AI generated people. Careful with covers that show nudity.
- Never put a real artist next to Riff prices or credits, and never imply any real artist is on Riffex or endorses it.

## Tagging artists (tags.json)
- Tag the artists featured, on the slide that shows them: queue/<date>/tags.json like {"2": ["handle"], "3": ["handle2"]} (slide numbers start at 1).
- Only the artist's real account: confirm it from a link on their official site, Bandcamp, Linktree or label page. If you can't confirm the handle, don't tag.
- Small artists matter most here (a tag from us means more to them), so always try to confirm and tag every small artist in the post.
- Max 5 tags per post. Never tag the same small artist more than once every 14 days (check POSTED_LOG.md). Never tag in negative or beef stories.
- Also @mention the main artist once in the caption, only with a confirmed handle.
Confirmed handles so far: @whoisconway (Conway The Machine) @danz_cm (Danz CM) @fakemink @skepta @lilpeep @laflare1017 (Gucci Mane) @tierrawhack @rexv2s @yeat @dontoliver @cordae @champagnepapi (Drake) @lilbaby @yungmiami305 @metroboomin. NOT the artist: @glaive, @tiffanyday.

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

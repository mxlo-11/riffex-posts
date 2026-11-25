# Riffex daily post rules (v4.1, Nov 24, 2026)

The daily scheduled task reads this file every run. Goal (Milo): keep @riffexapp full of on brand music news and culture posts so the account never looks empty, put small and rising artists in front of people next to the big names, and remind people Riffex exists. Posts are content first, not app ads.

## Formats (one post a day, America/New_York). Every post is a carousel (2 to 10 slides).
Milo, Nov 24: the format is NOT fixed by weekday. Research first, then pick whichever format below fits what you found best that day: one huge story is a Wire, several medium ones are a week in music, a stack of announced dates is Up next, a strong batch of underground drops is Rising, and so on. The one fixed day is Friday: always The Drop (New Music Friday release recap). Don't use the same format two days in a row (check POSTED_LOG.md) unless the news really calls for it, and keep a healthy mix across the week. The weekday column below is only a fallback for slow news days.
| Fallback day | Format | Main slide types |
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
- Label art correctly. If an upcoming album's cover isn't out yet, the slide is still about the album (headline = the album, kicker = its date) and you may use the lead single's art only if the slide also shows that single as a play chip with "out now" ("play": "Party With The Boys · out now"), so the image is explained. Never present a song that's already out as upcoming.
- Headline screenshots of articles are fine on a hero or ranked slide; crop to the headline and byline.
- Never use agency or wire press photos (Getty, AP, Reuters, USA Today). Never AI generated people. Careful with covers that show nudity.
- Never put a real artist next to Riff prices or credits, and never imply any real artist is on Riffex or endorses it.

## Tagging artists (tags.json)
- Tag every featured artist on the slide that shows them, small and rising artists first: queue/<date>/tags.json like {"2": [{"handle": "danz_cm", "artist": "Danz CM"}], "3": [{"handle": "whoisconway", "artist": "Conway The Machine"}]} (slide numbers start at 1). Always include the artist name: the posting script uses it to check the account.
- The artist does NOT need a verified badge (Milo, Nov 21). An account counts as theirs if it names them or links their music (SoundCloud, Spotify, Bandcamp, Apple Music, YouTube, Linktree). Find the handle with the best evidence you can reach, in this order: the confirmed list below; an instagram.com link on the artist's own pages (SoundCloud, Spotify, Bandcamp, Linktree, official site, label page), including links visible in search results for those pages; MusicBrainz artist URL relations (musicbrainz.org/ws/2/artist/<mbid> with inc url-rels and fmt json); Wikidata (property P2003, Instagram username); a news article that links the account. Write the source in checks.md. If two different accounts look plausible, leave that artist untagged.
- Never skip tagging just because artist sites are blocked from your network: use the other sources above. Right before posting, scripts/post.py double checks each handle with Instagram's own API: it keeps a tag when the account names the artist or links their music, drops it when the account clearly isn't them, drops handles Instagram doesn't recognize (one at a time, so the others stay), and never lets a bad tag stop the post. What it kept and dropped is in queue/<date>/posted.json under "tags".
- Max 5 tags per post. Never tag the same small artist more than once every 14 days (check POSTED_LOG.md). Never tag in negative or beef stories.
- @mention artists in the caption only with a handle from the confirmed list or one whose source is an official link (a wrong @mention can't be dropped automatically). The photo tags are what notify the artist.
- At the start of each run, add any handle the last post actually tagged (posted.json "tags" "tagged") to the confirmed list below.
Confirmed handles so far: @whoisconway (Conway The Machine) @danz_cm (Danz CM) @fakemink @skepta @lilpeep @laflare1017 (Gucci Mane) @tierrawhack @rexv2s @yeat @dontoliver @cordae @champagnepapi (Drake) @lilbaby @yungmiami305 @metroboomin @heisrema (Rema) @krissycelessss (Krissy Celess) @thehoodbrat (Hood Brat) @kodakblack (Kodak Black). NOT the artist: @glaive, @tiffanyday.

## Caption
1. A hook line that shows before "more", at most one emoji.
2. One or two plain sentences of context the slides skip.
3. A question for the comments.
4. A call to action that changes every day: the Riffex beta (link in bio) or the waitlist at riffex.app. Never "buy", never imply the artists in the post are on Riffex.
5. At most 5 hashtags. No source credits in the caption.

## Before you commit: the self check (Milo, Nov 18). Do this every run, in writing.
Write queue/<date>/checks.md (post.py ignores it) with these sections, and fix anything that fails before you push. If something can't be confirmed, cut it from the post instead of guessing.
1. Facts table: every date, number, name, feature and claim on the slides and in the caption, each with two sources (or one official source: the artist, label, Apple Music/iTunes or Deezer listing) and the date of each source. Release dates must be officially announced (artist, label, press release, or a streaming listing with that date). "Hinted", "rumored", "85% done" or "coming soon" is not a date: leave the date off or skip the item.
2. Out or upcoming: for every song and album, mark OUT (with its release date) or UPCOMING (with its date). Up next and calendar posts may only list UPCOMING releases as the subject; an OUT song can appear only as a play chip.
3. Tense and time words, checked against the day it posts (5 PM New York time): "this Friday", "next week", "tonight", "last week" must be true on that day.
4. Read every line as a stranger seeing only that slide. Each "it", "he", "she", "this" must point to exactly one thing (bad: "The first song off Nitrous. He plays SNL the night after it drops", where "it" could be the song). Name the thing instead when in doubt.
5. Words: no trivia or flat facts, nothing the slide already shows, no em dashes or hyphens, no banned words, every bottom pill is a real question for that slide, and it doesn't repeat the caption's question.
6. Art: each image is the official art for exactly what the slide names (or a single shown with an "out now" play chip, see Images). No image is used twice on one slide.
7. Structure: every overview item has its own slide, in the same order; at least one small or rising artist; full titles, nothing cut off or overlapping (look at every rendered slide).
8. Tags: tags.json lists every featured artist you found a handle for (handle, artist name, source in checks.md), max 5, small artists not tagged in the last 14 days, and caption @mentions only from the confirmed list or an official link.

## Publishing and account safety (most important)
- Commit queue/YYYY-MM-DD/ (today, New York time): 1.jpg, 2.jpg ... in slide order, caption.txt, and tags.json if tagging. Then push to main. The "Post to Instagram" Action posts it from 5 PM New York time through Instagram's official publishing API.
- One post per day, never more. If today's folder already exists or POSTED_LOG.md has today, stop.
- The only thing that touches Instagram is that Action. Never open Instagram in a browser, never log in, never DM, comment, like, follow, unfollow, reply, or change settings. Never boost or pay. Never post to Facebook.
- The token lives only in the repo secret IG_TOKEN. Never print, read, copy or ask for it.
- If the Action reports any error, limit, block, "API access blocked", or token problem: stop, queue nothing new, and tell Milo exactly what it said. Do not retry over and over.

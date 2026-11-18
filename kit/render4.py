#!/usr/bin/env python3
"""Riffex IG posts v4 (Nov 18, 2026): the Home screen look with a blurred glow background from each slide's artwork. 1080x1440 (3:4), brand blue #3DD6CD.
Every post is a carousel. JSON spec -> PNG slides. Image paths are relative to kit/.
Slide types: carousel, calendar, ranked, hero, pick, number, question, live, inside
Usage: python3 render4.py spec.json out_dir   (writes <id>_01.png ... and <id>_caption.txt)
See kit/examples/types.json for one of each.
"""
import json, sys, html, pathlib, asyncio, os
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent
F = ROOT / "node_modules/@fontsource"
WM = (ROOT / "brand/wordmark.svg").read_text().replace('width="1344" height="600"', 'width="98" height="44"')
PICK = 'M50 96 C38 90 8 52 8 30 C8 12 26 4 50 4 C74 4 92 12 92 30 C92 52 62 90 50 96 Z'
ARROW = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#090B0C" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PLAY = '<svg width="22" height="22" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="#F2EFE8"/></svg>'
def e(s): return html.escape(str(s or ""))
def h(s): return e(s).replace("&lt;br&gt;", "<br>")          # titles may use <br> for a line break
def u(p): return f"file://{ROOT / p}"

CSS = f"""
@font-face{{font-family:HG;src:url(file://{F}/host-grotesk/files/host-grotesk-latin-400-normal.woff2);font-weight:400}}
@font-face{{font-family:HG;src:url(file://{F}/host-grotesk/files/host-grotesk-latin-500-normal.woff2);font-weight:500}}
@font-face{{font-family:HG;src:url(file://{F}/host-grotesk/files/host-grotesk-latin-600-normal.woff2);font-weight:600}}
@font-face{{font-family:HG;src:url(file://{F}/host-grotesk/files/host-grotesk-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:HG;src:url(file://{F}/host-grotesk/files/host-grotesk-latin-800-normal.woff2);font-weight:800}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1440px;overflow:hidden;background:#08090A;font-family:HG;color:#F2EFE8;-webkit-font-smoothing:antialiased}}
.abs{{position:absolute}}
.pill{{display:inline-flex;align-items:center;gap:12px;height:62px;padding:0 26px;border-radius:999px;background:rgba(255,255,255,.14);backdrop-filter:blur(20px);font-weight:600;font-size:28px}}
.blue{{color:#3DD6CD}} .mute{{color:rgba(242,239,232,.66)}}
.title{{font-weight:800;letter-spacing:-.035em;line-height:1.0}}
.sub{{font-weight:500;font-size:34px;line-height:1.3;color:rgba(242,239,232,.7);text-wrap:pretty}}
.card{{outline:1.5px solid rgba(255,255,255,.10);outline-offset:-1.5px;border-radius:44px;background-size:cover;background-position:center;box-shadow:0 40px 90px rgba(0,0,0,.55)}}
.round{{border-radius:50%;background-size:cover;background-position:center;flex:none;box-shadow:inset 0 0 0 2px rgba(255,255,255,.1)}}
.panel{{background:rgba(10,12,13,.42);border:1.5px solid rgba(255,255,255,.10);border-radius:44px;backdrop-filter:blur(30px)}}
.cta{{position:absolute;left:64px;right:64px;bottom:56px;height:96px;border-radius:999px;display:flex;align-items:center;justify-content:space-between;
      padding:0 14px 0 36px;background:#3DD6CD;color:#090B0C;font-weight:700;font-size:31px}}
.cta span{{width:68px;height:68px;border-radius:50%;background:rgba(9,11,12,.12);display:flex;align-items:center;justify-content:center}}
.chip{{display:inline-flex;align-items:center;height:48px;padding:0 20px;border-radius:999px;background:rgba(255,255,255,.14);font-weight:600;font-size:24px}}
.grain{{position:absolute;inset:0;opacity:.06;mix-blend-mode:overlay;pointer-events:none;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>")}}
"""

def heart(full):
    return (f'<svg width="25" height="27" viewBox="0 0 100 100"><path d="{PICK}" '
            + ('fill="#3DD6CD"' if full else 'fill="none" stroke="#F2EFE8" stroke-width="8"') + '/></svg>')
def counter(n, i):
    if n <= 1: return ""
    if n > 6:  # too many picks to fit: show "3/8"
        return f'<span class="pill">{i + 1}/{n}</span>'
    return '<span class="pill" style="padding:0 20px;gap:6px">' + "".join(heart(k == i) for k in range(n)) + '</span>'
def header(cat, n, i):
    return (f'<div class="abs" style="left:64px;top:64px">{WM}</div>'
            f'<div class="abs" style="right:64px;top:54px;display:flex;gap:12px"><span class="pill">{e(cat)}</span>{counter(n, i)}</div>')
def cta(s): return f'<div class="cta">{e(s["ask"])}<span>{ARROW}</span></div>' if s.get("ask") else ""
def stage(img=None):
    if not img:
        return '<div class="abs" style="inset:0;background:radial-gradient(900px 760px at 540px 760px,rgba(255,255,255,.055),transparent 70%),#08090A"></div>'
    # Spotify style: the art, blown up and blurred into a colour wash, darker toward the bottom
    return (f'<div class="abs" style="inset:0;background:#08090A;overflow:hidden">'
            f'<div class="abs" style="left:-260px;top:-300px;width:1600px;height:1600px;background:url({u(img)}) center/cover;filter:blur(110px) saturate(1.7) brightness(.72)"></div>'
            f'<div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(8,9,10,.28) 0%,rgba(8,9,10,.42) 45%,rgba(8,9,10,.78) 82%,rgba(8,9,10,.9) 100%)"></div></div>')
def doc(body): return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}<div class="grain"></div></body></html>'
def title(t, sub=None, top=168, size=100):
    lines = t.count("<br>") + 1
    return (f'<div class="abs title" style="left:64px;right:64px;top:{top}px;font-size:{size}px">{h(t)}</div>'
            + (f'<div class="abs sub" style="left:64px;right:64px;top:{top + size * lines + 18}px">{e(sub)}</div>' if sub else ""))

# ---- carousel: one item in focus, neighbours peek like a real scroll ----
def t_carousel(s, n, i):
    items = s["items"]; k_on = s.get("index", 0); m = len(items); G = 26
    two = "<br>" in s.get("title", "")
    W, top = (590, 450) if two else (640, 400)
    x0 = 64 if k_on == 0 else (1080 - 64 - W if k_on == m - 1 else (1080 - W) // 2)
    it_on = items[k_on]
    cards = ""
    for k, it in enumerate(items):
        x = x0 + (k - k_on) * (W + G)
        if x > 1080 or x + W < 0: continue
        on = k == k_on
        cards += (f'<div class="abs card" style="left:{x}px;top:{top + (0 if on else 30)}px;width:{W}px;height:{W - (0 if on else 60)}px;'
                  f'background-image:url({u(it["img"])});{"" if on else "opacity:.5;"}"></div>')
    it = it_on; tx = max(64, x0); a = it.get("artist", "")
    dots = "".join(f'<span style="width:{36 if k == k_on else 13}px;height:13px;border-radius:7px;background:{"#F2EFE8" if k == k_on else "#3A4144"}"></span>' for k in range(m))
    return doc(stage(it["img"]) + header(s["cat"], n, i) + title(s["title"], s.get("sub")) + cards +
        f'<div class="abs" style="left:{tx}px;right:64px;top:{top + W + 34}px">'
        f'<div class="blue" style="font-weight:600;font-size:28px">{e(it.get("kicker"))}</div>'
        f'<div class="title" style="font-size:{58 if len(a) < 18 else 42}px;margin-top:10px">{e(a)}</div>'
        f'<div class="sub" style="margin-top:8px;font-size:31px">{e(it.get("line"))}</div></div>'
        f'<div class="abs" style="right:64px;top:{top + W + 44}px;display:flex;gap:9px">{dots}</div>' + cta(s))

# ---- calendar: dates, covers, app style details (no sentences) ----
def playchip(song):  # a song that's already out, shown as a play chip like a streaming app
    return (f'<span class="chip" style="height:44px;font-size:22px;gap:10px;margin-top:12px;max-width:100%">'
            f'<svg width="16" height="16" viewBox="0 0 24 24"><path d="M7 4v16l13-8z" fill="#3DD6CD"/></svg>'
            f'<span style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{e(song)}</span></span>') if song else ""
def t_calendar(s, n, i):
    def row(x):
        t = x.get("title", ""); tsz = 30 if len(t) <= 26 else 25   # long album titles wrap to two lines instead of being cut
        return f'''<div style="display:flex;align-items:center;gap:26px;padding:22px 26px">
        <div style="width:96px;text-align:center;flex:none"><div class="mute" style="font-weight:600;font-size:24px">{e(x.get("day"))}</div><div class="title" style="font-size:52px">{e(x.get("date"))}</div></div>
        <div style="width:150px;height:150px;border-radius:26px;background:url({u(x["img"])}) center/cover;flex:none;box-shadow:inset 0 0 0 2px rgba(255,255,255,.1)"></div>
        <div style="min-width:0;flex:1"><div style="font-weight:700;font-size:38px;line-height:1.1">{e(x.get("artist"))}</div>
        <div style="font-weight:500;font-size:{tsz}px;line-height:1.2;margin-top:6px;color:rgba(242,239,232,.86);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">{e(t)}</div>
        {f'<div class="mute" style="font-weight:500;font-size:23px;margin-top:6px">{e(x["meta"])}</div>' if x.get("meta") else ''}
        {playchip(x.get("play"))}
        {f'<div class="blue" style="font-weight:600;font-size:24px;margin-top:8px">{e(x["line"])}</div>' if x.get("line") else ''}</div></div>'''
    r = "".join(row(x) for x in s["rows"][:4])
    return doc(stage(s.get("bg") or s["rows"][0]["img"]) + header(s["cat"], n, i) + title(s["title"], s.get("sub")) +
               f'<div class="abs panel" style="left:64px;right:64px;top:{s.get("top", 520)}px;padding:8px 0">{r}</div>' + cta(s))

# ---- ranked: numbered stories like the Ranks screen (numbered:false for a plain list) ----
def t_ranked(s, n, i):
    num = s.get("numbered", True)
    r = "".join(f'''<div style="display:flex;align-items:center;gap:26px;padding:26px 30px;{'border-top:1.5px solid #1B2225;' if k else ''}">
        {f'<div class="title {"blue" if k == 0 else ""}" style="font-size:54px;width:44px">{s.get("start", 1) + k}</div>' if num else ''}
        <div class="round" style="width:160px;height:160px;background-image:url({u(x["img"])})"></div>
        <div><div style="font-weight:700;font-size:36px;line-height:1.15">{e(x.get("headline"))}</div><div class="mute" style="font-weight:500;font-size:28px;margin-top:8px">{e(x.get("line"))}</div></div></div>'''
        for k, x in enumerate(s["rows"][:4]))
    return doc(stage(s.get("bg") or s["rows"][0]["img"]) + header(s["cat"], n, i) + title(s["title"], s.get("sub")) +
               f'<div class="abs panel" style="left:64px;right:64px;top:{s.get("top", 520)}px">{r}</div>' + cta(s))

# ---- hero: one big story, the Home hero card ----
def t_hero(s, n, i):
    return doc(stage(s["img"]) + header(s["cat"], n, i) +
        f'''<div class="abs card" style="left:64px;right:64px;top:160px;height:1060px;background-image:url({u(s["img"])});background-position:{s.get("pos", "center")}"></div>
        <div class="abs" style="left:64px;right:64px;top:160px;height:1060px;border-radius:44px;background:linear-gradient(180deg,rgba(8,9,10,0) 38%,rgba(8,9,10,.92) 80%)"></div>
        <div class="abs" style="left:112px;right:112px;bottom:{252 if s.get("ask") else 160}px">
          <div style="display:flex;gap:12px;align-items:center">{f'<span class="chip">{e(s["chip"])}</span>' if s.get("chip") else ''}<span class="blue" style="font-weight:600;font-size:28px">{e(s.get("kicker"))}</span></div>
          <div class="title" style="font-size:{s.get("size", 84 if len(s["headline"]) < 16 else 68)}px;margin-top:22px">{h(s["headline"])}</div>
          {f'<div class="sub" style="margin-top:16px;font-size:32px;color:#C9CDCF">{e(s["line"])}</div>' if s.get("line") else ''}
          {f'<div style="margin-top:8px">{playchip(s["play"])}</div>' if s.get("play") else ''}
          {f'<div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:20px">' + "".join(f'<span class="chip" style="height:44px;font-size:22px">{e(f)}</span>' for f in s["feats"]) + '</div>' if s.get("feats") else ''}</div>''' + cta(s))

# ---- pick: the Home "Pick someone early" module, 2 or 3 albums ----
def t_pick(s, n, i):
    its = s["items"][:3]; d = 250 if len(its) == 3 else 320
    def col(x):
        return f'''<div style="flex:1;background:rgba(255,255,255,.07);border-radius:34px;padding:28px 12px 26px;text-align:center">
          <div style="position:relative;width:{d}px;height:{d}px;margin:0 auto"><div class="round" style="width:{d}px;height:{d}px;background-image:url({u(x["img"])})"></div>
          <span style="position:absolute;right:6px;bottom:6px;width:54px;height:54px;border-radius:50%;background:#090B0C;display:flex;align-items:center;justify-content:center">{PLAY}</span></div>
          <div style="font-weight:700;font-size:{30 if len(x.get("artist","")) < 16 else 24}px;margin-top:20px;line-height:1.15">{e(x.get("artist"))}</div>
          <div class="chip" style="margin-top:12px;height:42px;font-size:21px;color:#9AA3A6">{e(x.get("title"))}</div>
          <div class="blue" style="font-weight:700;font-size:30px;margin-top:18px">Pick</div></div>'''
    return doc(stage(s.get("bg") or its[0]["img"]) + header(s["cat"], n, i) + title(s["title"], s.get("sub")) +
        f'''<div class="abs panel" style="left:64px;right:64px;top:{s.get("top", 540)}px;padding:30px">
          <div style="display:flex;justify-content:space-between;align-items:center;padding:0 8px 26px"><span style="font-weight:700;font-size:38px">{e(s.get("panel_title", "Your pick"))}</span><span class="mute" style="font-weight:500;font-size:28px">{e(s.get("panel_note"))}</span></div>
          <div style="display:flex;gap:16px">{"".join(col(x) for x in its)}</div></div>''' + cta(s))

# ---- number: one giant blue number ----
def t_number(s, n, i):
    # two DIFFERENT images fan out ("imgs"); with one image, show one card (never the same cover twice)
    ims = [p for p in (s.get("imgs") or [s["img"]]) if p][:2]
    spots = ((610, 170, 8), (680, 230, -4)) if len(ims) == 2 else ((650, 190, 5),)
    fan = "".join(f'<div class="abs card" style="left:{x}px;top:{y}px;width:{300 if len(ims) == 2 else 340}px;height:{300 if len(ims) == 2 else 340}px;transform:rotate({r}deg);background-image:url({u(p)})"></div>'
                  for p, (x, y, r) in zip(ims, spots))
    c = s.get("card")
    card = (f'''<div class="abs panel" style="left:64px;right:64px;top:1000px;padding:30px 36px;display:flex;gap:28px;align-items:center">
          <div style="width:120px;height:120px;border-radius:24px;background:url({u(c["img"])}) center/cover;flex:none"></div>
          <div><div style="font-weight:700;font-size:32px">{e(c.get("title"))}</div><div class="mute" style="font-weight:500;font-size:27px;margin-top:6px">{e(c.get("line"))}</div></div></div>''' if c else "")
    return doc(stage(s["img"]) + header(s["cat"], n, i) + fan +
        f'''<div class="abs title blue" style="left:52px;top:190px;font-size:{s.get("big_size", 430)}px;letter-spacing:-.07em;line-height:.9">{e(s["big"])}</div>
        <div class="abs" style="left:64px;right:64px;top:640px"><div class="title" style="font-size:84px">{h(s["headline"])}</div>
          {f'<div class="sub" style="margin-top:22px">{e(s["sub"])}</div>' if s.get("sub") else ''}</div>{card}''' + cta(s))

# ---- question: a big fan question with a comment box ----
def t_question(s, n, i):
    tiles = "".join(f'<div class="round" style="width:150px;height:150px;background-image:url({u(x)})"></div>' for x in s.get("imgs", [])[:5])
    return doc(stage(s.get("bg") or (s.get("imgs") or [None])[0]) + header(s["cat"], n, i) +
        f'''<div class="abs title" style="left:64px;right:64px;top:200px;font-size:112px">{h(s["question"])}</div>
        <div class="abs sub" style="left:64px;right:64px;top:{200 + 112 * (s["question"].count("<br>") + 1) + 30}px">{e(s.get("sub"))}</div>
        <div class="abs" style="left:64px;right:64px;top:760px;display:flex;justify-content:space-between">{tiles}</div>
        <div class="abs panel" style="left:64px;right:64px;top:980px;height:150px;border-radius:999px;display:flex;align-items:center;padding:0 44px;gap:22px">
          <span style="height:60px;border-left:4px solid #3DD6CD"></span><span class="mute" style="font-weight:500;font-size:38px">{e(s.get("placeholder", "I was there first for..."))}</span></div>''' + cta(s))

# ---- live: two covers meet for a live moment ----
def t_live(s, n, i):
    a, b = s["imgs"][:2]
    return doc(stage(s.get("bg") or a) + header(s["cat"], n, i) +
        f'''<div class="abs card" style="left:64px;top:190px;width:560px;height:560px;transform:rotate(-5deg);background-image:url({u(a)})"></div>
        <div class="abs card" style="left:456px;top:330px;width:560px;height:560px;transform:rotate(5deg);background-image:url({u(b)})"></div>
        <div class="abs" style="left:64px;right:64px;top:960px">
          <div style="display:flex;gap:12px;align-items:center">{f'<span class="chip">{e(s["chip"])}</span>' if s.get("chip") else ''}<span class="blue" style="font-weight:600;font-size:28px">{e(s.get("kicker"))}</span></div>
          <div class="title" style="font-size:88px;margin-top:20px">{h(s["headline"])}</div></div>''' + cta(s))

# ---- inside: our own post, the phone with the app ----
def t_inside(s, n, i):
    return doc(stage() +
        f'''<div class="abs" style="left:300px;top:560px;width:560px;height:1210px;border-radius:92px;padding:18px;transform:rotate(-6deg);
             background:linear-gradient(135deg,#5b6266,#1c2022 18%,#3a4144 40%,#121516 62%,#4a5155 85%,#1a1d1f);box-shadow:0 60px 120px rgba(0,0,0,.65)">
          <div style="width:100%;height:100%;border-radius:76px;overflow:hidden;background:url({u(s.get("phone_img", "brand/app_home.jpg"))}) top/cover"></div></div>''' +
        header(s["cat"], n, i) + f'<div class="abs title" style="left:64px;right:64px;top:168px;font-size:88px">{h(s["headline"])}</div>' + cta(s))

TYPES = dict(carousel=t_carousel, calendar=t_calendar, ranked=t_ranked, hero=t_hero, pick=t_pick,
             number=t_number, question=t_question, live=t_live, inside=t_inside)

async def main(spec, out):
    spec = json.loads(pathlib.Path(spec).read_text()); out = pathlib.Path(out).resolve(); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("CHROME_PATH"))
        pg = await b.new_page(viewport={"width": 1080, "height": 1440})
        for post in spec["posts"]:
            sl = post["slides"]; n = len(sl)
            for k, s in enumerate(sl):
                f = out / f'{post["id"]}_{k + 1:02d}.html'; f.write_text(TYPES[s["type"]](s, n, k))
                await pg.goto(f"file://{f}"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
                await pg.screenshot(path=str(out / f'{post["id"]}_{k + 1:02d}.png'))
            (out / f'{post["id"]}_caption.txt').write_text(post.get("caption", ""))
            if post.get("tags"):
                (out / f'{post["id"]}_tags.json').write_text(json.dumps(post["tags"], indent=1))
        await b.close()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))

#!/usr/bin/env python3
"""Riffex IG posts v2: visual first, 1080x1080. JSON spec -> PNG slides.
Slide types: grid9, cover, image, shot, stat, title
Usage: python3 render2.py spec.json out_dir
"""
import json, sys, html, pathlib, asyncio
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent
F = ROOT / "node_modules/@fontsource"
WORDMARK = (ROOT / "brand/wordmark.svg").read_text()
C = dict(bg="#14181A", cream="#F2EFE8", mute="rgba(242,239,232,0.62)", dim="rgba(242,239,232,0.40)",
         line="rgba(242,239,232,0.14)", teal="#0ABAB5")
S = 1080

def esc(s): return html.escape(str(s or ""))
def url(p): return f"file://{ROOT / p}"

CSS = f"""
@font-face {{ font-family: HG; src: url(file://{F}/host-grotesk/files/host-grotesk-latin-500-normal.woff2); font-weight:500; }}
@font-face {{ font-family: HG; src: url(file://{F}/host-grotesk/files/host-grotesk-latin-600-normal.woff2); font-weight:600; }}
@font-face {{ font-family: HG; src: url(file://{F}/host-grotesk/files/host-grotesk-latin-700-normal.woff2); font-weight:700; }}
@font-face {{ font-family: HG; src: url(file://{F}/host-grotesk/files/host-grotesk-latin-800-normal.woff2); font-weight:800; }}
@font-face {{ font-family: GM; src: url(file://{F}/geist-mono/files/geist-mono-latin-500-normal.woff2); font-weight:500; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html,body {{ width:{S}px; height:{S}px; background:{C['bg']}; overflow:hidden; }}
body {{ font-family:HG,sans-serif; color:{C['cream']}; position:relative; -webkit-font-smoothing:antialiased; }}
.abs {{ position:absolute; }}
.mono {{ font-family:GM,monospace; text-transform:uppercase; letter-spacing:.14em; font-size:22px; font-weight:500; }}
.tag {{ display:inline-flex; align-items:center; gap:12px; }}
.dot {{ width:11px; height:11px; border-radius:50%; background:{C['teal']}; display:inline-block; }}
.logo svg {{ height:40px; width:auto; display:block; }}
.hl {{ font-weight:800; letter-spacing:-.035em; line-height:.92; text-transform:uppercase; }}
.blurbg {{ position:absolute; inset:-60px; background-size:cover; background-position:center; filter:blur(48px) saturate(1.2) brightness(.45); }}
.shade {{ position:absolute; inset:0; }}
.chip {{ display:inline-block; font-family:GM,monospace; font-weight:500; font-size:22px; letter-spacing:.14em; text-transform:uppercase;
        padding:12px 18px; border-radius:10px; background:{C['teal']}; color:{C['bg']}; }}
"""

def logo(h=40):
    return '<div class="logo">' + WORDMARK.replace('width="1344" height="600"', f'width="{h*2.24:.0f}" height="{h}"') + '</div>'

def top_label(series, light=True):
    return (f'<div class="abs mono tag" style="left:56px;top:52px;color:{C["cream"] if light else C["bg"]};'
            f'text-shadow:0 1px 12px rgba(0,0,0,.5)"><span class="dot"></span>{esc(series)}</div>')

def corner_logo():
    return f'<div class="abs" style="right:56px;top:46px;filter:drop-shadow(0 1px 10px rgba(0,0,0,.5))">{logo(36)}</div>'

def doc(inner):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{inner}</body></html>'

def headline(text, size=96, accent=None):
    t = esc(text)
    if accent:
        t = t.replace(esc(accent), f'<span style="color:{C["teal"]}">{esc(accent)}</span>', 1)
    return f'<div class="hl" style="font-size:{size}px">{t}</div>'

# ---------- types ----------
def t_grid9(s):
    imgs = s["imgs"][:6]
    tiles = "".join(f'<div style="background:url({url(i)}) center/cover"></div>' for i in imgs)
    return doc(
        f'<div class="abs" style="left:0;top:0;width:1080px;height:720px;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr);gap:0">{tiles}</div>'
        f'<div class="shade" style="background:linear-gradient(180deg,rgba(20,24,26,.55) 0%,rgba(20,24,26,0) 14%,rgba(20,24,26,0) 52%,{C["bg"]} 67%,{C["bg"]} 100%)"></div>'
        f'{top_label(s["series"])}{corner_logo()}'
        f'<div class="abs" style="left:56px;right:56px;bottom:60px">{headline(s["title"], s.get("size",132), s.get("accent"))}'
        f'<div class="mono" style="color:{C["mute"]};margin-top:22px">{esc(s.get("sub",""))}</div></div>')

def t_cover(s):
    sz = s.get("img_size", 700)
    chip = f'<div style="margin-bottom:18px"><span class="chip">{esc(s["chip"])}</span></div>' if s.get("chip") else ""
    return doc(
        f'<div class="blurbg" style="background-image:url({url(s["img"])})"></div>'
        f'{top_label(s["series"])}{corner_logo()}'
        f'<img src="{url(s["img"])}" class="abs" style="left:{(S-sz)//2}px;top:118px;width:{sz}px;height:{sz}px;object-fit:cover;'
        f'border-radius:18px;box-shadow:0 40px 90px rgba(0,0,0,.6)">'
        f'<div class="abs" style="left:56px;right:56px;bottom:52px;text-align:center">{chip}'
        f'<div style="font-weight:800;font-size:{s.get("a_size",54)}px;letter-spacing:-.025em;line-height:1">{esc(s["a"])}</div>'
        f'<div style="font-weight:500;font-size:34px;color:{C["mute"]};margin-top:10px">{esc(s.get("t",""))}</div></div>')

def t_image(s):
    pos = s.get("pos", "center")
    chip = f'<div style="margin-bottom:22px"><span class="chip">{esc(s["chip"])}</span></div>' if s.get("chip") else ""
    return doc(
        f'<div class="abs" style="inset:0;background:url({url(s["img"])}) {pos}/cover"></div>'
        f'<div class="shade" style="background:linear-gradient(180deg,rgba(20,24,26,.5) 0%,rgba(20,24,26,0) 20%,rgba(20,24,26,0) 50%,rgba(20,24,26,.88) 78%,{C["bg"]} 100%)"></div>'
        f'{top_label(s["series"])}{corner_logo()}'
        f'<div class="abs" style="left:56px;right:56px;bottom:58px">{chip}{headline(s["headline"], s.get("size",104), s.get("accent"))}'
        + (f'<div style="font-weight:500;font-size:32px;color:{C["mute"]};margin-top:18px;line-height:1.25">{esc(s["sub"])}</div>' if s.get("sub") else "")
        + '</div>')

def t_shot(s):
    """Screenshot card (article headline, post) on a blurred backdrop, with optional big headline."""
    w = s.get("w", 920)
    bg = s.get("bg_img")
    back = (f'<div class="blurbg" style="background-image:url({url(bg)})"></div>' if bg else
            f'<div class="abs" style="inset:0;background:radial-gradient(120% 80% at 50% 0%,#1F2629 0%,{C["bg"]} 60%)"></div>')
    hl = (f'<div class="abs" style="left:56px;right:56px;bottom:58px">{headline(s["headline"], s.get("size",88), s.get("accent"))}</div>'
          if s.get("headline") else "")
    top = s.get("top", 150)
    return doc(
        f'{back}{top_label(s["series"])}{corner_logo()}'
        f'<img src="{url(s["img"])}" class="abs" style="left:{(S-w)//2}px;top:{top}px;width:{w}px;border-radius:16px;'
        f'box-shadow:0 30px 80px rgba(0,0,0,.55);background:#fff">'
        f'{hl}' + (f'<div class="abs mono" style="left:{(S-w)//2}px;top:{top-40}px;color:{C["dim"]};font-size:18px">{esc(s.get("credit",""))}</div>' if s.get("credit") else ""))

def t_stat(s):
    return doc(
        f'<div class="blurbg" style="background-image:url({url(s["img"])})"></div>'
        f'{top_label(s["series"])}{corner_logo()}'
        f'<img src="{url(s["img"])}" class="abs" style="left:56px;top:150px;width:420px;height:420px;object-fit:cover;border-radius:16px;box-shadow:0 30px 80px rgba(0,0,0,.55)">'
        f'<div class="abs" style="left:520px;right:56px;top:150px;height:420px;display:flex;flex-direction:column;justify-content:center">'
        f'<div style="font-weight:800;font-size:{s.get("big_size",230)}px;letter-spacing:-.06em;line-height:.85;color:{C["teal"]}">{esc(s["big"])}</div>'
        f'<div class="mono" style="color:{C["cream"]};margin-top:20px;line-height:1.5">{esc(s["big_label"])}</div></div>'
        f'<div class="abs" style="left:56px;right:56px;bottom:58px">{headline(s["headline"], s.get("size",76))}'
        + (f'<div style="font-weight:500;font-size:30px;color:{C["mute"]};margin-top:16px">{esc(s["sub"])}</div>' if s.get("sub") else "")
        + '</div>')

def t_title(s):
    """Opening slide with a fanned stack of images and a big title."""
    imgs = s.get("imgs", [])[:3]
    rots = [-8, 6, -1]; offs = [(330, 120), (560, 150), (440, 260)]
    stack = "".join(f'<img src="{url(im)}" class="abs" style="left:{offs[k][0]}px;top:{offs[k][1]}px;width:400px;height:400px;'
                    f'object-fit:cover;border-radius:18px;transform:rotate({rots[k]}deg);box-shadow:0 40px 90px rgba(0,0,0,.6)">'
                    for k, im in enumerate(imgs))
    back = f'<div class="blurbg" style="background-image:url({url(imgs[-1])});filter:blur(60px) brightness(.32)"></div>' if imgs else ""
    return doc(
        f'{back}{stack}{top_label(s["series"])}{corner_logo()}'
        f'<div class="shade" style="background:linear-gradient(180deg,rgba(20,24,26,0) 45%,rgba(20,24,26,.9) 75%,{C["bg"]} 100%)"></div>'
        f'<div class="abs" style="left:56px;right:56px;bottom:60px">{headline(s["title"], s.get("size",132), s.get("accent"))}'
        f'<div class="mono" style="color:{C["mute"]};margin-top:22px">{esc(s.get("sub",""))}</div></div>')

def t_dates(s):
    rows = "".join(
        f'<div style="display:grid;grid-template-columns:150px 1fr;align-items:center;gap:28px;padding:22px 0;border-bottom:1px solid {C["line"]}">'
        f'<div class="mono" style="color:{C["teal"]};font-size:26px">{esc(r["d"])}</div>'
        f'<div><div style="font-weight:700;font-size:40px;letter-spacing:-.02em">{esc(r["a"])}</div>'
        f'<div style="font-weight:500;font-size:28px;color:{C["mute"]};margin-top:4px">{esc(r["t"])}</div></div></div>'
        for r in s["rows"])
    return doc(f'<div class="abs" style="inset:0;background:radial-gradient(120% 80% at 50% 0%,#1F2629 0%,{C["bg"]} 60%)"></div>'
               f'{top_label(s["series"])}{corner_logo()}'
               f'<div class="abs" style="left:56px;right:56px;top:140px">{headline(s["title"], 84)}'
               f'<div style="margin-top:30px;border-top:1px solid {C["line"]}">{rows}</div></div>')

TYPES = dict(grid9=t_grid9, cover=t_cover, image=t_image, shot=t_shot, stat=t_stat, title=t_title, dates=t_dates)

async def main(spec, out):
    spec = json.loads(pathlib.Path(spec).read_text()); out = pathlib.Path(out).resolve(); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": S, "height": S})
        for post in spec["posts"]:
            for k, s in enumerate(post["slides"], 1):
                f = out / f'{post["id"]}_{k:02d}.html'; f.write_text(TYPES[s["type"]](s))
                await pg.goto(f"file://{f}"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(200)
                await pg.screenshot(path=str(out / f'{post["id"]}_{k:02d}.png'))
            (out / f'{post["id"]}_caption.txt').write_text(post.get("caption", ""))
        await b.close()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))

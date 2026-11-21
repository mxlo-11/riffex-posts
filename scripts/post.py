"""Publish the queued Riffex post for today to Instagram.

Queue layout (committed by the daily Claude task):
  queue/YYYY-MM-DD/1.jpg, 2.jpg, ...   JPEG images, 1080x1440 (3:4), in slide order
  queue/YYYY-MM-DD/caption.txt          the caption
  queue/YYYY-MM-DD/tags.json            optional: {"1": ["handle"], "3": ["handle2"]} artists to tag on those slides
                                        (max 5 tags per post; a tag Instagram rejects is dropped, the post still goes out)
After posting, queue/YYYY-MM-DD/posted.json is committed with the media id.

The token comes only from the IG_TOKEN repository secret. Never print it.
Modes:
  pending (default for schedule and push): posts TODAY's folder only, from 5 PM New York time.
           Older unposted dated folders are marked skipped.json and never posted (stale). Future dates wait.
           Folders not named YYYY-MM-DD are only posted by a manual "post" run.
  post:    posts one folder now (POST_DATE, or today), ignoring the 5 PM rule.
  check:   reads the profile, posts nothing.
"""
import json, os, sys, time, datetime, pathlib, urllib.parse, urllib.request
from zoneinfo import ZoneInfo

API = "https://graph.instagram.com/v23.0"
TOKEN = os.environ.get("IG_TOKEN", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "mxlo-11/riffex-posts")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"


def call(method, path, soft=False, **params):
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode())
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace").replace(TOKEN, "***")
        if soft:
            print(f"Instagram API error {e.code} on {path} (handled): {body}")
            return None
        sys.exit(f"Instagram API error {e.code} on {path}: {body}")


def wait_ready(container_id):
    for _ in range(30):
        s = call("GET", container_id, fields="status_code").get("status_code")
        if s == "FINISHED":
            return
        if s in ("ERROR", "EXPIRED"):
            sys.exit(f"Container {container_id} failed: {s}")
        time.sleep(5)
    sys.exit(f"Container {container_id} not ready in time")


def main():
    if not TOKEN:
        sys.exit("IG_TOKEN secret is missing")
    mode = (sys.argv[1] if len(sys.argv) > 1 else "post").strip() or "post"
    me = call("GET", "me", fields="user_id,username")
    print(f"Connected as @{me.get('username')} ({me.get('user_id')})")
    if mode == "check":
        return

    now_ny = datetime.datetime.now(ZoneInfo("America/New_York"))
    today = now_ny.date().isoformat()
    if mode == "pending":
        # Only TODAY's folder can go out on its own (from 5 PM New York time). Any older unposted
        # dated folder is stale (its "this week" / "this Friday" words are no longer true), so it is
        # marked skipped and never posted. Folders not named YYYY-MM-DD (e.g. pin-1-trade) are only
        # ever posted by a manual run (mode post + date). Added Nov 18, 2026 after a stale Nov 5 post went out.
        import re
        due = None
        for f in sorted(pathlib.Path("queue").iterdir()):
            if not f.is_dir() or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", f.name):
                continue
            if (f / "posted.json").exists() or (f / "skipped.json").exists():
                continue
            if f.name < today:
                (f / "skipped.json").write_text(json.dumps({"skipped_at": now_ny.isoformat(), "reason": "stale: older than today, never auto posted"}))
                print(f"Skipped stale {f.name}.")
            elif f.name == today and now_ny.hour >= 17:
                due = f.name
        if not due:
            print(f"Nothing due at {now_ny:%Y-%m-%d %H:%M} New York time.")
            return
        publish(due)
        return
    publish(os.environ.get("POST_DATE") or today)


def publish(day):
    folder = pathlib.Path("queue") / day
    if not folder.is_dir():
        print(f"Nothing queued for {day}.")
        return
    if (folder / "posted.json").exists():
        print(f"{day} already posted.")
        return
    images = sorted((p for p in folder.iterdir() if p.suffix.lower() in (".jpg", ".jpeg")), key=lambda p: int(p.stem) if p.stem.isdigit() else 999)
    if not images:
        sys.exit(f"No .jpg images in {folder}")
    caption = (folder / "caption.txt").read_text().strip() if (folder / "caption.txt").exists() else ""
    urls = [f"{RAW}/{folder.as_posix()}/{p.name}" for p in images]
    tags = json.loads((folder / "tags.json").read_text()) if (folder / "tags.json").exists() else {}
    budget = 5
    tag_log = {"tagged": [], "dropped": []}
    me_id = call("GET", "me", fields="user_id").get("user_id") if tags else None

    def entries(slide_no):
        # tags.json values may be ["handle"] or [{"handle": "x", "artist": "Name"}]
        out = []
        for x in tags.get(str(slide_no), []):
            h, a = (str(x.get("handle", "")), str(x.get("artist", ""))) if isinstance(x, dict) else (str(x), "")
            h = h.lstrip("@").strip()
            if h:
                out.append((h, a))
        return out

    def looks_like_artist(handle, artist):
        # Milo, Nov 21: no verified badge needed. The account counts as the artist if it names them or
        # links their music (SoundCloud, Spotify, Bandcamp...). Instagram's own read only lookup; when it
        # can't be read (a personal account, or not available for this token) the handle's source stands.
        if not artist or not me_id:
            return True
        r = call("GET", me_id, soft=True, fields=f"business_discovery.username({handle}){{username,name,biography,website}}")
        bd = (r or {}).get("business_discovery")
        if not bd:
            return True
        blob = " ".join(str(bd.get(k, "")) for k in ("username", "name", "biography", "website")).lower()
        squash = lambda s: "".join(ch for ch in s.lower() if ch.isalnum())
        if squash(artist) and squash(artist) in squash(blob):
            return True
        return any(d in blob for d in ("soundcloud", "spotify", "bandcamp", "music.apple", "youtube", "linktr.ee", "audiomack", "tidal", "deezer"))

    def tag_json(names):
        # spread tags along the lower part of the slide, where the artist name sits
        return json.dumps([{"username": n, "x": round(0.2 + 0.6 * (k + 0.5) / len(names), 3), "y": 0.82} for k, n in enumerate(names)])

    def make_item(slide_no, url, **extra):
        nonlocal budget
        names = []
        for h, a in entries(slide_no):
            if len(names) >= budget:
                break
            if looks_like_artist(h, a):
                names.append(h)
            else:
                tag_log["dropped"].append({"slide": slide_no, "handle": h, "why": "account does not look like the artist"})
        if names:
            # all tags first; if Instagram rejects them, try each alone so one bad handle never costs the others
            good = names
            r = call("POST", "me/media", soft=True, image_url=url, user_tags=tag_json(names), **extra)
            if not r:
                good = []
                for n in names:
                    if call("POST", "me/media", soft=True, image_url=url, user_tags=tag_json([n]), **extra):
                        good.append(n)
                    else:
                        tag_log["dropped"].append({"slide": slide_no, "handle": n, "why": "Instagram rejected the username"})
                if good:
                    r = call("POST", "me/media", soft=True, image_url=url, user_tags=tag_json(good), **extra)
            if r:
                budget -= len(good)
                tag_log["tagged"] += [{"slide": slide_no, "handle": n} for n in good]
                return r
            print(f"Slide {slide_no}: posting it without tags")
        return call("POST", "me/media", image_url=url, **extra)

    if len(urls) == 1:
        c = make_item(1, urls[0], caption=caption)["id"]
    else:
        kids = []
        for n, u in enumerate(urls[:10], 1):
            k = make_item(n, u, is_carousel_item="true")["id"]
            wait_ready(k)
            kids.append(k)
        c = call("POST", "me/media", media_type="CAROUSEL", children=",".join(kids), caption=caption)["id"]
    if tags:
        print("Tags:", json.dumps(tag_log))
    wait_ready(c)
    media = call("POST", "me/media_publish", creation_id=c)["id"]
    (folder / "posted.json").write_text(json.dumps({"media_id": media, "posted_at": datetime.datetime.utcnow().isoformat() + "Z", "slides": len(urls), "tags": tag_log}, indent=2))
    print(f"Posted {day}: media {media} ({len(urls)} slide(s))")

if __name__ == "__main__":
    main()

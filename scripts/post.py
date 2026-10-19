"""Publish the queued Riffex post for today to Instagram.

Queue layout (committed by the daily Claude task):
  queue/YYYY-MM-DD/1.jpg, 2.jpg, ...   JPEG images, 4:5 (1080x1350), in slide order
  queue/YYYY-MM-DD/caption.txt          the caption
After posting, queue/YYYY-MM-DD/posted.json is committed with the media id.

The token comes only from the IG_TOKEN repository secret. Never print it.
Modes: post (default), check (reads the profile, posts nothing).
"""
import json, os, sys, time, datetime, pathlib, urllib.parse, urllib.request
from zoneinfo import ZoneInfo

API = "https://graph.instagram.com/v23.0"
TOKEN = os.environ.get("IG_TOKEN", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "mxlo-11/riffex-posts")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"


def call(method, path, **params):
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
    if os.environ.get("GITHUB_EVENT_NAME") == "schedule" and now_ny.hour < 17:
        print(f"Scheduled run at {now_ny:%H:%M} New York time, before 5 PM. Waiting for the next run.")
        return
    day = os.environ.get("POST_DATE") or now_ny.date().isoformat()
    folder = pathlib.Path("queue") / day
    if not folder.is_dir():
        print(f"Nothing queued for {day}.")
        return
    if (folder / "posted.json").exists():
        print(f"{day} already posted.")
        return
    images = sorted(p for p in folder.iterdir() if p.suffix.lower() in (".jpg", ".jpeg"))
    if not images:
        sys.exit(f"No .jpg images in {folder}")
    caption = (folder / "caption.txt").read_text().strip() if (folder / "caption.txt").exists() else ""
    urls = [f"{RAW}/{folder.as_posix()}/{p.name}" for p in images]

    if len(urls) == 1:
        c = call("POST", "me/media", image_url=urls[0], caption=caption)["id"]
    else:
        kids = []
        for u in urls[:10]:
            k = call("POST", "me/media", image_url=u, is_carousel_item="true")["id"]
            wait_ready(k)
            kids.append(k)
        c = call("POST", "me/media", media_type="CAROUSEL", children=",".join(kids), caption=caption)["id"]
    wait_ready(c)
    media = call("POST", "me/media_publish", creation_id=c)["id"]
    (folder / "posted.json").write_text(json.dumps({"media_id": media, "posted_at": datetime.datetime.utcnow().isoformat() + "Z", "slides": len(urls)}, indent=2))
    print(f"Posted {day}: media {media} ({len(urls)} slide(s))")


if __name__ == "__main__":
    main()

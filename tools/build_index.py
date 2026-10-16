#!/usr/bin/env python3
"""Rebuild lessons/index.json, and each lesson's index.html page, from the lesson folders.

Run from the site's top folder after adding or changing a lesson:

    python3 tools/build_index.py

What it does
- Reads every lessons/<slug>/lesson.json.
- Writes lessons/<slug>/index.html (the small page that loads the shared player),
  unless that lesson already has a page and you pass nothing (it is always safe to rewrite).
- Writes lessons/index.json: every lesson's title, summary, links, length and thumbnail,
  plus the planned lessons from lessons/planned.json. The home page and the
  "What's next?" map read this file.

Lesson addresses (the folder name, called the slug) are permanent once published,
because Circle lessons and bookmarks point at them. Rename a title freely; never rename a folder.
"""
import json, pathlib, html, datetime, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LESSONS = ROOT / "lessons"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Glitch'n</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..900&family=Atkinson+Hyperlegible:wght@400;700&family=IBM+Plex+Mono:wght@500;600&display=swap">
<link rel="stylesheet" href="../../player/player.css">
</head>
<body>
<div id="glitchn-player"></div>
<script src="../../player/player.js"></script>
</body>
</html>
"""


def lesson_page(title):
    return PAGE.format(title=html.escape(title, quote=False))


def main():
    lessons, problems = [], []
    for f in sorted(LESSONS.glob("*/lesson.json")):
        slug = f.parent.name
        try:
            L = json.loads(f.read_text())
        except Exception as e:  # noqa: BLE001
            problems.append(f"{f}: not valid JSON ({e})")
            continue
        if L.get("slug") and L["slug"] != slug:
            problems.append(f"{f}: slug '{L['slug']}' does not match its folder '{slug}' (the folder wins)")
        steps = L.get("steps", [])
        subs = sum(len(s.get("subs", [])) for s in steps)
        duration = round(sum(s.get("duration", 0) for s in L.get("segments", [])), 2)
        thumb = None
        for st in reversed(steps):  # the finished circuit makes the best card picture
            if st.get("subs"):
                thumb = st["subs"][-1].get("still")
                break
        if thumb:
            thumb = slug + "/" + thumb.replace("stills/", "thumbs/", 1)
        for p in (f.parent / s.get("src", "") for s in L.get("segments", [])):
            if not p.exists():
                problems.append(f"{slug}: missing video {p.relative_to(ROOT)}")
        lessons.append({
            "slug": slug,
            "title": L.get("title", slug),
            "summary": L.get("summary", ""),
            "status": L.get("status", "ready"),
            "duration": duration,
            "steps": len(steps),
            "subSteps": subs,
            "thumb": thumb,
            "links": L.get("links", []),
        })
        (f.parent / "index.html").write_text(lesson_page(L.get("title", slug)))

    planned_file = LESSONS / "planned.json"
    planned = json.loads(planned_file.read_text()).get("planned", []) if planned_file.exists() else []
    known = {x["slug"] for x in lessons}
    planned = [p for p in planned if p["slug"] not in known]  # a planned lesson that now exists drops off the list

    slugs = known | {p["slug"] for p in planned}
    for item in lessons + planned:
        for link in item.get("links", []):
            if link.get("to") not in slugs:
                problems.append(f"{item['slug']}: links to '{link.get('to')}', which isn't a lesson or a planned lesson")

    index = {
        "format": "glitchn-index/1",
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "lessons": lessons,
        "planned": planned,
    }
    (LESSONS / "index.json").write_text(json.dumps(index, indent=1) + "\n")
    print(f"lessons/index.json: {len(lessons)} lessons, {len(planned)} planned")
    for p in problems:
        print("  check:", p)
    return 1 if any("not valid JSON" in p for p in problems) else 0


if __name__ == "__main__":
    sys.exit(main())

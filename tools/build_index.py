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
- Copies each lesson's descriptors into the index: the lessons it requires, its concepts and
  sounds, its parts list (BOM), its chips and oscillators, and an Easy/Medium/Hard rating from
  tools/difficulty.py. Part, concept and sound names come from lessons/catalog.json, and any
  key that isn't in the catalog is reported.
- Reads each lesson's translations (lesson.<lang>.json, e.g. lesson.es.json) so the home page
  and maps can show translated titles, and reports lines that have no translation yet
  (for example after the English text was edited). Untranslated lines show in English.

Lesson addresses (the folder name, called the slug) are permanent once published,
because Circle lessons and bookmarks point at them. Rename a title freely; never rename a folder.
"""
import json, pathlib, html, datetime, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import difficulty  # noqa: E402  (tools/difficulty.py: the Easy/Medium/Hard formula)

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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..900&family=Atkinson+Hyperlegible:wght@400;700&family=IBM+Plex+Mono:wght@500;600&display=swap">
<link rel="stylesheet" href="../../player/player.css?v=202610190949">
<link rel="stylesheet" href="../../styles/all.css?v=202610190949">
</head>
<body>
<div id="glitchn-player"></div>
<script src="../../player/player.js?v=202610190949"></script>
</body>
</html>
"""


def lesson_page(title):
    return PAGE.format(title=html.escape(title, quote=False))


def main():
    lessons, problems, translations = [], [], {}
    catalog_file = LESSONS / "catalog.json"
    catalog = json.loads(catalog_file.read_text()) if catalog_file.exists() else {}
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
            # the outline the home page unfolds: each step's title and the board as that step ends
            "outline": [{"title": st.get("title", ""),
                         "thumb": (slug + "/" + st["subs"][-1]["still"].replace("stills/", "thumbs/", 1)) if st.get("subs") and st["subs"][-1].get("still") else None}
                        for st in steps],
            "links": L.get("links", []),
        })
        for o in lessons[-1]["outline"]:
            if o["thumb"] and not (LESSONS / o["thumb"]).exists():
                problems.append(f"{slug}: missing step picture lessons/{o['thumb']}")
        if "parts" in L:
            d = difficulty.rate(L)
            lessons[-1].update({
                "requires": L.get("requires", []),
                "startHere": bool(L.get("startHere")),
                "concepts": L.get("concepts", []),
                "sounds": L.get("sounds", []),
                "parts": L.get("parts", {}),
                "chips": [c for c in difficulty.CHIPS if L.get("parts", {}).get(c)],
                "oscillators": d["counts"]["oscillators"],
                "difficulty": {"level": d["level"], "points": d["points"], "why": d["why"]},
            })
            for kind, keys in (("parts", L.get("parts", {}).keys()), ("concepts", L.get("concepts", [])), ("sounds", L.get("sounds", []))):
                for k in keys:
                    if catalog and k not in catalog.get(kind, {}):
                        problems.append(f"{slug}: {kind[:-1]} '{k}' isn't in lessons/catalog.json")
        else:
            problems.append(f"{slug}: no parts list yet, so no descriptors or difficulty")
        i18n = {}
        english = [L.get("title"), L.get("summary")] + [st.get("title") for st in steps] + [sb.get("text") for st in steps for sb in st.get("subs", [])]
        english = [x for x in english if x]
        for tf in sorted(x for x in f.parent.glob("lesson.*.json") if x.name != "lesson.simple.json"):  # lesson.simple.json is Simple words, not a language
            lang = tf.name.split(".")[1]
            try:
                strings = json.loads(tf.read_text()).get("strings", {})
            except Exception as e:  # noqa: BLE001
                problems.append(f"{tf}: not valid JSON ({e})")
                continue
            i18n[lang] = {k: strings[v] for k, v in (("title", L.get("title")), ("summary", L.get("summary"))) if v in strings}
            i18n[lang]["outline"] = [strings.get(st.get("title", ""), st.get("title", "")) for st in steps]
            missing = [x for x in english if x not in strings]
            translations[lang] = translations.get(lang, 0) + 1
            if missing:
                problems.append(f"{slug}: {len(missing)} of {len(english)} lines have no {lang} translation yet (they show in English), e.g. \"{missing[0][:60]}\"")
        if i18n:
            lessons[-1]["i18n"] = i18n
        # Simple words (lesson.simple.json): each technical English line with its simple English and Spanish versions.
        sf = f.parent / "lesson.simple.json"
        if sf.exists():
            try:
                simple = json.loads(sf.read_text()).get("strings", {})
            except Exception as e:  # noqa: BLE001
                problems.append(f"{sf}: not valid JSON ({e})")
                simple = {}
            lacking = [x for x in english if x != L.get("title") and x not in simple]
            if lacking:
                problems.append(f"{slug}: {len(lacking)} lines have no simple version yet (they show as they are), e.g. \"{lacking[0][:60]}\"")
            for x, v in simple.items():
                if x not in english:
                    problems.append(f"{slug}: lesson.simple.json has a line that isn't in the lesson (old wording?): \"{x[:60]}\"")
                elif not (isinstance(v, dict) and v.get("en")):
                    problems.append(f"{slug}: simple line has no English: \"{x[:60]}\"")
            langs = sorted({k for v in simple.values() if isinstance(v, dict) for k in v})
            lessons[-1]["simple"] = {lg: {"summary": (simple.get(L.get("summary"), {}) or {}).get(lg),
                                          "outline": [(simple.get(st.get("title"), {}) or {}).get(lg) for st in steps]}
                                     for lg in langs}
        else:
            problems.append(f"{slug}: no lesson.simple.json yet, so Simple mode shows the technical words")
        (f.parent / "index.html").write_text(lesson_page(L.get("title", slug)))

    planned_file = LESSONS / "planned.json"
    planned = json.loads(planned_file.read_text()).get("planned", []) if planned_file.exists() else []
    known = {x["slug"] for x in lessons}
    planned = [p for p in planned if p["slug"] not in known]  # a planned lesson that now exists drops off the list

    slugs = known | {p["slug"] for p in planned}
    for item in lessons:
        for r in item.get("requires", []):
            if r not in known:
                problems.append(f"{item['slug']}: requires '{r}', which isn't a lesson")
    for item in lessons + planned:
        for link in item.get("links", []):
            if link.get("to") not in slugs:
                problems.append(f"{item['slug']}: links to '{link.get('to')}', which isn't a lesson or a planned lesson")

    index = {
        "format": "glitchn-index/1",
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "lessons": lessons,
        "planned": planned,
        "catalog": dict(catalog, partOrder=list(catalog.get("parts", {}))),  # JavaScript sorts keys like "40106" as numbers, so the kit order travels as a list
    }
    (LESSONS / "index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False) + "\n")
    print(f"lessons/index.json: {len(lessons)} lessons, {len(planned)} planned"
          + "".join(f"; {n} with {lang} translation" for lang, n in sorted(translations.items())))
    for x in lessons:
        for lang in translations:
            if lang not in x.get("i18n", {}):
                problems.append(f"{x['slug']}: no {lang} translation file yet (lesson.{lang}.json); it shows in English")
    for p in problems:
        print("  check:", p)
    return 1 if any("not valid JSON" in p for p in problems) else 0


if __name__ == "__main__":
    sys.exit(main())

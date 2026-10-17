# Glitch'n lessons

The public lesson library for Glitch'n: build sound circuits on a breadboard, one small step at a time.

Each **lesson** plays a build video beside step-by-step instructions, with close-up stills you can magnify, a progress bar, and a map of where to go next. Lessons link to each other, so the library can grow in any direction instead of following a fixed course.

## How it's organised

```
index.html                 home page: lesson cards, the map of all lessons, what's coming
player/player.js, .css     the one lesson player every lesson page uses
lessons/
  index.json               the list of lessons (made by tools/build_index.py; don't edit by hand)
  planned.json             lessons that are coming (edit by hand)
  <lesson-address>/        one folder per lesson
    index.html             the lesson page (made by the editor or build_index.py)
    lesson.json            steps, sub-steps, timestamps, and links to other lessons
    lesson.es.json         Spanish text for the lesson (English line → Spanish line)
    video/part-1.mp4 …     web-sized video clips, played back to back
    stills/  thumbs/       close-up stills and their small versions
editor/index.html          the step editor, for the Glitch'n team
tools/                     scripts for the team (see below)
```

**A lesson's folder name is its permanent web address** (for example `lessons/blink-to-drum-machine/`). Circle lessons and bookmarks point at it, so titles can change but folder names shouldn't.

## Adding a lesson

1. Open the **step editor**, start a blank lesson, open your clips, and mark steps (S) and sub-steps (A). A still is captured at each mark; press C to re-capture on a cleaner frame. Fill in the title, address, summary, and which lessons it leads to.
2. **Export** it. Put the exported folder into `lessons/`.
3. Make the web videos in that folder, in order:
   `bash tools/encode_clips.sh lessons/<address>/video clip1.mov clip2.mov …`
4. Rebuild the lesson list: `python3 tools/build_index.py`
5. Commit and push. GitHub Pages publishes the change in a minute or two.

## Links between lessons

Each lesson lists where it leads in its own `lesson.json`:

```json
"links": [ { "to": "another-lesson-address", "kind": "next" } ]
```

`kind` is `next`, `variation` or `related` (any short word works and shows on the map). The home page and each lesson's "What's next?" panel draw the map from these links, so connecting a new lesson means editing only that lesson, or the lesson that should point to it.

## Spanish (and other languages)

Visitors can switch between **English** and **Español** on every page. The choice is remembered, Spanish-language browsers start in Spanish, and a link can force a language with `?lang=es` (useful when embedding a lesson in Spanish).

- Interface wording (buttons, labels, messages) lives in `player/player.js` and `index.html`, in a small table with `en` and `es` entries.
- Each lesson's Spanish text lives beside it in `lesson.es.json`: a list of English lines with their translations. A line with no translation shows in English, so editing a lesson never breaks its Spanish version. `tools/build_index.py` lists lines that still need translating.
- The step editor stays English-only. When a lesson is ready, ask Claude to write or update its `lesson.es.json`.
- Spanish pages are marked "Traducción automática" (automatic translation) until a Spanish speaker reviews them. To mark a reviewed lesson, set `"reviewed": true` in its `lesson.es.json`.
- Planned lessons carry their Spanish titles in `lessons/planned.json` under `"i18n"`.

To add another language later, add its column to the two interface tables and a `lesson.<code>.json` file per lesson.

## Status

The first lesson's step text and the links are drafts for the Glitch'n team to review. Days 2–5 of the original five-day course are listed as planned lessons.

The site is plain HTML with no build step, published with GitHub Pages from the `main` branch.

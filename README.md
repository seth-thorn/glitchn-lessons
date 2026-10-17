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

## Styles

Every page has a **Style** menu that changes the page's whole personality, not just its colours. The choice is remembered across pages, and a link can force one with `?style=treehouse` (for example).

- **TV** (the default): the video sits in a chunky television with an antenna, feet, curved glass and a speed dial. While it plays, a power light glows and the antenna sways.
- **Clean**: calm, simple and precise, in the spirit of Dieter Rams, and built on Universal Design for Learning: no motion, no decoration, a warm off-white page, a highly legible typeface (Atkinson Hyperlegible), large controls, and nothing shown by colour alone. A quiet place to learn.
- **Gadget**: quiet, precise and tactile, after Dieter Rams's devices for Braun: warm greys, hairlines, round buttons and one orange accent. A radio-style tuning scale above the screen has a needle that moves through the lesson. (It was called "Rams" at first; old links with `?style=rams` still work.)
- **Solar Punk**: a cozy retro-future workshop full of plants: cream 1970s consoles, a CRT monitor with a radar dial, LED readouts and a level meter that come alive while the video plays, steps on green-bar printout paper, a radar-screen map, and a rug on the floor.
- **Treehouse**: a clubhouse in the leaves: wooden plank panels with nails, the screen hung from a branch by ropes with string lights, steps on paper notes. A little bird hops along the branch as the lesson plays.
- **Quest**: a 1980s fantasy film at twilight: mountains, a castle and pines behind the title, parchment panels, the screen in a stone frame under an arch with flickering torches, a wax-seal play button, a lantern on the trail, and an old map.
- **Skyline**: a dark style, a high-rise at dusk: a misty peak over a city of lit windows, dark glass panels warmed by lamplight (brighter while the video plays), progress shown as windows lighting up, and a burnt-orange sofa at the foot of the page.
- **Daydream**: a bright cloud world: deep blue sky, the video seen through a stone gateway, a water-slide scrub bar with a little raft, orchard rows for progress, and a map of lakes and channels.
- **Terminal**: a green-phosphor screen: glowing monospace text, scanlines, terminal windows, inverse-video highlights and a blinking cursor. The video itself is never tinted.

**Where styles live:** TV is part of `player/player.css`. Each other style is one file in `styles/` (`gadget.css`, `solarpunk.css`, `treehouse.css`) that styles both the lesson player and the home page. `styles/all.css` loads them all, along with their fonts.

**Things a style can use:** the player adds the class `is-playing` to `.app` while the video plays, sets `--played` (0 to 1) on `.app` as it goes, and has a spare decoration slot `.deco` (five empty `<i>` elements) inside the TV. Moving decorations stop for people who ask their device for reduced motion. The drawings are SVG pictures written into the CSS; their sources are in `tools/style_art.py`.

**To add a style** (Cartoon, say):
1. Copy a file in `styles/` to `styles/cartoon.css` and change `data-style="…"` throughout. Start with the colour and font tokens at the top, then restyle the parts.
2. Add `@import url("cartoon.css");` to `styles/all.css`, and add any new fonts to its first line.
3. Add `'cartoon'` to the `STYLES` list in `player/player.js` and in `index.html`, and its menu name (`style_cartoon`) to the English and Spanish word lists in both files.

## Status

The first lesson's step text and the links are drafts for the Glitch'n team to review. Days 2–5 of the original five-day course are listed as planned lessons.

The site is plain HTML with no build step, published with GitHub Pages from the `main` branch.

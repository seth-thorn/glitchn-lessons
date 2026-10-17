# Glitch'n lessons

**▶ Open the lessons: https://seth-thorn.github.io/glitchn-lessons/**

The public lesson library for Glitch'n: build sound circuits on a breadboard, one small step at a time.

Each **lesson** plays a build video beside step-by-step instructions, with close-up stills you can magnify, a progress bar, and a map of where to go next. Lessons link to each other, so the library can grow in any direction instead of following a fixed course.

## How it's organised

```
index.html                 home page: lesson cards, the map of all lessons, what's coming
player/player.js, .css     the one lesson player every lesson page uses
lessons/
  index.json               the list of lessons (made by tools/build_index.py; don't edit by hand)
  planned.json             lessons that are coming (edit by hand)
  catalog.json             names for parts, concepts and sounds that lessons refer to (edit by hand)
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

## What a lesson needs, teaches and asks of you

Each `lesson.json` also describes the lesson, so the home page can label and filter the lessons and each lesson page can show a parts list:

```json
"startHere": true,
"requires": [],
"concepts": ["oscillator", "light-sensing", "filter", "counter"],
"sounds": ["lights", "clicks", "rhythms"],
"oscillators": 1,
"parts": { "40106": 1, "4040": 1, "pot": 2, "led": 3, "jumpers": 13, "breadboard": 1 }
```

- **`startHere`** marks the foundation lesson. **`requires`** lists lessons to finish first (today every lesson requires "From Blink to Drum Machine", since every lesson builds on its oscillator). A future custom-course builder can use these to keep any order of lessons sensible.
- **`parts`** is the lesson's parts list: the most of each part on the board at once. The keys, names (English and Spanish) and kit part numbers live in **`lessons/catalog.json`**, taken from the kit list at the bottom of [glitchn.net/course](https://www.glitchn.net/course). Add a part there first, then use its key in lessons.
- **`concepts`** and **`sounds`** also use keys from `catalog.json`.
- **Difficulty** (Easy, Medium, Hard) is worked out from the chips, jumper wires and oscillators by **`tools/difficulty.py`**, where the formula, its weights and how they were chosen are written out. Run `python3 tools/difficulty.py` to see every lesson's rating and the arithmetic. To overrule the formula for one lesson, add `"difficulty": {"level": "medium", "why": "short reason"}` to its `lesson.json`.

On the home page, each lesson card can also unfold its steps ("See the 7 steps"): each step's title with a picture of the board as that step ends, linking straight to that step (`#step-3` at the end of a lesson's address opens it at step 3). `build_index.py` copies the step titles and pictures into `lessons/index.json`, and the pictures load only when someone opens the list.

`tools/build_index.py` checks every key against the catalog and every `requires` against the real lessons, and copies the catalog and the ratings into `lessons/index.json`.

## Simple and Technical words

Every page has a **Simple | Technical** switch next to the language buttons. **Simple** (the default) uses plain words for kids: "wire" for jumper, "knob" for trimmer, "light" for LED, "the minus (−) row" for ground, and so on. **Technical** shows the real names. Kids can switch back and forth as they learn the real names. The choice is remembered, and a link can set it with `?words=technical` or `?words=simple`.

- Each lesson's simple text lives beside it in `lesson.simple.json`: every technical English line from `lesson.json` with its simple English (`en`) and simple Spanish (`es`) version. A line with no simple version shows as it is, so editing a lesson never breaks Simple mode; `tools/build_index.py` lists lines that still need a simple version.
- Lesson titles stay the same in both modes. Chip numbers stay too, because they're printed on the chips.
- In Simple mode, the parts list shows a plain name and what each part is or does; in Technical mode, the real name and the kit part number. These come from the `simple` entries in `lessons/catalog.json`, which also give plain names for the concepts.
- The wording rules and the English/Spanish glossary are in `tools/simple-words.md`. Ask Claude to write or update a lesson's `lesson.simple.json` when its text changes.

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

- **TV** (the default): the video sits in a chunky television with an antenna, feet and a speed dial. While it plays, the antenna sways a little.
- **Clean**: calm, simple and precise, in the spirit of Dieter Rams, and built on Universal Design for Learning: no motion, no decoration, a warm off-white page, a highly legible typeface (Atkinson Hyperlegible), large controls, and nothing shown by colour alone. A quiet place to learn.
- **Gadget**: quiet, precise and tactile, after Dieter Rams's devices for Braun: warm greys, hairlines, round buttons, one orange accent and a small "glitch'n" nameplate above the screen. (It was called "Rams" at first; old links with `?style=rams` still work.)
- **Solar Punk**: a cozy retro-future workshop full of plants: cream 1970s consoles with an amber nameplate, a pothos trailing down the monitor, steps on cream paper and a dark green screen for the map.
- **Treehouse**: a clubhouse in the leaves: wooden plank panels with nails, the screen hung from a branch by ropes, a little bird perched on the branch, steps on paper notes.
- **Quest**: a 1980s fantasy film at twilight: mountains, a castle and pines behind the title, parchment panels, the screen in a smooth stone frame under an arch between two torches, a wax-seal play button, a lantern for the playhead, and an old map.
- **Skyline**: a dark style, a high-rise at dusk: a misty peak over a city of lit windows, dark glass panels warmed by lamplight and a warm progress bar.
- **Daydream**: a bright cloud world: deep blue sky, the video seen through a stone gateway, a calm blue stream for the timeline with a little raft for the playhead, and a meadow of lakes for the map.
- **Terminal**: a green-phosphor screen: glowing monospace text, terminal windows, inverse-video highlights and faint scanlines in the background (never over the video, pictures or text).

**Rules every style follows** (so a style can be playful without making the lesson harder to use):
1. **Only real controls look like controls.** No pictures of buttons, knobs, dials, lights, meters, speaker grilles or scales.
2. **One timeline, one progress bar.** Nothing else moves with the lesson or is marked with ticks, so nothing can be mistaken for them. Decorations don't use `--played`.
3. **The video and the close-up pictures are shown as they are:** no tint, lines, glass or shading over them.
4. **Fills are plain:** the timeline and progress bar fill with a solid colour, not stripes, dots or hatching.
5. **Calm behind reading and the map:** plain surfaces behind text, the steps and the map; pictures stay at the edges of the page, and nothing extra fills the foot of the page.
6. **Little motion, and none near the controls:** an antenna may sway, but nothing blinks, flickers or bobs, and anything that moves stops for people who ask their device for reduced motion.

**Where styles live:** TV is part of `player/player.css`. Each other style is one file in `styles/` (`clean.css`, `gadget.css`, `solarpunk.css` and so on) that styles both the lesson player and the home page. `styles/all.css` loads them all, along with their fonts.

**Things a style can use:** the player adds the class `is-playing` to `.app` while the video plays, sets `--played` (0 to 1) on `.app` as it goes (for the player itself, not decorations; see rule 2), and has a spare decoration slot `.deco` (five empty `<i>` elements) inside the TV. The drawings are SVG pictures written into the CSS; the files in `styles/` are the ones to edit, and `tools/style_art.py` keeps the sources of the original drawings.

**To add a style** (Cartoon, say):
1. Copy a file in `styles/` to `styles/cartoon.css` and change `data-style="…"` throughout. Start with the colour and font tokens at the top, then restyle the parts.
2. Add `@import url("cartoon.css");` to `styles/all.css`, and add any new fonts to its first line.
3. Add `'cartoon'` to the `STYLES` list in `player/player.js` and in `index.html`, and its menu name (`style_cartoon`) to the English and Spanish word lists in both files.

## Status

All five lessons from the original five-day course are up, as drafts for the Glitch'n team to review: step text, parts lists and difficulty ratings included.

The site is plain HTML with no build step, published with GitHub Pages from the `main` branch.

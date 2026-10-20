# Glitch'n lessons

**▶ Open the site: https://seth-thorn.github.io/glitchn-lessons/** · the lessons: https://seth-thorn.github.io/glitchn-lessons/lessons/

The public website for Glitch'n: a home page, and the lesson library for building sound circuits on a breadboard, one small step at a time. More of the old glitchn.net (the story of the project so far) will move here in steps.

Each **lesson** plays a build video beside step-by-step instructions, with close-up stills you can magnify, a progress bar, and a map of where to go next. Lessons link to each other, so the library can grow in any direction instead of following a fixed course.

## How it's organised

```
index.html                 the Glitch'n home page: what Glitch'n is, the way into the lessons, where it started
home/                      the home page's drum-machine clip and its poster picture
site.css, site.js          shared by the home page and other site pages: top bar (logo, pages, language), buttons, footer
about/
  index.html               About: an executive summary for donors (why, how, results, milestones, team, publications, funding)
  img/                     the About page's photos (team headshots in img/people/)
materials/
  index.html               "Materials": how many kits, 1 buy (one DigiKey cart), 2 print, 3 pop-up (optional), share
  kit.json                 the kit list: quantities and stores for each part (edit by hand)
downloads/                 files to download: chip labels, chip maps (pinout cards), posters and table signs, stickers, logos, colors,
                           and glitchn-pack.zip with all of them (made by tools/make_pack.py)
player/player.js, .css     the one lesson player every lesson page uses
parts-art.js               the part pictures, shared by the Materials page and the lessons' parts lists
lessons/
  index.html               the lesson library: lesson cards, the map of all lessons, what's coming
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

`kind` is `next`, `variation` or `related` (any short word works and shows on the map). The lesson library and each lesson's "What's next?" panel draw the map from these links, so connecting a new lesson means editing only that lesson, or the lesson that should point to it.

## What a lesson needs, teaches and asks of you

Each `lesson.json` also describes the lesson, so the lesson library can label and filter the lessons and each lesson page can show a parts list:

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

In the lesson library, each lesson card can also unfold its steps ("See the 7 steps"): each step's title with a picture of the board as that step ends, linking straight to that step (`#step-3` at the end of a lesson's address opens it at step 3). `build_index.py` copies the step titles and pictures into `lessons/index.json`, and the pictures load only when someone opens the list.

`tools/build_index.py` checks every key against the catalog and every `requires` against the real lessons, and copies the catalog and the ratings into `lessons/index.json`.

## Simple and Technical words

Every page has a **Simple | Technical** switch next to the language buttons. **Simple** (the default) uses plain words for kids: "wire" for jumper, "knob" for trimmer, "light" for LED, "the minus (−) row" for ground, and so on. **Technical** shows the real names. Kids can switch back and forth as they learn the real names. The choice is remembered, and a link can set it with `?words=technical` or `?words=simple`.

- Each lesson's simple text lives beside it in `lesson.simple.json`: every technical English line from `lesson.json` with its simple English (`en`) and simple Spanish (`es`) version. A line with no simple version shows as it is, so editing a lesson never breaks Simple mode; `tools/build_index.py` lists lines that still need a simple version.
- Lesson titles stay the same in both modes. Chip numbers stay too, because they're printed on the chips.
- In Simple mode, the parts list shows a plain name and what each part is or does; in Technical mode, the real name and the kit part number. These come from the `simple` entries in `lessons/catalog.json`, which also give plain names for the concepts.
- The wording rules and the English/Spanish glossary are in `tools/simple-words.md`. Ask Claude to write or update a lesson's `lesson.simple.json` when its text changes.

## Spanish (and other languages)

Visitors can switch between **English** and **Español** on every page. The choice is remembered, Spanish-language browsers start in Spanish, and a link can force a language with `?lang=es` (useful when embedding a lesson in Spanish).

- Interface wording (buttons, labels, messages) lives in `player/player.js`, `lessons/index.html` and the home page `index.html`, each in a small table with `en` and `es` entries.
- Each lesson's Spanish text lives beside it in `lesson.es.json`: a list of English lines with their translations. A line with no translation shows in English, so editing a lesson never breaks its Spanish version. `tools/build_index.py` lists lines that still need translating.
- The step editor stays English-only. When a lesson is ready, ask Claude to write or update its `lesson.es.json`.
- Spanish pages are marked "Traducción automática" (automatic translation) until a Spanish speaker reviews them. To mark a reviewed lesson, set `"reviewed": true` in its `lesson.es.json`.
- Planned lessons carry their Spanish titles in `lessons/planned.json` under `"i18n"`.

To add another language later, add its column to the two interface tables and a `lesson.<code>.json` file per lesson.

## Styles

Every page has a **Style** menu that changes the page's whole personality, not just its colours. The choice is remembered across pages, and a link can force one with `?style=treehouse` (for example).

- **Simple** (the default): the Glitch'n house style, the same look as the rest of the site: white and cream, the logo blue and pink, Manrope, the site header with a thin coral rule, flat colour, no TV cabinet, and fewer words on screen (no keyboard hints, legend or concept list). Old `?style=tv` links and saved TV choices open in Simple.
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

**Where styles live:** `player/player.css` holds the shared layout and the old TV look the styles build on. Each style is one file in `styles/` (`simple.css`, `clean.css`, `gadget.css`, `solarpunk.css` and so on) that styles both the lesson player and the lesson library (the Glitch'n home page keeps one fixed look). `styles/all.css` loads them all, along with their fonts.

**Things a style can use:** the player adds the class `is-playing` to `.app` while the video plays, sets `--played` (0 to 1) on `.app` as it goes (for the player itself, not decorations; see rule 2), and has a spare decoration slot `.deco` (five empty `<i>` elements) inside the TV. The drawings are SVG pictures written into the CSS; the files in `styles/` are the ones to edit, and `tools/style_art.py` keeps the sources of the original drawings.

**To add a style** (Cartoon, say):
1. Copy a file in `styles/` to `styles/cartoon.css` and change `data-style="…"` throughout. Start with the colour and font tokens at the top, then restyle the parts.
2. Add `@import url("cartoon.css");` to `styles/all.css`, and add any new fonts to its first line.
3. Add `'cartoon'` to the `STYLES` list in `player/player.js` and in `lessons/index.html`, and its menu name (`style_cartoon`) to the English and Spanish word lists in both files.

## Status

All five lessons from the original five-day course are up, as drafts for the Glitch'n team to review: step text, parts lists and difficulty ratings included.

The site is plain HTML with no build step, published with GitHub Pages from the `main` branch.

## Materials (materials/)

`materials/index.html` is for the adults who set Glitch'n up, so it explains more than the rest of the site. One number drives it: **how many kits** (kept in the address as `?kits=` and in the browser). A switch, **I'm hosting a pop-up event** (`?popup=1`), adds the pop-up section. Sections: **1 Buy** (one button fills a DigiKey cart with every part in the right amounts; "Also get" for what isn't in it; a note on screens; the kit in pictures; other stores with copyable lists and a CSV), **2 Print** (chip labels: must print; chip maps: recommended; with how-to steps and how many to print), **3 Pop-up** (only when switched on: the three zones, a room layout, a checklist, posters, table signs, stickers), **Share** (the Glitch'n pack zip). Each lesson's parts list and the lesson library link here.

- **The DigiKey cart** is a FastAdd link (`https://www.digikey.com/classic/ordering/fastadd.aspx?part1=…&qty1=…`) built from the `dk` field of each kit row: `dk.pn` is the DigiKey part number and `dk.per` the pieces in one DigiKey unit. Every `dk` number was checked in stock on 2026-10-18; the resistors, capacitors and diode are generic equivalents because DigiKey had the Adafruit packs on backorder. A wrong part number makes DigiKey stop on an error page, so check new numbers by opening the link. For bigger orders DigiKey may first show a "better value" page; the page tells buyers to press Submit there.
- **The kit list** is `materials/kit.json`: each row names a part (`key`, a `lessons/catalog.json` key where there is one), how many are in one full kit (`qty`), where else to buy it (`buy`, with `per` for packs) and its DigiKey number (`dk`). A row with no store shows "Any store".
- **The part pictures** are in `parts-art.js` at the site root (`GlitchnParts.picture(key)`), one small SVG per kit/catalog key; chips are drawn with their real pin count (40106: 14, the others: 16). The What you need page and every lesson's parts list use them (the player loads `parts-art.js` itself). A new part needs a picture there, and a short name in `NAMES` on the What you need page.
- **Chip labels** (`downloads/glitchn-chip-labels.pdf`) are made by `python3 tools/make_labels.py`: 13 × 5.6 mm labels for the top of a 14-pin chip, with the Glitch'n logo and "© Glitch'n" on the sheet.
- **The pack** (`downloads/glitchn-pack.zip`) is made by `python3 tools/make_pack.py` from the files in `downloads/`. Run it after changing any of them.
- **Chip maps, stickers, logos and colors** come from Seth's Design Assets folder. The chip map JPEGs were converted from CMYK to sRGB for screens. The colors sheet has the Glitch'n logo added.
- **Posters and table signs** (`downloads/posters/`) are Seth's print PDFs with the NSF logo removed (2026-10-18; the logo's drawing was taken out of each file, not covered). The "Feeling curious?" poster still names NSF support and the old school name in its small print.

## Glitch'n Radio (radio/)

A "Radio" button in the bottom-right corner of every page (home, lessons, each lesson, materials, about) opens a small player
with three channels of music from Audiobulb Records: **Listen** (glitchier electronic music, with how it was made),
**Play along** (slow textures with no beat, to play a circuit over) and **Calm**.

- `radio/tracks.js` is the playlist: each track's SoundCloud id and address on soundcloud.com/audiobulb, artist, title,
  cover picture, a two-line note (English and Spanish) retold from what the label published with the track, and
  optionally the lesson that teaches the idea. To add a track, copy an entry; the id is in the track page's source
  (`"id":` in the sound data) or in the SoundCloud share/embed code.
- `radio/radio.js` draws the button, the player and the "now playing" card, and drives SoundCloud's embedded player
  (its widget API). Nothing loads from SoundCloud until someone opens the radio; the player loads then, paused, so
  pressing play starts it straight from the tap (Safari plays silently otherwise). The player stays visible as a thin
  SoundCloud bar inside the panel, which keeps SoundCloud's credit on the page.
- Moving between pages, it remembers the track and the spot (for this browser tab) and picks up there. If a browser
  won't start sound on its own on the new page, the button turns pink and says Resume. Safari and iPhones/iPads
  always get Resume: there, sound may only start from a tap.
- The pages load it with one line before `</body>`; lesson pages get it from `player/player.js`.

## After changing CSS or JS

Run `python3 tools/bump_version.py`. It stamps a new `?v=` on every link to the site's own CSS and JS (pages, `styles/all.css` imports, the lesson page template in `tools/build_index.py`, and the parts pictures loaded by the player), so browsers fetch the new files right away instead of a copy they kept for up to 10 minutes.

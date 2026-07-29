# Hitstar Bingo

A randomized 5×5 colour bingo card for the web. Pick your own colours, tap fields to mark
them off, and the app spots a completed row, column or diagonal for you.

No framework, no build step, no npm install — it is plain HTML/CSS/JS. Open `index.html`
and it runs.

## Features

- **Randomized 5×5 card** drawn from your own set of colours.
- **Your colours, your rules** — add, edit (native colour picker) and remove colours,
  2 to 12 of them. Five presets included.
- **Tap to mark off**, tap again to undo. A tick appears in black or white, whichever
  is readable on that colour.
- **Bingo detection** — rows, columns and both diagonals. The winning line lights up,
  "BINGO!" flashes over the card with confetti and a short vibration.
- **Big text field under the card** — type anything (the round, the current song, a rule)
  and it scales up to the largest size that still fits, so it can be read from across the
  table.
- **Fullscreen** — expand the field to the whole display when the text needs to reach the
  far end of the table.
- **Draw on it** — finger or stylus, over the text if you like, with undo and a real eraser.
- **Everything is saved on the device** — card, marks, colours, text and settings survive
  a reload or an accidentally closed tab.
- **Installable and offline capable** (PWA) — add to the home screen, works with no
  connection at the party.
- Dark and light mode, follows the phone's setting. Fits any screen without scrolling.

## Card options

| Option | What it does |
| --- | --- |
| Even distribution | Every colour gets the same share of the 25 fields (with 5 colours: exactly 5 each). Off = each field is drawn independently, so the counts wobble. |
| Avoid neighbouring twins | Re-draws the card a few times and keeps the one where the fewest identical colours touch, so it looks properly mixed. |
| Vibration | Short buzz when marking a field. Ignored on iOS, which does not support the vibration API. |

## The field under the card

The panel under the card shows its text as large as it will go: one word fills the panel, a
long sentence wraps and shrinks. Useful for the round number, the song being guessed, or the
house rule currently in force — anything the whole table needs to read at once. You can also
draw on it.

The buttons in its top-right corner, left to right:

| Button | What it does |
| --- | --- |
| Pen / keyboard | Switches between typing and drawing. Text and drawing are both visible either way; this only decides what your finger does. |
| Undo | Draw mode only. Steps back one stroke. |
| Eraser | Draw mode only. Rubs out the parts of a stroke you drag over, rather than whole strokes. Tap it again to go back to drawing. |
| Expand / shrink | Fullscreen and back. Escape also leaves fullscreen. |
| × | Clears whichever layer you are in — the text in typing mode, the drawing in draw mode. |

Notes on behaviour:

- Text is independent of the card, so clearing the marks leaves it alone. Dealing a **new
  card** does clear the drawing, since it belongs to the round that just ended — the
  confirmation prompt says so.
- To clear the card's marks, use *Clear all marks* in the settings sheet.
- The pen follows the text colour, so it flips with light and dark mode.
- In fullscreen, **text** grows to fill whatever space there is. A **drawing** scales with
  the field's *width*, which keeps its shape from distorting — so in portrait it grows only
  a little (the width barely changes) and is centred vertically. Turn the phone landscape
  and it roughly doubles. That is the trick for showing something to the whole table.
- A drawing made fullscreen can be taller than the small panel; it is kept in full and
  reappears when you expand again, but it is cropped while minimised.

## Running it

**Locally** — just open `index.html` in a browser. Double-click works, `file://` works.
Only the install/offline part needs a real server (browsers do not allow service workers
on `file://`); everything else, including saving your card, works either way.

To have the full PWA locally:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

**On your phone via GitHub Pages** (the "no big deployment" route):

1. Push this repository to GitHub.
2. Repo → *Settings* → *Pages* → Source: *Deploy from a branch*, pick the branch and `/ (root)`.
3. Open `https://<user>.github.io/<repo>/` on your phone, then *Add to home screen*.

Any static host works the same way — Netlify drop, Vercel, a USB stick, your own web space.
There is nothing to compile.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole app: markup, styles, logic. Self-contained. |
| `manifest.webmanifest` | Name, colours and icons for "add to home screen". |
| `sw.js` | Service worker; caches the app for offline use. |
| `icons/` | App icons (PNG, generated). |
| `tools/make_icons.py` | Regenerates the icons — pure Python, no dependencies. |

## Notes for hacking on it

- Changed something and the phone still shows the old version? Bump `CACHE` in `sw.js`
  (`hitstar-bingo-v4` → `-v5`); the old cache is dropped on the next visit.
- The text is fitted by binary-searching the font size against a hidden measuring element.
  Three traps live here, all commented in the source:
  1. That element shares its typography with the textarea through one CSS rule
     (`#note, #note-measure`). Copying font properties in JS instead makes the fitted size
     oscillate, because a computed `line-height` or `letter-spacing` is relative to the font
     size being measured.
  2. It measures against a box two pixels narrower than the textarea (`SAFE`). A textarea
     wraps marginally earlier than a div, and the search converges on exactly the size where
     that flips a line break.
  3. The textarea is `overflow: hidden` unless the text does not fit even at the minimum
     size. A classic scrollbar appearing mid-fit steals width, re-wraps the text and
     invalidates the measurement.
- Strokes are flat `[x0,y0,x1,y1,…]` arrays with **both** axes divided by the field's
  *width*, so no stroke distorts when the field changes shape. `centreInk()` then offsets
  them vertically, and is deliberately only called on a layout change — recomputing it
  per stroke would make the drawing crawl as you draw.
- Saved state lives in `localStorage` under `hitstar-bingo-v1`. Clearing site data resets
  everything to the default palette.
- Deleting a colour does not damage a card already in play — those fields keep the colour
  they were dealt. Editing a colour recolours the running card immediately.
- The starting palette and the presets are the `PRESETS` array at the top of the script.

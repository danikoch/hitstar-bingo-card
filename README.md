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
  table. A clear button (×) wipes it in one tap.
- **Legend** under the card counting how many fields of each colour you already got (e.g. `3/5`).
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

## The text field

The panel under the card is a plain text box that always shows its content as large as it
will go: one word fills the panel, a long sentence wraps and shrinks. Useful for the round
number, the song being guessed, or the house rule currently in force — anything the whole
table needs to read at once.

- Tap it to type. Enter makes a new line.
- The × in the corner clears it. It only appears when there is something to clear.
- The text is independent of the card: dealing a new card or clearing the marks leaves it
  alone.
- To clear the *card* instead, use *Clear all marks* in the settings sheet.

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
  (`hitstar-bingo-v2` → `-v3`); the old cache is dropped on the next visit.
- The text is fitted by binary-searching the font size against a hidden measuring element.
  That element shares its typography with the textarea through one CSS rule
  (`#note, #note-measure`) — do not copy font properties in JS instead, because a computed
  `line-height` or `letter-spacing` is relative to the current font size and makes the
  fitted size oscillate.
- Saved state lives in `localStorage` under `hitstar-bingo-v1`. Clearing site data resets
  everything to the default palette.
- Deleting a colour does not damage a card already in play — those fields keep the colour
  they were dealt. Editing a colour recolours the running card immediately.
- The starting palette and the presets are the `PRESETS` array at the top of the script.

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
- **Legend** under the card counting how many fields of each colour you already got (e.g. `3/5`).
- **Everything is saved on the device** — card, marks, colours and settings survive a
  reload or an accidentally closed tab.
- **Installable and offline capable** (PWA) — add to the home screen, works with no
  connection at the party.
- Dark and light mode, follows the phone's setting. Fits any screen without scrolling.

## Card options

| Option | What it does |
| --- | --- |
| Even distribution | Every colour gets the same share of the 25 fields (with 5 colours: exactly 5 each). Off = each field is drawn independently, so the counts wobble. |
| Avoid neighbouring twins | Re-draws the card a few times and keeps the one where the fewest identical colours touch, so it looks properly mixed. |
| Vibration | Short buzz when marking a field. Ignored on iOS, which does not support the vibration API. |

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
  (`hitstar-bingo-v1` → `-v2`); the old cache is dropped on the next visit.
- Saved state lives in `localStorage` under `hitstar-bingo-v1`. Clearing site data resets
  everything to the default palette.
- Deleting a colour does not damage a card already in play — those fields keep the colour
  they were dealt. Editing a colour recolours the running card immediately.
- The starting palette and the presets are the `PRESETS` array at the top of the script.

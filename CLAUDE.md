# Working on this repository

## Branches

**Every feature or fix starts on its own branch, cut fresh from `main`.**

```bash
git fetch origin main
git checkout -b claude/<short-feature-name> origin/main
```

Never continue on a branch whose pull request has already been merged — a merged pull request
is finished and cannot carry new work. Follow-up work, however small, is a new branch off the
current `main`, even when the previous branch is still checked out.

Check before starting, since a branch can be merged without the local clone knowing:

```bash
git fetch origin main && git log --oneline origin/main..HEAD
```

Anything listed there is unmerged. If the branch's own commits are already in `main` and only
new work is left, move that work to a fresh branch (`git cherry-pick`) rather than pushing to
the merged one.

Do not merge to `main` or open a pull request unless asked.

## Verifying changes

There is no build step and no test runner in the repository — the app is `index.html` and it
runs by opening it. Changes are checked by driving the real page in a browser (Playwright
against a local `python3 -m http.server`), not by reading the diff. Worth covering:

- **A phone viewport in both orientations**, since the layout switches at 620px wide, and both
  dark and light mode.
- **A sandboxed iframe**, which is how the app runs when embedded. Modal dialogs (`confirm`,
  `alert`) and the Fullscreen API are refused there — that is how the new-card button came to
  do nothing at all, so no code may depend on them.
- **Anything that measures and resizes.** Text fitting and the grid layouts have produced
  several feedback loops where a box is sized from its content and its content from the box.
  `README.md` lists the ones already designed out, under "Notes for hacking on it"; read it
  before touching `fitNote()`, `fitBand()`, `fit()` or `fitWheel()`.

Bump `CACHE` in `sw.js` whenever a cached file changes, or installed copies keep the old
version.

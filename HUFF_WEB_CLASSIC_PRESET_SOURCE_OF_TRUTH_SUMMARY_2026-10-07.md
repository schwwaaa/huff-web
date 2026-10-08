# HUFF Web Classic — Preset Source-of-Truth Fix

## Problem

The preset catalog merged three sources at load: `presets/manifest.json`, a server directory listing, and the GitHub `presets/` directory. Because those sources were merged, a preset removed from the actual folder could remain visible if it was still listed in the manifest or still present in another discovery source.

## Fix

Preset discovery now selects one authoritative source instead of merging stale entries:

- **Local development with a directory listing:** the live `presets/` folder is authoritative. Additions and deletions are reflected on reload, including an empty folder.
- **Deployed web build:** the GitHub `presets/` directory is authoritative when the GitHub directory request succeeds. Adding or deleting a preset in the repository is reflected after reload.
- **Fallback hosting:** if neither authoritative source is available, `manifest.json` is treated only as a candidate index. Every listed preset is fetched with cache disabled and parsed before it is allowed into the menu. Missing/deleted files are discarded.

The repository preset map is cleared before each refresh, so removed entries do not survive an in-page catalog refresh.

## Files changed

- `canvas.js`

## Validation

- `canvas.js` syntax: PASS
- all first-party JavaScript syntax checks: PASS
- local package linkages: 18/18 PASS
- current preset JSON count: 63
- current manifest entry count: 63
- current stale manifest entries: 0

No playback, effects, camera, canvas-window, screenshot, CSS, or 60 fps behavior was changed.

# HUFF Web Classic — Preset Manifest Authority Fix

## Problem

HUFF was still showing the older preset catalog even after `presets/manifest.json` had been replaced.

The loader was fetching all discovery sources in parallel and, on a deployed/non-localhost page, **GitHub directory discovery had higher priority than the manifest**. If the GitHub repository still exposed the older preset set, the GUI ignored the new manifest and rebuilt the old menu.

The uploaded current `presets/` folder also contained a stale manifest listing the former factory/Preset-number files rather than the 19 JSON files actually present.

## Fix

- `presets/manifest.json` is now the canonical preset catalog whenever it exists.
- Every manifest entry is fetched and parsed before it is shown, so a filename that no longer resolves cannot remain visible from the manifest.
- Local directory enumeration is now a fallback used only when no manifest is available.
- GitHub Contents API discovery is now a fallback used only when no manifest is available.
- Repository preset menu labels remain based on the catalog/filename. Recalling a renamed preset no longer replaces the visible label with an older internal `name` stored inside the JSON document.
- Rebuilt `presets/manifest.json` from the uploaded current preset folder: **19 presets**.
- Added `presets/update_manifest.py` to rebuild the manifest from the folder at any time.

## Manifest updater

From the `presets/` folder:

```bash
python3 update_manifest.py
```

The script:

- scans every visible `*.json` beside it;
- ignores `manifest.json`;
- validates every preset file before changing the manifest;
- uses the filename stem as the public menu name;
- adds new files and removes deleted files;
- naturally sorts entries;
- preserves repository/branch metadata;
- writes the manifest atomically.

## Current preset catalog

19 preset files are present and the manifest matches them exactly.

## Verification

- `canvas.js`: JavaScript syntax PASS
- other first-party JavaScript: syntax PASS
- manifest: 19 entries / 19 current preset files PASS
- every listed preset JSON parses PASS
- second updater run reports manifest already current PASS
- package linkage verifier PASS

No effect, playback, camera, WINDOW, fullscreen, screenshot, or 60 fps behavior was intentionally changed.

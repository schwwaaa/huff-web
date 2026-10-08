# HUFF Web Classic — Scroll Fix

## Cause
The feature rename `Flow` → `Sift` was applied too broadly and changed the CSS property `overflow-y` into the invalid property `oversift-y` in both `css/huff.css` and `css/huff.min.css`.

The GUI shell intentionally keeps `html, body { overflow: hidden; }` because the fixed HUFF panel is the scrolling container. The panel therefore depends on `header { overflow-y: auto; }`. Once that property was corrupted, the panel could no longer scroll.

## Fix
- Restored `overflow-y: auto` in `css/huff.css`.
- Restored `overflow-y: auto` in `css/huff.min.css`.
- Audited first-party source for other accidental embedded `Sift` substitutions caused by the rename.
- No playback, effect, preset, canvas-window, fullscreen, or UI-layout logic was changed.

## Verification
- No `oversift` token remains in first-party source.
- `overflow-y: auto` is present in both shipped HUFF stylesheets.
- Existing package linkage verifier passes.
- First-party JavaScript syntax checks pass.

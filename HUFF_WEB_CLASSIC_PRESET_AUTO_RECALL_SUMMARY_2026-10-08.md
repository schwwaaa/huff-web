# HUFF Web Classic — Preset Auto Recall

## Change

Preset selection now recalls the selected preset immediately.

- Removed the `RECALL` button from the Presets UI.
- Added a `change` listener to `#presetList`.
- Choosing any valid built-in, catalog, legacy, or session preset calls the existing `recallPresetSelection()` path.
- The placeholder (`— choose preset —`) does not trigger recall.
- SAVE FILE and LOAD FILE behavior is unchanged.
- Preset application, undo snapshotting, status text, and toast behavior continue to use the existing recall function.

## Validation

- `canvas.js` passes JavaScript syntax validation.
- No `presetBuiltinLoadBtn` references remain in first-party source.
- No RECALL button remains in `index.html`.
- Local HTML/CSS asset linkage audit passes with zero missing references.

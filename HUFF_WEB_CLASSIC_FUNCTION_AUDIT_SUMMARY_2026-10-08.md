# HUFF Web Classic — Function Response Audit

Scope: first-party Web Classic controls and effect/runtime functions. The review focused on controls that are wired but can appear inactive because of transfer curves, endpoint handling, integer coercion, conditional routing, or neutral-state shortcuts.

## Corrections

1. **Vista stencil threshold accepted 0 in the UI but not in the runtime.**
   The runtime used `Number(value) || 128`, so a valid threshold of `0` silently became `128`. It now uses an explicit finite-number check, preserving all values from 0 through 255.

2. **Vista Glitch Size control granularity did not match the runtime.**
   Runtime tile size is integer-valued, but the slider exposed 0.01 increments. The slider now uses step 1 so each user-visible step can change the rendered state.

3. **Vista Smear control granularity did not match the runtime.**
   Smear is a count of repeated stamps and is integer-valued in the renderer, but the slider exposed 0.01 increments. The slider now uses step 1.

## Reviewed and confirmed

- Vista density, drift, speed, history depth, depth scatter, jitter, opacity, XYZ, update modes, cluster controls, and stencil routing all reach the renderer.
- Paneling BANDS and FIELD controls are routed to their intended modes. Mode-specific controls are intentionally inactive outside their associated layout.
- Feedback amount, persistence, transform, strobe, and restore controls are wired. Neutral transform states are intentionally skipped by the activity planner.
- Sift strength, scale, speed, pulse, implode, swirl, turbulence, and spread are wired. Strength 0 is intentionally neutral.
- Symmetry axes, direction, mix, split positions, and flips are wired. Edge split positions can intentionally become visually neutral.
- Solarize THRESHOLD, LUMA QUANTIZE, and CHROMA POSTERIZE controls are wired. Neutral endpoints are intentionally bypassed. CHROMA POSTERIZE uses the corrected exponential level mapping in both GPU and CPU paths.
- Pipeline Luma Key target, source, clip, gain, invert, cleanup, density, fade, and mix are wired.
- Global Mix amount, curve, blend, and insertion position are wired.
- History depth, source playback, camera controls, preset recall, screenshots, and detached WINDOW output remain connected.

## Static verification

- 191 first-party UI controls/buttons/selects were checked for code references; no orphan control IDs were found.
- No remaining render-control `Number(value) || nonzero-default` pattern was found after the Vista threshold correction.
- All preset JSON files parse successfully.
- First-party JavaScript syntax passes.
- Local asset linkage verification passes: 18/18.

No effect algorithms were redesigned in this audit. Corrections are limited to concrete control-response mismatches.

# Git commit message

```text
feat(web): finalize HUFF Web Classic browser build and project documentation

Refine HUFF Web Classic as a dedicated 720p browser video instrument and document
the current application as a web project rather than as a record of development
iterations.

- define Web Classic around a fixed 1280x720 processing surface for consistent
  temporal-history cost, preset behavior, and browser performance
- retain file and camera sources with playback transport, looping, seek, rate,
  volume, base-video mix, and source-status controls
- preserve the constrained HUFF effect system: Corrupt, Feedback, Scanlines,
  Luma Key, Global Mix, Flow, Symmetry, Solarize, and validated pipeline recipes
- keep the detached WINDOW output as the single external presentation path
- allow the detached canvas itself to enter true fullscreen by click or F while
  leaving the main HUFF control page outside fullscreen
- target the detached output transport at 60 fps with one-frame-in-flight
  backpressure so slow encode/decode cycles drop frames instead of accumulating
  latency
- keep the internal renderer at 720p while allowing the output canvas to scale
  to the available display size
- provide direct PNG capture for 16:9 1280x720, centered 4:3 960x720, and 9:16
  720x1280 output formats
- remove Syphon, Spout, MIDI, and OSC from the Web Classic interface and runtime
- remove source-fit and user seed controls that are not meaningful in this web
  edition; generate a fresh internal seed when the page loads
- keep the HUFF logo as the About control and present project, creator, company,
  copyright, and repository information in the desktop-style About dialog
- split interface and canvas styling into standalone readable CSS files with
  minified production counterparts
- correct CSS and image asset paths after stylesheet extraction and retain the
  linkage verifier for packaging checks
- dynamically discover repository presets at startup from a local directory
  index when available, presets/manifest.json, and the public GitHub presets
  directory
- lazily fetch repository preset JSON only when recalled and expose
  refreshHuffPresetCatalog() for manual catalog refresh during development
- keep portable JSON save/load behavior and session-loaded preset recall
- rewrite first-party source comments as application documentation covering
  resource ownership, timing, data flow, compatibility, and performance rules
  without development-history annotations
- replace the minimal README with Web Classic-specific project documentation
  covering features, architecture, sources, effects, presets, output transport,
  deployment, browser constraints, unsupported native capabilities, performance
  expectations, UI caveats, and troubleshooting

Web Classic remains intentionally browser-native: it does not provide native
texture sharing, MIDI/OSC integration, unrestricted filesystem access, or
1080p/4K processing. Browser fullscreen, popup, camera, codec, autoplay,
background scheduling, and hardware-acceleration policies remain controlled by
the host browser and operating system.
```

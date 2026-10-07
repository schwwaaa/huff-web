<p align="center">
  <img src="icon-name.jpg" width="220" alt="HUFF logo">
</p>

<h1 align="center">HUFF Web Classic</h1>

<p align="center">
  <strong>Real-time browser video corruption, feedback, compositing, and image transformation.</strong><br>
  Fixed 1280×720 processing · camera + local video files · detachable output window · portable JSON presets
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-Web%20Classic-ff4444?style=flat-square" alt="Web Classic">
  <img src="https://img.shields.io/badge/processing-1280%C3%97720-lightgrey?style=flat-square" alt="1280x720 processing">
  <img src="https://img.shields.io/badge/runtime-browser-blue?style=flat-square" alt="Browser runtime">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT license">
</p>

---

## What is HUFF Web Classic?

HUFF Web Classic is a browser-native version of HUFF: a real-time video instrument for temporal corruption, feedback, scan processing, luma compositing, symmetry, solarization, flow warping, and live image transformation.

Load a video file or select a camera, then process the source through a deliberately constrained serial pipeline. The interface is designed as an instrument rather than a generic editor: controls stay visible, effects remain immediately playable, presets can recall complete operating states, and the rendered image can be moved into a dedicated output window for projection, capture, or fullscreen display.

The Web Classic build is intentionally fixed at **1280×720 processing resolution**. Window size and monitor resolution affect presentation only; they do not change the internal processing surface.

**Creator:** Christopher Konopka  
**Company:** schwwaaa  
**Copyright:** © 2026 schwwaaa  
**Repository:** https://github.com/schwwaaa/huff-web

---

## Table of Contents

- [Features](#features)
- [What the Web Version Does Not Include](#what-the-web-version-does-not-include)
- [Running HUFF Web Classic](#running-huff-web-classic)
- [Sources and Playback](#sources-and-playback)
- [Effect Pipeline](#effect-pipeline)
- [Interface](#interface)
- [Output Window and Fullscreen](#output-window-and-fullscreen)
- [Screenshots](#screenshots)
- [Presets](#presets)
- [Architecture](#architecture)
- [Performance Model](#performance-model)
- [Browser and Web Limitations](#browser-and-web-limitations)
- [Deployment Notes](#deployment-notes)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- **720p real-time processing** — the instrument always processes at 1280×720 for a predictable browser workload and consistent preset behavior.
- **Video-file input** — load local video files through the browser file picker, with play, pause, looping, seek, playback-rate, and volume controls.
- **Camera input** — enumerate available cameras, start/stop capture, and switch devices without leaving the application.
- **Temporal frame history** — recent decoded frames are kept in a bounded reusable frame ring for corruption, history sampling, trails, scan processing, and other time-based operations.
- **Corrupt** — temporal patch displacement with random or clustered placement, temporal depth, spatial distribution, smear, repeat, motion, and composite controls.
- **Feedback** — recursively return the previous composite with translation, zoom, rotation, persistence, and memory behavior.
- **Scanlines** — horizontal or field-style scan processing with displacement, band sizing, drift, skew, gap, opacity, and related motion controls.
- **Luma Key** — live or captured-stencil luminance keying that can target the composite, Corrupt, or Scanlines.
- **Global Mix** — reintroduce clean source imagery at selectable locations in the processing chain using multiple blend modes.
- **Flow** — tiled spatial distortion driven by a noise field, temporal pulse/history sampling, implosion, swirl, turbulence, and spread controls.
- **Symmetry** — vertical, horizontal, or combined mirroring with independent source behavior and axis controls.
- **Solarize** — threshold solarization plus luminance-quantize and chroma-posterize modes.
- **Pipeline recipes** — switch among validated serial stage orders without exposing an unrestricted node graph.
- **Layer priority** — choose whether Scanlines or Corrupt/Luma is painted last at the front stage.
- **Portable JSON presets** — save, load, recall, and dynamically discover presets.
- **Repository preset discovery** — preset files pushed to the `presets/` directory in the public repository can appear in the website menu after reload without hard-coding filenames into the UI.
- **Dedicated output window** — open the rendered canvas in a separate browser window and enter true canvas fullscreen from that window.
- **60 Hz output target** — the detached output transport targets up to 60 frames per second and drops work rather than building a queue when the browser cannot keep up.
- **PNG capture** — export the current processed image as 16:9, 4:3, or 9:16 stills.
- **Windows 98/2000-inspired interface** — compact control groups, direct manipulation, collapsible panels, and an About dialog accessible from the HUFF logo.

---

## What the Web Version Does Not Include

Web Classic is deliberately narrower than a native desktop build.

It does **not** include:

- Syphon output;
- Spout output;
- MIDI input or mapping;
- OSC input or mapping;
- native GPU texture sharing with another application;
- unrestricted filesystem access;
- automatic enumeration of arbitrary server folders when the web server does not expose a directory index;
- native application-window control beyond what the browser permits;
- 1080p or 4K processing modes;
- a guarantee of 60 fps on every browser, GPU, source codec, or effect combination.

For external routing, use normal browser/window capture, display capture, OBS capture, or another capture path supported by the host operating system and browser.

---

## Running HUFF Web Classic

HUFF is a static browser application. It should be served over HTTP rather than opened directly with `file://` URLs.

### Quick local server

From the repository root:

```bash
python3 -m http.server 9999
```

Then open:

```text
http://localhost:9999/
```

Any normal static web server can be used instead.

### Recommended browser

A current Chromium-based browser is the primary target because HUFF makes extensive use of modern browser media and graphics APIs such as:

- Canvas2D;
- `requestAnimationFrame()`;
- `requestVideoFrameCallback()` when available;
- `createImageBitmap()`;
- `BroadcastChannel`;
- Web Workers;
- `OffscreenCanvas` when available;
- the Fullscreen API;
- `getUserMedia()` for cameras.

Other browsers may work, but behavior and performance can differ by implementation.

---

## Sources and Playback

### Video files

Use **SOURCE → FILE** to select a local video.

Available playback controls include:

- Play;
- Pause;
- Loop;
- Seek;
- 0.25×, 0.5×, 1×, 2×, and 4× playback rates;
- Volume;
- Base Video enable;
- Base Mix;
- Base background color.

The browser and operating system determine which codecs can actually be decoded. H.264/AAC MP4 is generally the safest cross-platform source format. MOV, WebM, and other containers/codecs depend on the browser and OS media stack.

### Camera

The Camera controls can:

- enumerate available video-input devices;
- start the selected camera;
- stop capture;
- refresh the camera list.

Camera acquisition requests a maximum of 1280×720 because Web Classic does not need higher-resolution frames internally.

Camera access requires browser permission. On a deployed website, camera capture normally requires **HTTPS**; `localhost` is treated as a secure development context by modern browsers.

---

## Effect Pipeline

HUFF uses a constrained serial image pipeline rather than an unrestricted node graph.

The default Classic relationship is:

```text
SOURCE
   ↓
FRONT-STAGE IMAGE FEED
Corrupt / Luma / Scanlines
   ↓
FEEDBACK
   ↓
FLOW
   ↓
SYMMETRY
   ↓
SOLARIZE
   ↓
OUTPUT
```

**Global Mix** can reintroduce the clean source at selected insertion points. **Layer Priority** determines the stable paint order between Scanlines and the Corrupt/Luma front stage.

The **Pipeline** control exposes a small set of validated serial recipes. Recipes change stage ordering; they do not create arbitrary branches, add hidden effects, or convert HUFF into a general node editor.

### Core image resources

The renderer keeps a deliberately small set of full-resolution working surfaces:

```text
gCur      clean decoded source frame
gBuf      active/persistent composite
gScratch  shared scratch / ping-pong surface
```

A separate bounded frame ring stores reusable historical frames for temporal effects. Additional small scratch surfaces are used only where an effect needs bounded CPU or GPU processing.

---

## Interface

The control surface is organized into collapsible instrument groups.

### Source

File and camera selection, playback transport, loop, rate, seek, volume, base-video controls, background selection, and source status.

### Presets

Recall repository/folder presets, save the current state as JSON, load external JSON preset files, or reset the instrument.

### Pipeline

Choose the active serial recipe and front-stage layer priority. The diagram reflects the currently selected stage order.

### Symmetry

Mirror along vertical, horizontal, or combined axes and control the symmetry relationship.

### Global Mix

Blend clean source imagery back into the processing chain and choose the insertion position.

### Feedback

Control recursive return, persistence, translation, zoom, rotation, and feedback-memory behavior.

### Corrupt

HUFF's temporal corruption system. Controls cover update behavior, temporal depth, regions, cluster distribution, group shape, group motion, patch motion, patch repeat, timing, and composite behavior.

### Luma Key

Shape a live or captured luminance stencil and apply it to the composite, Corrupt, or Scanlines.

### Scanlines

Create displaced scan bands or distributed scan fields with motion, size, shift, skew, gap, and composite controls.

### Solarize

Use threshold solarization, luminance quantization, or chroma posterization with mode-specific shaping controls.

### Flow

Distort the current image through the tiled flow field using strength, scale, pulse, implosion, swirl, turbulence, and related controls.

---

## Output Window and Fullscreen

Press **WINDOW** to open `canvas.html` as the dedicated rendered-output window.

The output window contains only the rendered HUFF canvas. It does not run another effect chain.

While the output is windowed, the browser may display its normal address/origin bar. Web pages cannot reliably remove this browser chrome from a standard popup.

To enter true fullscreen for the **canvas only**:

- click the canvas in the detached output window; or
- press **F** while that output window has focus.

Press **Esc** to leave fullscreen.

The main HUFF GUI is not the fullscreen target.

### Output transport

The main HUFF page and `canvas.html` exchange frames through `BroadcastChannel`.

The presentation path is intentionally independent from the internal 1280×720 processing resolution:

```text
HUFF render canvas
      ↓
ImageBitmap capture
      ↓
worker-assisted scale / JPEG encode when available
      ↓
BroadcastChannel
      ↓
canvas.html
      ↓
ImageBitmap decode
      ↓
output canvas / fullscreen presentation
```

The stream targets **60 fps** and uses a one-frame-in-flight policy. If encoding, transport, or decoding falls behind, frames are dropped instead of queued. This keeps latency bounded.

The output window is therefore a presentation mirror, not a second renderer.

---

## Screenshots

The top bar includes three PNG capture buttons:

| Button | Output | Behavior |
|---|---:|---|
| **SHOT 16:9** | 1280×720 | Saves the full processed canvas. |
| **SHOT 4:3** | 960×720 | Saves a centered 4:3 crop. |
| **SHOT 9:16** | 720×1280 | Saves a centered 9:16 crop scaled to portrait output. |

Screenshot export operates on the current processed canvas, not on the JPEG-compressed detached-window stream.

---

## Presets

HUFF presets are portable JSON documents containing instrument state. They do not store source video frames or captured stencil pixels.

### Recall

Choose a preset from the menu and press **RECALL**.

### Save

Enter a preset name and press **SAVE FILE…**. The browser downloads a JSON preset file.

### Load

Press **LOAD FILE…** and choose a compatible HUFF preset JSON file. The preset is applied and added to the current session menu.

### Dynamic repository presets

Web Classic does not hard-code every preset filename into `index.html` or `canvas.js`.

At startup it checks:

1. a local `presets/` directory listing when the development server exposes one;
2. `presets/manifest.json` as the deterministic static-host fallback;
3. the public GitHub repository's `presets/` directory.

On the deployed website, GitHub discovery is authoritative when available. This allows a newly pushed JSON preset in `schwwaaa/huff-web/presets/` to appear in the menu after page reload without modifying the application JavaScript.

Preset JSON itself is fetched only when recalled.

For deterministic releases, keep `presets/manifest.json` synchronized with the preset files shipped in the website package. GitHub discovery is still subject to network availability, GitHub API availability, and public API rate limiting.

Developers can manually refresh the catalog from the browser console with:

```js
refreshHuffPresetCatalog()
```

---

## Architecture

```text
huff-web/
├── index.html                    main HUFF control surface
├── canvas.html                   detached output / fullscreen page
├── canvas.js                     source lifecycle, playback, render loop,
│                                 state, presets, output transport
├── effects.js                    image-effect implementations
├── pipeline-runtime.js           validated serial recipe/runtime rules
├── capability-instrumentation.js runtime capability/performance instrumentation
├── mirror-encoder-worker.js      off-main-thread output scaling/JPEG encoding
├── p5.js                         bundled third-party p5.js runtime
│
├── css/
│   ├── huff.css                  readable interface stylesheet
│   ├── huff.min.css              production interface stylesheet
│   ├── canvas.css                readable output-window stylesheet
│   └── canvas.min.css            production output-window stylesheet
│
├── presets/
│   ├── manifest.json             shipped preset catalog fallback
│   └── *.json                    portable HUFF presets
│
├── icon-name.jpg                 HUFF artwork
├── verify-linkages.py            local package/linkage verification
├── LICENSE
└── README.md
```

`ws-mirror.js` and `ws-server.js` remain available as legacy/experimental mirror utilities, but the current Web Classic output window uses the browser-native `BroadcastChannel` path and does not require the localhost WebSocket relay.

---

## Performance Model

HUFF intentionally pushes browser video APIs hard, but its runtime is designed to bound expensive work rather than accumulate it.

### Fixed 720p processing

The render surface is always 1280×720. A full RGBA frame at that size is approximately 3.5 MiB, which keeps temporal history substantially more practical than 1080p in a browser Canvas2D pipeline.

### Decoded-frame scheduling

When supported, `requestVideoFrameCallback()` updates the clean source and temporal history when the video decoder actually produces a new frame. The visual render loop remains display-driven.

### Background rendering

Browsers normally throttle rendering when a page is hidden or unfocused. HUFF uses a small Web Worker heartbeat to keep requesting render work near 60 Hz when the control page loses focus. Browser and operating-system power policies can still impose stronger throttling outside the application's control.

### Frame history

The history ring reuses canvas-backed storage and has a bounded memory budget. Temporal depth therefore depends on processing resolution and the configured history amount rather than growing without limit.

### Effect work

HUFF avoids unnecessary full-frame work where possible through:

- shared scratch surfaces;
- cached geometry/workspaces;
- direct Canvas2D `drawImage()` sampling from frame-history canvases;
- bounded Solarize/Luma processing surfaces;
- effect bypass when a stage cannot visibly change the frame;
- event-cached control state instead of repeated DOM parsing in hot loops.

### Output mirror

The detached output window adds additional capture, encode, transfer, decode, and presentation work. HUFF performs that work only while the output viewer is present and uses one-frame-in-flight backpressure to avoid latency growth.

Actual frame rate depends on the source codec, browser, CPU/GPU, enabled effects, history depth, output-window state, and display refresh rate.

---

## Browser and Web Limitations

These are platform constraints of the Web Classic edition rather than hidden configuration options.

### Browser chrome

A normal `window.open()` output can show an address/origin bar while windowed. Browsers intentionally control this chrome. Use canvas fullscreen from the output window when a clean display is required.

### Fullscreen requires user interaction

Browsers restrict fullscreen requests. Click the detached canvas or press **F** inside its window. The application cannot silently force fullscreen during arbitrary background execution.

### Popup blocking

The **WINDOW** button is a direct user gesture and should normally be allowed, but browser popup policies, extensions, or enterprise settings can still block the detached output.

### Camera security

Camera capture requires permission and normally requires HTTPS on a deployed site. `localhost` is the normal development exception.

### Codec support

HUFF uses the browser's media decoder. A filename extension does not guarantee that the contained codec can be decoded. Browser/OS codec support differs.

### Autoplay restrictions

A browser may require a user gesture before starting media with audio. If autoplay is rejected, press **Play**.

### Background throttling

HUFF includes a background render heartbeat, but browsers and operating systems may reduce timers, video decode, GPU work, or process priority when a tab/window is hidden, minimized, power constrained, or suspended.

### Output frame rate

The output transport targets 60 fps; it is not a promise that every frame will arrive. HUFF intentionally drops late output frames instead of queuing them.

### 720p processing ceiling

The internal engine does not offer 1080p or 4K processing in Web Classic. A fullscreen 4K monitor displays an enlarged 1280×720 result.

### No native texture sharing

A browser cannot expose the processed Web Classic canvas as a native Syphon or Spout texture through this application. Use window/display capture when another program needs the result.

### Filesystem restrictions

A web page cannot freely enumerate a user's local filesystem or arbitrary server directories. HUFF therefore uses explicit file pickers for user files and manifest/GitHub discovery for repository presets.

### GitHub preset discovery

Live repository discovery depends on public network access to GitHub. If that request fails, the shipped `presets/manifest.json` remains the static fallback.

### Browser API variation

`OffscreenCanvas`, ImageBitmap resizing, media timing, fullscreen behavior, and hardware acceleration can vary between browsers and versions. The application contains fallbacks for several paths, but Chromium remains the primary target.

---

## Deployment Notes

HUFF Web Classic can be deployed as a static website.

Recommended deployment requirements:

- serve all files from the same origin;
- use HTTPS for public deployment so camera access is available;
- preserve the `css/` and `presets/` directory structure;
- serve JavaScript, JSON, JPEG, and CSS with normal MIME types;
- do not aggressively cache `presets/manifest.json` if rapid preset updates are important;
- keep the public preset repository configuration in `canvas.js` aligned with the repository used for deployment.

### Preset updates on GitHub

For the current repository configuration:

```text
schwwaaa/huff-web
└── presets/
    └── new-preset.json
```

Push the JSON file to the `main` branch, then reload HUFF. The preset catalog checks GitHub during startup and can surface the new file without rebuilding the menu code.

For a fully deterministic packaged release, also update `presets/manifest.json`.

---

## Troubleshooting

### Preset added to `presets/` but not visible

- Reload the page.
- On localhost, confirm your web server exposes a directory index if you expect automatic local-folder enumeration.
- Confirm the preset appears in `presets/manifest.json`, or push it to the configured GitHub `presets/` directory.
- Open DevTools and run `refreshHuffPresetCatalog()`.
- Check the console for GitHub/network errors.

### Output window does not open

- Allow popups for the HUFF site.
- Press **WINDOW** again; if the viewer already exists, HUFF focuses the existing window.

### Output window is not fullscreen

- Focus the detached canvas window.
- Click the canvas or press **F**.
- Browser chrome remains visible while the popup is merely windowed; this is expected.

### Output feels slower than the main renderer

The detached viewer requires an additional image capture/encode/decode path. Close the output window to remove that transport cost. If the main HUFF interface itself is also slow, reduce expensive effect combinations or temporal-history demand.

### Camera is unavailable

- Confirm camera permission was granted.
- Use HTTPS or `localhost`.
- Press the Camera refresh button after connecting a new device.
- Close other applications that may have exclusive camera ownership.

### Video does not play

- Try H.264/AAC MP4.
- Press **Play** manually if autoplay was blocked.
- Check DevTools for decode/media errors.

### Missing assets / 404 errors

Run the included linkage verifier from the repository root:

```bash
python3 verify-linkages.py
```

The verifier checks local application references after packaging or directory changes.

---

## License

HUFF Web Classic is released under the **MIT License**. See [`LICENSE`](LICENSE).

---

<p align="center">
  <sub>HUFF Web Classic · 720p browser video instrument · © 2026 schwwaaa</sub>
</p>

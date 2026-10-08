# HUFF Web Classic — Playback Optimization Update

## Scope

This update stays inside the existing HUFF Web Classic architecture: browser video/camera input, p5.js + Canvas2D rendering, the existing effect pipeline, 1280×720 processing, the detached WINDOW output, presets, and screenshots.

No effect algorithms or visual parameter behavior were intentionally changed.

## Primary bottleneck addressed

The detached WINDOW output previously used this path while active:

render canvas -> ImageBitmap capture -> Worker JPEG encode -> BroadcastChannel Blob/ArrayBuffer -> JPEG decode -> ImageBitmap -> output canvas

At a 60 fps target this creates continuous encode/decode work in addition to the main HUFF render pipeline. JPEG quality was 0.97, so the output path could consume meaningful CPU/GPU time even though the output window was only reproducing pixels already present on the main render canvas.

## New primary WINDOW transport

The WINDOW output now prefers the browser-native `HTMLCanvasElement.captureStream(60)` path.

The main HUFF canvas is exposed as a live `MediaStream`. The detached `canvas.html` page attaches that stream directly to an output-only `<video>` surface. The browser therefore owns frame delivery between the two same-origin windows.

Primary path:

render canvas -> canvas.captureStream(60) -> MediaStream -> detached output surface

This removes from the normal path:

- per-frame JPEG encoding
- per-frame JPEG decoding
- Blob/ArrayBuffer frame transport
- mirror Worker encoding work
- output-side createImageBitmap reconstruction
- explicit one-frame JPEG acknowledgement scheduling

The existing encoded BroadcastChannel mirror remains intact as a compatibility fallback. If `captureStream()` is unavailable or cannot be attached, `canvas.html` automatically starts the previous encoded mirror transport.

## Fullscreen behavior

Fullscreen still belongs exclusively to the detached output window. In direct-stream mode the output-only video surface enters fullscreen. In fallback mode the output canvas enters fullscreen. The main HUFF controls page is never used as the fullscreen target.

## Stream lifetime

The direct MediaStream exists only while needed by the detached WINDOW viewer. Closing the viewer releases its capture track so the browser does not continue unnecessary canvas-stream work after the output window is gone.

The track is marked with `contentHint = "motion"` when supported.

## Existing playback optimizations preserved

The current source engine remains unchanged:

- requestVideoFrameCallback remains the decoded-frame notification path where available
- decoded source frames are copied into `gCur` only when a new source frame is presented
- temporal ring capture remains tied to decoded source frames rather than every render tick
- frame history uses reusable canvas-backed slots
- the renderer remains display/rAF driven for continuously animated HUFF effects
- the hidden/unfocused heartbeat remains intact
- source replacement generation guards remain intact
- camera acquisition remains capped to 1280×720
- Canvas2D effect caches and bypass paths remain intact

## Alternatives reviewed but not implemented

### WebCodecs / VideoFrame decode pipeline

WebCodecs could give HUFF more direct control over decoded `VideoFrame` objects, but file playback would also require a reliable container demuxing layer and a substantially different media lifecycle. That is beyond a playback optimization pass inside the current framework and would increase compatibility risk.

### OffscreenCanvas renderer migration

Moving the complete HUFF effect engine into a Worker/OffscreenCanvas architecture could remove main-thread contention, but it would be a renderer architecture change rather than an optimization of the current Classic implementation.

### Lower-resolution temporal history

Reducing temporal-ring resolution would cut memory bandwidth but would alter the source material used by Corrupt, Scanlines, Flow Pulse, and Trails. It was not applied because this pass preserves the current image behavior.

## Files changed

- `canvas.js`
- `canvas.html`
- `css/canvas.css`
- `css/canvas.min.css`
- `README.md`

## Validation

Static validation completed:

- `canvas.js` syntax: PASS
- `effects.js` syntax: PASS
- `pipeline-runtime.js` syntax: PASS
- `capability-instrumentation.js` syntax: PASS
- `mirror-encoder-worker.js` syntax: PASS
- inline JavaScript in `index.html`: PASS
- inline JavaScript in `canvas.html`: PASS
- package linkage verifier: 18/18 local asset links resolve

A browser runtime comparison should test both with WINDOW closed and WINDOW open. The expected largest improvement is with WINDOW open because the JPEG mirror workload is removed from the primary path.

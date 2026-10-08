# HUFF Web Classic

HUFF Web Classic is the free browser version of HUFF. It is a real-time video instrument for live image processing.

The web version uses a fixed 1280 × 720 processing surface. It accepts a video file or a camera source. It processes the image in the browser and can open the output in a separate window.

For full documentation of the HUFF instrument family, use the HUFF Classic documentation.

## Main functions

HUFF Web Classic provides these image processes:

- **Vista** — Uses recent frames to move and repeat image regions. It supports temporal depth, clusters, smear, motion, masks, and composite controls.
- **Feedback** — Feeds the processed image back into itself. It supports position, zoom, rotation, persistence, and restore controls.
- **Paneling** — Divides the image into bands or panels. It supports displacement, field layouts, drift, skew, zoom, depth, and motion.
- **Luma Key** — Uses luminance to control the composite, Vista regions, or Paneling regions.
- **Global Mix** — Mixes the clean source back into the processing chain at a selected stage.
- **Sift** — Distorts the image with a tiled spatial field. It supports strength, scale, temporal pulse, implosion, swirl, turbulence, and spread.
- **Symmetry** — Mirrors the image across one or two axes.
- **Solarize** — Applies threshold or luminance-quantize color processing.
- **Trails** — Uses frame history to create persistent image trails.

The interface also provides source controls, pipeline recipes, screenshots, presets, and a separate output window.

## Sources

HUFF Web Classic supports these sources:

- Local video files that the browser can decode.
- Cameras that the browser exposes through `getUserMedia()`.

The application requests a 1280 × 720 camera stream when the camera supports that size.

Browser codec support is not identical on all systems. A file that works in one browser can fail in another browser.

## Output window

Select **WINDOW** to open `canvas.html` in a separate browser window.

The browser can show an address bar while the output is windowed. Web code cannot reliably remove this browser control.

To enter fullscreen, click the output surface or press `F` in the output window. Fullscreen applies to the output surface. It does not apply to the control interface.

The internal processing size remains 1280 × 720. The browser scales this image to the fullscreen display size.

## Frame rate

HUFF Web Classic targets display-rate playback and a 60 fps output path when the browser and computer can sustain it.

The actual frame rate depends on:

- source frame rate;
- video decoder load;
- active HUFF processes;
- browser scheduling;
- GPU and CPU performance;
- display refresh rate;
- background-tab throttling.

The browser can reduce work when a page is not active. HUFF uses its available browser scheduling paths to keep processing active, but the operating system and browser keep final control.

## Screenshots

HUFF can save the processed output in these formats:

- 1280 × 720 (16:9)
- 960 × 720 (4:3)
- 720 × 1280 (9:16)

The screenshot operation uses the processed canvas.

## Presets

Preset files are JSON files in `presets/`.

`presets/manifest.json` is the primary catalog for the web application. The application reads this catalog when it loads.

After you add or remove preset JSON files, run:

```bash
cd presets
python3 update_manifest.py
```

The script scans the preset folder and rebuilds `manifest.json` from the files that are present.

Deploy the updated preset files and the updated manifest together.

## Run locally

HUFF Web Classic must run from an HTTP server. Do not rely on direct `file://` loading.

One simple local server is:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/
```

Camera access normally requires a secure context. Browsers treat `localhost` as a secure development context. A public deployment should use HTTPS.

## Web limitations

HUFF Web Classic intentionally does not include the native integrations from HUFF Classic.

The web version does not provide:

- Syphon;
- Spout;
- MIDI;
- OSC;
- native GPU texture sharing;
- guaranteed background execution;
- control of browser window chrome;
- identical codec support on all operating systems and browsers.

A browser can also block a popup if the popup does not start from a user action. Use the **WINDOW** button to open the output window.

Autoplay rules can require a user action before video or audio playback starts.

Camera names can remain hidden until the user grants camera permission.

## Browser behavior

Use a current Chromium-based browser for the primary test path.

Other browsers can work, but API behavior and media performance can differ. Test the target browser before a live performance.

For best results:

1. Close browser tabs that use significant CPU or GPU resources.
2. Use a hardware-decoded video format when possible.
3. Keep the source near the 1280 × 720 processing size when possible.
4. Test camera permissions before the performance.
5. Test the output window and fullscreen mode before the performance.

## Project structure

```text
index.html                 Main control interface
canvas.html                Separate output window
canvas.js                  Source, playback, state, presets, and render control
effects.js                 Image-process implementations
pipeline-runtime.js        Pipeline recipes and stage rules
capability-instrumentation.js
                           Runtime capability and performance measurements
css/huff.css               Readable control-interface styles
css/huff.min.css           Release control-interface styles
css/canvas.css             Readable output-window styles
css/canvas.min.css         Release output-window styles
presets/                   Preset JSON files and manifest updater
mirror-encoder-worker.js   Compatibility output transport worker
ws-mirror.js               Compatibility mirror transport
p5.js                      Local p5.js dependency
```

## Distribution

HUFF Web Classic is intended for free public use.

Keep the project files on the same web origin unless you deliberately configure cross-origin access. Deploy `presets/manifest.json` with the preset JSON files so that the menu matches the deployed preset folder.

## License

See `LICENSE`.

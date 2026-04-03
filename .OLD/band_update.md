# Band Editor UI Redesign — Pro-Q 4 Style Floating Panel

## Goal

Replace the current fixed-height band editor (a grid of sliders below the EQ canvas) with a **floating panel** that overlays the bottom of the canvas, horizontally aligned to the selected band dot — matching the real Pro-Q 4 band editing UX.

---

## Current State

- **Location:** A `<section class="band-editor">` sits below the canvas inside `#eqWrap`, occupying a fixed 155px height slot.
- **Layout:** A header row (dot + label + close button) above a responsive CSS grid (`grid-template-columns: repeat(auto-fill, minmax(180px, 1fr))`) of `param-group` items, each containing a label + slider/select/toggle.
- **Parameters exposed:** Include in Merge, Frequency, Gain, Q, Shape, Slope, Stereo, Enabled, Dynamic Range, Dynamics, Dynamics Auto, Threshold, Attack, Release, Spectral, Spectral Density, SC Filtering.
- **Problem:** Takes up permanent vertical space, disconnected from the selected band visually, and too spread out compared to the real Pro-Q 4 compact floating UI.

---

## Target Design (from Pro-Q 4 reference screenshot)

The real Pro-Q 4 editor is a single **compact floating bar** pinned to the bottom of the EQ display, horizontally centered on the selected band's frequency. It contains (left to right):

```
[ Power ] [ Shape ▾ ] [ FREQ knob ] [ GAIN knob ] [ Q knob ] [ Slope icon ] [ Stereo ▾ ] [ ‹ # › ] [ × ]
                        (multiple)
```

### Key characteristics:
1. **Floating overlay** — sits inside `.canvas-wrap`, absolutely positioned near the bottom, does not consume layout space.
2. **Horizontally aligned** — its center X follows the selected band's frequency position on the canvas (clamped so it doesn't overflow edges).
3. **Compact single row** — all primary controls on one line (~500px wide, ~70px tall).
4. **Rotary knobs** — FREQ, GAIN, and Q use circular knob controls with arc indicators, not linear sliders.
5. **Minimal chrome** — dark semi-transparent background (`rgba(20,20,28,0.92)`), subtle border, large border-radius, no title bar.
6. **Top icon strip** — small row of icon buttons above the main controls: delete band (×), bypass (power), analyzer toggle, dynamics arrows.
7. **Band navigation** — `‹ # ›` arrows to step through bands in the current preset without closing the editor.

---

## Implementation Plan

### 1. CSS — New floating editor styles

**[MODIFY]** `index.html` — Replace `.band-editor` CSS block (lines 183–240)

- Remove the old `.band-editor` fixed-height section styles.
- Add new `.band-float-editor` styles:
  - `position: absolute; bottom: 16px;` inside `.canvas-wrap`
  - `transform: translateX(-50%)` with a dynamic `left` value set via JS
  - `background: rgba(20, 20, 28, 0.92); backdrop-filter: blur(12px);`
  - `border-radius: 14px; border: 1px solid rgba(255,255,255,0.08);`
  - `padding: 6px 12px; z-index: 15;`
  - `display: flex; align-items: center; gap: 10px;`
  - `box-shadow: 0 8px 32px rgba(0,0,0,0.5);`
  - `transition: left 0.2s ease, opacity 0.2s;`
  - `pointer-events: auto;`
  - Keep `opacity: 0; pointer-events: none;` by default, `.visible` shows it.

- Add `.knob-wrap` styles:
  - `width: 48px; display: flex; flex-direction: column; align-items: center; gap: 2px;`
  - Contains a `<canvas>` (48×48) for the rotary knob drawing + a label `<span>`.

- Add `.band-float-editor .shape-btn`, `.stereo-btn` — small dropdown-style buttons (icon + text, ~70px wide).
- Add `.band-float-editor .nav-group` — `‹ # ›` band stepping controls.
- Add `.band-float-editor .icon-strip` — top row of 14px icon buttons.
- Keep existing `.param-input` style for the click-to-type value displays under each knob.

### 2. HTML — Replace editor markup

**[MODIFY]** `index.html` — Move the editor inside `.canvas-wrap` (line 531–534)

Remove the current `<section class="band-editor" id="bandEditor">` block (lines 537–543) and instead place inside `.canvas-wrap`:

```html
<div class="canvas-wrap">
  <canvas id="eqCanvas"></canvas>
  <div class="canvas-tooltip" id="tooltip"></div>

  <!-- Floating Band Editor (Pro-Q 4 style) -->
  <div class="band-float-editor" id="bandEditor">
    <div class="bf-icon-strip">
      <button class="bf-icon" id="bfBypass" title="Bypass band"><!-- power SVG --></button>
      <button class="bf-icon" id="bfDelete" title="Delete band"><!-- × SVG --></button>
      <button class="bf-icon" id="bfSelect" title="Include in merge"><!-- check SVG --></button>
    </div>
    <div class="bf-main-row">
      <button class="bf-shape-btn" id="bfShape" title="Shape">
        <span class="bf-shape-icon"></span>
        <span class="bf-shape-label">Bell</span>
      </button>
      <div class="bf-knob-wrap" data-param="freq">
        <canvas class="bf-knob" width="48" height="48"></canvas>
        <span class="bf-knob-val">1.00 kHz</span>
        <span class="bf-knob-label">FREQ</span>
      </div>
      <div class="bf-knob-wrap" data-param="gain">
        <canvas class="bf-knob" width="48" height="48"></canvas>
        <span class="bf-knob-val">0.0 dB</span>
        <span class="bf-knob-label">GAIN</span>
      </div>
      <div class="bf-knob-wrap" data-param="q">
        <canvas class="bf-knob" width="48" height="48"></canvas>
        <span class="bf-knob-val">1.00</span>
        <span class="bf-knob-label">Q</span>
      </div>
      <button class="bf-slope-btn" id="bfSlope" title="Slope">
        <span class="bf-slope-label">24</span>
      </button>
      <button class="bf-stereo-btn" id="bfStereo" title="Stereo placement">
        <span class="bf-stereo-icon"><!-- stereo SVG --></span>
        <span class="bf-stereo-label">Stereo</span>
      </button>
      <div class="bf-nav-group">
        <button class="bf-icon" id="bfPrev" title="Previous band">‹</button>
        <span class="bf-band-num" id="bfBandNum">#1</span>
        <button class="bf-icon" id="bfNext" title="Next band">›</button>
      </div>
      <button class="bf-icon bf-close" id="bfClose" title="Close">×</button>
    </div>
  </div>
</div>
```

### 3. JS — Rotary knob interaction

**[ADD]** A `Knob` helper class or function set:

- **Drawing:** Render an arc from ~135° to ~405° (270° sweep). Fill the "active" portion with the band's color (accent for freq/Q, colored arc for gain based on +/−). Draw a thumb dot at the current angle.
- **Interaction:** On `mousedown` on a knob canvas, enter drag mode. `mousemove` calculates angle from center → maps to parameter range. `mouseup` ends drag. Double-click to type a value (show a tiny `<input>` overlay).
- **Parameters:**
  - **FREQ** — log scale, range 10 Hz – 30 kHz (maps to the existing `band.frequency` log2 value: 2.32–15.61).
  - **GAIN** — linear, −30 to +30 dB. Arc color: gold above 0, blue-ish below 0.
  - **Q** — log-ish scale, 0.025 – 40. Arc drawn from the standard "1.0" midpoint.

### 4. JS — Horizontal positioning

**[MODIFY]** `openBandEditor()` in App class:

- After setting up the editor, compute the X position of the selected band on the canvas:
  ```js
  const bandX = this.eqCanvas._freqToX(Math.pow(2, band.frequency));
  ```
- Get the `.canvas-wrap` width, clamp so the editor doesn't overflow:
  ```js
  const editorW = editor.offsetWidth;
  const wrapW = canvasWrap.offsetWidth;
  const left = Math.max(editorW / 2 + 8, Math.min(wrapW - editorW / 2 - 8, bandX));
  editor.style.left = left + 'px';
  ```
- On band drag (`_onDragMove`), also update the editor position live so it follows the dot.

### 5. JS — Shape & Stereo dropdown

- **Shape button** (`#bfShape`): On click, show a small absolutely-positioned dropdown above the button listing all `SHAPES` entries. Click an option → update `band.shape`, re-render, update label and shape icon SVG.
- **Stereo button** (`#bfStereo`): Same pattern with `STEREO_MODES`.
- **Slope button** (`#bfSlope`): Cycle through `SLOPE_DB` values on click (6 → 12 → 18 → … → 96 → 6). Display current value.

### 6. JS — Band navigation (`‹ # ›`)

- `#bfPrev` / `#bfNext` step through used bands within the same preset.
- `#bfBandNum` displays the current band index (e.g., `#3`).
- Stepping updates `state.selectedBand`, repositions the editor, and refreshes knob values.

### 7. JS — Rewire `openBandEditor` / `closeBandEditor`

**[MODIFY]** `openBandEditor(presetIdx, bandIdx, color)`:

- Instead of building param-groups in a grid, populate the knob canvases and button labels from the selected band's data.
- Store current band reference: `this._editBand = { presetIdx, bandIdx, band, color }`.
- Draw all three knobs.
- Set shape/stereo/slope labels.
- Position and show the editor.

**[MODIFY]** `closeBandEditor()`:

- `editor.classList.remove('visible');`
- Clear `this._editBand`.

### 8. JS — Advanced parameters (dynamics, spectral, SC)

These don't fit in the compact main row. Options:

- **Option A (recommended):** Add a small `⚙` (gear) icon button in the icon strip. Clicking it opens a **mini popover** above the floating editor with the advanced params (Dynamic Range, Dynamics enabled/auto, Threshold, Attack, Release, Spectral, SC Filtering) laid out as a compact 2-column mini-grid — similar to the current grid style but smaller.
- **Option B:** A second row that expands below the main row when toggled.

### 9. Cleanup

- Remove the old `<section class="band-editor">` HTML and its CSS (`.band-editor`, `.editor-header`, `.editor-title`, `.editor-close`, `.editor-grid`, `.param-group`, `.param-label`, `.param-row`, `.param-slider`, `.param-input`, `.param-select`, `.param-toggle`).
- Remove the `#editorClose` event listener from `_init()`.
- Update the resize handle logic — the editor no longer occupies layout space between the canvas and bottom panels, so vertical resizing is simpler.

---

## Files Changed

| File | Action | Description |
|------|--------|-------------|
| `index.html` | MODIFY | Replace band editor CSS, HTML, and JS |

Single file — everything is in `index.html`.

---

## Visual Summary

```
┌─────────────────────────────────────────────────────────────┐
│  EQ Canvas                                                  │
│                         ● (selected band)                   │
│                         │                                   │
│                         ▼                                   │
│         ┌───────────────────────────────────┐               │
│         │ ⚡ × ✓              ‹ #3 ›   ×    │  ← icon strip │
│         │ ∧ Bell │ FREQ │ GAIN │ Q │24│Stereo│  ← main row  │
│         │        │1.0kHz│+3.2dB│1.41│  │     │              │
│         └───────────────────────────────────┘               │
│              ↑ centered on band's X position                │
└─────────────────────────────────────────────────────────────┘
```

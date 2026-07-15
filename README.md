# Pro-Q4 Preset Merger

A browser-based tool for merging, blending, and editing FabFilter Pro-Q 4 equalizer presets. Load multiple `.ffp` preset files, visually compare their EQ curves, adjust individual band parameters, and export merged results — all without installing anything.

https://pro-q4-merger.pages.dev/

## Getting Started

1. **Open `index.html`** in any modern browser (Chrome, Firefox, Edge, Safari).
2. **Load presets** by dragging `.ffp` files onto the preset slots, or click a slot to browse.
3. That's it — your EQ curves appear immediately on the interactive display.

No presets handy? Click **Try Demo** to load two example presets and see a merge in action.

> **Note:** This tool works with **Pro-Q 4** format presets only. If you have Pro-Q 3 presets, open them in Pro-Q 4 and re-save to convert them to the compatible format.

## Where to Find Your Presets

Pro-Q 4 stores presets as `.ffp` files in your Documents folder:

- **Windows & macOS:** `Documents/FabFilter/Presets/Pro-Q 4`
- **Older macOS:** `~/Library/Audio/Presets/FabFilter/FabFilter Pro-Q 4`

Presets you save to this folder will appear directly in Pro-Q 4's built-in preset browser. If your Documents folder syncs to iCloud, presets may get offloaded — keep a local copy if this is an issue.

## Features

### Interactive EQ Display
- Full-resolution EQ curve visualization with per-band and composite response curves
- Click any band dot to select or deselect it for merging
- Drag band dots to adjust frequency and gain in real-time
- Scroll over a band to adjust Q width (hold Shift to adjust slope)
- Auto-scaling gain range that adapts to your loaded presets
- Bypassed bands are shown greyed out with dashed outlines for clear visual distinction

### Floating Band Editor
- Click any band dot to open the **Pro-Q 4 style floating editor** that follows the selected band
- **Rotary knobs** for Frequency, Gain, and Q — drag vertically or scroll wheel to adjust, hold Shift for fine control
- **Double-click** any value to type it in manually (works on all controls including knobs, shape, slope, and stereo)
- **Scroll wheel** works on every control — knobs, shape selector, slope, and stereo placement
- Shape dropdown, slope cycling, stereo placement, bypass toggle, and merge selection
- **Band navigation** arrows to step through bands without closing the editor
- **Advanced parameters** (dynamics, threshold, attack/release, spectral, sidechain) behind the gear icon

### Multiple View Modes
- **Overlay** — see all loaded presets layered on one display
- **Tabs** — switch between individual presets or view the Merged/Preview result

### Preset Blending & Toggle
- **Mix sliders** on every preset slot let you blend each preset's contribution (0–100%)
- **Toggle switches** (power icon) enable/disable presets without losing your mix settings
- **Global mix** slider in the Merged tab controls the overall blend level
- Disabled presets are dimmed on the display and excluded from merge output

### Preview Before Download
- Click **Preview Merge** to see the merged result as a white dashed curve on the display
- Review the preview, adjust settings, then click **Download Preset(s)** to export
- The preview tab shows the combined result of all your selected bands and blend settings

### Undo / Redo
- **Back/Forward arrows** in the header (or keyboard shortcuts below)
- Tracks all meaningful changes: file loads, blend adjustments, band edits, toggles, and previews
- Up to 50 levels of undo history

### Merge Modes
- **Standard** — stacks all selected bands sorted by frequency
- **Smart** — detects nearby bands (within ~1 semitone) and offers options:
  - **Keep Both** — include both bands as-is
  - **Combine** — average their gain, Q, and frequency into one band
  - **Skip 2nd** — drop the duplicate

### Output Options
- Custom preset name and author fields
- Choose which loaded preset's global settings (processing mode, resolution) to use
- Select character setting (Off, Subtle, Warm)
- Automatic splitting into multiple presets (A, B, C...) if you exceed the 24-band limit

## Keyboard & Mouse Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Ctrl+Y` | Redo |
| Scroll on band dot | Adjust Q |
| Shift+Scroll on band dot | Adjust slope |
| Click band dot | Select/deselect for merge |
| Drag band dot | Move frequency & gain |
| Scroll on editor knobs | Adjust value |
| Double-click any value | Type in a value manually |
| Shift+drag on knobs | Fine adjustment |

## How Band Selection Works

- **Enabled bands** are automatically selected for merging
- **Disabled bands** that still have non-default settings (like a specific frequency or gain) are shown with reduced opacity — click them to include them in the merge
- **Bypassed bands** appear greyed out with a dashed outline and a strike-through indicator

## Limitations

- Maximum **24 bands** per output preset (this is a Pro-Q 4 limit)
- If your merge exceeds 24 bands, it will automatically split into multiple presets (A, B, C...)
- Only Pro-Q 4 `.ffp` format is supported — Pro-Q 3 presets must be converted first by opening and re-saving in Pro-Q 4
- Dynamic EQ and mid/side processing parameters are preserved in the output but not visually simulated on the display

## Pro-Q 3 Presets

Pro-Q 3 uses a different binary format that isn't directly compatible with this tool. To convert your Pro-Q 3 presets:

1. Open the preset in Pro-Q 4
2. Re-save it (the plugin will automatically convert to the new format)
3. The resulting `.ffp` file can be loaded here

## License

This is a standalone utility tool. No server, no dependencies, no build step — just open and use.

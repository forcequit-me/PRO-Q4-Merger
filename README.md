# Pro-Q4 Preset Merger

A browser-based tool for merging, blending, and editing FabFilter Pro-Q 4 equalizer presets. Load multiple `.ffp` preset files, visually compare their EQ curves, adjust individual band parameters, and export merged results — all without installing anything.

## Getting Started

1. **Open `index.html`** in any modern browser (Chrome, Firefox, Edge, Safari).
2. **Load presets** by dragging `.ffp` files onto the preset slots, or click a slot to browse.
3. That's it — your EQ curves appear immediately on the interactive display.

> **Note:** This tool works with **Pro-Q 4** format presets only (`.ffp` text-based INI files with `FQ4p` signature). If you have Pro-Q 3 presets, open them in Pro-Q 4 and re-save to convert.

## Features

### Interactive EQ Display
- Full-resolution EQ curve visualization with per-band and composite response curves
- Click any band dot to select/deselect it for merging
- Drag band dots to adjust frequency and gain in real-time
- Scroll over a band to adjust Q width (hold Shift to adjust slope)
- Auto-scaling gain range that adapts to your loaded presets

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
- The preview updates the tab bar to show a "Preview" tab

### Undo / Redo
- **Back/Forward arrows** in the header (or `Ctrl+Z` / `Ctrl+Shift+Z` / `Ctrl+Y`)
- Tracks all meaningful changes: file loads, blend adjustments, band edits, toggles, and previews
- Up to 50 levels of undo history

### Band Editor
- Click any band dot to open the detailed editor panel
- Adjust frequency, gain, Q, shape (Bell, Low Shelf, High Shelf, Notch, Band Pass, and more), stereo placement, and slope
- Toggle individual band bypass and selection state
- Changes are reflected live on the EQ display

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
- Automatic splitting into multiple presets (A, B, C…) if you exceed the 24-band limit

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Ctrl+Y` | Redo |
| Scroll on band | Adjust Q |
| Shift+Scroll on band | Adjust slope |
| Click band dot | Select/deselect for merge |
| Drag band dot | Move frequency & gain |

## Limitations

- Maximum **24 bands** per output preset (Pro-Q 4 hardware limit)
- Presets with more than 24 selected bands are automatically split into multiple files
- Only Pro-Q 4 `.ffp` format is supported — Pro-Q 3 binary presets must be converted first
- Dynamic EQ ranges and mid/side processing parameters are preserved but not visually simulated

## File Format

Pro-Q 4 presets use a text-based INI format:

```ini
[FabFilter Pro-Q 4]
Version=4
Bands=24
Band1 Frequency=...
Band1 Gain=...
Band1 Q=...
Band1 Shape=...
...
```

The tool reads and writes this format directly, preserving all parameters including dynamic range, stereo placement, slope, and global settings.

## License

This is a standalone utility tool. No server, no dependencies, no build step — just open and use.

# FabFilter Pro-Q 4 Preset Merger

A single-file HTML web app to merge multiple Pro-Q 4 preset files (.ffp) into one, reducing the number of plugin instances needed in long effect chains.

## Background

### Preset Format Analysis (from your files)

Pro-Q 4 text presets (`.ffp`) use an INI-like format:

```ini
[Preset]
Signature=FQ4p
Version=4
Author=...
Description="..."
Tags=...

[Parameters]
Band 1 Used=1          # 0=unused, 1=active
Band 1 Enabled=1       # 0=bypassed, 1=enabled
Band 1 Frequency=9.19  # log2(Hz) scale
Band 1 Gain=-1.16      # dB
Band 1 Q=0.47          # Q factor
Band 1 Shape=0         # 0=Bell, 1=Low Shelf, 2=Low Cut, 3=High Shelf, 4=High Cut, 5=Notch, 6=Band Pass, 7=Tilt Shelf, 8=Flat Tilt
Band 1 Slope=2         # dB/oct encoded as fractional value
Band 1 Stereo Placement=2  # 0=Left, 1=Right, 2=Stereo, 3=Mid, 4=Side
Band 1 Speakers=1
Band 1 Dynamic Range=0
Band 1 Dynamics Enabled=1
Band 1 Dynamics Auto=1
Band 1 Threshold=0.666
Band 1 Attack=50
Band 1 Release=50
Band 1 External Side Chain=0
Band 1 Side Chain Filtering=0
Band 1 Side Chain Low Frequency=...
Band 1 Side Chain High Frequency=...
Band 1 Side Chain Audition=0
Band 1 Spectral Enabled=0
Band 1 Spectral Density=50
Band 1 Solo=0
... (Bands 1–24, same structure)

# Global parameters
Processing Mode=0       # 0=Zero Latency, 1=Natural Phase, 2=Linear Phase
Processing Resolution=1 # 0=Low, 1=Medium, 2=High, 3=Very High, 4=Max
Character=0
Gain Scale=1
Output Level=0
Output Pan=0
...
```

**Key constraints:**
- **24 bands max** per instance
- Bands with `Used=0` are available slots — the merge fills them
- **Pro-Q 4 only** — older binary `FQ3p` presets (~1348 bytes) are detected and rejected with guidance
- Frequency is stored as `log2(Hz)` (e.g., 9.96 ≈ 1000 Hz)

### Band Inclusion Rule

Active bands (`Used=1`) are always included. Additionally, **bands with `Used=0` but non-default parameter values** (custom frequency, gain, Q, shape, etc.) are detected and presented to the user as "inactive but configured" bands that can be optionally included in the merge.

---

## Proposed Changes

### [NEW] [index.html](file:///c:/Users/plagi/Desktop/PRO-Q4/index.html)

A single self-contained HTML file with embedded CSS and JavaScript.

---

### Feature 1: File Input & Parsing

- Drag & drop zone or file picker for multiple `.ffp` files, should be able to handle merging custom amount of presets, default is 2 presets, but should be able to handle more with a + button, and remove with a - button.
- Parses text-format `FQ4p` presets, extracts all bands and global settings
- Detects binary `FQ3p` files → shows error with guidance to re-save in Pro-Q 4
- About section includes explanation of Pro-Q 3 vs Pro-Q 4 format differences

---

### Feature 2: EQ Curve Visualization (Interactive)

Canvas-based display with **two view modes** toggled via a button:

#### View Mode A: "Overlay" (default)
- All loaded presets shown simultaneously on one frequency/gain grid
- Each preset gets a unique color
- Band dots are color-coded per source preset
- Bands can be **clicked to select/deselect** for merging
- Hovering a dot shows a tooltip with all band parameters

#### View Mode B: "Tabs"
- Tab bar at top of the EQ display, one tab per loaded preset
- Selecting a tab isolates that preset's bands on the grid
- Individual band editing happens in this view
- A special **"Merged" tab** shows the combined result in real-time

Both views share:
- Frequency axis: 20 Hz – 20 kHz (logarithmic)
- Gain axis: ±30 dB
- Grid lines with labeled frequency markers and dB markers
- Filter shape indicators (different dot shapes for Bell, Shelf, Cut, etc.)

---

### Feature 3: Full Band Parameter Editor

Clicking a band dot (in either view mode) opens an **inline editor panel** with full control over all parameters:

| Parameter | Control Type |
|-----------|-------------|
| Frequency | Slider + numeric input (displays Hz, stores log2) |
| Gain | Slider + numeric input (dB) |
| Q | Slider + numeric input |
| Shape | Dropdown (Bell, Low Shelf, Low Cut, High Shelf, High Cut, Notch, Band Pass, Tilt Shelf, Flat Tilt) |
| Slope | Slider + numeric (dB/oct) |
| Stereo Placement | Dropdown (Left, Right, Stereo, Mid, Side) |
| Enabled | Toggle switch |
| Dynamic Range | Slider + numeric |
| Dynamics Enabled | Toggle |
| Dynamics Auto | Toggle |
| Threshold | Slider |
| Attack | Slider |
| Release | Slider |
| Spectral Enabled | Toggle |
| Spectral Density | Slider |
| Side Chain Filtering | Toggle |
| SC Low/High Freq | Sliders |

Changes are reflected live on the EQ visualization canvas.

---

### Feature 4: Merge Logic

Two merge modes available:

#### Mode 1: Standard Merge
- Collects all selected bands from input presets
- Sorts bands by frequency (low → mid → high)
- Packs them into Band 1, 2, ... 24 slots
- If total exceeds 24 → **auto-splits** into multiple output presets

#### Mode 2: Smart Merge (experimental)
- Same as standard, but additionally:
  - Detects bands with very close frequencies (within configurable threshold, e.g. ±1 semitone)
  - Highlights potential duplicates/conflicts for user review
  - Suggests combining overlapping bells by averaging gain/Q
  - User confirms each suggestion before it's applied
- This is a "suggest and confirm" workflow, not automatic

#### Output Naming

- User provides a **custom base name** via text input (e.g. `"Vocal Chain"`)
- Single output → `Vocal Chain.ffp`
- Multiple outputs (>24 bands split) → `Vocal Chain A.ffp`, `Vocal Chain B.ffp`, `Vocal Chain C.ffp`, etc.

#### Global Settings

When merging presets with different global settings (Processing Mode, Resolution, etc.), the user **must manually select** which preset's globals to use via a clear dropdown/radio selector. No automatic defaulting — the UI prompts the user to choose.

---

### Feature 5: Export

- Download individual `.ffp` files or a `.zip` bundle if multiple outputs
- Exported files are valid `FQ4p` format with all 24 band slots filled (unused = defaults)
- Custom Author and Description fields in the export dialog

---

### UI Design & Style Guide

Dark theme strictly matching the FabFilter Pro-Q 4 aesthetic shown in the reference screenshot:

#### Color Palette
- **Main Background**: Deep space charcoal (`#111116` to `#181820`), with a subtle warm gradient tint near the bottom left corner.
- **Grid Lines**: Extremely faint gray (`rgba(255, 255, 255, 0.05)`) for the background frequency/gain grid.
- **Text Labels (Axes)**: Muted gray (`#777780`) for frequency (Hz) and gain (dB) markers.
- **Active Accent**: FabFilter signature bright yellow/orange (`#ffca1f`) used for active selected bands, highlighted text, and global toggle dots.
- **UI Panels (Top/Bottom Bars)**: Slightly lighter charcoal (`#15151b`) or flat dark grey to separate controls from the main canvas.

#### Band Curve Colors (Dynamic Assignment)
When multiple bands/presets are loaded, they should use the distinct Pro-Q 4 color scheme, featuring translucent fill (approx 20-30% opacity) and solid glowing strokes:
- **Blue**: `#3b82f6` (Fill: `rgba(59, 130, 246, 0.25)`)
- **Green**: `#22c55e` (Fill: `rgba(34, 197, 94, 0.25)`)
- **Purple**: `#d946ef` (Fill: `rgba(217, 70, 239, 0.25)`)
- **Red/Pink**: `#ef4444` (Fill: `rgba(239, 68, 68, 0.25)`)
- **Yellow/Orange**: `#f59e0b` (Fill: `rgba(245, 158, 11, 0.25)`)

#### Typography & Details
- **Font**: Inter, Roboto, or a clean modern sans-serif. Numbers should use tabular figures for clean alignment.
- **Band Dots**: Colored circles representing the control node. Selected dots get a subtle white/lighter outline to indicate active status.
- **Secondary Controls**: Dynamic range markers appear as small vertical arrows above/below the main band dot (as seen on the blue and green bands).
- **Preset/Editor Panels**: Use solid dark panels (`#1c1c24`) with very subtle 1px lighter top borders (`rgba(255,255,255,0.1)`) and soft drop shadows to mimic the plugin's flat-but-layered feel, avoiding overly 'glassy' looks.
- **Smooth Animations**: For band dragging, canvas view mode transitions, and editor panel revealing.

#### Layout

```
┌─────────────────────────────────────────────────────────┐
│  ⬡ Pro-Q4 Preset Merger         [Overlay|Tabs] [About] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─ EQ Visualization ──────────────────────────────┐   │
│   │  20Hz ──────── 1kHz ──────── 20kHz              │   │
│   │  +30dB  ●(red)    ●(blue)    ●(green)           │   │
│   │    0dB  ────────────────────────────             │   │
│   │  -30dB         ●(red)                           │   │
│   └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌── Band Editor (when band selected) ───────────────┐  │
│  │  Freq: [====●====] 2.4 kHz   Gain: [-3.2 dB]     │  │
│  │  Q: [0.47]  Shape: [Bell ▼]  Slope: [12 dB/oct]  │  │
│  │  Dynamics ☐  Spectral ☐  Stereo: [Stereo ▼]      │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌── Input Presets ───────┐  ┌── Merge Output ───────┐  │
│  │ [Drop .ffp files here] │  │ Name: [Vocal Chain  ] │  │
│  │ ● Vocal Rescue   (9)  │  │ Globals: [Preset ▼  ] │  │
│  │ ● Elixir         (11) │  │ Mode: ○Standard ○Smart│  │
│  │ ● Kick IN 01     (4)  │  │ 24/24 bands ⚠️ Split  │  │
│  │                       │  │                       │  │
│  │ Total: 24 bands       │  │ [Merge & Download]    │  │
│  └───────────────────────┘  └───────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Verification Plan

### Automated Tests (in-app)
- Load a known preset → verify parser extracts correct band count and values
- Merge two presets → verify output has correct combined band count
- Exceed 24 bands → verify auto-split with alphabetical naming
- Attempt to load binary (FQ3p) → verify graceful error with guidance
- Edit a band parameter → verify canvas updates and export includes edit

### Manual Verification
- Open generated `.ffp` file in FabFilter Pro-Q 4 → verify all bands appear correctly
- Compare band frequencies, gains, shapes against what was set in the app
- Verify split presets (`A`, `B`, `C`) each load independently in Pro-Q 4
- Test with real-world merge scenarios (e.g., 2 vocal presets + 1 drum preset)

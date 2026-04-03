# Pro-Q 4 Preset Merger — Grid & Accuracy Fixes

## Context
After comparing our interface against real Pro-Q 4 screenshots, analyzing real .ffp preset files, and reviewing the FabFilter YouTube tutorial transcript, several accuracy issues were identified. The grid pattern is visibly different from Pro-Q 4, slope values are being rounded (losing data), and default band values are wrong.

## Changes (in order)

### 1. Fix DEFAULT_BAND values
**File**: `index.html` ~line 458
- Change `q:1` → `q:0.5`
- Change `slope:3` → `slope:1`
- Real .ffp files confirm unused bands have Q=0.5 and Slope=1

### 2. Fix grid to match Pro-Q 4 pattern
**File**: `index.html`, `_drawGrid` method (~line 1010)

**Add all missing frequency lines** — fill in complete integer multiples per decade:
```
20,30,40,50,60,70,80,90,100,
200,300,400,500,600,700,800,900,1000,
2000,3000,4000,5000,6000,7000,8000,9000,10000,
20000
```

**Add 3-tier brightness hierarchy**:
- Decade boundaries (100, 1000, 10000): `rgba(255,255,255,0.08)`
- "Round" positions (20, 50, 200, 500, 2000, 5000, 20000): `rgba(255,255,255,0.05)`
- All others (30, 40, 60, 70, 80, 90, 300, etc.): `rgba(255,255,255,0.025)`

This creates the characteristic "bunching" near decade boundaries that makes log-scale EQ displays look natural.

### 3. Handle continuous slope values
**File**: `index.html`, FilterMath + FFP + band editor

**Problem**: Real .ffp files have fractional slopes like `Slope=2.44138884544373`. Our code does `Math.round(band.slope)` losing this data.

**Add helper function**:
```js
function slopeToDB(slopeVal) {
  const idx = Math.min(Math.floor(slopeVal), SLOPE_DB.length - 2);
  const frac = slopeVal - idx;
  return SLOPE_DB[idx] + frac * (SLOPE_DB[Math.min(idx + 1, SLOPE_DB.length - 1)] - SLOPE_DB[idx]);
}
```

**Update FilterMath.bandResponse** — use `slopeToDB(band.slope)` instead of `SLOPE_DB[Math.round(...)]`

**Update band editor slope control** — change from discrete dropdown to slider + numeric input showing dB/oct, preserving the original float on export

**Update tooltip** — show interpolated dB/oct value

### 4. Preserve all global parameters on export
**File**: `index.html`, FFP.parse() and FFP.serialize()

**In parse()**: After extracting known globals, collect remaining non-band [Parameters] keys into `globals._extra` object. Known band keys start with `Band N `. Everything else that isn't a known global goes into `_extra`.

**In serialize()**: The `_extra` write-out already exists but `_extra` is never populated. Fix the parser to actually populate it.

### 5. Add Character mode to UI
**File**: `index.html`, output panel HTML + JS

Add a row to the output panel:
```html
<div class="output-row">
  <label>Character</label>
  <select id="characterSelect">
    <option value="0">Off</option>
    <option value="1">Subtle</option>
    <option value="2">Warm</option>
  </select>
</div>
```

When globals source changes, update the Character dropdown. On merge, use the selected Character value.

### 6. Drag band dots to adjust frequency/gain
**File**: `index.html`, EQCanvas class

Add click-and-drag behavior on band dots:
- **Drag horizontally** → adjusts frequency (convert pixel X back to Hz via `_xToFreq`, then to log2 for storage)
- **Drag vertically** → adjusts gain (convert pixel Y back to dB via inverse of `_gainToY`)
- For cut/notch/bandpass shapes (gain-less), vertical drag is ignored
- Show crosshair cursor while dragging
- Update the band editor panel in real-time if it's open for that band
- Clamp frequency to 10 Hz–30 kHz range, gain to ±30 dB

Implementation:
- On `mousedown` over a band dot: enter drag mode, store the dragged band reference
- On `mousemove` while dragging: update band.frequency and band.gain, re-render canvas + editor
- On `mouseup`: exit drag mode
- Prevent default click behavior (opening editor) when a drag has occurred (threshold: >3px movement)

### 7. Mouse wheel Q/slope adjustment on band dots
**File**: `index.html`, EQCanvas class

Add `wheel` event listener on canvas:
- When hovering over a band dot: scroll adjusts Q (multiply by 1.05 per tick up, /1.05 down, clamped 0.025–40)
- With Shift held: scroll adjusts slope (±0.1 per tick, clamped 0–8)
- Re-render and update band editor if open

## Key Findings from Real Preset Files

### Slope is continuous, not discrete
```
Slope=2.44138884544373  (Kick - IN 01.ffp, Band 3)
Slope=1.49666666984558  (Elixir.ffp, Band 2)
Slope=0.423333346843719 (Elixir.ffp, Band 4)
Slope=3.09583330154419  (Elixir.ffp, Band 3)
```

### Default unused band values
```
Q=0.5 (NOT 1.0 as we assumed)
Slope=1 (NOT 3 as we assumed)
```

### Extra global parameters not being preserved
```
Output Pan Mode, Bypass, Output Invert Phase, Auto Gain,
Analyzer Show Pre-Processing, Analyzer Show Post-Processing,
Analyzer Show External Spectrum, Analyzer External Spectrum,
Analyzer Range, Analyzer Resolution, Analyzer Speed,
Analyzer Tilt, Analyzer Freeze, Analyzer Show Collisions,
Spectrum Grab, Display Range, Receive Midi, Solo Gain
```

### Character mode values
- `Character=0` → Off (clean)
- `Character=1` → Subtle (harmonics)
- `Character=2` → Warm (2nd harmonic)

## Key Findings from YouTube Tutorial Transcript

1. **Continuous slope** — Shift+scroll allows in-between slope values, confirmed by real preset data
2. **Character modes** — "Subtle" and "Warm" harmonic saturation, stored as Character=0/1/2
3. **Mouse wheel interaction** — scroll on band adjusts Q, matches Pro-Q workflow
4. **Attack/Release on dynamics** — already supported in our editor
5. **Spectral processing** — FFT-based resonance suppression, already supported via spectral params
6. **Auto Gain** — global parameter we need to preserve on export

## Verification
1. Load real .ffp files from `Presets (Default)/` directory (e.g., "Kick - IN 01.ffp", "Elixir.ffp")
2. Compare grid visually against Pro-Q 4 screenshots — look for line bunching near 100/1000/10000
3. Verify slope=2.44 from Kick preset renders as ~20.6 dB/oct (not snapping to 18 or 24)
4. Export a merged preset, re-open the .ffp in a text editor, confirm all extra globals are preserved
5. Verify unused bands in export have Q=0.5 and Slope=1
6. Test mouse wheel on band dots for Q and Shift+wheel for slope

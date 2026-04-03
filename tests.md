# Pro-Q4 Preset Merger — Feature Tests

Run these tests in a browser after opening `index.html`. Use real `.ffp` files from the `Presets (Default)/` directory (e.g. `Kick - IN 01.ffp`, `Elixir.ffp`).

---

## 1. File Loading

- [ ] **Drag & drop onto slot** — drag a `.ffp` file onto an empty preset slot; slot shows file name and active band count
- [ ] **File picker** — click an empty slot to open the file picker; select a `.ffp` file; slot populates correctly
- [ ] **Drag & drop onto body** — drag a `.ffp` file anywhere on the window (not onto a slot); it loads into the first empty slot
- [ ] **Multiple files at once** — drag 3 `.ffp` files onto the body; each loads into a separate slot in order
- [ ] **Wrong file type** — try loading a non-`.ffp` file; expect a red error toast, no crash
- [ ] **Pro-Q 3 binary preset** — load a `FQ3p` format file; expect a descriptive error toast explaining it needs re-saving in Pro-Q 4

---

## 2. Preset Slots

- [ ] **Two slots on load** — app starts with exactly 2 empty slots visible
- [ ] **Add slot** — click `+ Add`; a third slot appears
- [ ] **Auto-add slot** — load a file into the last slot; a new empty slot appears automatically (up to 10)
- [ ] **Remove preset** — hover a loaded slot and click ×; slot is removed, EQ canvas updates, band summary updates
- [ ] **Slot colour dots** — each slot has a distinct colour dot (blue, green, purple, red, orange…)
- [ ] **2-col grid layout** — with 3+ presets loaded, slots display side-by-side in two columns

---

## 3. EQ Canvas — Grid

- [ ] **All frequency lines present** — visually confirm lines at 20, 30, 40, 50, 60, 70, 80, 90, 100 … 10 000, 20 000 Hz (28 lines total)
- [ ] **3-tier brightness** — decade boundaries (100, 1 k, 10 k) are brightest; round positions (20, 50, 200, 500…) are mid; all others are faintest
- [ ] **Gain grid lines** — horizontal lines every 3 dB, thicker every 6 dB; 0 dB line most prominent
- [ ] **Frequency labels** — labels at 20, 50, 100, 200, 500, 1k, 2k, 5k, 10k, 20k along the bottom

---

## 4. EQ Canvas — Curves & Dots

- [ ] **Curves appear on load** — loading a preset draws its EQ curve in the preset's colour
- [ ] **Overlay mode** — with 2 presets loaded, both curves appear simultaneously with a gold composite line
- [ ] **No composite line with 1 preset** — single preset shows only its own curve, no gold line
- [ ] **Band dots** — coloured dots appear at each active band's frequency position
- [ ] **Cut/notch dots at 0 dB** — Low Cut, High Cut, Notch, Band Pass band dots are positioned on the 0 dB line
- [ ] **Inactive bands** — bands with `Used=0` but non-default params appear at reduced opacity
- [ ] **Auto-scale gain axis** — load a preset with high-gain bands (e.g. ±20 dB); the Y axis expands to accommodate

---

## 5. Tooltips

- [ ] **Hover over band dot** — tooltip appears showing Freq, Gain, Q, Shape, Slope in dB/oct
- [ ] **Fractional slope in tooltip** — if a band has slope=2.44 (from `Kick - IN 01.ffp`), tooltip should show ~20.6 dB/oct not 18 or 24
- [ ] **Tooltip hides on mouse leave** — moving the mouse away from the canvas removes the tooltip

---

## 6. Band Selection

- [ ] **Active bands auto-selected** — bands with `Used=1` have a white selection ring on load
- [ ] **Shift+click toggles selection** — shift-clicking a dot toggles its white ring without opening the editor
- [ ] **Band summary updates** — the "X / 24 bands selected" counter updates immediately on toggle

---

## 7. Band Editor — Open / Close

- [ ] **Click band dot to open** — clicking a dot opens the band editor panel (fades in)
- [ ] **Editor fades in, EQ does not resize** — the EQ canvas maintains the same height when the editor opens
- [ ] **Correct band label** — editor title shows preset name, band number, and shape (e.g. `Elixir — Band 2 (Bell)`)
- [ ] **Colour dot in title** — the dot in the editor header matches the preset's colour
- [ ] **Click empty canvas to close** — clicking anywhere on the canvas with no dot nearby closes the editor (fades out)
- [ ] **Close button** — clicking × closes the editor

---

## 8. Band Editor — Parameters

- [ ] **Frequency slider** — drag slider; canvas curve updates in real time; display shows Hz/kHz
- [ ] **Gain slider** — drag slider; canvas curve updates; display shows dB
- [ ] **Q slider** — drag slider; narrow/wide bell shape changes live
- [ ] **Shape dropdown** — change shape; curve shape updates; editor label updates
- [ ] **Slope slider (continuous)** — drag slope slider slowly; rendered dB/oct value changes continuously (e.g. 20.6 not snapping to 18/24)
- [ ] **Stereo dropdown** — change stereo placement (Mid/Side etc.); no crash
- [ ] **Enabled toggle** — toggle Enabled off; the band curve disappears from canvas
- [ ] **Include in Merge toggle** — toggle off; band count in summary decreases
- [ ] **Dynamic Range slider** — adjustable 0–30 dB, no crash
- [ ] **Dynamics toggle** — toggleable, no crash
- [ ] **Attack / Release sliders** — show values in ms
- [ ] **Spectral toggle + Density slider** — adjustable, no crash

---

## 9. Drag Band Dots

- [ ] **Horizontal drag adjusts frequency** — click and drag a dot left/right; dot moves, curve shifts to new frequency; value shown in editor updates live if open
- [ ] **Vertical drag adjusts gain** — drag a dot up/down; gain changes; curve height updates
- [ ] **Gainless shapes ignore vertical drag** — drag a Low Cut/High Cut/Notch/Band Pass dot; it only moves horizontally
- [ ] **Clamp frequency** — drag a dot to extreme left/right; frequency clamps at 10 Hz / 30 kHz
- [ ] **Clamp gain** — drag a dot to extreme top/bottom; gain clamps at ±30 dB
- [ ] **Crosshair cursor while dragging** — cursor changes to crosshair during drag
- [ ] **No editor popup on drag** — dragging (>3 px movement) does not open the band editor

---

## 10. Mouse Wheel on Dots

- [ ] **Scroll narrows/widens Q** — hover over a dot and scroll up → Q increases (narrower bell); scroll down → Q decreases
- [ ] **Shift+scroll adjusts slope** — hold Shift and scroll → slope dB/oct value changes; canvas re-renders
- [ ] **Q clamped 0.025–40** — scrolling at extremes does not go beyond limits
- [ ] **Slope clamped 0–8** — shift-scrolling at extremes does not go beyond limits
- [ ] **Editor updates live** — if editor is open for the hovered band, Q/slope values update while scrolling

---

## 11. View Mode — Overlay / Tabs

- [ ] **Overlay button** — default mode; all presets drawn simultaneously
- [ ] **Tabs button** — tab bar appears above the canvas with one tab per preset + Merged tab
- [ ] **Tab switching** — clicking a tab shows only that preset's curve
- [ ] **Merged tab** — clicking Merged shows all preset curves simultaneously (same as overlay)
- [ ] **Tab bar hidden in overlay mode** — no tab bar shown in Overlay mode

---

## 12. Globals Source

- [ ] **Dropdown populates on load** — after loading presets, Globals dropdown shows each preset name + processing mode/resolution
- [ ] **Character dropdown syncs** — switching globals source updates the Character dropdown to reflect the new source preset's Character value
- [ ] **Character options** — Off / Subtle / Warm selectable independently of the source preset

---

## 13. Merge Mode — Standard

- [ ] **Standard selected by default** — ⧫ Standard button is highlighted gold on load
- [ ] **Mode description** — text below buttons reads "Stacks all selected bands by frequency"
- [ ] **Basic merge** — load 2 presets, click Merge & Download; a `.ffp` file downloads
- [ ] **Downloaded file is valid INI** — open the file in a text editor; confirm `[Preset]`, `Signature=FQ4p`, `[Parameters]` sections
- [ ] **Correct band count in output** — if 5 bands were selected, the first 5 bands in the file have `Used=1`
- [ ] **Unused bands have correct defaults** — remaining bands in the output have `Q=0.5` and `Slope=1`
- [ ] **Bands sorted by frequency** — band slots in the output file are ordered lowest to highest Hz
- [ ] **Extra globals preserved** — open the output `.ffp`; confirm `Auto Gain`, `Analyzer Range`, etc. from the source preset are present

---

## 14. Merge Mode — Smart

- [ ] **Smart button active** — clicking ✦ Smart highlights it in cyan with glow; ✦ icon pulses
- [ ] **Mode description changes** — text reads "Detects nearby bands — suggests combining them"
- [ ] **Smart with no conflicts** — if no two bands are within 1 semitone, merge proceeds immediately without dialog
- [ ] **Conflict dialog appears** — load two presets with overlapping frequencies; click Merge; Smart dialog shows nearby band pairs
- [ ] **Keep Both** — select Keep Both for a pair; both bands appear in output
- [ ] **Combine** — select Combine; a single averaged band appears in output
- [ ] **Skip 2nd** — select Skip 2nd; only first band of the pair appears in output
- [ ] **Cancel dialog** — clicking Cancel closes dialog without merging

---

## 15. Band Count > 24 (Overflow Split)

- [ ] **Warning in summary** — select more than 24 bands; summary shows orange "Will split into N presets (A–B)" warning
- [ ] **Multiple files downloaded** — click Merge; multiple `.ffp` files download (A, B…) or a fallback sequential download
- [ ] **Each output file ≤ 24 bands** — check each downloaded file; max 24 bands with `Used=1`

---

## 16. Merge Output Settings

- [ ] **Name field** — change output name; downloaded filename reflects it
- [ ] **Author field** — set author; `Author=` key present in output `.ffp`
- [ ] **Character value written** — set Character to Warm (2); output `.ffp` contains `Character=2`

---

## 17. Resize Handles

- [ ] **Vertical handle visible** — a subtle horizontal pill is visible between the EQ+editor area and the bottom panels
- [ ] **Vertical handle glows on hover** — pill turns gold on hover
- [ ] **Drag vertical handle down** — bottom panels grow taller; EQ area shrinks; both respect minimum heights
- [ ] **Drag vertical handle up** — EQ area grows; bottom panels shrink to minimum (130px)
- [ ] **EQ canvas re-renders after resize** — no blank areas or distortion on the canvas
- [ ] **Horizontal handle visible** — a subtle vertical pill between the Input Presets and Merge Output panels
- [ ] **Horizontal handle glows on hover** — pill turns gold on hover
- [ ] **Drag horizontal handle right** — Input Presets panel widens; Merge Output shrinks (min 180px each)
- [ ] **Drag horizontal handle left** — Merge Output panel widens; Input Presets shrinks

---

## 18. Default Band Accuracy

- [ ] **Load a preset with unused bands** — open the output `.ffp` in a text editor; confirm unused bands have `Q=0.5` and `Slope=1` (not `Q=1, Slope=3`)

---

## 19. Slope Rendering Accuracy

- [ ] **Load `Kick - IN 01.ffp`** — Band 3 has Slope≈2.44; confirm the rendered curve sits between 18 dB/oct and 24 dB/oct slopes visually (not snapped)
- [ ] **Load `Elixir.ffp`** — Band 2 has Slope≈1.497; renders between 6 and 12 dB/oct

---

## 20. Error Handling & Edge Cases

- [ ] **No presets loaded** — Merge button is disabled
- [ ] **No bands selected** — click Merge with all bands deselected (shift+click all); red toast "No bands selected"
- [ ] **No globals source** — shouldn't happen once presets are loaded, but verify Globals dropdown is always populated after loading
- [ ] **Remove all presets** — remove every preset; EQ canvas goes blank; summary resets; Merge button disables
- [ ] **Reload same file twice** — load the same `.ffp` into two different slots; both appear independently with different colours

---

## 21. About Modal

- [ ] **? button opens modal** — clicking the ? button in the header shows the About modal
- [ ] **Click backdrop to close** — clicking outside the modal box closes it
- [ ] **× button closes modal** — clicking × inside the modal closes it

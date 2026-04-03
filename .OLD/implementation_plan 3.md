# Expanded Implementation Plan



Brief: Responsive merge output, universal preview-before-download, undo/redo with simple arrows, and preset toggle switches.

when done create a comprehensive README.md file that is user oriented. Also update the about section to be more user friendly as well

---

## Proposed Changes

### 1. Condensed & Responsive Merge Output Panel

#### [MODIFY] index.html — Output panel HTML + CSS

- Redesign `.bottom-panels` and `.panel` to use responsive flex layouts (`flex-wrap: wrap`) so content flows correctly on smaller heights/widths.
- Turn the `.output-row`s into a compact grid or wrapping flex container.
  - Row 1: Name & Author side-by-side
  - Row 2: Globals & Character side-by-side
- Ensure the panel content can scroll if space becomes too tight, rather than cutting off the "Merge" button.

---

### 2. Universal Merge Preview (render before download)

#### [MODIFY] index.html — Preview logic

**New Flow for ALL Merges:**
- User clicks "Preview Merge" (formerly "Merge & Download") or "Apply" in Smart Dialog.
- `state.mergedPreview` is populated with the final blended & sorted bands.
- The EqCanvas draws a distinct **bright white dashed line** labeled "Preview".
- A "Preview" tab is added to the active tabs.
- A prominent **"Download Preset(s)"** button appears (replacing "Preview Merge" or right next to it) so the user can download what they see.

---

### 3. Undo / Redo History (Back/Forward Arrows)

#### [MODIFY] index.html — History manager & Header UI

**Implementation:**
- Create a `HistoryManager` singleton.
- Stores snapshots of editable app state: band data, selected bands, blend values, toggles.
- Add simple **Back (Undo)** and **Forward (Redo)** arrow icons to the `<header>` (matching the Pro-Q 4 interface aesthetic).
- Enable `Ctrl+Z` and `Ctrl+Shift+Z` / `Ctrl+Y` shortcuts.
- Connect slider `change` / `mouseup` and click events to push state.

---

### 4. Preset Toggle (On/Off) Switch

#### [MODIFY] index.html — Preset Slots & Tab Blend Rows

- Add an `enabled` bypass toggle to each preset in `state`.
- **UI Element:** A power icon or simple toggle switch next to the mix slider in the Preset slots.
- **Merge Blend Panel & Tab Bar:** Add the toggle switch next to the blend sliders.
- When toggled off, the preset's curves disappear from the canvas (or become extremely dim) and its bands are excluded from the `mergedPreview` and final download output, without losing the recorded mix percentage.

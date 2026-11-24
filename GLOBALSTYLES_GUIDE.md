# GlobalStyles Guide — Bluloco Dark for Notepad++

## Overview

This guide documents all **54 `WidgetStyle` entries** in `BlulocoDark.xml` under `<GlobalStyles>`. Unlike `WordsStyle` (which belongs to a specific lexer), `WidgetStyle` controls **Notepad++ UI chrome** — the editor frame, margins, tabs, find bar, caret, selections, and more. These styles have no upstream VSCode equivalent; they are dictated entirely by Notepad++'s widget model.

> **Key point:** Many `WidgetStyle` entries share `styleID="0"`. This is intentional — in Notepad++, `styleID` in `GlobalStyles` is a legacy field used only for a handful of Scintilla-mapped widgets (Default Style, Brace highlight, etc.). For the rest, Notepad++ identifies widgets **by their `name` attribute alone**. Do not deduplicate or renumber these.

---

## Quick Reference Table

| # | Widget Name | styleID | fgColor | bgColor | fontStyle | Visual Role |
|---|-------------|---------|---------|---------|-----------|-------------|
| 1 | Default Style | 32 | ABB2BF | 282C34 | 0 | Fallback text color for any un-styled widget text |
| 2 | Indent guideline style | 37 | 3D434F | 282C34 | 0 | Vertical indent guides in the editing area |
| 3 | Brace highlight style | 34 | 7A82DA | 282C34 | 1 (bold) | Matching brace highlight (when cursor on brace) |
| 4 | Bad brace colour | 35 | FF2E3F | 282C34 | 0 | Mismatched/unpaired brace highlight |
| 5 | Current line background colour | 0 | — | 2D333D | — | Highlight of the line containing the caret |
| 6 | Selected text colour | 0 | FFFFFF | 1C4670 | — | Text color inside active selection |
| 7 | Multi-selected text color | 0 | — | 1C6143 | — | Background for additional multi-carets selections |
| 8 | Caret colour | 2069 | FFCC00 | — | — | The blinking text cursor (caret) |
| 9 | Multi-edit carets color | 0 | FFCC00 | — | — | Carets for multi-cursor editing |
| 10 | Edge colour | 0 | 3D434F | — | — | Vertical edge line (right margin guide) |
| 11 | Line number margin | 33 | 8A95B0 | 22252A | 0 | Line numbers gutter |
| 12 | Bookmark margin | 0 | — | 22252A | — | Bookmark icon column (left of line numbers) |
| 13 | Change History margin | 0 | — | 22252A | — | Change history marker column |
| 14 | Change History modified | 0 | FF936A | 22252A | — | Modified-since-save marker (orange) |
| 15 | Change History revert modified | 0 | 3FC56B | 22252A | — | Reverted modified marker (green) |
| 16 | Change History revert origin | 0 | 10B1FE | 22252A | — | Reverted to origin marker (blue) |
| 17 | Change History saved | 0 | 3FC56B | 22252A | — | Saved state marker (green) |
| 18 | Fold | 0 | 8A95B0 | 22252A | — | Fold margin symbols (collapsed/expanded) |
| 19 | Fold active | 0 | ABB2BF | — | — | Active fold symbol (hover/click state) |
| 20 | Fold margin | 0 | 3D434F | 22252A | — | Fold margin background |
| 21 | White space symbol | 0 | 3D434F | — | — | Whitespace dots/arrows (View → Show Symbol) |
| 22 | Smart Highlighting | 29 | — | 36465A | — | Highlight all occurrences of selected word |
| 23 | Find Mark Style | 31 | — | 1C6143 | — | "Mark all" results from Find dialog |
| 24 | Mark Style 1 | 25 | — | 215471 | — | Bookmark style 1 (blue tint) |
| 25 | Mark Style 2 | 24 | — | 684B44 | — | Bookmark style 2 (brown tint) |
| 26 | Mark Style 3 | 23 | — | 675B3F | — | Bookmark style 3 (yellow tint) |
| 27 | Mark Style 4 | 22 | — | 4C4571 | — | Bookmark style 4 (purple tint) |
| 28 | Mark Style 5 | 21 | — | 2F5A45 | — | Bookmark style 5 (green tint) |
| 29 | Incremental highlight all | 28 | — | 1C6143 | — | Incremental search highlight (Ctrl+I) |
| 30 | Tags match highlighting | 27 | — | 3A3F58 | — | Matching HTML/XML tag highlight |
| 31 | Tags attribute | 26 | — | 735047 | — | Attribute highlight in tag matching |
| 32 | Active tab focused indicator | 0 | 3691FF | — | — | Top border line on active tab (focused window) |
| 33 | Active tab text | 0 | ABB2BF | — | — | Text color on active tab |
| 34 | Inactive tabs | 0 | 8A95B0 | 25272D | — | Text + background for inactive tabs |
| 35 | URL hovered | 0 | 3691FF | — | — | Hovered clickable link color |
| 36 | Document map | 0 | ABB2BF | 282C34 | — | Minimap (Document Map panel) colors |
| 37 | Global override | 0 | ABB2BF | 282C34 | 0 | Overrides all lexer styles when enabled |
| 38 | EOL custom color | 0 | DADADA | — | — | End-of-line markers (¶, $) |
| 39 | Non-printing characters custom color | 0 | 3D434F | — | — | Spaces, tabs, other invisible chars |
| 40 | Find status: Not found | 0 | FF2E3F | — | 0 | "Not found" message in Find bar |
| 41 | Active tab unfocused indicator | 0 | 8A95B0 | — | 0 | Top border on active tab (unfocused window) |
| 42 | Tab color 1 | 0 | — | 215471 | 0 | Tab group color 1 (blue) |
| 43 | Tab color 2 | 0 | — | 684B44 | 0 | Tab group color 2 (brown) |
| 44 | Tab color 3 | 0 | — | 675B3F | 0 | Tab group color 3 (yellow) |
| 45 | Tab color 4 | 0 | — | 4C4571 | 0 | Tab group color 4 (purple) |
| 46 | Tab color 5 | 0 | — | 2F5A45 | 0 | Tab group color 5 (green) |
| 47 | Tab color dark mode 1 | 0 | — | 215471 | 0 | Dark mode tab group 1 |
| 48 | Tab color dark mode 2 | 0 | — | 684B44 | 0 | Dark mode tab group 2 |
| 49 | Tab color dark mode 3 | 0 | — | 675B3F | 0 | Dark mode tab group 3 |
| 50 | Tab color dark mode 4 | 0 | — | 4C4571 | 0 | Dark mode tab group 4 |
| 51 | Tab color dark mode 5 | 0 | — | 2F5A45 | 0 | Dark mode tab group 5 |
| 52 | (reserved) | — | — | — | — | |
| 53 | (reserved) | — | — | — | — | |
| 54 | (reserved) | — | — | — | — | |

> **Note:** The last three entries don't exist in the XML; the count is 51 actual styles. Notepad++ reserves additional slots for future use.

---

## Category Breakdown

### 1. Core Editor Surface (4 styles)

| Widget | Purpose | Key Colors |
|--------|---------|------------|
| **Default Style** | Ultimate fallback for any widget text not otherwise styled | fg `ABB2BF` (fg), bg `282C34` (bg) |
| **Current line background colour** | Highlights the line with the caret | bg `2D333D` (slightly lighter than editor bg) |
| **Global override** | When enabled (Style Configurator → Global override), forces all text to these colors | fg `ABB2BF`, bg `282C34` |
| **Document map** | Minimap panel colors | fg `ABB2BF`, bg `282C34` |

### 2. Caret & Selection (5 styles)

| Widget | Purpose | Key Colors |
|--------|---------|------------|
| **Caret colour** | Main blinking cursor | fg `FFCC00` (yellow) |
| **Multi-edit carets color** | Additional cursors in multi-cursor mode | fg `FFCC00` |
| **Selected text colour** | Text inside primary selection | fg `FFFFFF` on bg `1C4670` (blue tint) |
| **Multi-selected text color** | Background for secondary selections | bg `1C6143` (green tint) |
| **Incremental highlight all** | Ctrl+I incremental search matches | bg `1C6143` (green tint) |

### 3. Braces & Matching (3 styles)

| Widget | Purpose | Key Colors |
|--------|---------|------------|
| **Brace highlight style** | Matching brace (bold) | fg `7A82DA` (operator purple), bold |
| **Bad brace colour** | Unmatched brace | fg `FF2E3F` (error red) |
| **Tags match highlighting** | Matching HTML/XML tag pair | bg `3A3F58` (muted blue) |
| **Tags attribute** | Attribute in tag matching | bg `735047` (muted brown) |

### 4. Line Number & Margins (9 styles)

| Widget | Purpose | Key Colors |
|--------|---------|------------|
| **Line number margin** | Gutter with line numbers | fg `8A95B0` (comment), bg `22252A` (darker sidebar) |
| **Bookmark margin** | Bookmark icon column | bg `22252A` |
| **Fold margin** | Folding +/- column background | fg `3D434F`, bg `22252A` |
| **Fold** | Fold symbols (collapsed/expanded) | fg `8A95B0`, bg `22252A` |
| **Fold active** | Fold symbol on hover | fg `ABB2BF` |
| **Change History margin** | Change history column | bg `22252A` |
| **Change History modified** | Unsaved changes marker | fg `FF936A` (orange) |
| **Change History revert modified** | Reverted unsaved marker | fg `3FC56B` (green) |
| **Change History revert origin** | Reverted to saved marker | fg `10B1FE` (blue) |
| **Change History saved** | Saved state marker | fg `3FC56B` (green) |

### 5. Whitespace & Edge (3 styles)

| Widget | Purpose | Key Colors |
|--------|---------|------------|
| **Edge colour** | Vertical right-margin guide line | fg `3D434F` |
| **White space symbol** | Dots for spaces, arrows for tabs | fg `3D434F` |
| **EOL custom color** | End-of-line markers (¶) | fg `DADADA` (subtle) |
| **Non-printing characters custom color** | Other invisible chars | fg `3D434F` |

### 6. Smart Highlighting & Find (4 styles)

| Widget | Purpose | Key Colors |
|--------|---------|------------|
| **Smart Highlighting** | Double-click word → highlight all occurrences | bg `36465A` (muted blue-green) |
| **Find Mark Style** | "Mark all" in Find/Replace dialog | bg `1C6143` (green tint) |
| **Find status: Not found** | "Not found" text in Find bar | fg `FF2E3F` (error red) |
| **URL hovered** | Clickable link hover state | fg `3691FF` (link blue) |

### 7. Bookmarks / Mark Styles (5 styles)

Five user-configurable mark styles (right-click line → Bookmark → Style 1–5):

| Widget | styleID | bgColor | Tint |
|--------|---------|---------|------|
| Mark Style 1 | 25 | 215471 | Blue |
| Mark Style 2 | 24 | 684B44 | Brown |
| Mark Style 3 | 23 | 675B3F | Yellow |
| Mark Style 4 | 22 | 4C4571 | Purple |
| Mark Style 5 | 21 | 2F5A45 | Green |

> These use only `bgColor` (no `fgColor`) — they tint the line background.

### 8. Tab Bar (13 styles)

| Widget | Purpose | Key Colors |
|--------|---------|------------|
| **Active tab focused indicator** | Top border on active tab (window focused) | fg `3691FF` (blue) |
| **Active tab unfocused indicator** | Top border on active tab (window unfocused) | fg `8A95B0` (muted) |
| **Active tab text** | Text on active tab | fg `ABB2BF` |
| **Inactive tabs** | Text + bg for inactive tabs | fg `8A95B0`, bg `25272D` |
| **Tab color 1–5** | Tab group colors (light theme) | bg `215471` / `684B44` / `675B3F` / `4C4571` / `2F5A45` |
| **Tab color dark mode 1–5** | Tab group colors (dark theme) | Same as above |

> **Tab groups:** Right-click a tab → "Tab color" → assign 1–5. Useful for visual project grouping.

### 9. Indent Guides (1 style)

| Widget | Purpose | Key Colors |
|--------|---------|------------|
| **Indent guideline style** | Vertical indent lines | fg `3D434F` (subtle) |

---

## Color Provenance

| Color | Role | Source |
|-------|------|--------|
| `282C34` | Editor background | Canonical palette `bg` |
| `2D333D` | Current line highlight | UI exception (slightly lighter bg) |
| `22252A` | Margin/sidebar background | UI exception (darker than editor) |
| `25272D` | Inactive tab background | UI exception |
| `ABB2BF` | Default foreground | Canonical palette `fg` |
| `8A95B0` | Comments / muted text | Canonical palette `comments` (v2.3.2+) |
| `3D434F` | Subtle UI lines (guides, edge, whitespace) | UI exception |
| `1C4670` | Selection background | Documented exception (selection tint) |
| `1C6143` | Multi-selection / find mark | Documented exception (search tint) |
| `36465A` | Smart highlighting | Documented exception |
| `215471` | Mark Style 1 / Tab color 1 | Documented exception |
| `684B44` | Mark Style 2 / Tab color 2 | Documented exception |
| `675B3F` | Mark Style 3 / Tab color 3 | Documented exception |
| `4C4571` | Mark Style 4 / Tab color 4 | Documented exception |
| `2F5A45` | Mark Style 5 / Tab color 5 | Documented exception |
| `3A3F58` | Tag match highlight | Documented exception |
| `735047` | Tag attribute highlight | Documented exception |
| `FFCC00` | Caret | UI exception (high visibility yellow) |
| `FF2E3F` | Error / bad brace / not found | Canonical palette `errors` |
| `7A82DA` | Brace highlight / operators | Canonical palette `operators` |
| `3FC56B` | Change history saved/revert | Canonical palette `functions` (green) |
| `FF936A` | Change history modified | Canonical palette `attrs` (orange) |
| `10B1FE` | Change history revert origin | Canonical palette `keywords` (blue) |
| `3691FF` | Active tab indicator / URL hover | Canonical palette `tags` (blue) |
| `DADADA` | EOL markers | UI exception (subtle) |

---

## Editing Guidelines

1. **Never change `styleID` values** — Notepad++ matches widgets by `name`, not `styleID`. Only these few map to Scintilla: 32 (Default), 33 (Line number), 34 (Brace highlight), 35 (Bad brace), 37 (Indent guide), 21–29 (Mark styles).

2. **Preserve `styleID="0"` duplicates** — This is the expected pattern for name-matched widgets.

3. **Keep `fontName=""` and `fontSize=""` empty** — Let Notepad++ use the global font setting.

4. **`fontStyle`** — Only `Brace highlight style` uses `1` (bold). All others `0` or empty.

5. **When adjusting colors:**
   - Use canonical palette roles where possible
   - Document any new exceptions in this guide
   - Run `python3 tools/validate_theme.py` after changes

6. **Testing:** Visual verification requires Windows + Notepad++ 8.9.9. Load the theme, open Settings → Style Configurator → Global Styles, and inspect each widget.

---

## Related Files

- `BlulocoDark.xml` — Source of truth (search `<GlobalStyles>`)
- `tools/validate_theme.py` — Validates contrast, palette adherence, structure
- `tools/npp_lexer_model.json` — Notepad++ v8.9.9 stylers.model.xml inventory
- `README.md` — User documentation (references this guide)

---

*Generated for Bluloco Dark v2.3.2+ — part of the documentation overhaul to make the theme fully auditable and maintainable.*
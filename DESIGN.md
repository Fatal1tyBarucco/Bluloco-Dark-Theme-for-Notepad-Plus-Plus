---
name: Bluloco Dark Theme for Notepad++
description: Audited, palette-normalized port of the VSCode Bluloco Dark theme to Notepad++ with 67 lexers and validation tooling
colors:
  # Canonical token palette (14 roles) — normalized against upstream bluloco-dark-color-theme.json
  base-bg: "#282C34"
  base-fg: "#ABB2BF"
  comment: "#636D83"
  keyword: "#10B1FE"
  string: "#F9C859"
  number: "#FF78F8"
  function: "#3FC56B"
  class-type: "#FF6480"
  error: "#FF2E3F"
  constant: "#9F7EFE"
  parameter: "#8BCDEF"
  property: "#CE9887"
  operator: "#7A82DA"
  tag: "#3691FF"
  attribute: "#FF936A"
  decorator: "#50ACAE"
  namespace: "#FF839B"
  # Documented exceptions
  doc-comment: "#7C8495"
  # Notepad++ UI chrome (GlobalStyles widgets — no VSCode counterpart)
  ui-current-line: "#2D333D"
  ui-margin-bg: "#22252A"
  ui-border: "#3D434F"
  ui-caret: "#FFCC00"
  ui-selection: "#0084FF"
  ui-selection-text: "#FFFFFF"
  ui-find-mark: "#1C6143"
  ui-smart-highlight: "#36465A"
  ui-mark-1: "#215471"
  ui-mark-2: "#684B44"
  ui-mark-3: "#675B3F"
  ui-mark-4: "#4C4571"
  ui-mark-5: "#2F5A45"
  ui-incremental: "#1C6143"
  ui-tag-match: "#3A3F58"
  ui-tag-attr: "#735047"
  ui-tab-inactive-bg: "#25272D"
  ui-tab-active-indicator: "#3691FF"
  ui-tab-unfocused: "#636D83"
  ui-url-hover: "#3691FF"
  ui-doc-map: "#282C34"
  ui-eol: "#DADADA"
  ui-nonprint: "#3D434F"
  ui-find-not-found: "#FF2E3F"
  ui-tab-color-1: "#215471"
  ui-tab-color-2: "#684B44"
  ui-tab-color-3: "#675B3F"
  ui-tab-color-4: "#4C4571"
  ui-tab-color-5: "#2F5A45"
  # ANSI terminal ramp (errorlist lexer — carried verbatim from upstream terminal.ansi*)
  ansi-black: "#42444D"
  ansi-red: "#FF2E3F"
  ansi-green: "#25A45C"
  ansi-brown: "#FF936A"
  ansi-blue: "#3375FE"
  ansi-magenta: "#9F7EFE"
  ansi-cyan: "#4483AA"
  ansi-gray: "#CDD3E0"
  ansi-dark-gray: "#8F9AAE"
  ansi-bright-red: "#FF6480"
  ansi-bright-green: "#3FC56B"
  ansi-yellow: "#F9C859"
  ansi-bright-blue: "#10B1FE"
  ansi-bright-magenta: "#FF78F8"
  ansi-bright-cyan: "#5FB9BC"
  ansi-white: "#FFFFFF"
typography:
  default:
    fontFamily: "Consolas, 'Fira Code', 'JetBrains Mono', 'Cascadia Code', monospace"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0"
  # Notepad++ uses a single editor font; no display/headline hierarchy in the theme itself
rounded: {}
spacing: {}
components: {}
---

# Design System: Bluloco Dark Theme for Notepad++

## Overview

**Creative North Star: "The Deep-Syntax Lab"**

A clinical, audited dark syntax theme where every color has a defined semantic role and every deviation from the canonical palette is documented with provenance. The system prioritizes fidelity to the upstream Bluloco Dark VSCode theme over completeness — 67 lexers are covered with palette-perfect accuracy, while 26 lexers honestly fall back to the default style rather than receiving invented colors.

The aesthetic is precise and tool-like: blue-based accents (`#10B1FE` keywords, `#3691FF` tags, `#8BCDEF` parameters) against a deep charcoal base (`#282C34`), with warm gold strings (`#F9C859`), magenta numbers (`#FF78F8`), green functions (`#3FC56B`), and coral types (`#FF6480`). Comments sit at a deliberate sub-AA contrast (`#636D83` on `#282C34` = 2.7:1), matching the upstream's trade-off. The only colors outside the 14-role token palette are the `errorlist` ANSI terminal ramp (16 colors, styleIDs 40–55), Notepad++ UI chrome widgets (28 GlobalStyles entries), the documentation-comment grey (`#7C8495`), and selection/search/mark/tab tints — each group documented with its rationale.

**Key Characteristics:**
- 14-role canonical token palette applied without deviation across all 67 lexers
- USER KEYWORDS 1–8 scheme traceable to upstream `semanticTokenColors` (property, constant, parameter, function, decorator, namespace, typeParameter, macro)
- Static validation gate: XML syntax, hex format, palette adherence, WCAG contrast, SHA-256 drift detection
- Honest limitations documented: 26 unthemed lexers, style-ID coverage gaps, comment contrast below AA, ANSI ramp exception
- No build system, no generated files — the XML is the source of truth

## Colors

A single 14-role palette governs all token styles. Every `fgColor`/`bgColor` in `BlulocoDark.xml` maps to one of these roles or a documented exception group.

### Primary

- **Base Background** (`#282C34`): Editor background, default token background — the foundation charcoal
- **Base Foreground** (`#ABB2BF`): Default text, identifiers, fallback color — soft silver with high readability

### Secondary

- **Keyword Blue** (`#10B1FE`): Keywords, storage types, preprocessor directives, instruction words — the primary accent
- **Tag Blue** (`#3691FF`): HTML/XML tags, CSS selectors/classes, YAML references, GDScript node paths — structural markers
- **Function Green** (`#3FC56B`): Function/method definitions, macros, diff additions, INI sections — executable constructs
- **String Gold** (`#F9C859`): All string literals, regex, template literals, heredocs, verbatim strings — data content
- **Number Magenta** (`#FF78F8`): Numeric literals across all languages — distinct from strings and keywords
- **Class/Type Coral** (`#FF6480`): Class names, type definitions, CSS IDs, SQL keywords — type-level constructs
- **Error Crimson** (`#FF2E3F`): Errors, bad braces, find marks, diff deletions, lexer errors — critical signals

### Tertiary

- **Constant Violet** (`#9F7EFE`): Constants, enums, TOML keys, Haskell modules, Erlang atoms — immutable values
- **Parameter Cyan** (`#8BCDEF`): Parameters, Rust lifetimes, LaTeX optional args — contextual variables
- **Property Terracotta** (`#CE9887`): Object properties, JSON keys, CSS variables, Python attributes — member access
- **Operator Violet** (`#7A82DA`): Operators, punctuation, braces, brackets — structural syntax
- **Attribute Amber** (`#FF936A`): HTML/XML attributes, CSS property names, TOML escape chars, JSON compact IRIs — metadata
- **Decorator Mint** (`#50ACAE`): Decorators, annotations, GDScript annotations — meta-programming
- **Namespace Rose** (`#FF839B`): Namespaces, modules, Erlang node names — organizational scope

### Neutral

- **Comment Slate** (`#636D83`): All comments, doc comments, comment lines — deliberately sub-AA (2.7:1) to match upstream
- **Doc Comment Grey** (`#7C8495`): Documentation comment keywords (COMMENT DOC KEYWORD) — slightly warmer than base comments

### Named Rules

**The Palette Fidelity Rule.** No token style may use a color outside the 14-role canonical palette except for the four documented exception groups: (1) `errorlist` ANSI terminal ramp (styleIDs 40–55), (2) Notepad++ UI chrome in `GlobalStyles` (28 widget styles), (3) documentation-comment grey (`#7C8495`), (4) GlobalStyles selection/search/mark/tab tints. Any new color requires a documented provenance decision.

**The ANSI Ramp Preservation Rule.** The `errorlist` lexer's ANSI COLOR styles (styleIDs 40–55) reproduce a real terminal's 16-color ramp verbatim from the upstream `terminal.ansi*` tokens. These are not aligned to the Bluloco palette and must not be "corrected" — they are a faithful terminal emulation.

**The Deliberate Divergence Rule.** `errorlist` ANSI COLOR RED uses `#FF2E3F` (the theme's canonical error color) while the upstream source uses `terminal.ansiRed` = `#FC2F52`. This is a documented intentional divergence for internal consistency, not an error.

## Typography

Notepad++ themes do not define a typographic hierarchy — they specify only the editor font via the Default Style widget. The theme deliberately removed the hardcoded `fontName="monofur for Powerline"` and `fontSize="12"` in v2.2 to respect the user's configured editor font.

**Editor Font:** Consolas, Fira Code, JetBrains Mono, Cascadia Code, monospace (user-configured)
**Character:** Monospace, programming-oriented, ligature-capable when available. The theme imposes no font opinion.

**Named Rule:**

**The User Font Rule.** The theme never hardcodes a font family or size in the Default Style widget. Font choice belongs entirely to the user via Notepad++'s Font Settings.

## Layout

Notepad++ themes do not control layout — they provide color assignments for Scintilla lexer styles and GlobalStyles widgets. Spatial rhythm, density, and responsive behavior are editor concerns, not theme concerns.

**Widget Color Assignments (GlobalStyles):**
- **Current line highlight:** `#2D333D` (bg only)
- **Selection:** `#1C4670` bg / `#FFFFFF` fg
- **Multi-selection:** `#1C6143` bg
- **Line numbers:** `#636D83` fg / `#22252A` bg
- **Fold margin:** `#3D434F` fg / `#22252A` bg
- **Indent guides:** `#3D434F`
- **Smart highlighting:** `#36465A` bg
- **Find marks:** `#1C6143` bg
- **Mark styles 1–5:** `#215471`, `#684B44`, `#675B3F`, `#4C4571`, `#2F5A45` bg
- **Tab colors 1–5 (light/dark):** `#215471`, `#684B44`, `#675B3F`, `#4C4571`, `#2F5A45` bg
- **Active tab indicator:** `#3691FF` fg
- **Inactive tabs:** `#636D83` fg / `#25272D` bg

## Elevation & Depth

This system uses **tonal layering only — no shadows**. Depth is conveyed through background color shifts:

- Base layer: `#282C34` (editor background)
- Margin/chrome layer: `#22252A` (darker, recessive)
- Current line: `#2D333D` (slightly lifted)
- Selection: `#1C4670` (blue tint, focused)
- Inactive tabs: `#25272D` (recessed)
- Active tab indicator: `#3691FF` (accent line)

**Named Rule:**

**The Flat-By-Design Rule.** Notepad++ themes cannot express shadows or elevation. Depth is communicated exclusively through background color temperature and saturation shifts within the dark palette.

## Shapes

Not applicable — the theme defines only color assignments. Corner radius, borders, and form language are controlled by Notepad++'s native UI, not the theme XML.

## Components

Notepad++ themes have no component library in the web sense. The closest analogs are the **GlobalStyles widgets** (51 entries) and **LexerType style blocks** (67 lexers × ~18 styles avg = ~1,212 WordsStyle entries). These are documented in the XML and validated by `tools/validate_theme.py`.

### GlobalStyles Widgets (51)

Each widget maps a Notepad++ UI element to a color role. Key widgets:

| Widget | StyleID | Colors | Role |
|--------|---------|--------|------|
| Default Style | 32 | `#ABB2BF` / `#282C34` | Base editor text |
| Current line background | 0 | `#2D333D` | Line highlight |
| Selected text | 0 | `#1C4670` / `#FFFFFF` | Selection |
| Multi-selected text | 0 | `#1C6143` | Multi-caret selection |
| Brace highlight | 34 | `#7A82DA` / `#282C34` (bold) | Matching brace |
| Bad brace | 35 | `#FF2E3F` / `#282C34` | Mismatched brace |
| Line number margin | 33 | `#636D83` / `#22252A` | Line numbers |
| Caret | 2069 | `#FFCC00` | Insertion point |
| Smart Highlighting | 29 | `#36465A` | Symbol matches |
| Find Mark | 31 | `#1C6143` | Find results |
| Mark Styles 1–5 | 25–21 | Five tinted backgrounds | User marks |
| Tab colors 1–5 | 0 | Five backgrounds | Document tabs |

### LexerType Styles (67 lexers)

Each lexer defines `WordsStyle` entries mapping Scintilla styleIDs to palette roles. The mapping follows a consistent cross-lexer pattern:

| Semantic Role | Palette Color | Example Lexers |
|---------------|---------------|----------------|
| Keywords/Instructions | `#10B1FE` | All C-family, Python, JS, TS, Go, Java, etc. |
| Types/Classes | `#FF6480` | C, C++, C#, Java, Go, TypeScript, Rust, Swift, etc. |
| Functions | `#3FC56B` | Python, Ruby, Lua, PowerShell, NSIS, etc. |
| Strings | `#F9C859` | Universal |
| Numbers | `#FF78F8` | Universal |
| Comments | `#636D83` | Universal |
| Operators | `#7A82DA` | Universal |
| Tags (HTML/XML) | `#3691FF` | HTML, XML, CSS, LaTeX, GDScript |
| Attributes | `#FF936A` | HTML, XML, CSS, TOML, YAML |
| Decorators/Annotations | `#50ACAE` | Python, TypeScript, Nim, GDScript |
| Namespaces/Modules | `#FF839B` | Haskell, Erlang, Rust (macro), etc. |
| Constants | `#9F7EFE` | Haskell, Erlang, TOML, etc. |
| Parameters | `#8BCDEF` | Rust lifetimes, LaTeX, CMake, etc. |
| Properties | `#CE9887` | JSON, CSS, Python, GDScript |

**USER KEYWORDS 1–8** (manual keyword lists in Style Configurator) follow the upstream `semanticTokenColors` mapping:

| Slot | Role | Color | Lexers |
|------|------|-------|--------|
| 1 | Property | `#CE9887` | C-family, Python, JS, TS, PHP, ASP, Bash, Lua, GDScript |
| 2 | Constant | `#9F7EFE` | C-family, Python, JS, TS, PHP, ASP, Bash, Lua, GDScript |
| 3 | Parameter | `#8BCDEF` | C-family, Python, JS, TS, PHP, ASP, Bash, Lua, GDScript |
| 4 | Function | `#3FC56B` | C-family, Python, JS, TS, PHP, ASP, Bash, Lua, GDScript |
| 5 | Decorator | `#50ACAE` | C-family, Python, JS, TS, PHP, ASP, Lua, GDScript |
| 6 | Namespace | `#FF839B` | C-family, Python, JS, TS, PHP, ASP, Lua, GDScript |
| 7 | Type Parameter | `#FF6480` | C-family, Python, JS, TS, PHP, ASP, Lua, GDScript |
| 8 | Macro | `#3FC56B` | C-family, Python, JS, TS, PHP, ASP, Lua, GDScript |

## Do's and Don'ts

### Do:

- **Do** map every new token style to one of the 14 canonical palette roles — consult the palette table before assigning a color
- **Do** run `python3 tools/validate_theme.py` after any XML edit — it catches palette drift, hex format errors, contrast issues, and SHA-256 baseline drift
- **Do** add missing styleIDs by consulting `tools/npp_lexer_model.json` (Notepad++ v8.9.9 `stylers.model.xml` inventory) — never invent a styleID
- **Do** document any new palette exception in the XML comments and README — exceptions are legitimate but must be traceable
- **Do** preserve the USER KEYWORDS 1–8 semantic mapping when adding support to a new lexer — slots 1–8 have fixed roles
- **Do** keep `fontStyle="0"` for all code tokens (except `searchResult` styles 1/2 and Brace highlight which use bold)
- **Do** use uppercase 6-digit hex without `#` prefix — the validator enforces this

### Don't:

- **Don't** introduce a color not in the canonical palette or documented exceptions without a recorded provenance decision
- **Don't** "fix" the `errorlist` ANSI ramp colors to match the Bluloco palette — they are terminal emulation, not syntax tokens
- **Don't** hardcode a font family or size in the Default Style widget — the user's font choice must be respected
- **Don't** claim visual verification without a real Notepad++ on Windows — renders and screenshots are illustrative only
- **Don't** present the 7 PNG screenshots as evidence of the current palette — they predate the v2.1 normalization
- **Don't** present the 7 SVG renders as visual verification — they are programmatic approximations of Scintilla lexers
- **Don't** remove existing lexers or styles without justification — coverage reductions must be intentional and documented
- **Don't** reformat or reorder the XML wholesale — make focused diffs only

---

*Generated from `BlulocoDark.xml` v2.2 (67 lexers, 1,212 WordsStyle entries, 51 GlobalStyles widgets) — validated by `tools/validate_theme.py` with 0 errors, 334 warnings (contrast and coverage).*
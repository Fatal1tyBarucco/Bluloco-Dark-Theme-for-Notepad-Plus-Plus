# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Added `tools/validate_renders.py` and a CI step to validate all seven SVG previews for XML well-formedness, current README release marker, explicit non-screenshot disclosure, and fill/stroke colour provenance against `BlulocoDark.xml`.

### Changed
- Updated `AGENTS.md` from stale v2.2/v2.3 render references to the released v2.3.1 state and documented the limits of automated render validation.
- Updated the README hero image to use the current programmatic SVG preview and explicitly separated it from historical pre-v2.1 PNG screenshots.

### Validation limits
- SVG validation does not verify Scintilla token classification or native Notepad++ rendering. A real Windows + Notepad++ visual pass remains required before claiming 100% visual fidelity.

## [2.3.1] - 2026-11-10

### Fixed
- **css**: restored the three missing `keywordClass` mappings — `PSEUDOCLASS` (styleID 3) `instre2`, `PSEUDOELEMENT` (18) `type3`, `LEGACY PSEUDOELEMENT` (20) `type5` — the only keyword lists the theme had silently dropped (all other 311 theme `keywordClass` values match the current `stylers.model.xml` exactly).
- **nim**: `END OF LINE WHERE STRING IS NOT CLOSED` (13, `SCE_NIM_STRINGEOL`) `FF2E3F` → `F9C859`, matching all 12 other string-EOL states; `HIGHLIGHTED IDENTIFIERS` (14, actually `SCE_NIM_NUMERROR` per `SciLexer.h`/`LexNim.cxx` — the stylers label is stale) `9F7EFE` → `FF2E3F`, matching the theme ERROR convention (json/yaml/toml).
- **makefile**: `IDEOL` (9, `SCE_MAKE_IDEOL`, "error identifier / incomplete identifier reference" per `LexMake.cxx`) `FF936A` → `FF2E3F`.
- **toml**: `KEYWORD` (3, instre1 = `false inf nan true`) `9F7EFE` → `10B1FE`, matching upstream `constant.language` and the theme's json `KEYWORD`.
- **go**: `PREDECLARED IDENTIFIERS` (19, instre2 = 19 builtin functions + 5 constants) `9F7EFE` → `3FC56B`, matching upstream `function.defaultLibrary` and the theme's python `BUILTINS`.

### Added
- **GlobalStyles**: `Find status: Message` (`3691FF`, upstream `debugConsole.infoForeground`) and `Find status: Search end reached` (`3FC56B`) — documented since v2.2 but never actually present in the XML; without them Notepad++ falls back to its `0000FF`/`008000` defaults, unreadable on the dark background.
- **GlobalStyles**: `Find matches highlight all` (styleID 28, bg `1C6143`) alongside the legacy `Incremental highlight all` name — the current `stylers.model.xml` renamed this widget; identical colours under both names cover every Notepad++ build.
- `renders/` — 7 programmatic SVG previews (`css`, `html`, `js`, `php`, `py`, `rb`, `ts`) generated directly from the v2.3.1 `BlulocoDark.xml`: every colour is extracted from the theme file and the content comes from `samples/sample.*`. Clearly labelled as renders, **not** screenshots; visual verification still requires Windows + Notepad++. Python preview: `BUILTINS` (`print`, `sum`, `int`) `3FC56B` and `DECORATOR` (`@debug`) `50ACAE` (`None` keeps the keyword colour `10B1FE` — it is instre1, not a builtin); TypeScript preview: the line-1 comment now uses the comment colour (`636D83`).
- README: Renders gallery subsection, repository tree and Known Limitations updated for the regenerated previews.

### Changed
- `tools/baseline.json` regenerated for the new XML (67 lexers, 1212 words styles, 54 widget styles).

## [2.3] - 2026-11-09

### Fixed
- **Structural bug**: the `ini` KEY (styleID 5) and `vhdl` COMMENT BLOCK (styleID 15) styles were declared after their `</LexerType>` closers (with stray LF line endings), where Notepad++ never loads them. Both now sit inside their `<LexerType>` blocks; every themed lexer has full style-ID coverage against the v8.9.9 `stylers.model.xml`.
- **Upstream fidelity**: python TRIPLE (6) / F TRIPLE (18) → `F9C859`, DECORATOR (15) → `50ACAE`, BUILTINS (14) → `3FC56B`; css IDENTIFIER (6) / UNKNOWN_IDENTIFIER (7) → `CE9887` (`meta.property-name`); erlang MODULE NAME (23) → `FF839B`; haskell MODULE (7) → `FF839B`, CLASS (6) → `FF6480`; ini/props ASSIGNMENT (3) → `7A82DA` (`punctuation.separator.key-value`); javascript.js WINDOW INSTRUCTION (19) → `10B1FE`; vhdl ATTRIBUTE (10) → `FF6480`, STD PACKAGE (12) → `FF839B`; gdscript STRING EOL (13) → `F9C859`.
- **`IDENTIFIER` policy**: 16 lexers coloured plain identifier states as keywords, functions or types; Scintilla identifier states cannot distinguish variables from function calls, and the upstream theme renders plain identifiers `#abb2bf`, so all `IDENTIFIER` styles now use `ABB2BF` (asp 86, makefile 3, pascal 1, bash 8, fortran 7, fortran77 7, lisp 9, asm 5, ruby 11, vhdl 6, caml 1, verilog 11, ada 2, matlab 7, haskell 1, inno 12). Function colouring remains USER KEYWORDS 4.
- **Contrast**: `searchResult` `Selected Line` (styleID 5) used `ABB2BF` on `3691FF` (≈1.5:1); now `FFFFFF` on `3691FF`. `json` ERROR (13) used `F9C859` on `FF2E3F` (≈2.4:1); now `FF2E3F` on `282C34` like all other ERROR styles.
- **README**: the unthemed-lexer list cited `er` (which does not exist in the model) and omitted `avs` and `baanc`; corrected to the real 26 lexer names.
- **nfo** DEFAULT (32): missing `fontStyle="0"` added.

### Changed
- **46 style names** aligned to `tools/npp_lexer_model.json` (`DOUBLESTRING` → `DOUBLE STRING`, `USER TAGS 1` → `USER TAGS1`, `COMMENTLINE` → `COMMENT LINE`, …) so Style Configurator labels match the Notepad++ model.
- **`COMMENT DOC KEYWORD ERROR`** unified to the comment colour `636D83` in swift (18), javascript.js (18), coffeescript (18) and d (17) — was `7C8495`; Scintilla treats an unrecognized doc keyword as plain comment text, matching the other 9 lexers.
- **`searchResult` `Current line background colour`** (6) is bg-only again (`fgColor` removed), matching the stock theme.

### Added
- **`tools/validate_theme.py` hardening**: warns on style-name drift vs `tools/npp_lexer_model.json`, errors on `<WordsStyle>` outside its lexer block or `<WidgetStyle>` outside `<GlobalStyles>` (the exact v2.2 bug class), and whitelists the 10 Lexilla-only states (`KNOWN_LEXILLA_STATES`) that exist in SciLexer.h but not in the v8.9.9 model.
- **`tools/baseline.json`** regenerated against the v2.3 XML (SHA-256, line/byte counts, full per-style inventory).

## [2.2] - 2026-11-08

### Added
- **12 new themed lexers**: rust, swift, yaml, javascript.js (standalone), coffeescript, erlang, d, nim, r, scheme, latex, gdscript — coverage against the Notepad++ v8.9.9 `stylers.model.xml` with exact `keywordClass` values.
- **26 missing styleIDs added** across 11 existing lexers: cpp STRINGRAW 20; html/xml SGML 22–25/31; php COMPLEX VARIABLE 104; ini KEY 5; props SECTION 2/KEY 5; pascal 6/8/10/15; lua 11/20; lisp FUNCTION WORD2 4; vhdl COMMENT BLOCK 15; powershell IDENTIFIER 7/FUNCTION 11/USER KEYWORDS 12.
- **New USER KEYWORDS 1–8 scheme** traceable to upstream `semanticTokenColors`: 1=property `CE9887`, 2=constant `9F7EFE`, 3=parameter `8BCDEF`, 4=function `3FC56B`, 5=decorator `50ACAE`, 6=namespace `FF839B`, 7=typeParameter `FF6480`, 8=macro `3FC56B`.
- **New palette colors**: `50ACAE` (decorator/label), `FF839B` (namespace/module).
- **GlobalStyles**: selection/search/mark/tab tints (`1C4670`, `1C6143`, `36465A`, `215471`, `684B44`, `675B3F`, `4C4571`, `2F5A45`, `3A3F58`, `735047`); Find status widgets: Not found, Message, Search end reached, Active tab unfocused indicator, Tab color 1–5 and Tab color dark mode 1–5.
- `tools/generate_baseline.py` (reproducible) + regeneration of `tools/baseline.json`.
- Hardening of `tools/validate_theme.py`: out-of-palette→error with documented exceptions; text in `WordsStyle`; duplicates; fg==bg; unknown IDs; widget bg-only contrast; README consistency.

### Changed
- **VERBATIM**: `FF78F8` → `F9C859` (string color) in all lexers that had it.
- **Default Style**: removed `fontName="monofur for Powerline"` and `fontSize="12"` (respects the user's font).
- **fontStyle** normalized to `0` for code tokens (except `searchResult` 1/2 and Brace highlight).
- **75 "neutralized" tokens** (`fgColor` `ABB2BF` with a semantic role) corrected to the correct semantic color.
- **Renamings aligned to the model**: php 121 KEYWORDS; pascal 3/4; lua 16–19; vhdl 2.

### Removed
- Spurious text inside `<WordsStyle>` of `searchResult` styles 5/6.

### Fixed
- `searchResult` styles 5/6 had no inner content.

### Documentação
- `README.md`/`AGENTS.md` reconciled with the XML v2.2 (counts, colors, honest limitations).
- 8 new samples in `samples/`: `sample.coffee`, `sample.erl`, `sample.d`, `sample.nim`, `sample.r`, `sample.scm`, `sample.tex`, `sample.gd`.

## [2.1] - 2026-11-07
### Fixed
- **Color accuracy audit**: Corrected 9 critical color mismatches vs VSCode Bluloco Dark reference
  - Error/Bad Brace/Find Mark: `FC2E51` → `FF2E3F`
  - Python triple strings: now use string yellow (`F9C859`) instead of comment color
  - CSS class/selectors: standardized to `3691FF` (blue)
  - CSS property names: standardized to `FF936A` (orange)
  - HTML attribute values: now `F9C859` (string yellow) instead of pink
  - JSON `true`/`false`/`null`: now `10B1FE` (keyword blue) instead of green
  - TOML escape characters: now `FF936A` (orange) instead of green
- **Documentation reconciliation**: `AGENTS.md` and `README.md` now describe the shipped v2.1 theme accurately (searchResult palette migration, JSON/CSS/Python/HTML token colours, Objective-C's lack of USER KEYWORDS slots, lexer coverage gaps, sample set, validator tooling)
- **License attribution**: the documentation stated that the original Bluloco theme was MIT-licensed; the upstream repository is licensed under **LGPL-3.0**, so `README.md` now states LGPL-3.0 and links the upstream `LICENSE` (the repository `LICENSE` was already LGPL-3.0)
- **Stale palette claims in `README.md`**: the "off-palette variants" statements and the stale per-language colour references no longer match the XML and were corrected
- **Regression baseline counters were stale**: `tools/baseline.json` had been generated against the pre-v2.1 XML, so `theme.words_style_count` (928 → 950), the per-lexer `style_count` of 11 lexers and the coverage counters were regenerated against the current theme (`total_unknown_style_ids` 26 → 11, `total_missing_model_style_ids` 63 → 26, `total_name_mismatches` 22 → 8, `lexers_with_missing_styles` 20 → 11, `suspected_copied_lexers` now empty)

### Changed
- **Palette consistency**: Applied canonical Bluloco palette across all 55 lexers
  - Keywords: `10B1FE` | Numbers: `FF78F8` | Classes/Types: `FF6480`
  - Functions: `3FC56B` | Constants: `9F7EFE` | Parameters: `8BCDEF`
  - Properties: `CE9887` | Operators: `7A82DA` | Tags: `3691FF`
  - Attributes: `FF936A` | Errors: `FF2E3F`
- **Full palette normalization against the upstream source**: the token palette was normalized in full against the original VSCode source (`uloco/theme-bluloco-dark` @ `d604c347564d16eea5a98c5fb1fb1703816929b5`, file `themes/bluloco-dark-color-theme.json`) — **88 colour attributes across 9 colour pairs** were corrected, removing drift and transcription typos that do not exist in the source. Every token style now uses the canonical palette.
  - `14B5FF` → `10B1FE` (76)
  - `FF7A96` → `FF6480` (4)
  - `9FD6F0` → `8BCDEF` (1 — tcl `USER3`, styleID 18)
  - `9FD6F0` → `CE9887` (1 — css `VARIABLE`, styleID 23)
  - `FFA57A` → `FF936A` (2)
  - `FF637F` → `FF6480` (1)
  - `3FC56A` → `3FC56B` (1)
  - `F9C858` → `F9C859` (1)
  - `10B0FE` → `10B1FE` (1)
  - Total: 76+4+1+1+2+1+1+1+1 = **88** colour attributes changed
- **Palette exceptions documented**: the only colours outside the canonical palette are the `errorlist` ANSI terminal ramp (styleIDs 40–55), the Notepad++ UI chrome colours in `GlobalStyles`, and the documentation-comment grey (`7C8495`)
- **Screenshot gallery**: the 7 PNGs in `screenshots/` are real Notepad++ captures, but they were taken before the palette normalization; `README.md` now states this, and the v2.1 visual check still requires Windows + Notepad++
- **USER KEYWORDS rationalization (Wave 3)**:
  - Python: Added USER KEYWORDS 1–8 (128–135) + DECORATOR (15) + ATTRIBUTE (20)
  - JavaScript: USER KEYWORDS 1–8 corrected to styleIDs 200–207
  - TypeScript: USER KEYWORDS 1–8 at 128–135 + WINDOW INSTRUCTION (19) + STRING RAW (20)
  - All C-family lexers: Differentiated USER KEYWORDS 5–8 (decorator, namespace, typeParameter, macro)
  - PHP, ASP, Bash, Lua: Rationalized USER KEYWORDS to match lexer capabilities
  - USER KEYWORDS 3 standardized to `8BCDEF` (parameters) per palette model

### Added
- **Source provenance**: `README.md` and `AGENTS.md` now record the upstream repository, the reference commit (`d604c347564d16eea5a98c5fb1fb1703816929b5`), the reference file (`themes/bluloco-dark-color-theme.json`), and the fact that the port was audited colour by colour against that file
- **Deliberate divergence recorded**: `errorlist` `ANSI COLOR RED` is kept at `FF2E3F` instead of the source's `terminal.ansiRed` (`#fc2f52`), on purpose, for internal consistency with the theme's canonical error colour — a documented decision, not an oversight
- **Static validation tooling**:
  - `tools/validate_theme.py`: XML syntax, palette adherence, hex format, WCAG contrast, plus coverage of the `GlobalStyles` widget colours and SHA-256 drift detection against the baseline
  - `tools/npp_lexer_model.json`: Lexer style inventory from Notepad++ stylers.model.xml
  - `tools/baseline.json`: Baseline for lexer count and structure regression prevention (also records the XML's SHA-256, line count and size for drift detection)
- **Continuous validation**: `.github/workflows/validate-theme.yml` runs `python3 tools/validate_theme.py` on every push and pull request, turning the static palette/contrast/coverage checks and the baseline drift gate into an automated check
- `LICENSE` (LGPL-3.0)
- `CHANGELOG.md`

### Removed
- Stale documentation references to `bluloco-dark.xml` (filename is `BlulocoDark.xml`)
- Stale documentation claims of off-palette token variants (the token palette is fully normalized against the upstream source)

## [2.0] - 2026-11-06
### Added
- Major optimization: High-fidelity match to VSCode Bluloco Dark theme
- Fixed error/bad brace/find mark colors (`FC2E51` → `FF2E3F`)
- Applied consistent Bluloco palette across all 55 lexers
- Fixed Python triple strings, CSS selectors/properties, HTML values, JSON keywords, TOML escape chars
- **Wave 3**: Rationalized USER KEYWORDS across lexers
  - Python: Added USER KEYWORDS 1–8 (styleIDs 128–135) + DECORATOR + ATTRIBUTE
  - JavaScript/TypeScript: Corrected USER KEYWORDS styleID ranges (JS: 200–207, TS: 128–135) + TS missing styles (19, 20)
  - All C-family lexers: Differentiated USER KEYWORDS 5–8 (decorator, namespace, typeParameter, macro)
  - Fixed USER KEYWORDS 3 color to `8BCDEF` (params) per model
- Added theme gallery with 7 language previews

## [1.0] - 2026-11-05
### Added
- Initial port from VSCode Bluloco Dark theme
- Basic syntax highlighting for 20+ languages
- GlobalStyles and LexerStyles implementation

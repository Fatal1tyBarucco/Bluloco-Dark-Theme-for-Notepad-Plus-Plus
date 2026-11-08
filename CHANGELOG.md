# Changelog

All notable changes to this project will be documented in this file.

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

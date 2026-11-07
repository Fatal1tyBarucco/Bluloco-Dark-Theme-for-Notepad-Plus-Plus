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

### Changed
- **Palette consistency**: Applied canonical Bluloco palette across all 55 lexers
  - Keywords: `10B1FE` | Numbers: `FF78F8` | Classes/Types: `FF6480`
  - Functions: `3FC56B` | Constants: `9F7EFE` | Parameters: `8BCDEF`
  - Properties: `CE9887` | Operators: `7A82DA` | Tags: `3691FF`
  - Attributes: `FF936A` | Errors: `FF2E3F`
- **USER KEYWORDS rationalization (Wave 3)**:
  - Python: Added USER KEYWORDS 1–8 (128–135) + DECORATOR (15) + ATTRIBUTE (20)
  - JavaScript: USER KEYWORDS 1–8 corrected to styleIDs 200–207
  - TypeScript: USER KEYWORDS 1–8 at 128–135 + WINDOW INSTRUCTION (19) + STRING RAW (20)
  - All C-family lexers: Differentiated USER KEYWORDS 5–8 (decorator, namespace, typeParameter, macro)
  - PHP, ASP, Bash, Lua: Rationalized USER KEYWORDS to match lexer capabilities
  - USER KEYWORDS 3 standardized to `8BCDEF` (parameters) per palette model

### Added
- **Static validation tooling**:
  - `tools/validate_theme.py`: XML syntax, palette adherence, hex format, WCAG contrast
  - `tools/npp_lexer_model.json`: Lexer style inventory from Notepad++ stylers.model.xml
  - `tools/baseline.json`: Baseline for lexer count and structure regression prevention
- `LICENSE` (LGPL-3.0)
- `CHANGELOG.md`

### Removed
- Stale documentation references to `bluloco-dark.xml` (filename is `BlulocoDark.xml`)

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

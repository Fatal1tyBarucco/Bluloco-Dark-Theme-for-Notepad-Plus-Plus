# Bluloco Dark for Notepad++ — Agent Instructions

## Overview
This repo is a Notepad++ theme port of VSCode Bluloco Dark. The deliverable is a single XML file, `BlulocoDark.xml`; there is no package manager, build system, or codegen. Static validation lives in `tools/validate_theme.py` (XML syntax, hex format, palette adherence, WCAG contrast); edit the XML directly and run the validator.

## Repo map
- `BlulocoDark.xml` — canonical theme. `<NotepadPlus>` → `<LexerStyles>` (55 `<LexerType>` blocks) → `<GlobalStyles>` (39 `<WidgetStyle>` entries).
- `README.md` — user documentation reflecting the audited v2.1 state. It references the real filename (`BlulocoDark.xml`) everywhere and keeps the honest limitations: no native semantic tokens, USER KEYWORDS are manual lists, comment contrast below WCAG AA, partial style-ID coverage in some lexers, and visual validation requiring Windows + Notepad++. The XML remains the source of truth.
- `PROMPT_APERFEICOAMENTO_BLULOCO_DARK.md` — audit/overhaul brief with project quality rules. Reference material, not a standing TODO.
- `screenshots/` — 7 PNG previews (`css`, `html`, `js`, `php`, `py`, `rb`, `ts`).
- `samples/` — 27 per-language code samples used for manual visual validation of the theme. 24 map to a shipped lexer; `sample.rust`, `sample.swift` and `sample.yaml` have no dedicated lexer in the theme and are reference-only. Not referenced by the validator; load them in Notepad++ to eyeball the result.
- `tools/` — static validation tooling: `validate_theme.py` (XML syntax, hex format, palette adherence, WCAG contrast), `npp_lexer_model.json` (Notepad++ v8.9.9 `stylers.model.xml` inventory), `baseline.json` (regression baseline). The script resolves paths against the repo root, so it runs from any working directory.
- `.github/workflows/summary.yml` — summarizes newly opened issues via `actions/ai-inference`. It does not build or validate the theme.

## XML editing rules
- Colors are exactly 6 uppercase hex digits, no `#` (`282C34`). Empty `fontName=""` / `fontSize=""` are normal.
- `styleID` is scoped to its `<LexerType>`; different lexers legitimately reuse numbers for different tokens (C `DEFAULT`=11, Python `DEFAULT`=0). `GlobalStyles` intentionally repeats `styleID="0"` across 23 named widgets.
- `LexerType name=` is Notepad++'s internal lexer ID (`cpp`, `cs`, `javascript`, `bash`, `typescript`, `searchResult`), not a display name or file extension.
- `keywordClass` and user-keyword IDs differ per lexer: C user keywords 128–135 / `substyle1-8`; JS/TS 200–207; HTML `USER TAGS` 192–195 and `USER ATTRIBUTES` 196–199; Lua `USER KEYWORDS 5-8` 128–131. Copy style blocks from the same lexer only.
- `USER KEYWORDS`, `USER TAGS`, and `USER ATTRIBUTES` are keyword-list styles, not semantic tokens. They only color words the user adds in Style Configurator.
- `errorlist` keeps the legacy ANSI terminal colors for its `ANSI COLOR` styles (styleIDs 40–55); treat those as known exceptions, not palette references. `searchResult` was migrated to the dark theme palette (`10B1FE`, `3FC56B`, `636D83`, `FF2E3F`/`F9C859`, `ABB2BF`/`3691FF`, `2D333D`) and is no longer an exception.

## Palette
| Role | Hex | Role | Hex |
|---|---|---|---|
| bg | `282C34` | fg | `ABB2BF` |
| comments | `636D83` | keywords | `10B1FE` |
| strings | `F9C859` | numbers | `FF78F8` |
| functions | `3FC56B` | classes/types | `FF6480` |
| errors | `FF2E3F` | constants | `9F7EFE` |
| params | `8BCDEF` | props | `CE9887` |
| operators | `7A82DA` | tags | `3691FF` |
| attrs | `FF936A` | | |

## Tasks
- **Change colors:** edit `fgColor` / `bgColor` in place; keep normal lexer backgrounds `282C34` unless there is a documented reason.
- **Add a lexer:** confirm the real internal `name` and style IDs for the target Notepad++/Scintilla version; never invent IDs. Insert the `<LexerType>` inside `<LexerStyles>`, before `<GlobalStyles>`. Update README coverage only to match what you actually implemented.
- Make focused diffs; do not reformat or reorder unrelated styles.

## Validation
Run from the repo root:
- `xmllint --noout BlulocoDark.xml` (fallback: `python3 -c 'import xml.etree.ElementTree as ET; ET.parse("BlulocoDark.xml")'`)
- `grep -oE '(fg|bg)Color="[^"]*"' BlulocoDark.xml | grep -vE '"[0-9A-F]{6}"'` — expect no output.
- `grep -c '<LexerType' BlulocoDark.xml` — baseline 55; only changes when adding/removing a lexer.
- `python3 tools/validate_theme.py` — static checks; resolves paths from the repo root, so it runs from any directory.
- Visual check requires Windows + Notepad++: copy to `%APPDATA%\Notepad++\themes\`, then Settings → Style Configurator. It cannot be done natively in this Linux environment; never claim visual verification or add screenshots without a real run.
- For visual review, load the files in `samples/` manually in Notepad++ and inspect the rendering per language. This is a manual, non-automatable step; do not describe it as machine-verified. The Rust, Swift and YAML samples have no dedicated lexer, so they cannot demonstrate theme colours.

## Constraints
- No build tooling, dependencies, installers, or generated files.
- Do not whole-file reformat or reorder; do not remove existing lexers/styles without justification.
- Do not rename the XML to match stale README text; fix the docs instead.

# Bluloco Dark for Notepad++ — Agent Instructions

## Overview
This repo is a Notepad++ theme port of VSCode Bluloco Dark. The deliverable is a single XML file, `BlulocoDark.xml`; there is no package manager, build system, or codegen. Static validation lives in `tools/validate_theme.py` (XML syntax, hex format, palette adherence, WCAG contrast); edit the XML directly and run the validator.

## Source provenance
- Upstream: [uloco/theme-bluloco-dark](https://github.com/uloco/theme-bluloco-dark) — the VSCode *Bluloco Dark* theme by uloco. The Notepad++ port derives from this project.
- Reference commit: `d604c347564d16eea5a98c5fb1fb1703816929b5`.
- Reference file: `themes/bluloco-dark-color-theme.json`. The port was audited colour by colour against that file; it is a palette reference, not a build input.
- License of the original material: **LGPL-3.0** (the upstream `LICENSE` is the GNU LGPL v3). This repository ships the same license. Never describe the upstream theme as MIT.

## Repo map
- `BlulocoDark.xml` — canonical theme. `<NotepadPlus>` → `<LexerStyles>` (**67 `<LexerType>` blocks**) → `<GlobalStyles>` (**51 `<WidgetStyle>` entries**).
- `README.md` — user documentation reflecting the audited v2.2 state. It references the real filename (`BlulocoDark.xml`) everywhere and keeps the honest limitations: no native semantic tokens, USER KEYWORDS are manual lists, comment contrast below WCAG AA, partial style-ID coverage in some lexers, visual validation requiring Windows + Notepad++. The XML remains the source of truth.
- `CHANGELOG.md` — release history; entry `[2.2] - 2026-11-08` documents the current version.
- `PROMPT_APERFEICOAMENTO_BLULOCO_DARK.md` — audit/overhaul brief with project quality rules. Reference material, not a standing TODO.
- `screenshots/` — 7 PNG previews (`css`, `html`, `js`, `php`, `py`, `rb`, `ts`). They are real Notepad++ captures, but they were taken **before** the v2.1 palette normalization, so they may show the previous palette; never present them as evidence of the current colours.
- `renders/` — 7 SVG previews (`css`, `html`, `js`, `php`, `py`, `rb`, `ts`) generated programmatically from the v2.2 `BlulocoDark.xml` (commit `588c48d`). Programmatic renders, **not** screenshots: every colour is extracted from the XML, but the token classification only approximates the Scintilla lexers. Never present them as visual verification, as captures, or as evidence of the current colours.
- `samples/` — 35 per-language code samples used for manual visual validation of the theme. All 35 map to a lexer shipped in this theme (including `sample.rust`, `sample.swift` and `sample.yaml`, which now have dedicated lexers). Not referenced by the validator; load them in Notepad++ to eyeball the result.
- `tools/` — static validation tooling: `validate_theme.py` (XML syntax, hex format, palette adherence, WCAG contrast, `GlobalStyles` colour coverage, baseline drift detection), `generate_baseline.py` (reproducible baseline regeneration), `npp_lexer_model.json` (Notepad++ v8.9.9 `stylers.model.xml` inventory), `baseline.json` (regression baseline: `sha256`/`line_count`/`size_bytes` of the XML plus lexer/style counts). The scripts resolve paths against the repo root, so they run from any working directory.
- `.github/workflows/summary.yml` — summarizes newly opened issues via `actions/ai-inference`. It does not build or validate the theme.

## XML editing rules
- Colors are exactly 6 uppercase hex digits, no `#` (`282C34`). Empty `fontName=""` / `fontSize=""` are normal.
- `styleID` is scoped to its `<LexerType>`; different lexers legitimately reuse numbers for different tokens (C `DEFAULT`=11, Python `DEFAULT`=0). `GlobalStyles` intentionally repeats `styleID="0"` across widgets.
- `LexerType name=` is Notepad++'s internal lexer ID (`cpp`, `cs`, `javascript`, `bash`, `typescript`, `searchResult`), not a display name or file extension.
- `keywordClass` and user-keyword IDs differ per lexer: C user keywords 128–135 / `substyle1-8`; JS/TS 200–207; HTML `USER TAGS` 192–195 and `USER ATTRIBUTES` 196–199; Lua `USER KEYWORDS 5-8` 128–131. Copy style blocks from the same lexer only.
- `USER KEYWORDS`, `USER TAGS`, and `USER ATTRIBUTES` are keyword-list styles, not semantic tokens. They only color words the user adds in Style Configurator.
- `errorlist` keeps the legacy ANSI terminal colors for its `ANSI COLOR` styles (styleIDs 40–55); treat those as known exceptions, not palette references. `searchResult` was migrated to the dark theme palette (`10B1FE`, `3FC56B`, `636D83`, `FF2E3F`/`F9C859`, `ABB2BF`/`3691FF`, `2D333D`) and is no longer an exception.
- Canonical palette roles: bg `282C34`, fg `ABB2BF`, comments `636D83`, keywords `10B1FE`, strings `F9C859`, numbers `FF78F8`, functions `3FC56B`, classes `FF6480`, errors `FF2E3F`, constants `9F7EFE`, params `8BCDEF`, props `CE9887`, operators `7A82DA`, tags `3691FF`, attrs `FF936A`, decorator `50ACAE`, namespace `FF839B`.
- Documented exceptions: doc comment grey `7C8495`; errorlist ANSI ramp (40–55); UI chrome (`2D333D`, `22252A`, `3D434F`, `FFCC00`, `177849`, `0084FF`, `25272D`, `DADADA`, `FFFFFF`); GlobalStyles tints (`1C4670`, `1C6143`, `36465A`, `215471`, `684B44`, `675B3F`, `4C4571`, `2F5A45`, `3A3F58`, `735047`).
- `fontStyle` is `0` for code tokens except `searchResult` (1/2) and Brace highlight.
- Make focused diffs; do not reformat or reorder unrelated styles; do not remove existing lexers/styles without justification.

### Adding a lexer (without inventing IDs)
1. Confirm the real internal `name`, `desc`, `ext` and style IDs for the target Notepad++/Scintilla version against `tools/npp_lexer_model.json` (v8.9.9 `stylers.model.xml`).
2. Never invent a `styleID`.
3. Insert the `<LexerType>` inside `<LexerStyles>`, before `</LexerStyles>` (i.e., before `<GlobalStyles>`).
4. Update README coverage only to match what you actually implemented.
5. Run the validator afterwards.

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
| attrs | `FF936A` | decorator | `50ACAE` |
| | | namespace | `FF839B` |

## Palette exceptions
The canonical palette above is applied to every token style. The only colours outside it are legitimate exceptions, grouped by provenance:
- **Terminal ANSI ramp** — the `errorlist` lexer's `ANSI COLOR` styles (styleIDs 40–55) reproduce a real terminal's 16-colour ramp and are carried verbatim from the upstream `terminal.ansi*` tokens.
- **Notepad++ UI chrome** — `GlobalStyles` widget colours dictated by Notepad++'s own widget model, with no VSCode counterpart: `2D333D`, `22252A`, `3D434F`, `FFCC00`, `177849`, `0084FF`, `25272D`, `DADADA`, `FFFFFF`.
- **Documentation comment grey** — `7C8495`, used by `COMMENT DOC KEYWORD`.
- **GlobalStyles tints** — selection/search/mark/tab tints (`1C4670`, `1C6143`, `36465A`, `215471`, `684B44`, `675B3F`, `4C4571`, `2F5A45`, `3A3F58`, `735047`).
- **Deliberate divergence** — `errorlist` `ANSI COLOR RED` is `FF2E3F`, while the upstream source uses `terminal.ansiRed` = `#fc2f52`. `FF2E3F` is kept on purpose, for internal consistency with the canonical error colour. Documented, not a bug.

## Validation
Run from the repo root:
- `xmllint --noout BlulocoDark.xml` (fallback: `python3 -c 'import xml.etree.ElementTree as ET; ET.parse("BlulocoDark.xml")'`)
- `grep -oE '(fg|bg)Color="[^"]*"' BlulocoDark.xml | grep -vE '"[0-9A-F]{6}"'` — expect no output.
- `grep -c '<LexerType' BlulocoDark.xml` — baseline 67 (v2.2); only changes when adding/removing a lexer.
- `python3 tools/validate_theme.py` — static checks; it also validates the `GlobalStyles` widget colours against `PALETTE | UI_EXCEPTIONS` and detects SHA-256 drift of the XML against `tools/baseline.json`; resolves paths from the repo root, so it runs from any directory.
- `python3 tools/generate_baseline.py` — regenerates `tools/baseline.json` reproducibly.
- Visual check requires Windows + Notepad++: copy to `%APPDATA%\Notepad++\themes\`, then Settings → Style Configurator. It cannot be done natively in this Linux environment; never claim visual verification or add screenshots without a real run.
- For visual review, load the files in `samples/` manually in Notepad++ and inspect the rendering per language. This is a manual, non-automatable step; do not describe it as machine-verified.

## Constraints
- No build tooling, dependencies, installers, or generated files.
- Do not whole-file reformat or reorder; do not remove existing lexers/styles without justification.
- Do not rename the XML to match stale README text; fix the docs instead.
- Do not touch `BlulocoDark.xml`, `tools/`, or `screenshots/` unless the assigned task explicitly requires it.
- Never commit changes.

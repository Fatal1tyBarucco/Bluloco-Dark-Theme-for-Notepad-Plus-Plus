# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: Developers using Notepad++ on Windows who want the Bluloco Dark color scheme from VSCode in their editor. They work in Windows environments, often on legacy or lightweight projects where Notepad++ is the preferred editor, and they want a familiar, carefully crafted dark theme without switching editors.

## Product Purpose

A faithful, audited port of the VSCode Bluloco Dark theme to Notepad++. It makes the Bluloco color scheme available in Notepad++ with high fidelity across 67 lexers, backed by static validation tooling that enforces palette adherence, hex format, WCAG contrast checks, and regression baselines. Success means a developer can install the single XML file and get a Bluloco Dark experience that is color-accurate to the upstream source, with honest documentation of every known limitation.

## Positioning

Not just a color copy — it is a color-by-color audited port with full palette normalization against the upstream `bluloco-dark-color-theme.json`, a USER KEYWORDS 1–8 scheme traceable to upstream `semanticTokenColors`, validation tooling that catches drift, and explicit documentation of every exception (ANSI terminal ramp, Notepad++ UI chrome, documentation-comment grey, deliberate error-color divergence). Neighboring ports typically lack the audit trail, the validation gate, or the honesty about coverage gaps.

## Operating Context

- Distribution: GitHub repository, manual download of `BlulocoDark.xml`
- Installation: Copy to `%APPDATA%\Notepad++\themes\` or import via Style Configurator
- Validation: Run `python3 tools/validate_theme.py` from repo root (XML syntax, palette adherence, hex format, WCAG contrast, GlobalStyles widget coverage, SHA-256 drift detection against `tools/baseline.json`)
- Visual verification: Requires Windows + Notepad++; load `samples/` files and inspect rendering per language
- No build system, package manager, or generated files — the XML is the source of truth

## Capabilities and Constraints

- **Deliverable**: Single `BlulocoDark.xml` file (Notepad++ theme format)
- **Lexer coverage**: 67 of Notepad++ v8.9.9's 93 model lexers have dedicated style blocks; 26 fall back to Default Style
- **Palette**: Canonical 14-role palette applied without deviation to all token styles; only exceptions are `errorlist` ANSI ramp (styleIDs 40–55), Notepad++ UI chrome in `GlobalStyles`, documentation-comment grey `7C8495`, and GlobalStyles selection/search/mark/tab tints
- **USER KEYWORDS 1–8**: Manual keyword-list styles (not semantic tokens) mapped to upstream semantic roles across 9 lexer families
- **Validation tooling**: `tools/validate_theme.py` (static checks), `tools/generate_baseline.py` (reproducible baseline), `tools/npp_lexer_model.json` (v8.9.9 stylers.model.xml inventory), `tools/baseline.json` (regression baseline)
- **License**: LGPL-3.0 (inherited from upstream uloco/theme-bluloco-dark)
- **No build step, no dependencies, no installers** — edit XML directly and run validator

## Brand Commitments

- **Name**: Bluloco Dark Theme for Notepad++
- **Upstream**: uloco's Bluloco Dark VSCode theme (reference commit `d604c347564d16eea5a98c5fb1fb1703816929b5`, file `themes/bluloco-dark-color-theme.json`)
- **License**: LGPL-3.0 (same as upstream)
- **Voice**: Technical, precise, honest about limitations — no marketing fluff, no hidden gaps

## Evidence on Hand

- `BlulocoDark.xml` — canonical theme (67 `<LexerType>` blocks, 51 `<WidgetStyle>` entries)
- `README.md` — user documentation reflecting audited v2.2 state with honest limitations
- `CHANGELOG.md` — release history from v1.0 through v2.2
- `tools/validate_theme.py` — static validation (palette, hex, contrast, coverage, drift)
- `tools/generate_baseline.py` — reproducible baseline regeneration
- `tools/npp_lexer_model.json` — Notepad++ v8.9.9 `stylers.model.xml` inventory
- `tools/baseline.json` — regression baseline (SHA-256, counts, coverage)
- `samples/` — 35 per-language code samples for manual visual validation
- `screenshots/` — 7 PNG previews (captured pre-v2.1 normalization, illustrative only)
- `renders/` — 7 SVG programmatic renders from v2.2 XML (not screenshots, not visual verification)
- `.github/workflows/validate-theme.yml` — CI validation on push/PR

## Product Principles

1. **Fidelity over completeness** — Better to have 67 lexers audited and palette-perfect than 93 with drift
2. **Validation over assumption** — Every color change must pass the validator; drift is caught, not discovered
3. **Honesty over polish** — Document every limitation, exception, and gap explicitly; never present renders as screenshots
4. **No build complexity** — The XML is the source of truth; tooling validates, never generates
5. **Upstream traceability** — Every palette role and USER KEYWORDS slot maps to a documented upstream source

## Accessibility & Inclusion

- Comment color (`636D83` on `282C34`) falls below WCAG AA (2.7:1) — this matches the original VSCode theme and is a documented trade-off
- No product-specific accessibility requirements beyond the upstream's choices
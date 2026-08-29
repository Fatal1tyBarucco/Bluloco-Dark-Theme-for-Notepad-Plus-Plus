# Bluloco Dark Theme for Notepad++ - Agent Instructions

## Project Overview
This is a **Notepad++ theme** (XML file) ported from the VSCode Bluloco Dark theme. No build, test, or lint tooling exists.

## Key Files
- `BlulocoDark.xml` - Main theme file (Notepad++ XML format)
- `README.md` - Complete documentation with color mappings and installation
- `screenshots/` - Preview images for various languages
- `.github/workflows/summary.yml` - AI issue summarization workflow

## Color Format
- Notepad++ uses **6-character hex without `#` prefix** (e.g., `282C34` not `#282C34`)
- Background: `282C34`, Foreground: `ABB2BF`, Comments: `636D83`

## Common Tasks

### Modify Theme Colors
Edit `BlulocoDark.xml` directly. Colors are in `fgColor`/`bgColor` attributes as 6-char hex.

### Test Theme
1. Copy `BlulocoDark.xml` to Notepad++ themes folder:
   - Windows: `%APPDATA%\Notepad++\themes\`
2. Open Notepad++ → Settings → Style Configurator → Select "bluloco-dark"

### Add Language Support
Add new `<LexerType>` blocks in `BlulocoDark.xml` under `<LexerStyles>`. Follow existing patterns for style IDs.

## GitHub Workflow
- `summary.yml` runs on new issues, uses `actions/ai-inference` to summarize, posts comment via `gh`

## No Commands Needed
No package.json, no build scripts, no tests. Direct XML editing only.
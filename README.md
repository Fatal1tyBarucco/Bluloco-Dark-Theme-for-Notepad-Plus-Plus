# Bluloco Dark Theme for Notepad++

A complete port of the Bluloco Dark Visual Studio Code theme to Notepad++. This theme brings the beautiful, carefully crafted Bluloco color scheme to Notepad++ with full syntax highlighting support.

![Bluloco Dark Theme Preview](https://github.com/barucco-renato/Bluloco-Dark-Theme-for-Notepad-Plus-Plus/blob/main/screenshots/js.png)

## 🎨 About Bluloco

Bluloco is a sophisticated color scheme that combines blue-based accents with a carefully balanced palette that's easy on the eyes during long coding sessions. The dark variant provides excellent contrast while maintaining readability.

## ⚡ Recent Improvements (v2.1)

This version includes a **comprehensive audit and refinement** to achieve high-fidelity matching with the original VSCode Bluloco Dark theme:

### 🎯 Color Accuracy Fixes
| Element | Before | After | VSCode Reference |
|---------|--------|-------|------------------|
| **Error Color** | `FC2E51` | `FF2E3F` | `#ff2e3f` ✅ |
| **Bad Brace** | `FC2E51` | `FF2E3F` | `#ff2e3f` ✅ |
| **Find Mark** | `FC2E51` | `FF2E3F` | `#ff2e3f` ✅ |
| **Python Triple Strings** | Comment color | `F9C859` (String yellow) | ✅ |
| **CSS Class/Selector** | Various | `3691FF` (Blue) | ✅ |
| **CSS Property Names** | Various | `FF936A` (Orange) | ✅ |
| **HTML Attribute Values** | Pink | `F9C859` (String yellow) | ✅ |
| **JSON true/false/null** | Green | `10B1FE` (Keyword blue) | ✅ |
| **TOML Escape Char** | Green | `FF936A` (Orange) | ✅ |

### 🎨 Palette Refinements
Applied consistent Bluloco color palette across all 55 supported lexers:

| Role | Hex | Role | Hex |
|------|-----|------|-----|
| Background | `282C34` | Foreground | `ABB2BF` |
| Comments | `636D83` | Keywords | `10B1FE` |
| Strings | `F9C859` | Numbers | `FF78F8` |
| Functions | `3FC56B` | Classes/Types | `FF6480` |
| Errors | `FF2E3F` | Constants | `9F7EFE` |
| Parameters | `8BCDEF` | Properties | `CE9887` |
| Operators | `7A82DA` | Tags | `3691FF` |
| Attributes | `FF936A` | | |

### 🔧 USER KEYWORDS Rationalization (Wave 3)
- **Python**: Added USER KEYWORDS 1–8 (styleIDs 128–135) + DECORATOR (15) + ATTRIBUTE (20)
- **JavaScript/TypeScript**: Corrected USER KEYWORDS styleID ranges (JS: 200–207, TS: 128–135) + TS missing styles WINDOW INSTRUCTION (19) + STRING RAW (20)
- **All C-family lexers** (C, C++, C#, Java, Go, RC, ActionScript): Differentiated USER KEYWORDS 5–8 (decorator, namespace, typeParameter, macro) instead of duplicating slot 4
- **USER KEYWORDS 3** color standardized to `8BCDEF` (parameters) per palette model
- **PHP, ASP, Bash, Lua**: Rationalized USER KEYWORDS slots to match lexer capabilities

### ✅ Static Validation Ecosystem
- Added `tools/validate_theme.py`: static analysis for XML syntax, color palette adherence, hex format, and WCAG contrast
- Added `tools/npp_lexer_model.json`: Lexer style inventory from Notepad++ stylers.model.xml
- Added `tools/baseline.json`: Baseline for lexer count and theme structure to prevent regressions
- All 55 lexers validated against palette and structure baselines

## 📋 Conversion Process

### Step 1: Analysis of Source Themes

#### VSCode Theme Structure Analysis
The original Bluloco Dark theme uses a JSON structure with:
- `colors`: Global UI colors (background, foreground, panels, etc.)
- `tokenColors`: Syntax token colors for different programming constructs
- `semanticTokenColors`: Additional semantic highlighting

#### Notepad++ Theme Structure Analysis
Notepad++ uses XML configuration with:
- `GlobalStyles`: Editor-wide settings (background, caret, selection, etc.)
- `LexerStyles`: Language-specific syntax highlighting rules
- Color format: RGB hex values without `#` prefix

### Step 2: Color Mapping Strategy

#### Core Color Palette Mapping
| VSCode Color | Notepad++ Color | Usage |
|--------------|-----------------|-------|
| `#282c34` | `282C34` | Main background |
| `#abb2bf` | `ABB2BF` | Default text |
| `#636d83` | `636D83` | Comments |
| `#10b1fe` | `10B1FE` | Keywords, storage types |
| `#3fc56b` | `3FC56B` | Functions, methods |
| `#ff6480` | `FF6480` | Classes, types |
| `#f9c859` | `F9C859` | Strings, regex |
| `#ff78f8` | `FF78F8` | Numbers |
| `#ff2e3f` | `FF2E3F` | **Errors, bad braces, find marks** |
| `#9f7efe` | `9F7EFE` | **Constants** |
| `#8bcdef` | `8BCDEF` | **Parameters** |
| `#ce9887` | `CE9887` | **Object properties, variables** |
| `#7a82da` | `7A82DA` | Operators, punctuation |
| `#3691ff` | `3691FF` | Tags, HTML elements |
| `#ff936a` | `FF936A` | Attributes, parameters, escape chars |

#### UI Element Mapping
- **Editor Background**: `#282c34` → `282C34`
- **Current Line**: `#2d333d` → `2D333D`
- **Selection**: `#0084ff4b` → `0084FF` (simplified)
- **Line Numbers**: `#636d83` on `#22252a` background
- **Caret Color**: `#ffcc00` → `FFCC00`

### Step 3: Syntax Token Conversion

#### Language-Specific Mappings

**C/C++/Java Family:**
- Preprocessor: `#10b1fe` (blue)
- Instructions: `#10b1fe` (blue)
- Types: `#ff6480` (red-pink)
- Strings: `#f9c859` (yellow)
- Numbers: `#ff78f8` (pink)

**Python:**
- Keywords: `#10b1fe` (blue)
- Function definitions: `#3fc56b` (green)
- Class names: `#ff6480` (red-pink)
- Triple quotes: `#636d83` (comments color)

**JavaScript:**
- Keywords: `#10b1fe` (blue)
- Strings: `#f9c859` (yellow)
- Regex: `#f9c859` (yellow)

**HTML/XML:**
- Tags: `#3691ff` (bright blue)
- Attributes: `#ff936a` (orange)
- Values: `#ff78f8` (pink)

**CSS:**
- Selectors: `#3691ff` (blue)
- Properties: `#ce9887` (brown)
- Values: `#ff78f8` (pink)
- Classes/IDs: `#3fc56b` (green)

### Step 4: XML Structure Implementation

#### Global Styles Section
```xml
<GlobalStyles>
    <WidgetStyle name="Default Style" styleID="32" fgColor="ABB2BF" bgColor="282C34"/>
    <WidgetStyle name="Current line background colour" styleID="0" bgColor="2D333D"/>
    <WidgetStyle name="Selected text colour" styleID="0" bgColor="0084FF" fgColor="FFFFFF"/>
    <!-- ... more global styles -->
</GlobalStyles>
```

#### Lexer Styles Section
```xml
<LexerStyles>
    <LexerType name="python" desc="Python" ext="">
        <WordsStyle name="DEFAULT" styleID="0" fgColor="ABB2BF" bgColor="282C34"/>
        <WordsStyle name="COMMENTLINE" styleID="1" fgColor="636D83" bgColor="282C34"/>
        <WordsStyle name="STRING" styleID="3" fgColor="F9C859" bgColor="282C34"/>
        <!-- ... more Python styles -->
    </LexerType>
    <!-- ... more languages -->
</LexerStyles>
```

## 🛠 Installation

### Method 1: Manual Installation

1. **Download the theme file:**
   - Save `BlulocoDark.xml` to your Notepad++ themes directory

2. **Locate Notepad++ themes folder:**
   - Windows: `C:\Users\[YourUsername]\AppData\Roaming\Notepad++\themes\`
   - Or via Notepad++: `Settings` → `Style Configurator` → `Theme` (shows folder location)

3. **Apply the theme:**
   - Open Notepad++
   - Go to `Settings` → `Style Configurator`
   - Select "BlulocoDark" from the theme dropdown
   - Click "Save & Close"

### Method 2: Import via Style Configurator

1. Open Notepad++
2. Go to `Settings` → `Style Configurator`
3. Click the "Import" button
4. Navigate to and select the `BlulocoDark.xml` file
5. The theme will be automatically installed and selected

## 🖼️ Theme Gallery

| Language | Preview |
|----------|---------|
| **JavaScript** | ![JavaScript](screenshots/js.png) |
| **TypeScript** | ![TypeScript](screenshots/ts.png) |
| **Python** | ![Python](screenshots/py.png) |
| **HTML** | ![HTML](screenshots/html.png) |
| **CSS** | ![CSS](screenshots/css.png) |
| **PHP** | ![PHP](screenshots/php.png) |
| **Ruby** | ![Ruby](screenshots/rb.png) |

*Click images to view full-size previews*

## 📁 File Structure

```
Bluloco-Dark-Theme-for-Notepad-Plus-Plus/
├── BlulocoDark.xml          # Main theme file
├── README.md                 # This file
└── screenshots/              # Theme preview images
    ├── css.png
    ├── html.png
    ├── js.png
    ├── php.png
    ├── py.png
    ├── rb.png
    └── ts.png
    
```

## 🎯 Supported Languages

The theme includes syntax highlighting for **55 lexers** covering many popular languages:

### Languages with USER KEYWORDS 1–8 Support
- **C/C++/Objective-C/C#/Java/Go/RC/ActionScript** — USER KEYWORDS 1–8 (styleIDs 128–135) with differentiated slots 5–8
- **Python** — USER KEYWORDS 1–8 (styleIDs 128–135) + DECORATOR (15) + ATTRIBUTE (20)
- **JavaScript** — USER KEYWORDS 1–8 (styleIDs 200–207)
- **TypeScript** — USER KEYWORDS 1–8 (styleIDs 128–135) + WINDOW INSTRUCTION (19) + STRING RAW (20)
- **PHP** — USER KEYWORDS 1–5 (styleIDs 208–212)
- **ASP** — USER KEYWORDS 1–8 (styleIDs 216–223)
- **Bash** — USER KEYWORDS 1–4 + USER SCALAR 1–4 (styleIDs 128–135)
- **Lua** — USER KEYWORD 1–4 + USER KEYWORDS 5–8 (styleIDs 16–19, 128–131)

### Standard Syntax Highlighting
- **HTML/XML** — Tags, attributes, values, entities, USER TAGS/ATTRIBUTES
- **CSS** — Selectors, properties, values, classes, IDs, variables
- **SQL** — Keywords, functions, strings
- **JSON** — Keys, strings, numbers, booleans, null
- **TOML** — Keys, strings, numbers, dates, tables, escape chars
- **Batch files** — Commands, variables
- **INI/Properties** — Sections, keys, values
- **Ruby** — Keywords, strings, symbols
- **Perl, Lua, Raku, Tcl, Pascal, SQL, VB/VBS, Makefile, Diff, PowerShell, CMake, Haskell, and more...**

### 🧪 Manual Validation Samples

The `samples/` directory ships **27 code samples**, one per covered lexer subset, to support **manual visual validation** of the theme in Notepad++. Each sample deliberately exercises the token types that matter for that lexer (strings, numbers, comments, keywords, operators, preprocessor directives, user-keyword slots, and so on), so you can open it and confirm the colors at a glance.

Open a file from `samples/` in Notepad++ with the Bluloco Dark theme applied to inspect the result. This check is **not automatable** — it requires a real Notepad++ installation on Windows.

Available samples:

| Language | File | Language | File |
|---|---|---|---|
| Batch | `sample.bat` | PHP | `sample.php` |
| C | `sample.c` | Perl | `sample.pl` |
| CMake | `sample.cmake` | PowerShell | `sample.ps1` |
| C++ | `sample.cpp` | Python | `sample.py` |
| C# | `sample.cs` | Ruby | `sample.rb` |
| CSS | `sample.css` | Rust | `sample.rust` |
| Diff | `sample.diff` | Bash | `sample.sh` |
| Go | `sample.go` | SQL | `sample.sql` |
| HTML | `sample.html` | Swift | `sample.swift` |
| INI | `sample.ini` | TOML | `sample.toml` |
| Java | `sample.java` | TypeScript | `sample.ts` |
| JavaScript | `sample.js` | YAML | `sample.yaml` |
| JSON | `sample.json` | Lua | `sample.lua` |
| Makefile | `sample.makefile` | | |

## ⚠️ Known Limitations

- **Not pixel-perfect**: Notepad++'s lexer model differs from VSCode's TextMate grammars; some semantic tokens (e.g., function vs method, parameter vs variable) cannot be distinguished without language server integration.
- **No true semantic token support**: USER KEYWORDS are manual keyword lists configured in Style Configurator, not automatic semantic highlighting.
- **Lexer coverage varies**: Some lexers (HTML, XML, PHP, PowerShell) miss style IDs present in Notepad++'s stylers.model.xml.
- **Contrast trade-offs**: Comment color (`636D83` on `282C34`) falls below WCAG AA (2.7:1); this matches the original VSCode theme.
- **searchResult/errorlist**: Use hardcoded ANSI/legacy colors not aligned with the Bluloco palette.
- **20+ languages claim**: The theme ships 55 lexers, but "enhanced semantic highlighting" only applies to USER KEYWORDS slots where the lexer model permits.

## 🔧 Customization

### Font Recommendations
For the best experience, use these fonts with Bluloco Dark:

- **Consolas** (Windows)
- **Fira Code** (with ligatures)
- **JetBrains Mono**
- **Cascadia Code**

### Adjusting Colors
To modify colors:

1. Open `BlulocoDark.xml` in a text editor
2. Locate the color values (6-character hex codes without `#`)
3. Replace with your preferred colors
4. Save and re-import the theme

### Example: Changing Background Color
```xml
<!-- Change from: -->
<WidgetStyle name="Default Style" styleID="32" fgColor="ABB2BF" bgColor="282C34"/>

<!-- To: -->
<WidgetStyle name="Default Style" styleID="32" fgColor="ABB2BF" bgColor="1E1E1E"/>
```

## 🐛 Troubleshooting

### Theme Not Appearing
- Ensure the XML file is in the correct themes folder
- Check file permissions
- Restart Notepad++ after adding the theme

### Colors Not Applying Correctly
- Verify the XML file is well-formed
- Check for duplicate style definitions
- Ensure color values are 6-character hex without `#`

### Specific Language Not Highlighting
- The theme might not include that specific lexer
- Check if the language is enabled in Notepad++
- Consider adding the lexer style manually

## 📝 Changelog

### v2.0 (Latest)
- **Major optimization**: High-fidelity match to VSCode Bluloco Dark theme
- Fixed error/bad brace/find mark colors (`FC2E51` → `FF2E3F`)
- Applied consistent Bluloco palette across all 55 lexers
- Fixed Python triple strings, CSS selectors/properties, HTML values, JSON keywords, TOML escape chars
- **Wave 3**: Rationalized USER KEYWORDS across lexers
  - Python: Added USER KEYWORDS 1–8 (styleIDs 128–135) + DECORATOR + ATTRIBUTE
  - JavaScript/TypeScript: Corrected USER KEYWORDS styleID ranges (JS: 200–207, TS: 128–135) + TS missing styles (19, 20)
  - All C-family lexers: Differentiated USER KEYWORDS 5–8 (decorator, namespace, typeParameter, macro)
  - Fixed USER KEYWORDS 3 color to `8BCDEF` (params) per model
- Added theme gallery with 7 language previews

### v1.0
- Initial port from VSCode Bluloco Dark theme
- Basic syntax highlighting for 20+ languages
- GlobalStyles and LexerStyles implementation

## 🤝 Contributing

### [Buy me a coffee!](https://mepagaumcafe.com.br/barucco-renato/)

Contributions to improve the theme are welcome!

### Areas for Improvement
- Add support for more programming languages
- Improve specific language token mappings
- Create light variant of the theme
- Add Rust, Swift, Kotlin, Dart language support

### Reporting Issues
When reporting issues, please include:
1. Notepad++ version
2. Operating system
3. Specific language/file type having issues
4. Screenshot of the problem

## 📄 License

This theme is based on the [Bluloco Dark theme](https://github.com/uloco/theme-bluloco-dark) by uloco, converted for Notepad++.

Original Bluloco theme is licensed under MIT License.

## 🙏 Acknowledgments

- **uloco** for creating the original Bluloco theme
- **Notepad++ team** for the excellent editor
- **Community contributors** for testing and feedback

## 📞 Support

If you encounter any issues or have questions:

1. Check this README first
2. Open an issue on GitHub
3. Contact the maintainers

---

**Enjoy coding with Bluloco Dark in Notepad++!** 🎉

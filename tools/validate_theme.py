import xml.etree.ElementTree as ET
import json
import re
import sys
import os

# Repository root: parent directory of this script's directory (tools/).
# Resolving against __file__ keeps the script runnable from any working directory.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Palette Definition
PALETTE = {
    "bg": "282C34",
    "fg": "ABB2BF",
    "comments": "636D83",
    "keywords": "10B1FE",
    "strings": "F9C859",
    "numbers": "FF78F8",
    "functions": "3FC56B",
    "classes": "FF6480",
    "errors": "FF2E3F",
    "constants": "9F7EFE",
    "params": "8BCDEF",
    "props": "CE9887",
    "operators": "7A82DA",
    "tags": "3691FF",
    "attrs": "FF936A",
}

# UI Exceptions (Colors allowed but not in the main palette)
#
# These are NOT palette drifts: every entry is either a color carried over
# verbatim from the upstream VSCode Bluloco Dark source (uloco/theme-bluloco-dark,
# commit d604c347564d16eea5a98c5fb1fb1703816929b5) or a color dictated by the
# Notepad++ widget model that has no VSCode equivalent. They are grouped below
# by provenance so that a future palette change can audit them independently.
UI_EXCEPTIONS = {
    # --- Terminal ANSI palette (VSCode source: terminal.ansi* tokens) ---
    # Used by the errorlist lexer's "ANSI COLOR *" styles (styleIDs 40-55),
    # which intentionally reproduce a real terminal's 16-color ramp.
    "42444D",  # terminal.ansiBlack
    "25A45C",  # terminal.ansiGreen
    "3375FE",  # terminal.ansiBlue
    "4483AA",  # terminal.ansiCyan
    "CDD3E0",  # terminal.ansiWhite
    "8F9AAE",  # terminal.ansiBrightBlack
    "5FB9BC",  # terminal.ansiBrightCyan
    "FFFFFF",  # terminal.ansiBrightWhite

    # --- Notepad++ UI chrome (GlobalStyles widget model) ---
    # Widget colors that exist only because Notepad++ draws its own chrome;
    # they have no semantic counterpart in the VSCode theme.
    "FFCC00",  # Caret / multi-edit carets
    "177849",  # Smart Highlighting background
    "2D333D",  # Current line background (also searchResult highlight)
    "22252A",  # Margin backgrounds (line number, bookmark, change history)
    "3D434F",  # Indent guideline, edge, fold margin, non-printing characters
    "DADADA",  # EOL custom color
    "0084FF",  # Selected text background
    "25272D",  # Inactive tabs background

    # --- Documentation comment color ---
    # "COMMENT DOC KEYWORD" styles (e.g. Python/TypeScript docstring tags)
    # use a muted gray distinct from regular comments (636D83).
    "7C8495",
}

def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_luminance(color):
    rgb = [int(x) / 255.0 for x in hex_to_rgb(color)]
    processed = []
    for c in rgb:
        if c <= 0.03928:
            processed.append(c / 12.92)
        else:
            processed.append(((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * processed[0] + 0.7152 * processed[1] + 0.0722 * processed[2]

def get_contrast(fg, bg):
    l1 = get_luminance(fg)
    l2 = get_luminance(bg)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

def validate_theme(theme_path, model_path, baseline_path):
    errors = []
    warnings = []
    
    # 1. Syntax Validation
    try:
        tree = ET.parse(theme_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"CRITICAL: XML Syntax Error: {e}")
        sys.exit(1)

    # Load Model and Baseline
    with open(model_path, 'r') as f:
        model = json.load(f)
    with open(baseline_path, 'r') as f:
        baseline = json.load(f)

    # Palette check
    palette_set = set(PALETTE.values()) | UI_EXCEPTIONS
    
    # Analyze Lexers
    theme_lexers = root.findall(".//LexerType")
    theme_lexer_names = [l.get("name") for l in theme_lexers]
    
    # Lexer Baseline Comparison
    baseline_count = baseline["theme"]["lexer_type_count"]
    current_count = len(theme_lexer_names)
    if current_count != baseline_count:
        errors.append(f"Lexer count mismatch: baseline {baseline_count}, current {current_count}")

    # Global Styles analysis
    global_styles = root.findall(".//WidgetStyle")
    
    # Detailed Token Audit
    for lexer in theme_lexers:
        name = lexer.get("name")
        styles = lexer.findall("WordsStyle")
        
        # Coverage
        if name in model:
            model_styles = model[name]
            model_ids = {s[0] for s in model_styles}
            theme_ids = {s.get("styleID") for s in styles}
            
            missing = model_ids - theme_ids
            coverage = (len(theme_ids & model_ids) / len(model_ids)) * 100 if model_ids else 100
            
            if coverage < 100:
                warnings.append(f"Lexer '{name}' coverage: {coverage:.1f}% (Missing IDs: {list(missing)})")
        
        for style in styles:
            fg = style.get("fgColor")
            bg = style.get("bgColor")
            
            # Hex Format (6 Uppercase)
            if fg and not re.match(r"^[0-9A-F]{6}$", fg):
                errors.append(f"Invalid fgColor format in {name}: {fg}")
            if bg and not re.match(r"^[0-9A-F]{6}$", bg):
                errors.append(f"Invalid bgColor format in {name}: {bg}")
                
            # Palette Membership
            if fg and fg not in palette_set:
                warnings.append(f"Color {fg} in {name} not in palette")
            if bg and bg not in palette_set:
                warnings.append(f"Color {bg} in {name} not in palette")

            # Contrast Check
            if fg and bg:
                contrast = get_contrast(fg, bg)
                if contrast < 4.5:
                    warnings.append(f"Low contrast ({contrast:.2f}) in {name} style {style.get('styleID')} (fg:{fg}, bg:{bg})")

    # Summary
    print(f"--- Theme Validation Report ---")
    print(f"Lexers found: {current_count} (Baseline: {baseline_count})")
    print(f"Errors: {len(errors)}")
    for e in errors: print(f"  [ERROR] {e}")
    print(f"Warnings: {len(warnings)}")
    for w in warnings: print(f"  [WARN] {w}")
    
    if errors:
        sys.exit(1)
    else:
        print("Validation successful!")

if __name__ == "__main__":
    validate_theme(
        os.path.join(REPO_ROOT, "BlulocoDark.xml"),
        os.path.join(REPO_ROOT, "tools", "npp_lexer_model.json"),
        os.path.join(REPO_ROOT, "tools", "baseline.json"),
    )

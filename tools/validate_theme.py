import xml.etree.ElementTree as ET
import json
import re
import sys
import os

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
UI_EXCEPTIONS = {
    "BBBBFF", "FFFFFF", "FFFFBF", "7C8495", "000000"
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
    validate_theme("BlulocoDark.xml", "tools/npp_lexer_model.json", "tools/baseline.json")

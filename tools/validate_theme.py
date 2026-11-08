import xml.etree.ElementTree as ET
import json
import re
import sys
import os
import hashlib

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
    # The theme file is read once as raw bytes: the same byte string is used for
    # the XML parse and for the SHA-256 drift check below, so the digest matches
    # `sha256sum BlulocoDark.xml` exactly (no newline/text normalisation).
    try:
        with open(theme_path, "rb") as f:
            theme_bytes = f.read()
        root = ET.fromstring(theme_bytes)
    except ET.ParseError as e:
        print(f"CRITICAL: XML Syntax Error: {e}")
        sys.exit(1)

    theme_sha256 = hashlib.sha256(theme_bytes).hexdigest()

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

    # Baseline SHA-256 Drift Detection
    # The baseline pins the exact bytes of the audited theme. A mismatch means the
    # XML changed without a baseline refresh, so the regression gate is stale.
    baseline_sha256 = baseline["theme"].get("sha256")
    if baseline_sha256 and baseline_sha256 != theme_sha256:
        warnings.append(
            "Theme SHA-256 differs from baseline (XML changed without a baseline refresh): "
            f"baseline={baseline_sha256}, current={theme_sha256}"
        )

    # Global Styles analysis
    global_styles = root.findall(".//WidgetStyle")

    # Baseline Structural Count Drift Detection
    # The baseline also pins the number of <WordsStyle> and <WidgetStyle>
    # elements. A drift means the theme's structure changed without a baseline
    # refresh, which the SHA-256 check above already flags; reporting the counts
    # makes the drift actionable (it says *how many* styles moved) instead of
    # leaving the reader to diff the hashes by hand.
    #
    # These are warnings, not errors: a theme may legitimately gain or lose
    # styles in a change that has not been baselined yet, and the SHA-256
    # warning above is the authoritative "stale baseline" signal. The
    # lexer_type_count comparison stays an error because a lexer count change
    # is a structural contract violation, not an audit refresh.
    #
    # line_count and size_bytes are deliberately NOT checked here: they are
    # fully redundant against the SHA-256 above, since any change to the line
    # count or the file size necessarily changes the hash, which is already
    # reported. Checking them would only add duplicate noise.
    baseline_words_count = baseline["theme"].get("words_style_count")
    current_words_count = len(root.findall(".//WordsStyle"))
    if baseline_words_count is not None and baseline_words_count != current_words_count:
        warnings.append(
            "Theme WordsStyle count differs from baseline: "
            f"baseline={baseline_words_count}, current={current_words_count}"
        )

    baseline_widget_count = baseline["theme"].get("widget_style_count")
    current_widget_count = len(global_styles)
    if baseline_widget_count is not None and baseline_widget_count != current_widget_count:
        warnings.append(
            "Theme WidgetStyle count differs from baseline: "
            f"baseline={baseline_widget_count}, current={current_widget_count}"
        )

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
                # sorted() keeps the output byte-identical across runs: `missing`
                # is a set, whose iteration order depends on PYTHONHASHSEED.
                warnings.append(
                    f"Lexer '{name}' coverage: {coverage:.1f}% "
                    f"(Missing IDs: {sorted(missing)})"
                )
        
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

    # Detailed GlobalStyles Widget Audit
    # <WidgetStyle> entries were previously collected but never inspected, so the
    # 39 UI colours escaped the hex-format, palette and contrast checks entirely.
    # The checks below mirror the lexer audit; every message is tagged with
    # "GlobalStyles" so UI findings stay distinguishable from lexer findings.
    for widget in global_styles:
        widget_name = widget.get("name") or f"styleID={widget.get('styleID')}"
        fg = widget.get("fgColor")
        bg = widget.get("bgColor")

        # Hex Format (6 Uppercase)
        if fg and not re.match(r"^[0-9A-F]{6}$", fg):
            errors.append(f"Invalid fgColor format in GlobalStyles widget '{widget_name}': {fg}")
        if bg and not re.match(r"^[0-9A-F]{6}$", bg):
            errors.append(f"Invalid bgColor format in GlobalStyles widget '{widget_name}': {bg}")

        # Palette Membership
        if fg and fg not in palette_set:
            warnings.append(f"Color {fg} in GlobalStyles widget '{widget_name}' not in palette")
        if bg and bg not in palette_set:
            warnings.append(f"Color {bg} in GlobalStyles widget '{widget_name}' not in palette")

        # Contrast Check
        if fg and bg:
            contrast = get_contrast(fg, bg)
            if contrast < 4.5:
                warnings.append(f"Low contrast ({contrast:.2f}) in GlobalStyles widget '{widget_name}' (fg:{fg}, bg:{bg})")

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

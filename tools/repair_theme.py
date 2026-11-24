#!/usr/bin/env python3
"""
Bluloco Dark Theme Repair Tool

Fixes common issues detected by validate_theme.py:
- Invalid hex color formats (lowercase -> uppercase, 3->6 digits)
- fgColor == bgColor conflicts
- Style name drift vs npp_lexer_model.json
- Palette drift (maps to closest canonical color)
- Stray elements outside valid parent blocks
- Missing styleIDs from model (adds skeleton entries)

Usage:
    python3 tools/repair_theme.py --dry-run    # Show what would change
    python3 tools/repair_theme.py --fix        # Apply fixes in-place
    python3 tools/repair_theme.py --backup     # Create backup before fixing
"""

import xml.etree.ElementTree as ET
import json
import re
import sys
import os
import shutil
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

REPO_ROOT = Path(__file__).parent.parent
THEME_PATH = REPO_ROOT / "BlulocoDark.xml"
MODEL_PATH = REPO_ROOT / "tools" / "npp_lexer_model.json"

# Canonical palette (must match validate_theme.py)
PALETTE = {
    "bg": "282C34",
    "fg": "ABB2BF",
    "comments": "8A95B0",
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

UI_EXCEPTIONS = {
    "42444D", "25A45C", "3375FE", "4483AA", "CDD3E0", "8F9AAE", "5FB9BC", "FFFFFF",
    "FFCC00", "177849", "2D333D", "22252A", "3D434F", "DADADA", "0084FF", "25272D",
    "7C8495",
}

DOCUMENTED_EXCEPTIONS = {
    "1C4670", "1C6143", "36465A", "215471", "684B44", "675B3F", "4C4571",
    "2F5A45", "3A3F58", "735047", "50ACAE", "FF839B",
}

ALLOWED_COLORS = set(PALETTE.values()) | UI_EXCEPTIONS | DOCUMENTED_EXCEPTIONS

KNOWN_LEXILLA_STATES = {
    ("asp", "87"),
    ("python", "13"),
    ("fortran", "5"),
    ("fortran77", "5"),
    ("lisp", "8"),
    ("asm", "13"),
    ("verilog", "12"),
    ("ada", "6"),
    ("ada", "8"),
    ("typescript", "9"),
}


def load_model() -> Dict[str, List[Tuple[str, str]]]:
    """Load npp_lexer_model.json as {lexer_name: [(styleID, styleName), ...]}"""
    with open(MODEL_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    model = {}
    for lexer in data.get("lexers", []):
        name = lexer.get("name")
        styles = []
        for s in lexer.get("styles", []):
            if isinstance(s, list) and len(s) >= 2:
                styles.append((str(s[0]), s[1]))
        model[name] = styles
    return model


def normalize_hex(color: str) -> str:
    """Normalize hex color to 6 uppercase digits."""
    if not color:
        return color
    c = color.strip().upper()
    # Remove # if present
    if c.startswith("#"):
        c = c[1:]
    # Expand 3-digit to 6-digit
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    # Pad with zeros if needed
    if len(c) < 6:
        c = c.zfill(6)
    # Truncate if too long
    if len(c) > 6:
        c = c[:6]
    # Validate hex digits
    if not re.match(r"^[0-9A-F]{6}$", c):
        return "282C34"  # fallback to background
    return c


def color_distance(c1: str, c2: str) -> float:
    """Euclidean distance in RGB space."""
    r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
    r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


def map_to_palette(color: str) -> str:
    """Map an out-of-palette color to the closest allowed color."""
    if color in ALLOWED_COLORS:
        return color
    normalized = normalize_hex(color)
    if normalized in ALLOWED_COLORS:
        return normalized
    # Find closest allowed color
    best = min(ALLOWED_COLORS, key=lambda c: color_distance(normalized, c))
    return best


def fix_hex_format(tree: ET.ElementTree) -> int:
    """Fix invalid hex color formats. Returns count of fixes."""
    fixes = 0
    for elem in tree.iter():
        for attr in ("fgColor", "bgColor"):
            val = elem.get(attr)
            if val:
                normalized = normalize_hex(val)
                if normalized != val:
                    elem.set(attr, normalized)
                    fixes += 1
    return fixes


def fix_fg_eq_bg(tree: ET.ElementTree) -> int:
    """Fix fgColor == bgColor by slightly adjusting bgColor. Returns count of fixes."""
    fixes = 0
    for elem in tree.iter("WordsStyle"):
        fg = elem.get("fgColor")
        bg = elem.get("bgColor")
        if fg and bg and fg == bg:
            # Lighten or darken bg slightly
            r, g, b = int(bg[0:2], 16), int(bg[2:4], 16), int(bg[4:6], 16)
            # If dark, lighten; if light, darken
            if r + g + b < 384:  # dark
                r = min(255, r + 16)
                g = min(255, g + 16)
                b = min(255, b + 16)
            else:
                r = max(0, r - 16)
                g = max(0, g - 16)
                b = max(0, b - 16)
            new_bg = f"{r:02X}{g:02X}{b:02X}"
            elem.set("bgColor", new_bg)
            fixes += 1
    for elem in tree.iter("WidgetStyle"):
        fg = elem.get("fgColor")
        bg = elem.get("bgColor")
        if fg and bg and fg == bg:
            r, g, b = int(bg[0:2], 16), int(bg[2:4], 16), int(bg[4:6], 16)
            if r + g + b < 384:
                r = min(255, r + 16)
                g = min(255, g + 16)
                b = min(255, b + 16)
            else:
                r = max(0, r - 16)
                g = max(0, g - 16)
                b = max(0, b - 16)
            new_bg = f"{r:02X}{g:02X}{b:02X}"
            elem.set("bgColor", new_bg)
            fixes += 1
    return fixes


def fix_style_name_drift(tree: ET.ElementTree, model: Dict) -> int:
    """Fix style names that drift from model. Returns count of fixes."""
    fixes = 0
    for lexer in tree.findall(".//LexerType"):
        name = lexer.get("name")
        if name not in model:
            continue
        model_names = {sid: sname for sid, sname in model[name]}
        for style in lexer.findall("WordsStyle"):
            sid = style.get("styleID")
            if sid in model_names:
                expected = model_names[sid]
                current = style.get("name") or ""
                if current != expected:
                    style.set("name", expected)
                    fixes += 1
    return fixes


def fix_palette_drift(tree: ET.ElementTree) -> int:
    """Map out-of-palette colors to closest allowed color. Returns count of fixes."""
    fixes = 0
    for elem in tree.iter():
        for attr in ("fgColor", "bgColor"):
            val = elem.get(attr)
            if val:
                mapped = map_to_palette(val)
                if mapped != val:
                    elem.set(attr, mapped)
                    fixes += 1
    return fixes


def remove_stray_elements(tree: ET.ElementTree) -> int:
    """Remove WordsStyle outside LexerType and WidgetStyle outside GlobalStyles. Returns count."""
    fixes = 0
    root = tree.getroot()

    # Find valid parent elements
    valid_ws_parents = set()
    for lexer in root.findall(".//LexerType"):
        valid_ws_parents.add(id(lexer))

    valid_widget_parents = set()
    gs = root.find(".//GlobalStyles")
    if gs is not None:
        valid_widget_parents.add(id(gs))

    # Remove stray WordsStyle
    for ws in list(root.iter("WordsStyle")):
        parent = ws.getparent() if hasattr(ws, 'getparent') else None
        # ElementTree doesn't have getparent, use iteration
        found = False
        for p in root.iter():
            for child in p:
                if child is ws:
                    if id(p) in valid_ws_parents:
                        found = True
                    break
            if found:
                break
        if not found:
            # Remove from its actual parent
            for p in root.iter():
                if ws in list(p):
                    p.remove(ws)
                    fixes += 1
                    break

    # Remove stray WidgetStyle
    for w in list(root.iter("WidgetStyle")):
        found = False
        for p in root.iter():
            for child in p:
                if child is w:
                    if id(p) in valid_widget_parents:
                        found = True
                    break
            if found:
                break
        if not found:
            for p in root.iter():
                if w in list(p):
                    p.remove(w)
                    fixes += 1
                    break

    return fixes


def add_missing_styleids(tree: ET.ElementTree, model: Dict) -> int:
    """Add missing styleIDs from model as skeleton entries. Returns count."""
    fixes = 0
    for lexer in tree.findall(".//LexerType"):
        name = lexer.get("name")
        if name not in model:
            continue
        model_ids = {sid for sid, _ in model[name]}
        theme_ids = {s.get("styleID") for s in lexer.findall("WordsStyle")}
        missing = model_ids - theme_ids
        for sid in sorted(missing):
            style_name = next(sname for msid, sname in model[name] if msid == sid)
            ws = ET.SubElement(lexer, "WordsStyle")
            ws.set("name", style_name)
            ws.set("styleID", sid)
            ws.set("fgColor", PALETTE["fg"])
            ws.set("bgColor", PALETTE["bg"])
            ws.set("fontName", "")
            ws.set("fontStyle", "0")
            ws.set("fontSize", "")
            if name in ("html", "xml", "css", "javascript", "typescript"):
                # Some lexers have keywordClass
                pass
            fixes += 1
    return fixes


def clean_internal_text(tree: ET.ElementTree) -> int:
    """Remove text content from WordsStyle and WidgetStyle elements. Returns count."""
    fixes = 0
    for elem in tree.iter():
        if elem.tag in ("WordsStyle", "WidgetStyle"):
            if elem.text and elem.text.strip():
                elem.text = None
                fixes += 1
            # Also clear tail
            if elem.tail and elem.tail.strip():
                elem.tail = None
                fixes += 1
    return fixes


def repair_theme(dry_run: bool = False, backup: bool = False) -> Dict[str, int]:
    """Run all repairs. Returns dict of fix counts."""
    # Load model
    model = load_model()

    # Parse theme
    tree = ET.parse(THEME_PATH)

    if backup and not dry_run:
        backup_path = THEME_PATH.with_suffix(".xml.backup")
        shutil.copy2(THEME_PATH, backup_path)
        print(f"Backup created: {backup_path}")

    results = {}

    # Run fixes in order
    results["hex_format"] = fix_hex_format(tree)
    results["fg_eq_bg"] = fix_fg_eq_bg(tree)
    results["palette_drift"] = fix_palette_drift(tree)
    results["style_name_drift"] = fix_style_name_drift(tree, model)
    results["stray_elements"] = remove_stray_elements(tree)
    results["internal_text"] = clean_internal_text(tree)
    results["missing_styleids"] = add_missing_styleids(tree, model)

    if not dry_run:
        # Write back with proper formatting
        ET.indent(tree, space="    ")
        tree.write(THEME_PATH, encoding="utf-8", xml_declaration=True)
        print(f"Theme written to {THEME_PATH}")

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Repair BlulocoDark.xml theme")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    parser.add_argument("--fix", action="store_true", help="Apply fixes (default with --dry-run off)")
    parser.add_argument("--backup", action="store_true", help="Create backup before fixing")
    args = parser.parse_args()

    if not args.dry_run and not args.fix:
        args.fix = True  # default behavior

    print(f"Repairing {THEME_PATH} ({'DRY RUN' if args.dry_run else 'LIVE'})...")
    results = repair_theme(dry_run=args.dry_run, backup=args.backup)

    print("\nFix summary:")
    total = 0
    for category, count in results.items():
        if count > 0:
            print(f"  {category}: {count}")
            total += count
    if total == 0:
        print("  No fixes needed - theme is clean!")
    else:
        print(f"\nTotal fixes: {total}")

    if args.dry_run:
        print("\nRun with --fix to apply changes.")


if __name__ == "__main__":
    main()
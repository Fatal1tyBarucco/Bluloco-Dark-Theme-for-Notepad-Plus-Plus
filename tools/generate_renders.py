#!/usr/bin/env python3
"""
Generate SVG renders from BlulocoDark.xml theme and sample files.

This script creates programmatic SVG previews that approximate how code
would look in Notepad++ with the Bluloco Dark theme. It uses hand-authored
token-to-styleID mappings per lexer (since we can't run Scintilla lexers here).

Usage:
    python3 tools/generate_renders.py [--theme PATH] [--samples PATH] [--output PATH] [--version VERSION]

The script reads:
- BlulocoDark.xml for color palette (fgColor/bgColor by lexer + styleID)
- samples/sample.{ext} for source code
- Hand-authored token mappings in TOKEN_MAPS below

Outputs SVG files to renders/ directory.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# ─── Configuration ────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
DEFAULT_THEME = REPO_ROOT / "BlulocoDark.xml"
DEFAULT_SAMPLES = REPO_ROOT / "samples"
DEFAULT_RENDERS = REPO_ROOT / "renders"

# Render configuration per language
RENDER_CONFIG = {
    "css": {
        "lexer": "css",
        "sample": "sample.css",
        "width": 540,
        "height": 479,
        "font_size": 13,
        "line_height": 19,
        "char_width": 7.8,  # Approximate for Consolas 13px
        "tab_width": 4,
    },
    "html": {
        "lexer": "html",
        "sample": "sample.html",
        "width": 540,
        "height": 479,
        "font_size": 13,
        "line_height": 19,
        "char_width": 7.8,
        "tab_width": 4,
    },
    "js": {
        "lexer": "cpp",  # Notepad++ uses CPP lexer for standalone JS
        "sample": "sample.js",
        "width": 540,
        "height": 479,
        "font_size": 13,
        "line_height": 19,
        "char_width": 7.8,
        "tab_width": 4,
    },
    "php": {
        "lexer": "php",
        "sample": "sample.php",
        "width": 540,
        "height": 479,
        "font_size": 13,
        "line_height": 19,
        "char_width": 7.8,
        "tab_width": 4,
    },
    "py": {
        "lexer": "python",
        "sample": "sample.py",
        "width": 728,
        "height": 441,
        "font_size": 13,
        "line_height": 19,
        "char_width": 7.8,
        "tab_width": 4,
    },
    "rb": {
        "lexer": "ruby",
        "sample": "sample.rb",
        "width": 540,
        "height": 479,
        "font_size": 13,
        "line_height": 19,
        "char_width": 7.8,
        "tab_width": 4,
    },
    "ts": {
        "lexer": "typescript",
        "sample": "sample.ts",
        "width": 540,
        "height": 479,
        "font_size": 13,
        "line_height": 19,
        "char_width": 7.8,
        "tab_width": 4,
    },
}

# ─── Theme Color Extraction ────────────────────────────────────────────────

@dataclass
class StyleColor:
    fg: Optional[str] = None
    bg: Optional[str] = None

def load_theme_colors(theme_path: Path) -> Dict[str, Dict[str, StyleColor]]:
    """Load all fgColor/bgColor from theme XML, keyed by lexer name and styleID."""
    tree = ET.parse(theme_path)
    root = tree.getroot()

    colors: Dict[str, Dict[str, StyleColor]] = {}

    # GlobalStyles (widgets)
    global_styles = {}
    for widget in root.findall(".//GlobalStyles/WidgetStyle"):
        sid = widget.get("styleID")
        fg = widget.get("fgColor")
        bg = widget.get("bgColor")
        if sid:
            global_styles[sid] = StyleColor(
                fg="#" + fg.upper() if fg else None,
                bg="#" + bg.upper() if bg else None,
            )
    colors["_global"] = global_styles

    # LexerStyles
    for lexer in root.findall(".//LexerType"):
        name = lexer.get("name")
        if not name:
            continue
        lexer_colors = {}
        for style in lexer.findall("WordsStyle"):
            sid = style.get("styleID")
            fg = style.get("fgColor")
            bg = style.get("bgColor")
            if sid:
                lexer_colors[sid] = StyleColor(
                    fg="#" + fg.upper() if fg else None,
                    bg="#" + bg.upper() if bg else None,
                )
        colors[name] = lexer_colors

    return colors


# ─── Token Mappings (hand-authored per lexer) ─────────────────────────────
# Each entry: (regex_pattern, styleID, description)
# Pattern matches a token; styleID is the Notepad++ styleID for that lexer

TOKEN_MAPS = {
    "cpp": [  # Used for JavaScript (standalone)
        (r"//.*", "2", "COMMENT LINE"),
        (r"/\*.*?\*/", "3", "COMMENT DOC"),
        (r"\b(const|let|var|async|await|try|catch|return|if|else|for|while|function|class|new|this|throw|typeof|instanceof|in|of|delete|void|yield|import|export|from|default|extends|super|static|get|set)\b", "5", "INSTRUCTION WORD"),
        (r"\b(console|fetch|json|error|log|name|data|response|url|err|apiCall|user|greet|then|catch|finally)\b", "11", "DEFAULT (identifiers)"),
        (r"[=\(\)\{\}\[\];,\.\:\?\+\-\*\/\%\&\|\^\~\<\>\!\=\?]", "10", "OPERATOR"),
        (r"`[^`]*`", "20", "TEMPLATE LITERAL (STRINGRAW)"),
        (r"\$\{", "10", "TEMPLATE INTERPOLATION START"),
        (r"\}", "10", "TEMPLATE INTERPOLATION END"),
        (r"'[^']*'", "6", "STRING"),
        (r'"[^"]*"', "6", "STRING"),
        (r"\b\d+\b", "4", "NUMBER"),
        (r"=>", "10", "ARROW"),
    ],
    "python": [
        (r'""".*?"""', "6", "TRIPLE DOUBLE STRING"),
        (r"'''.*?'''", "6", "TRIPLE STRING"),
        (r'f""".*?"""', "16", "F TRIPLEDOUBLE"),
        (r"f'''.*?'''", "18", "F TRIPLE"),
        (r'f"[^"]*"', "16", "F STRING"),
        (r"f'[^']*'", "17", "F CHARACTER"),
        (r"#.*", "1", "COMMENTLINE"),
        (r"\b(def|class|if|else|elif|for|while|try|except|finally|with|as|import|from|return|yield|lambda|async|await|raise|assert|break|continue|pass|del|global|nonlocal|match|case)\b", "5", "KEYWORDS"),
        (r"\b(print|sum|int|list|dict|str|len|range|enumerate|zip|map|filter|open|close|read|write|input|type|isinstance|hasattr|getattr|setattr)\b", "14", "BUILTINS"),
        (r"@\w+", "15", "DECORATOR"),
        (r"\b(self|cls)\b", "11", "IDENTIFIER"),
        (r"[=\(\)\[\]\{\},\.\:\+\-\*\/\%\&\|\^\~\<\>\!\=\?]", "10", "OPERATOR"),
        (r"'[^']*'", "3", "STRING"),
        (r'"[^"]*"', "3", "STRING"),
        (r"\b\d+\b", "2", "NUMBER"),
        (r"\b([A-Z][a-zA-Z0-9]*)\b", "8", "CLASSNAME"),
        (r"\b(calculate_sum|wrapper|func|debug|numbers|multiplier|res|args|kwargs|Result)\b", "9", "DEFNAME"),
    ],
    "ruby": [
        (r"#.*", "2", "COMMENTLINE"),
        (r"\b(def|class|module|if|else|elsif|unless|end|do|while|until|for|return|yield|break|next|redo|retry|begin|rescue|ensure|raise|throw|catch|super|yield_self|then|when|case|in|and|or|not|defined\?)\b", "5", "KEYWORD"),
        (r"\b(attr_accessor|puts|each|new|describe|it|expect|to|eq|themes|name|t|Theme)\b", "11", "IDENTIFIER"),
        (r"[=\(\)\[\]\{\},\.\:\+\-\*\/\%\&\|\^\~\<\>\!\=\?]", "10", "OPERATOR"),
        (r"'[^']*'", "6", "STRING"),
        (r'"[^"]*"', "6", "STRING"),
        (r":\w+", "13", "SYMBOL"),
        (r"\b\d+\b", "4", "NUMBER"),
        (r"@\w+", "11", "INSTANCE VARIABLE"),
        (r"@@\w+", "11", "CLASS VARIABLE"),
        (r"\$\w+", "11", "GLOBAL VARIABLE"),
    ],
    "html": [
        (r"<!DOCTYPE[^>]*>", "21", "SGML DEFAULT"),
        (r"</?[a-zA-Z][a-zA-Z0-9]*", "1", "TAG"),
        (r"/>", "1", "TAG"),
        (r">", "1", "TAG"),
        (r"\b([a-zA-Z-]+)\s*=", "3", "ATTRIBUTE"),
        (r'"[^"]*"', "19", "VALUE"),
        (r"'[^']*'", "19", "VALUE"),
        (r"<!--.*?-->", "9", "COMMENT"),
        (r"\s+", "0", "DEFAULT (whitespace)"),
    ],
    "css": [
        (r"/\*.*?\*/", "9", "COMMENT"),
        (r"\.[a-zA-Z_-]+", "2", "CLASS"),
        (r"#[a-zA-Z_-]+", "10", "ID"),
        (r"\b([a-zA-Z-]+)\s*\{", "1", "TAG"),
        (r"\}", "1", "TAG"),
        (r"\b(color|background|font|margin|padding|border|display|flex|grid|gap|width|height|max-width|min-width)\b\s*:", "16", "ATTRIBUTE"),
        (r":[a-zA-Z-]+", "3", "PSEUDOCLASS"),
        (r"::[a-zA-Z-]+", "18", "PSEUDOELEMENT"),
        (r"@media", "22", "MEDIA"),
        (r"@import", "12", "DIRECTIVE"),
        (r"!important", "11", "IMPORTANT"),
        (r"[=\(\)\{\}\[\];,\:\+\-\*\/\%\&\|\^\~\<\>\!\=\?]", "5", "OPERATOR"),
        (r'"[^"]*"', "13", "DOUBLE STRING"),
        (r"'[^']*'", "14", "SINGLE STRING"),
        (r"#?[0-9a-fA-F]{3,8}\b", "8", "HEX NUMBER"),
        (r"\b\d+(\.\d+)?(px|em|rem|%|vh|vw)?\b", "8", "NUMBER"),
    ],
    "php": [
        (r"<\?php", "18", "QUESTION MARK"),
        (r"\?>", "18", "QUESTION MARK"),
        (r"\$[a-zA-Z_][a-zA-Z0-9_]*", "123", "VARIABLE"),
        (r"\b(function|class|if|else|elseif|while|for|foreach|return|try|catch|throw|new|public|private|protected|static|abstract|interface|trait|implements|extends|use|namespace|const|echo|print|isset|unset|empty|array|count|strlen|strpos|substr|date|time)\b", "121", "KEYWORDS"),
        (r"//.*", "124", "COMMENT"),
        (r"/\*.*?\*/", "124", "COMMENT"),
        (r'"[^"]*"', "119", "STRING"),
        (r"'[^']*'", "120", "SIMPLE STRING"),
        (r"[=\(\)\[\]\{\},\.\:\+\-\*\/\%\&\|\^\~\<\>\!\=\?\;]", "127", "OPERATOR"),
        (r"\b\d+\b", "122", "NUMBER"),
        (r"->", "127", "OPERATOR"),
    ],
    "typescript": [
        (r"//.*", "2", "COMMENT LINE"),
        (r"/\*.*?\*/", "3", "COMMENT DOC"),
        (r"\b(const|let|var|async|await|try|catch|return|if|else|for|while|function|class|new|this|throw|typeof|instanceof|in|of|delete|void|yield|import|export|from|default|extends|super|static|get|set|interface|type|enum|namespace|declare|abstract|implements)\b", "5", "INSTRUCTION WORD"),
        (r"\b(string|number|boolean|any|void|null|undefined|never|unknown|object|Array|Promise|Record|Partial|Pick|Omit)\b", "16", "TYPE WORD"),
        (r"[=\(\)\[\]\{\},\.\:\+\-\*\/\%\&\|\^\~\<\>\!\=\?\;]", "10", "OPERATOR"),
        (r"'[^']*'", "6", "STRING"),
        (r'"[^"]*"', "6", "STRING"),
        (r"`[^`]*`", "6", "TEMPLATE LITERAL"),
        (r"\$\{", "10", "INTERPOLATION"),
        (r"\}", "10", "INTERPOLATION"),
        (r"\b\d+\b", "4", "NUMBER"),
        (r"\b(console|log|error|fetch|then|catch|finally|url|data|response|err|apiCall|user|greet|name)\b", "11", "DEFAULT"),
    ],
}


# ─── SVG Generation ────────────────────────────────────────────────────────

def tokenize_line(line: str, token_map: List[Tuple[str, str, str]]) -> List[Tuple[str, str]]:
    """
    Tokenize a single line using the token map.
    Returns list of (token_text, styleID).
    """
    if not line:
        return [("", "0")]

    # Sort patterns by length (longest first) for better matching
    sorted_patterns = sorted(token_map, key=lambda x: -len(x[0]))

    tokens = []
    pos = 0
    line_len = len(line)

    while pos < line_len:
        matched = False
        for pattern, style_id, _desc in sorted_patterns:
            regex = re.compile(pattern)
            match = regex.match(line[pos:])
            if match:
                token_text = match.group(0)
                tokens.append((token_text, style_id))
                pos += len(token_text)
                matched = True
                break
        if not matched:
            # Fallback: single character
            tokens.append((line[pos], "0"))
            pos += 1

    return tokens


def build_svg(
    name: str,
    config: dict,
    theme_colors: Dict[str, Dict[str, StyleColor]],
    version: str,
) -> ET.Element:
    """Build SVG element for a render."""

    lexer = config["lexer"]
    sample_path = DEFAULT_SAMPLES / config["sample"]

    with open(sample_path, "r", encoding="utf-8") as f:
        source_lines = f.read().splitlines()

    # Get colors for this lexer
    lexer_colors = theme_colors.get(lexer, {})
    global_colors = theme_colors.get("_global", {})

    def get_color(style_id: str, attr: str) -> str:
        """Get color for styleID, falling back to global, then defaults."""
        if style_id in lexer_colors:
            color = getattr(lexer_colors[style_id], attr)
            if color:
                return color
        if style_id in global_colors:
            color = getattr(global_colors[style_id], attr)
            if color:
                return color
        # Defaults
        if attr == "fg":
            return "#ABB2BF"
        return "#282C34"

    token_map = TOKEN_MAPS.get(lexer, [])

    # SVG dimensions
    width = config["width"]
    height = config["height"]
    font_size = config["font_size"]
    line_height = config["line_height"]
    char_width = config["char_width"]
    tab_width = config["tab_width"]

    # Layout constants
    margin_left = 46  # Line number gutter
    margin_top = 34   # Tab bar height
    code_left = margin_left + 12  # Code starts after gutter
    line_number_right = margin_left - 4

    # Create SVG root
    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(width),
        "height": str(height),
        "viewBox": f"0 0 {width} {height}",
    })

    # Background
    ET.SubElement(svg, "rect", {
        "width": str(width),
        "height": str(height),
        "rx": "8",
        "fill": "#25272D",  # Window chrome bg
    })

    # Tab bar
    tab_bg = "#282C34"
    tab_accent = "#3691FF"
    ET.SubElement(svg, "rect", {
        "x": "12", "y": "7", "width": "168", "height": "27", "rx": "4",
        "fill": tab_bg,
    })
    ET.SubElement(svg, "rect", {
        "x": "12", "y": "7", "width": "168", "height": "2.6", "rx": "1.3",
        "fill": tab_accent,
    })
    ET.SubElement(svg, "text", {
        "x": "24", "y": "25", "font-size": "12", "fill": "#ABB2BF",
        "font-family": "Consolas,'DejaVu Sans Mono',Menlo,monospace",
    }).text = config["sample"]
    ET.SubElement(svg, "text", {
        "x": "166", "y": "25", "font-size": "12", "fill": "#636D83",
        "font-family": "Consolas,monospace",
    }).text = "×"
    ET.SubElement(svg, "text", {
        "x": "196", "y": "25", "font-size": "12", "fill": "#636D83",
        "font-family": "Consolas,'DejaVu Sans Mono',Menlo,monospace",
    }).text = "README.md"

    # Editor area
    editor_height = height - margin_top - 20  # Leave space for status bar
    ET.SubElement(svg, "rect", {
        "x": "0", "y": str(margin_top), "width": str(width), "height": str(editor_height),
        "fill": "#282C34",
    })
    ET.SubElement(svg, "rect", {
        "x": "0", "y": str(margin_top), "width": str(margin_left), "height": str(editor_height),
        "fill": "#22252A",  # Line number gutter
    })

    # Current line highlight (line 4 in all samples)
    current_line_y = margin_top + (4 - 1) * line_height
    ET.SubElement(svg, "rect", {
        "x": str(margin_left), "y": str(current_line_y),
        "width": str(width - margin_left), "height": str(line_height),
        "fill": "#2D333D",
    })

    # Line numbers
    for i, _ in enumerate(source_lines, 1):
        y = margin_top + (i - 1) * line_height + font_size - 3
        ET.SubElement(svg, "text", {
            "x": str(line_number_right), "y": str(y),
            "font-size": "10", "fill": "#636D83",
            "text-anchor": "end",
            "font-family": "Consolas,'DejaVu Sans Mono',Menlo,monospace",
        }).text = str(i)

    # Code tokens
    token_map = TOKEN_MAPS.get(lexer, [])

    for line_idx, line in enumerate(source_lines):
        y = margin_top + line_idx * line_height + font_size - 3

        # Expand tabs
        display_line = line.replace("\t", " " * tab_width)
        tokens = tokenize_line(display_line, token_map)

        x = code_left
        for token_text, style_id in tokens:
            if not token_text:
                continue

            fg_color = get_color(style_id, "fg")

            # Calculate textLength for monospace alignment
            text_length = len(token_text) * char_width

            text_elem = ET.SubElement(svg, "text", {
                "font-size": str(font_size),
                "x": f"{x:.1f}",
                "y": str(y),
                "fill": fg_color,
                "textLength": f"{text_length:.1f}",
                "lengthAdjust": "spacingAndGlyphs",
                "font-family": "Consolas,'DejaVu Sans Mono',Menlo,monospace",
                "data-style-id": style_id,
            })
            text_elem.text = token_text

            x += text_length

    # Cursor (line 4, column 0)
    cursor_y = margin_top + (4 - 1) * line_height + 2
    ET.SubElement(svg, "rect", {
        "x": str(code_left), "y": str(cursor_y),
        "width": "1.6", "height": "15",
        "fill": "#FFCC00",
    })

    # Status bar
    status_y = height - 20
    ET.SubElement(svg, "rect", {
        "x": "0", "y": str(status_y),
        "width": str(width), "height": "20",
        "fill": "#22252A",
    })
    ET.SubElement(svg, "text", {
        "x": "12", "y": str(status_y + 13.5),
        "font-size": "10", "fill": "#636D83",
        "font-family": "Consolas,'DejaVu Sans Mono',Menlo,monospace",
    }).text = f"Render de demonstração — Bluloco Dark v{version} · cores extraídas de BlulocoDark.xml · não é uma captura do Notepad++"

    # Add disclosure comment
    comment = ET.Comment(f" Render de demonstracao gerado programaticamente a partir de BlulocoDark.xml (v{version}). Nao e uma captura de tela do Notepad++. ")
    svg.insert(0, comment)

    return svg


def generate_all(theme_path: Path, version: str, output_dir: Path):
    """Generate all renders."""
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading theme from {theme_path}...")
    theme_colors = load_theme_colors(theme_path)
    print(f"Loaded colors for {len(theme_colors)} lexers")

    for name, config in RENDER_CONFIG.items():
        print(f"Generating {name}.svg...")
        svg = build_svg(name, config, theme_colors, version)

        output_path = output_dir / f"{name}.svg"
        ET.ElementTree(svg).write(output_path, encoding="utf-8", xml_declaration=True)
        print(f"  -> {output_path}")


def main():
    global RENDER_CONFIG
    import argparse

    parser = argparse.ArgumentParser(description="Generate SVG renders from BlulocoDark.xml")
    parser.add_argument("--theme", type=Path, default=DEFAULT_THEME, help="Path to BlulocoDark.xml")
    parser.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES, help="Path to samples directory")
    parser.add_argument("--output", type=Path, default=DEFAULT_RENDERS, help="Output directory for SVGs")
    parser.add_argument("--version", default="2.3.1", help="Version string for render marker")
    parser.add_argument("--only", choices=list(RENDER_CONFIG.keys()), help="Generate only one render")

    args = parser.parse_args()

    if args.only:
        RENDER_CONFIG = {args.only: RENDER_CONFIG[args.only]}

    generate_all(args.theme, args.version, args.output)
    print("Done!")


if __name__ == "__main__":
    main()
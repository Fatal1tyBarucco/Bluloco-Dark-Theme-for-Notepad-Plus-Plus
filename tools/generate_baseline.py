#!/usr/bin/env python3
"""Generate tools/baseline.json from BlulocoDark.xml.

Reproducible script: resolves every path against the repository root (the
directory that contains this script's parent folder), so it can be run from
any working directory. Uses only the Python standard library.

Produced schema (keys are emitted deterministically via sort_keys):
{
  "generated_at": "<ISO-8601 UTC>",
  "theme": {
    "path", "sha256", "line_count", "size_bytes",
    "lexer_type_count", "words_style_count", "widget_style_count"
  },
  "summary": {
    "lexers_in_theme", "duplicate_lexers",
    "lexers_with_duplicate_style_ids", "lexers_with_unknown_ids",
    "total_unknown_style_ids", "fg_eq_bg_styles",
    "words_styles_with_text", "widget_styles_with_text",
    "colors_used", "out_of_palette", "out_of_palette_criteria"
  },
  "lexers": { "<name>": { "name","desc","ext","style_count",
      "duplicate_style_ids","unknown_style_ids","unknown_style_details","styles": [...] } },
  "widgets": [ { "name","styleID","fgColor","bgColor","text" }, ... ],
  "colors": { "used", "palette", "ui_exceptions", "documented_exceptions", "out_of_palette" },
  "palette": { ... },
  "text_content": { "words_styles_with_text": [...], "widget_styles_with_text": [...] },
  "generated_at": "..."
}
"""

import argparse
import hashlib
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, OrderedDict
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Paths (resolved against this file's location => repo root / tools/)
# ---------------------------------------------------------------------------
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)

DEFAULT_THEME = os.path.join(REPO_ROOT, "BlulocoDark.xml")
DEFAULT_OUT = os.path.join(TOOLS_DIR, "baseline.json")
DEFAULT_MODEL = os.path.join(TOOLS_DIR, "npp_lexer_model.json")

# Canonical palette (mirrors tools/validate_theme.py PALETTE).
PALETTE = OrderedDict([
    ("bg", "282C34"),
    ("fg", "ABB2BF"),
    ("comments", "636D83"),
    ("keywords", "10B1FE"),
    ("strings", "F9C859"),
    ("numbers", "FF78F8"),
    ("functions", "3FC56B"),
    ("classes", "FF6480"),
    ("errors", "FF2E3F"),
    ("constants", "9F7EFE"),
    ("params", "8BCDEF"),
    ("props", "CE9887"),
    ("operators", "7A82DA"),
    ("tags", "3691FF"),
    ("attrs", "FF936A"),
])

# Existing UI exceptions carried from tools/validate_theme.py.
UI_EXCEPTIONS = OrderedDict([
    # Terminal ANSI palette (VSCode source: terminal.ansi* tokens).
    ("ansi_black", "42444D"),
    ("ansi_green", "25A45C"),
    ("ansi_blue", "3375FE"),
    ("ansi_cyan", "4483AA"),
    ("ansi_white", "CDD3E0"),
    ("ansi_bright_black", "8F9AAE"),
    ("ansi_bright_cyan", "5FB9BC"),
    ("ansi_bright_white", "FFFFFF"),
    # Notepad++ UI chrome.
    ("caret", "FFCC00"),
    ("smart_highlight_bg", "177849"),
    ("current_line_bg", "2D333D"),
    ("margin_bg", "22252A"),
    ("indent_edge_fold", "3D434F"),
    ("eol_custom", "DADADA"),
    ("selected_text_bg", "0084FF"),
    ("inactive_tabs_bg", "25272D"),
    # Documentation comment colour.
    ("comment_doc_keyword", "7C8495"),
])

# Documented exceptions introduced with the v2.1+ tint/ramp batch.
# Each entry is a color that does NOT belong to the canonical palette but is
# intentionally present in the theme. Provenance is noted per entry.
DOCUMENTED_EXCEPTIONS = OrderedDict([
    # --- Tinted GlobalStyles (VSCode alpha composite over bg 282C34) ---
    # These are the tab/tint colors computed by compositing VSCode
    # `workbench*` / tab colors over the Bluloco background.
    ("tab_tint_1", "1C4670"),
    ("tab_tint_2", "1C6143"),
    ("tab_tint_3", "36465A"),
    ("tab_tint_4", "215471"),
    ("tab_tint_5", "684B44"),
    ("tab_tint_6", "675B3F"),
    ("tab_tint_7", "4C4571"),
    ("tab_tint_8", "2F5A45"),
    ("tab_tint_9", "3A3F58"),
    ("tab_tint_10", "735047"),
    # --- USER KEYWORDS ramp (semanticTokenColors upstream) ---
    # Additional user-keyword substyles beyond the canonical 128-135 ramp.
    ("user_keyword_ramp_a", "50ACAE"),
    ("user_keyword_ramp_b", "FF839B"),
])

HEX_RE = re.compile(r"^[0-9A-F]{6}$")

WORDS_STYLE_ATTRS = [
    "styleID", "name", "fgColor", "bgColor",
    "fontName", "fontStyle", "fontSize", "keywordClass", "text",
]
WIDGET_ATTRS = ["name", "styleID", "fgColor", "bgColor", "text"]


def _text(el):
    """Return stripped element text, or '' when empty/absent."""
    if el.text is None:
        return ""
    return el.text.strip()


def _attrs(el, names):
    return {n: el.get(n) for n in names}


def _load_model(model_path):
    """Return the lexer model dict, or {} when the file does not exist."""
    if not model_path or not os.path.isfile(model_path):
        return {}
    try:
        with open(model_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (ValueError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def _model_ids(model, lexer_name):
    """Set of styleIDs declared by the model for a given lexer."""
    styles = model.get(lexer_name)
    if not isinstance(styles, list):
        return set()
    return {str(s[0]) for s in styles if isinstance(s, (list, tuple)) and len(s) >= 1}


def generate(theme_path, model_path):
    with open(theme_path, "rb") as f:
        theme_bytes = f.read()
    root = ET.fromstring(theme_bytes)

    text_content = theme_bytes.decode("utf-8")
    line_count = len(text_content.splitlines())
    size_bytes = len(theme_bytes)
    sha256 = hashlib.sha256(theme_bytes).hexdigest()

    model = _load_model(model_path)

    # ---- Lexers -------------------------------------------------------
    lexers = root.findall(".//LexerType")
    lexer_names = [l.get("name") for l in lexers]
    name_counts = Counter(lexer_names)
    duplicate_lexers = sorted([n for n, c in name_counts.items() if c > 1])

    lexers_out = OrderedDict()
    all_unknown = []          # {lexer, styleID, name}
    all_fg_eq_bg = []         # {lexer, styleID, name, color}
    all_used_colors = set()
    lexers_with_dup_ids = []
    lexers_with_unknown_ids = []

    for lexer in lexers:
        name = lexer.get("name")
        styles = lexer.findall("WordsStyle")
        style_ids = [s.get("styleID") for s in styles]
        id_counts = Counter(style_ids)
        dup_ids = sorted([i for i, c in id_counts.items() if i is not None and c > 1])
        if dup_ids:
            lexers_with_dup_ids.append(name)

        model_ids = _model_ids(model, name)
        lexer_unknown = []
        lexer_unknown_details = []
        unknown_ids = [s.get("styleID") for s in styles
                       if s.get("styleID") is not None and s.get("styleID") not in model_ids]
        if unknown_ids:
            lexers_with_unknown_ids.append(name)
            for s in styles:
                sid = s.get("styleID")
                if sid is not None and sid not in model_ids:
                    lexer_unknown.append(sid)
                    lexer_unknown_details.append({
                        "styleID": sid,
                        "name": s.get("name"),
                    })
                    all_unknown.append({
                        "lexer": name,
                        "styleID": sid,
                        "name": s.get("name"),
                    })

        style_entries = []
        for s in styles:
            fg = s.get("fgColor")
            bg = s.get("bgColor")
            if fg:
                all_used_colors.add(fg)
            if bg:
                all_used_colors.add(bg)
            if fg and bg and fg == bg:
                all_fg_eq_bg.append({
                    "lexer": name,
                    "styleID": s.get("styleID"),
                    "name": s.get("name"),
                    "color": fg,
                })
            entry = _attrs(s, WORDS_STYLE_ATTRS)
            entry["text"] = _text(s)
            style_entries.append(entry)

        lexers_out[name] = OrderedDict([
            ("name", name),
            ("desc", lexer.get("desc")),
            ("ext", lexer.get("ext")),
            ("style_count", len(styles)),
            ("duplicate_style_ids", dup_ids),
            ("unknown_style_ids", lexer_unknown),
            ("unknown_style_details", lexer_unknown_details),
            ("styles", style_entries),
        ])

    # ---- Widgets (GlobalStyles) ---------------------------------------
    widgets = root.findall(".//WidgetStyle")
    widgets_out = []
    widgets_with_text = []
    for w in widgets:
        fg = w.get("fgColor")
        bg = w.get("bgColor")
        if fg:
            all_used_colors.add(fg)
        if bg:
            all_used_colors.add(bg)
        entry = _attrs(w, WIDGET_ATTRS)
        entry["text"] = _text(w)
        widgets_out.append(entry)
        if entry["text"]:
            widgets_with_text.append({
                "tag": "WidgetStyle",
                "name": w.get("name"),
                "styleID": w.get("styleID"),
                "text": entry["text"],
            })

    words_with_text = []
    for lexer in lexers:
        for s in lexer.findall("WordsStyle"):
            t = _text(s)
            if t:
                words_with_text.append({
                    "tag": "WordsStyle",
                    "lexer": lexer.get("name"),
                    "styleID": s.get("styleID"),
                    "name": s.get("name"),
                    "text": t,
                })

    allowed_colors = (set(PALETTE.values()) | set(UI_EXCEPTIONS.values())
                      | set(DOCUMENTED_EXCEPTIONS.values()))
    out_of_palette = sorted(c for c in all_used_colors if c not in allowed_colors)

    theme = OrderedDict([
        ("path", os.path.relpath(theme_path, REPO_ROOT)
         if os.path.commonpath([theme_path, REPO_ROOT]) == REPO_ROOT
         else theme_path),
        ("sha256", sha256),
        ("line_count", line_count),
        ("size_bytes", size_bytes),
        ("lexer_type_count", len(lexers)),
        ("words_style_count", len(root.findall(".//WordsStyle"))),
        ("widget_style_count", len(widgets)),
    ])

    summary = OrderedDict([
        ("lexers_in_theme", len(lexers)),
        ("duplicate_lexers", duplicate_lexers),
        ("lexers_with_duplicate_style_ids", lexers_with_dup_ids),
        ("lexers_with_unknown_ids", lexers_with_unknown_ids),
        ("total_unknown_style_ids", len(all_unknown)),
        ("fg_eq_bg_styles", all_fg_eq_bg),
        ("words_styles_with_text", len(words_with_text)),
        ("widget_styles_with_text", len(widgets_with_text)),
        ("colors_used", sorted(all_used_colors)),
        ("out_of_palette", out_of_palette),
        ("out_of_palette_criteria",
         "not in PALETTE | UI_EXCEPTIONS | DOCUMENTED_EXCEPTIONS (tools/validate_theme.py)"),
    ])

    colors = OrderedDict([
        ("used", sorted(all_used_colors)),
        ("palette", dict(PALETTE)),
        ("ui_exceptions", dict(UI_EXCEPTIONS)),
        ("documented_exceptions", dict(DOCUMENTED_EXCEPTIONS)),
        ("out_of_palette", out_of_palette),
    ])

    baseline = OrderedDict([
        ("generated_at", datetime.now(timezone.utc).isoformat()),
        ("theme", theme),
        ("summary", summary),
        ("lexers", lexers_out),
        ("widgets", widgets_out),
        ("colors", colors),
        ("palette", dict(PALETTE)),
        ("text_content", OrderedDict([
            ("words_styles_with_text", words_with_text),
            ("widget_styles_with_text", widgets_with_text),
        ])),
    ])
    return baseline


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate tools/baseline.json from BlulocoDark.xml.")
    parser.add_argument("--theme", default=DEFAULT_THEME,
                        help="Path to the theme XML (default: %(default)s)")
    parser.add_argument("--out", default=DEFAULT_OUT,
                        help="Output baseline JSON path (default: %(default)s)")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="Path to npp_lexer_model.json (default: %(default)s)")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress the summary printout")
    args = parser.parse_args(argv)

    baseline = generate(args.theme, args.model)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")

    if not args.quiet:
        t = baseline["theme"]
        print(f"baseline generated: {args.out}")
        print(f"  theme      : {t['path']}")
        print(f"  sha256     : {t['sha256']}")
        print(f"  size_bytes : {t['size_bytes']}")
        print(f"  line_count : {t['line_count']}")
        print(f"  lexers     : {t['lexer_type_count']}")
        print(f"  words      : {t['words_style_count']}")
        print(f"  widgets    : {t['widget_style_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

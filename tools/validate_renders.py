#!/usr/bin/env python3
"""Validate generated SVG previews against the canonical Notepad++ theme XML.

This checks structural integrity, release labelling, honest disclosure and
colour provenance only. It cannot validate Scintilla token classification,
font metrics, UI behaviour, or native Notepad++ rendering.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME_PATH = os.path.join(REPO_ROOT, "BlulocoDark.xml")
README_PATH = os.path.join(REPO_ROOT, "README.md")
RENDER_DIR = os.path.join(REPO_ROOT, "renders")
EXPECTED_RENDERS = ("css", "html", "js", "php", "py", "rb", "ts")
RENDER_LEXERS = {
    "css": "css",
    "html": "html",
    "js": "cpp",
    "php": "php",
    "py": "python",
    "rb": "ruby",
    "ts": "typescript",
}
HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
TOKEN_STYLE_REGRESSION_CASES = {
    "css": (
        ("89.2", "202", "background-color", "6"),
        ("89.2", "221", "color", "6"),
        ("89.2", "240", "font-family", "6"),
        ("89.2", "316", "display", "6"),
        ("89.2", "335", "grid-template-columns", "6"),
        ("89.2", "354", "gap", "6"),
        ("120.4", "411", "max-width", "22"),
        ("206.2", "411", "600px", "22"),
        ("120.4", "449", "padding", "6"),
    ),
    "rb": (
        ("73.6", "126", "attr_accessor", "11"),
        ("190.6", "164", "name", "11"),
        ("151.6", "183", "name", "11"),
        ("89.2", "259", "puts", "11"),
        ("58.0", "335", "themes", "11"),
        ("58.0", "354", "themes", "11"),
        ("112.6", "354", "each", "11"),
        ("182.8", "354", "t", "11"),
        ("73.6", "373", "puts", "11"),
        ("58.0", "430", "Theme", "11"),
        ("104.8", "430", "new", "11"),
        ("260.8", "430", "describe", "11"),
    ),
    "js": (
        ("58.0", "107", "const", "5"),
        ("104.8", "107", "apiCall", "11"),
        ("167.2", "107", "=", "10"),
        ("182.8", "107", "async", "5"),
        ("276.4", "107", "=>", "10"),
        ("229.6", "221", "`Error fetching ", "20"),
        ("354.4", "221", "${", "10"),
        ("370.0", "221", "url", "11"),
        ("401.2", "221", ": ", "20"),
        ("416.8", "221", "${", "10"),
        ("432.4", "221", "err", "11"),
        ("214.0", "354", "`Hello, I am ", "20"),
        ("331.0", "354", "this", "5"),
        ("362.2", "354", ".", "10"),
        ("370.0", "354", "name", "11"),
    ),
    "ts": (
        ("292.0", "354", "undefined", "5"),
    ),
    "html": (
        ("58.0", "50", "<!", "21"),
        ("73.6", "50", "DOCTYPE", "22"),
        ("128.2", "50", " ", "21"),
        ("136.0", "50", "html", "23"),
        ("167.2", "50", ">", "21"),
    ),
    "py": (
        ("167.2", "202", 'f"Calling ', "16"),
        ("245.2", "202", "{", "10"),
        ("253.0", "202", "func", "11"),
        ("284.2", "202", ".", "10"),
        ("292.0", "202", "__name__", "20"),
        ("354.4", "202", "}", "10"),
        ("362.2", "202", " with ", "16"),
        ("409.0", "202", "{", "10"),
        ("416.8", "202", "args", "11"),
        ("448.0", "202", "}", "10"),
        ("455.8", "202", '"', "16"),
        ("136.0", "392", 'f"Result: ', "16"),
        ("214.0", "392", "{", "10"),
        ("221.8", "392", "calculate_sum", "11"),
        ("323.2", "392", "(", "10"),
        ("331.0", "392", "[", "10"),
        ("338.8", "392", "1", "2"),
        ("346.6", "392", ",", "10"),
        ("354.4", "392", " ", "0"),
        ("362.2", "392", "2", "2"),
        ("370.0", "392", ",", "10"),
        ("377.8", "392", " ", "0"),
        ("385.6", "392", "3", "2"),
        ("393.4", "392", "]", "10"),
        ("401.2", "392", ",", "10"),
        ("409.0", "392", " ", "0"),
        ("416.8", "392", "2", "2"),
        ("424.6", "392", ")", "10"),
        ("432.4", "392", "}", "10"),
        ("440.2", "392", '"', "16"),
    ),
}


def main():
    errors = []
    with open(THEME_PATH, "r", encoding="utf-8") as theme_file:
        theme_xml = ET.parse(theme_file).getroot()
    with open(README_PATH, "r", encoding="utf-8") as readme_file:
        readme = readme_file.read()

    global_styles = theme_xml.find(".//GlobalStyles")
    global_colors = {
        "#" + value.upper()
        for element in (global_styles if global_styles is not None else [])
        for attribute in ("fgColor", "bgColor")
        if (value := element.get(attribute))
    }
    lexer_colors = {}
    lexer_styles = {}
    for lexer in theme_xml.findall(".//LexerType"):
        lexer_name = lexer.get("name")
        lexer_styles[lexer_name] = {
            element.get("styleID"): {
                "name": element.get("name"),
                "fg": "#" + element.get("fgColor", "").upper()
                if element.get("fgColor")
                else None,
            }
            for element in lexer.findall("WordsStyle")
        }
        lexer_colors[lexer_name] = {
            "#" + value.upper()
            for element in lexer.findall("WordsStyle")
            for attribute in ("fgColor", "bgColor")
            if (value := element.get(attribute))
        }
    theme_colors = global_colors | set().union(*lexer_colors.values())
    release_match = re.search(r"^### v([0-9]+\.[0-9]+\.[0-9]+)", readme, re.MULTILINE)
    if not release_match:
        errors.append("README.md has no current semantic-version heading (### vX.Y.Z)")
        expected_version = None
    else:
        expected_version = release_match.group(1)

    actual_files = {
        name[:-4]
        for name in os.listdir(RENDER_DIR)
        if name.lower().endswith(".svg")
    }
    if actual_files != set(EXPECTED_RENDERS):
        errors.append(
            "SVG render set mismatch: expected "
            + ", ".join(EXPECTED_RENDERS)
            + "; found "
            + ", ".join(sorted(actual_files))
        )

    for render_name in EXPECTED_RENDERS:
        render_path = os.path.join(RENDER_DIR, render_name + ".svg")
        if not os.path.isfile(render_path):
            continue
        try:
            tree = ET.parse(render_path)
        except ET.ParseError as error:
            errors.append(f"{render_name}.svg is not well-formed XML: {error}")
            continue

        root = tree.getroot()
        if not root.tag.endswith("svg"):
            errors.append(f"{render_name}.svg root element is not <svg>")

        lexer_name = RENDER_LEXERS[render_name]
        allowed_render_colors = lexer_colors.get(lexer_name, set()) | global_colors
        if lexer_name not in lexer_colors:
            errors.append(
                f"Canonical XML does not contain the expected lexer {lexer_name!r} "
                f"for {render_name}.svg"
            )

        with open(render_path, "r", encoding="utf-8") as render_file:
            source = render_file.read()

        if expected_version and f"Bluloco Dark v{expected_version}" not in source:
            errors.append(
                f"{render_name}.svg release marker does not match README v{expected_version}"
            )
        if "não é uma captura do Notepad++" not in source:
            errors.append(
                f"{render_name}.svg must explicitly disclose that it is not a Notepad++ screenshot"
            )

        for element in root.iter():
            for attribute in ("fill", "stroke"):
                value = element.get(attribute)
                if not value or value.lower() == "none":
                    continue
                if not HEX_COLOR.fullmatch(value):
                    errors.append(
                        f"{render_name}.svg has unsupported {attribute} value {value!r}"
                    )
                elif value.upper() not in allowed_render_colors:
                    errors.append(
                        f"{render_name}.svg uses {attribute} {value} absent from "
                        f"the {lexer_name!r} lexer and GlobalStyles in BlulocoDark.xml"
                    )

    regression_count = 0
    for render_name, cases in TOKEN_STYLE_REGRESSION_CASES.items():
        render_path = os.path.join(RENDER_DIR, render_name + ".svg")
        if not os.path.isfile(render_path):
            continue
        try:
            root = ET.parse(render_path).getroot()
        except ET.ParseError:
            continue
        lexer_name = RENDER_LEXERS[render_name]
        style_lookup = lexer_styles.get(lexer_name, {})
        for expected_x, expected_y, expected_text, expected_style_id in cases:
            matching_elements = []
            for element in root.iter():
                if not element.tag.endswith(("text", "tspan")):
                    continue
                if element.get("x") != expected_x or element.get("y") != expected_y:
                    continue
                rendered_text = "".join(element.itertext())
                if rendered_text == expected_text:
                    matching_elements.append(element)
            if len(matching_elements) != 1:
                errors.append(
                    f"{render_name}.svg expected exactly one token "
                    f"{expected_text!r} at ({expected_x}, {expected_y}); "
                    f"found {len(matching_elements)}"
                )
                continue
            element = matching_elements[0]
            actual_style_id = element.get("data-style-id")
            if actual_style_id != expected_style_id:
                errors.append(
                    f"{render_name}.svg token {expected_text!r} at "
                    f"({expected_x}, {expected_y}) has data-style-id "
                    f"{actual_style_id!r}; expected {expected_style_id!r}"
                )
                continue
            style = style_lookup.get(expected_style_id)
            if style is None:
                errors.append(
                    f"{render_name}.svg token {expected_text!r} references "
                    f"styleID {expected_style_id}, absent from {lexer_name!r} in XML"
                )
                continue
            actual_fill = (element.get("fill") or "").upper()
            if actual_fill != style["fg"]:
                errors.append(
                    f"{render_name}.svg token {expected_text!r} uses fill "
                    f"{actual_fill!r}; {lexer_name!r} styleID {expected_style_id} "
                    f"({style['name']}) requires {style['fg']!r}"
                )
                continue
            regression_count += 1

    print("--- Render Validation Report ---")
    print(f"Semantic token regression cases: {regression_count}")
    print(f"Theme colours available: {len(theme_colors)}")
    print("Render colours checked against their matching lexer plus GlobalStyles")
    print(f"Expected renders: {len(EXPECTED_RENDERS)}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"  [ERROR] {error}")
    if errors:
        return 1
    print(
        "Render validation successful. Colour provenance and disclosure passed; "
        "token classification and native Notepad++ fidelity remain unverified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

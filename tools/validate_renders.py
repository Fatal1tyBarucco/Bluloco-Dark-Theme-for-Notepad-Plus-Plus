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
    "js": "javascript",
    "php": "php",
    "py": "python",
    "rb": "ruby",
    "ts": "typescript",
}
HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")


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
    for lexer in theme_xml.findall(".//LexerType"):
        lexer_name = lexer.get("name")
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

    print("--- Render Validation Report ---")
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

#!/usr/bin/env python3
"""Verify native Notepad++ lexer styles and theme colours on Windows."""

import argparse
import ctypes
import json
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from ctypes import wintypes
from pathlib import Path

SCI_GETLENGTH = 2006
SCI_GETSTYLEAT = 2010
SCI_COLOURISE = 4003
SCI_STYLEGETFORE = 2481
SCI_STYLEGETBACK = 2482
WM_CLOSE = 0x0010
SW_RESTORE = 9

TEST_CASES = (
    ("css", "sample.css", 9, "background-color", 0, 6),
    ("css", "sample.css", 20, "max-width", 0, 22),
    ("css", "sample.css", 20, "600px", 0, 22),
    ("css", "sample.css", 22, "padding", 0, 6),
    ("html", "sample.html", 1, "<!", 0, 21),
    ("html", "sample.html", 1, "DOCTYPE", 0, 22),
    ("html", "sample.html", 1, "html", 0, 23),
    ("html", "sample.html", 1, ">", 0, 21),
    ("javascript", "sample.js", 4, "const", 0, 5),
    ("javascript", "sample.js", 4, "async", 0, 5),
    ("javascript", "sample.js", 6, "await", 0, 5),
    ("javascript", "sample.js", 10, "console", 0, 11),
    ("javascript", "sample.js", 10, "Error fetching ", 0, 20),
    ("javascript", "sample.js", 10, "${", 0, 10),
    ("javascript", "sample.js", 10, "url", 0, 11),
    ("javascript", "sample.js", 10, "err", 0, 11),
    ("javascript", "sample.js", 17, "Hello, I am ", 0, 20),
    ("javascript", "sample.js", 17, "${", 0, 10),
    ("javascript", "sample.js", 17, "this", 0, 5),
    ("javascript", "sample.js", 17, ".", 1, 10),
    ("javascript", "sample.js", 17, "name", 0, 11),
    ("php", "sample.php", 6, "namespace", 0, 121),
    ("php", "sample.php", 8, "ThemeManager", 0, 118),
    ("php", "sample.php", 23, "echo", 0, 121),
    ("python", "sample.py", 9, "print", 0, 14),
    ("python", "sample.py", 9, "func", 0, 11),
    ("python", "sample.py", 9, "__name__", 0, 20),
    ("python", "sample.py", 9, "args", 0, 11),
    ("python", "sample.py", 14, "None", 0, 5),
    ("python", "sample.py", 14, "int", 0, 14),
    ("python", "sample.py", 14, "int", 1, 14),
    ("python", "sample.py", 14, "int", 2, 14),
    ("python", "sample.py", 15, "sum", 0, 14),
    ("python", "sample.py", 19, "calculate_sum", 0, 11),
    ("python", "sample.py", 19, "1", 0, 2),
    ("python", "sample.py", 19, "2", 0, 2),
    ("python", "sample.py", 19, "2", 1, 2),
    ("ruby", "sample.rb", 5, "attr_accessor", 0, 11),
    ("ruby", "sample.rb", 7, "initialize", 0, 9),
    ("ruby", "sample.rb", 7, "name", 0, 11),
    ("ruby", "sample.rb", 12, "puts", 0, 11),
    ("ruby", "sample.rb", 17, "each", 0, 11),
    ("ruby", "sample.rb", 21, "Theme", 0, 11),
    ("ruby", "sample.rb", 21, "new", 0, 11),
    ("ruby", "sample.rb", 21, "describe", 0, 11),
    ("typescript", "sample.ts", 2, "interface", 0, 5),
    ("typescript", "sample.ts", 3, "number", 0, 16),
    ("typescript", "sample.ts", 4, "string", 0, 16),
    ("typescript", "sample.ts", 13, "void", 0, 16),
    ("typescript", "sample.ts", 17, "undefined", 0, 5),
)


def _windows_api():
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    enum_proc_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows.argtypes = [enum_proc_type, wintypes.LPARAM]
    user32.EnumWindows.restype = wintypes.BOOL
    user32.EnumChildWindows.argtypes = [wintypes.HWND, enum_proc_type, wintypes.LPARAM]
    user32.EnumChildWindows.restype = wintypes.BOOL
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.GetWindowThreadProcessId.restype = wintypes.DWORD
    user32.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.GetClassNameW.restype = ctypes.c_int
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.IsWindowVisible.restype = wintypes.BOOL
    user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.SetForegroundWindow.argtypes = [wintypes.HWND]
    user32.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    user32.SendMessageW.restype = ctypes.c_ssize_t
    return user32, enum_proc_type


def _class_name(user32, window_handle):
    buffer = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(window_handle, buffer, len(buffer))
    return buffer.value


def _find_main_window(user32, enum_proc_type, process_id):
    matches = []

    def callback(window_handle, _):
        window_process_id = wintypes.DWORD()
        user32.GetWindowThreadProcessId(window_handle, ctypes.byref(window_process_id))
        if (
            window_process_id.value == process_id
            and _class_name(user32, window_handle) == "Notepad++"
            and user32.IsWindowVisible(window_handle)
        ):
            matches.append(window_handle)
        return True

    user32.EnumWindows(enum_proc_type(callback), 0)
    return matches[0] if matches else None


def _find_scintilla_windows(user32, enum_proc_type, main_window):
    matches = []

    def callback(window_handle, _):
        if _class_name(user32, window_handle) == "Scintilla":
            matches.append(window_handle)
        return True

    user32.EnumChildWindows(main_window, enum_proc_type(callback), 0)
    return matches


def _find_token_offset(sample_content, line_number, token, occurrence):
    lines = sample_content.splitlines(keepends=True)
    if line_number < 1 or line_number > len(lines):
        raise ValueError(f"Line {line_number} is outside the sample file")
    line = lines[line_number - 1].rstrip("\r\n")
    search_from = 0
    found_index = -1
    for _ in range(occurrence + 1):
        found_index = line.find(token, search_from)
        if found_index < 0:
            raise ValueError(
                f"Could not find occurrence {occurrence} of {token!r} on line {line_number}"
            )
        search_from = found_index + len(token)
    prefix = "".join(lines[: line_number - 1]) + line[:found_index]
    return len(prefix.encode("utf-8"))


def _colourref_to_hex(colourref):
    value = colourref & 0xFFFFFF
    red = value & 0xFF
    green = (value >> 8) & 0xFF
    blue = (value >> 16) & 0xFF
    return f"{red:02X}{green:02X}{blue:02X}"


def _load_theme_styles(theme_path):
    root = ET.parse(theme_path).getroot()
    lexer_styles = {}
    for lexer in root.findall(".//LexerType"):
        lexer_name = lexer.get("name")
        lexer_styles[lexer_name] = {}
        for word_style in lexer.findall("WordsStyle"):
            style_id = word_style.get("styleID")
            lexer_styles[lexer_name][style_id] = {
                "name": word_style.get("name"),
                "fg": word_style.get("fgColor", "").upper(),
                "bg": word_style.get("bgColor", "").upper(),
            }
    return lexer_styles


def _verify_sample(user32, enum_proc_type, executable, settings_dir, sample_path, language, test_cases, lexer_styles):
    process = subprocess.Popen(
        [
            str(executable),
            "-multiInst",
            "-nosession",
            "-noPlugin",
            f"-settingsDir={settings_dir}",
            f"-L{language}",
            str(sample_path),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    main_window = None
    try:
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            main_window = _find_main_window(user32, enum_proc_type, process.pid)
            if main_window:
                break
            if process.poll() is not None:
                raise RuntimeError(
                    f"Notepad++ exited before opening {sample_path.name} "
                    f"(exit code {process.returncode})"
                )
            time.sleep(0.25)
        if not main_window:
            raise TimeoutError(f"Notepad++ window did not appear for {sample_path.name}")

        user32.ShowWindow(main_window, SW_RESTORE)
        user32.SetForegroundWindow(main_window)
        scintilla_windows = _find_scintilla_windows(user32, enum_proc_type, main_window)
        if not scintilla_windows:
            raise RuntimeError(f"No Scintilla control found for {sample_path.name}")

        expected_length = len(sample_path.read_bytes())
        selected_scintilla = None
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            for scintilla_window in scintilla_windows:
                actual_length = user32.SendMessageW(scintilla_window, SCI_GETLENGTH, 0, 0)
                if actual_length == expected_length:
                    selected_scintilla = scintilla_window
                    break
            if selected_scintilla:
                break
            time.sleep(0.25)
        if not selected_scintilla:
            raise TimeoutError(
                f"Scintilla did not load {sample_path.name}; expected {expected_length} UTF-8 bytes"
            )

        user32.SendMessageW(selected_scintilla, SCI_COLOURISE, 0, -1)
        time.sleep(0.5)
        sample_content = sample_path.read_bytes().decode("utf-8")
        results = []
        errors = []
        styles = lexer_styles.get(language, {})

        for line_number, token, occurrence, expected_style_id in test_cases:
            style_id_text = str(expected_style_id)
            style_definition = styles.get(style_id_text)
            if style_definition is None:
                errors.append(
                    f"{language}: styleID {expected_style_id} is absent from BlulocoDark.xml"
                )
                continue

            try:
                position = _find_token_offset(sample_content, line_number, token, occurrence)
            except ValueError as error:
                errors.append(f"{language}: {error}")
                continue

            observed_style_ids = [
                user32.SendMessageW(selected_scintilla, SCI_GETSTYLEAT, position + offset, 0)
                for offset in range(len(token))
            ]
            actual_style_ids = sorted(set(observed_style_ids))
            actual_foreground = _colourref_to_hex(
                user32.SendMessageW(selected_scintilla, SCI_STYLEGETFORE, expected_style_id, 0)
            )
            actual_background = _colourref_to_hex(
                user32.SendMessageW(selected_scintilla, SCI_STYLEGETBACK, expected_style_id, 0)
            )
            results.append({
                "language": language,
                "file": sample_path.name,
                "line": line_number,
                "token": token,
                "expected_style_id": expected_style_id,
                "actual_style_ids": actual_style_ids,
                "expected_foreground": style_definition["fg"],
                "actual_foreground": actual_foreground,
                "expected_background": style_definition["bg"],
                "actual_background": actual_background,
            })

            if actual_style_ids != [expected_style_id]:
                errors.append(
                    f"{sample_path.name}:{line_number}: {token!r} expected styleID "
                    f"{expected_style_id}, received {actual_style_ids}"
                )
            if actual_foreground != style_definition["fg"]:
                errors.append(
                    f"{sample_path.name}:{line_number}: styleID {expected_style_id} "
                    f"foreground expected #{style_definition['fg']}, received #{actual_foreground}"
                )
            if actual_background != style_definition["bg"]:
                errors.append(
                    f"{sample_path.name}:{line_number}: styleID {expected_style_id} "
                    f"background expected #{style_definition['bg']}, received #{actual_background}"
                )
        return results, errors
    finally:
        if main_window:
            user32.SendMessageW(main_window, WM_CLOSE, 0, 0)
        try:
            process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--notepadpp", required=True)
    parser.add_argument("--theme", default="BlulocoDark.xml")
    parser.add_argument("--settings-dir", required=True)
    parser.add_argument("--samples", default="samples")
    parser.add_argument("--output", default="artifacts/notepadpp-native-validation.json")
    arguments = parser.parse_args()

    if os.name != "nt":
        print("This validator must run on Windows.", file=sys.stderr)
        return 2

    executable = Path(arguments.notepadpp).resolve()
    theme_path = Path(arguments.theme).resolve()
    samples_dir = Path(arguments.samples).resolve()
    settings_dir = Path(arguments.settings_dir).resolve()
    if not executable.is_file():
        raise FileNotFoundError(executable)
    if not theme_path.is_file():
        raise FileNotFoundError(theme_path)

    file_version = subprocess.check_output(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"(Get-Item -LiteralPath '{executable}').VersionInfo.FileVersion",
        ],
        text=True,
    ).strip()
    if not file_version.startswith("8.9.9"):
        raise RuntimeError(f"Expected Notepad++ 8.9.9, found file version {file_version!r}")

    lexer_styles = _load_theme_styles(theme_path)
    grouped_cases = {}
    for language, filename, line, token, occurrence, style_id in TEST_CASES:
        grouped_cases.setdefault((language, filename), []).append(
            (line, token, occurrence, style_id)
        )

    user32, enum_proc_type = _windows_api()
    all_results = []
    all_errors = []
    for (language, filename), cases in grouped_cases.items():
        results, errors = _verify_sample(
            user32,
            enum_proc_type,
            executable,
            settings_dir,
            samples_dir / filename,
            language,
            cases,
            lexer_styles,
        )
        all_results.extend(results)
        all_errors.extend(errors)
        print(f"{filename}: {len(results)} native token checks, {len(errors)} errors")

    report = {
        "notepadpp_version": file_version,
        "theme": str(theme_path),
        "sample_checks": len(all_results),
        "errors": all_errors,
        "results": all_results,
    }
    output_path = Path(arguments.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Native Notepad++ token checks: {len(all_results)}")
    print(f"Errors: {len(all_errors)}")
    for error in all_errors:
        print(f"[ERROR] {error}")
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Generate LexerType blocks for the 17 unthemed lexers and insert into BlulocoDark.xml
"""
import xml.etree.ElementTree as ET
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
THEME_PATH = REPO_ROOT / "BlulocoDark.xml"
MODEL_PATH = REPO_ROOT / "tools" / "npp_lexer_model.json"

# Canonical palette
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
    "decorator": "50ACAE",
    "namespace": "FF839B",
}

# Lexer-specific description and extension mapping
LEXER_META = {
    "avs": ("AVS", "avs"),
    "baanc": ("BaanC", "bsc"),
    "blitzbasic": ("BlitzBasic", "bb"),
    "csound": ("Csound", "csd"),
    "escript": ("Escript", "es"),
    "escseq": ("Escape Sequences", "esc"),
    "fcST": ("ST", "st"),
    "gui4cli": ("Gui4Cli", "gc"),
    "hollywood": ("Hollywood", "hwa"),
    "ihex": ("Intel HEX", "hex"),
    "mmixal": ("MMIXAL", "mms"),
    "nncrontab": ("nnCron tab", "tab"),
    "oscript": ("OneScript", "os"),
    "registry": ("Registry", "reg"),
    "srec": ("S-Record", "srec"),
    "tehex": ("TE Hex", "hex"),
    "txt2tags": ("Txt2tags", "t2t"),
}

# Style name -> palette role mapping (with lexer-specific overrides)
STYLE_COLOR_MAP = {
    # Common patterns
    "DEFAULT": "fg",
    "WHITE SPACE": "fg",
    "DEFAULT STYLE": "fg",
    "DEFAULT TEXT STYLE": "fg",
    "DEFAULT on DEFAULT": "fg",
    "DIVSION OF LEADING WHITESPACE IN LINE": "fg",
    "WHITESPACE": "fg",
    "ANY OTHER TEXT": "fg",

    "COMMENT": "comments",
    "COMMENT LINE": "comments",
    "COMMENT BLOCK": "comments",
    "COMMENT DOC": "comments",
    "COMMENT LINE DOC": "comments",
    "COMMENT: /* */": "comments",
    "COMMENT: [* *]": "comments",
    "LINE COMMENT: #": "comments",
    "SINGLE-LINE COMMENT": "comments",
    "MULTI-LINE COMMENT": "comments",
    "#IFDEF DOC AND #ENDIF": "comments",
    "COMMENT OTHERWISE": "comments",
    "DOC COMMENT": "comments",
    "COMMENT LINE": "comments",
    "COMMENT BLOCK": "comments",
    "POD": "comments",

    "NUMBER": "numbers",
    "HEX NUMBER": "numbers",
    "HEXNUMBER": "numbers",
    "BINNUMBER": "numbers",
    "HEXADECIMAL NUMBER": "numbers",
    "OCTAL NUMBER": "numbers",
    "INTEGER": "numbers",
    "FLOAT": "numbers",

    "STRING": "strings",
    "DOUBLE STRING": "strings",
    "SINGLE STRING": "strings",
    "DOUBLE QUOTED STRING": "strings",
    "SINGLE QUOTED STRING": "strings",
    "STRING SINGLE QUOTES": "strings",
    "STRING DOUBLE QUOTES": "strings",
    "STRING WITH THREE DOUBLE QUOTES": "strings",
    "STRING BLOCK": "strings",
    "STRING VARIABLE": "strings",
    "SIMPLE STRING": "strings",
    "COMPLEX VARIABLE": "strings",
    "STRING EOL": "strings",
    "STRING EOL NC": "strings",
    "HEREDOC": "strings",
    "HEREDOC Q": "strings",
    "HEREDOC QQ": "strings",
    "TEMPLATE LIT": "strings",
    "TEMPLATE LIT. (CLIENT)": "strings",
    "TEMPLATE LIT. (SERVER)": "strings",
    "VERBATIM": "strings",
    "VERBATIM SEGMENT": "strings",
    "RAW STRING": "strings",
    "REGEX": "strings",
    "BACKTICKS": "strings",
    "TEMPLATE": "strings",

    "KEYWORD": "keywords",
    "KEYWORD1": "keywords",
    "KEYWORD2": "classes",
    "KEYWORD3": "decorator",
    "KEYWORD4": "namespace",
    "KEYWORD5": "props",
    "KEYWORD6": "constants",
    "KEYWORD7": "params",
    "KEYWORDS": "keywords",
    "KEYWORDS2": "decorator",
    "KEYWORDS3": "namespace",
    "KEYWORDS 1": "keywords",
    "KEYWORDS 2": "classes",
    "KEYWORDS 3": "decorator",
    "KEYWORDS 4": "namespace",
    "KEYWORDS 5": "props",
    "KEYWORDS 6": "constants",
    "KEYWORDS 7": "params",
    "INSTRUCTION WORD": "keywords",
    "INSTRUCTION": "keywords",
    "RESERVED WORD": "keywords",
    "LANGUAGE NATIVE KEYWORD OR RESERVED WORD": "keywords",
    "COMMAND": "keywords",
    "STATEMENT": "keywords",
    "DECLARATION": "classes",
    "TYPE WORD": "classes",
    "TYPE": "classes",
    "TYPEDEF": "classes",
    "DATA TYPE": "classes",
    "BUILIN FUNC & TYPE": "classes",
    "CORE API": "functions",
    "PLUGIN API": "functions",
    "PLUGIN METHOD": "functions",
    "BUILT-IN FUNCTIONS": "functions",
    "FUNCS AND METHODS 1": "functions",
    "FUNCS AND METHODS 2": "functions",
    "FUNCTION": "functions",
    "FUNCTIONS": "functions",
    "FUNCTIONS ABRIDGED": "functions",
    "FUNC NAME": "functions",
    "DEF NAME": "functions",
    "FUNC1": "functions",
    "FUNC2": "functions",
    "FUNC3": "functions",
    "FUNCTION BLOCK": "functions",
    "METHOD": "functions",
    "CMDLET": "functions",
    "ALIAS": "functions",
    "OPCODE": "functions",
    "VALID OPCODE": "functions",
    "INSTR": "functions",
    "DIRECTIVE": "keywords",
    "PREPROCESSOR": "keywords",
    "PREPROCESSOR DIRECTIVE": "keywords",
    "PREPROC": "keywords",
    "PREPROCESSOR COMMENT": "comments",
    "PREPROCESSOR COMMENT DOC": "comments",
    "PREPROC DEFINITIONS": "keywords",
    "PRAGMA": "keywords",
    "PRAGMA KEYWORD": "keywords",
    "MACRO": "decorator",
    "MACRODEF": "decorator",
    "MACRO QUOTED": "decorator",
    "MACRO FUNCTION": "decorator",
    "DEFWORDS": "decorator",
    "PREWORD1": "decorator",
    "PREWORD2": "decorator",

    "OPERATOR": "operators",
    "OPERATORS": "operators",
    "OPERATORS (DELIMITERS)": "operators",
    "OPERATOR; EITHER SYMBOLIC OR LITERAL": "operators",
    "OPERATOR2": "operators",
    "OPERATORS2": "operators",
    "INFIX": "operators",
    "INFIXEOL": "operators",
    "SYMBOLS": "operators",
    "SYMBOL": "operators",
    "SPECIAL": "operators",
    "OPERATORS": "operators",
    "BRACES": "operators",
    "PAREN ARRAY": "operators",
    "PAREN DICT": "operators",
    "PAREN PROC": "operators",
    "ASTERISK": "operators",
    "MODIFICATORS": "operators",
    "SECTION KEYWORDS": "keywords",
    "TASK START/END": "keywords",

    "IDENTIFIER": "fg",
    "IDENTIFIERS": "fg",
    "IDENTIFIER (PREFIXED BY $)": "params",
    "SERVER-GLOBAL VARIABLE (PREFIXED BY $)": "params",
    "VARIABLE": "params",
    "VARIABLES": "params",
    "A-RATE VARIABLE": "params",
    "K-RATE VARIABLE": "params",
    "I-RATE VARIABLE": "params",
    "GLOBAL VARIABLE": "params",
    "PREDEFINED VARIABLE": "params",
    "CONSTANT": "constants",
    "CONSTANT LITERAL": "constants",
    "CONSTANT LITERAL": "constants",
    "ENUM DOMAINS": "constants",
    "PREDEFINED ATTRIBUTES": "props",
    "PREDEFINED CONSTANT": "constants",
    "PREDECLARED IDENTIFIERS": "constants",
    "BUILTINS": "constants",
    "STATIC BUILT-IN OBJECT": "constants",
    "OBJECT PROPERTY": "props",
    "OBJECT METHOD": "functions",
    "OBJECT DEFINITIONS": "classes",
    "CLASS NAME": "classes",
    "CLASS": "classes",
    "MODULE NAME": "namespace",
    "MODULE": "namespace",
    "MODULE ATTRIBUTES": "props",
    "NAMESPACE": "namespace",
    "IMPORT": "namespace",
    "ATTRIBUTE": "attrs",
    "ATTRIBUTE UNKNOWN": "attrs",
    "VALUE NAME": "props",
    "VALUE TYPE": "classes",
    "PROPERTY NAME": "props",
    "MEMBER": "props",
    "FIELD": "props",
    "CLIP PROPERTIES": "props",
    "TAG": "tags",
    "TAG END": "tags",
    "TAG UNKNOWN": "tags",
    "TAG OPENING": "tags",
    "TAG CLOSING": "tags",
    "SGML DEFAULT": "tags",
    "SGML COMMAND": "keywords",
    "SGML 1ST PARAM": "attrs",
    "SGML DOUBLESTRING": "strings",
    "SGML SIMPLESTRING": "strings",
    "SGML BLOCK DEFAULT": "tags",
    "CDATA": "strings",
    "ENTITY": "constants",
    "VALUE": "strings",
    "USER TAGS1": "decorator",
    "USER TAGS2": "decorator",
    "USER TAGS3": "decorator",
    "USER TAGS4": "decorator",
    "USER ATTRIBUTES1": "decorator",
    "USER ATTRIBUTES2": "decorator",
    "USER ATTRIBUTES3": "decorator",
    "USER ATTRIBUTES4": "decorator",
    "USER KEYWORDS": "decorator",
    "USER KEYWORDS 1": "decorator",
    "USER KEYWORDS 2": "decorator",
    "USER KEYWORDS 3": "decorator",
    "USER KEYWORDS 4": "decorator",
    "USER KEYWORDS 5": "decorator",
    "USER KEYWORDS 6": "decorator",
    "USER KEYWORDS 7": "decorator",
    "USER KEYWORDS 8": "decorator",
    "USER DEFINED": "decorator",
    "USER KEYWORD": "decorator",
    "USER WORD": "decorator",
    "DECORATOR": "decorator",
    "DECORATORS": "decorator",
    "ANNOTATION": "decorator",
    "ATTRIBUTE": "decorator",
    "QUALIFIER": "decorator",
    "LABEL": "props",
    "LABEL TO JUMP TO WITH THE GOTO STATEMENT": "props",
    "LINE": "props",
    "ERROR": "errors",
    "SYNTAX ERROR": "errors",
    "ILLEGAL": "errors",
    "UNKNOWN: ERROR": "errors",
    "LEXICAL ERROR": "errors",
    "CHARACTER TOO MANY": "errors",
    "CHARACTER ESCAPE ERROR": "errors",
    "STRING ESCAPE ERROR": "errors",
    "STRING EOL OPEN": "errors",
    "COMMENT DOC KEYWORD ERROR": "errors",
    "COMMENT KEY ERROR": "errors",
    "RECTYPE_UNKNOWN": "errors",
    "BYTECOUNT_WRONG": "errors",
    "CHECKSUM_WRONG": "errors",
    "GARBAGE": "errors",
    "ESCAPED CHARACTERS IN STRINGS": "errors",
    "BAD STRING CHAR": "errors",
    "UNKNOWN OPCODE": "errors",
    "INVALID": "errors",
    "RECSTART": "operators",
    "RECTYPE": "keywords",
    "BYTECOUNT": "numbers",
    "NOADDRESS": "errors",
    "DATAADDRESS": "numbers",
    "STARTADDRESS": "numbers",
    "ADDRESSFIELD_UNKNOWN": "errors",
    "EXTENDEDADDRESS": "numbers",
    "DATA_ODD": "numbers",
    "DATA_EVEN": "numbers",
    "DATA_UNKNOWN": "errors",
    "DATA_EMPTY": "comments",
    "RECCOUNT": "numbers",
    "CHECKSUM": "numbers",
    "GUID IN KEY PATH": "constants",
    "GUID IN STRING": "constants",
    "PARAMETER": "params",
    "PARAMETER (PREFIXED BY $)": "params",
    "PARAMETERS": "params",
    "ARGUMENT": "params",
    "ARGS": "params",
    "VAR IN STRING": "strings",
    "VAR IN REGEX": "strings",
    "VAR IN REGEX SUBSTITUTION": "strings",
    "VAR IN BACKTICKS": "strings",
    "VAR IN HEREDOC": "strings",
    "VAR IN STRING QQ": "strings",
    "VAR IN STRING QX": "strings",
    "VAR IN STRING QR": "strings",
    "FORMAT IDENTIFIER": "props",
    "FORMAT BODY": "strings",
    "DATA SECTION": "comments",
    "POD VERBATIM": "strings",
    "HEREDOC DELIMITER": "operators",
    "HEREDOC SINGLEQUOTE": "strings",
    "HEREDOC DOUBLEQUOTE": "strings",
    "HEREDOC BACKTICK": "strings",
    "TRANSLATION": "strings",
    "REGEX MATCH": "strings",
    "REGEX SUBSTITUTION": "strings",
    "STRING Q": "strings",
    "STRING QQ": "strings",
    "STRING QX": "strings",
    "STRING QR": "strings",
    "STRING QW": "strings",
    "STRING Q_LANG": "strings",
    "STRING VAR": "strings",
    "ADVERB": "decorator",
    "MU": "decorator",
    "POSITIONAL": "params",
    "ASSOCIATIVE": "params",
    "CALLABLE": "functions",
    "GRAMMAR": "classes",
    "CLASS": "classes",
    "INSTANCE VAR": "params",
    "CLASS VAR": "params",
    "GLOBAL": "namespace",
    "SYMBOL": "constants",
    "ATOM": "constants",
    "ATOM QUOTED": "constants",
    "NODE NAME": "namespace",
    "NODE NAME QUOTED": "namespace",
    "RECORD": "classes",
    "RECORD QUOTED": "classes",
    "ENUM": "constants",
    "TYPE": "classes",
    "TYPES": "classes",
    "DESCRIPTORS": "props",
    "ATTRIBUTES": "props",
    "DOMAIN DEFINITIONS": "classes",
    "FUNCTION DEFINITIONS": "functions",
    "TABLE DEFINITIONS": "classes",
    "TABLE SQL": "strings",
    "DLL FUNCTIONS": "functions",
    "MAIN SECTIONS": "keywords",
    "SUB SECTIONS": "keywords",
    "SECTION": "keywords",
    "SECTION GROUP": "keywords",
    "PAGE EX": "keywords",
    "IF DEFINE": "keywords",
    "STRING LEFT QUOTE": "strings",
    "STRING RIGHT QUOTE": "strings",
    "STRING VAR": "strings",
    "HERE STRING": "strings",
    "HERE CHARACTER": "strings",
    "COMMENT STREAM": "comments",
    "COMMENT DOC KEYWORD": "comments",
    "COMMENT LINE": "comments",
    "COMMENT BLOCK": "comments",
    "COMMENT DOC": "comments",
    "COMMENT DOC KEYWORD": "comments",
    "COMMENT DOC KEYWORD ERROR": "errors",
    "COMMENT KEY": "comments",
    "COMMENT KEY ERROR": "errors",
    "COMMENT LINE DOC": "comments",
    "COMMENT BLOCK2": "comments",
    "COMMENT BLOCK3": "comments",
    "COMMENT BLOCK": "comments",
    "COMMENT NESTED": "comments",
    "VERBOSE REGEX": "strings",
    "VERBOSE REGEX COMMENT": "comments",
    "PREDEFINED": "constants",
    "DELIMITER": "operators",
    "CHARACTER": "numbers",
    "CHAR": "numbers",
    "SPECIAL CHAR": "operators",
    "COMMAND OPTIONAL ARGUMENT": "params",
    "SHORT COMMAND": "keywords",
    "VERBATIM SEGMENT": "strings",
    "TAG": "tags",
    "CLASS NAME": "classes",
    "DEF NAME": "functions",
    "FUNC NAME": "functions",
    "MODULE NAME": "namespace",
    "INSTANCE VAR": "params",
    "CLASS VAR": "params",
    "GLOBAL": "namespace",
    "SYMBOL": "constants",
    "BACKTICKS": "strings",
    "DATA SECTION": "comments",
    "STRING Q": "strings",
    "BLOCKQUOTE": "comments",
    "HRULE": "operators",
    "LINK": "tags",
    "CODE": "strings",
    "CODE2": "strings",
    "CODEBLOCK": "strings",
    "OPTION": "keywords",
    "POSTPROC": "keywords",
    "PRECHAR": "operators",
    "ULIST": "operators",
    "OLIST": "operators",
    "STRIKEOUT": "operators",
    "STRONG": "keywords",
    "STRONG 2 (NOT USED)": "keywords",
    "EM1 (ITALIC)": "decorator",
    "EM2 (UNDERLINE)": "decorator",
    "H1": "keywords",
    "H2": "keywords",
    "H3": "keywords",
    "H4": "keywords",
    "H5": "keywords",
    "H6": "keywords",
    "PREPROC": "keywords",
    "SPECIAL": "operators",
    "DIVISION BETWEEN LABEL AND OPCODE": "operators",
    "DIVISION BETWEEN OPCODE AND OPERANDS": "operators",
    "DIVISION OF OPERANDS": "operators",
    "REFERENCE (TO A LABEL)": "props",
    "REGISTER": "props",
    "SYMBOL": "constants",
    "STRING WITH QUOTES": "strings",
    "STRING WITH BRACES": "strings",
    "PAIR ( 800X600 )": "numbers",
    "TUPLE ( 127.0.0.1 )": "numbers",
    "BINARY ( 16#{1A803F59} )": "numbers",
    "MONEY": "numbers",
    "ISSUE { #123-CD-456 }": "props",
    "TAG { <TITLE HEIGHT=100> }": "tags",
    "FILE { %/C/WINNT/SOME.DLL }": "strings",
    "EMAIL { JOE@MAIL.DOM }": "strings",
    "URL { FTP://THERE.DOM }": "tags",
    "DATE { 17-FEB-2004 1/3/99 }": "numbers",
    "TIME { 12:30 11:22:59 01:59:59.123 }": "numbers",
    "WORD": "keywords",
    "WORD2": "keywords",
    "NAME": "props",
    "NAME": "props",
    "SCALAR": "params",
    "ARRAY": "props",
    "HASH": "props",
    "SYMBOL TABLE": "namespace",
    "PROTOTYPE": "functions",
    "FORMAT IDENTIFIER": "props",
    "FORMAT BODY": "strings",
    "DATA SECTION": "comments",
    "POD": "comments",
    "POD VERBATIM": "strings",
    "COMMENT LINE": "comments",
    "LINE COMMENT": "comments",
    "BLOCK COMMENT": "comments",
    "ML COMMENT": "comments",
    "BLOCK DOC COMMENT": "comments",
    "LINE DOC COMMENT": "comments",
    "BLOCK COMMENT": "comments",
    "COMMENT EMBED": "comments",
    "COMMENT EMBED": "comments",
    "LINE COMMENT": "comments",
    "COMMENT": "comments",
    "COMMENT LINE": "comments",
    "COMMENT BLOCK": "comments",
    "COMMENT DOC": "comments",
    "COMMENT DOC KEYWORD": "comments",
    "COMMENT DOC KEYWORD ERROR": "errors",
    "COMMENT KEY": "comments",
    "COMMENT KEY ERROR": "errors",
    "COMMENT LINE DOC": "comments",
    "COMMENT BLOCK2": "comments",
    "COMMENT BLOCK3": "comments",
    "COMMENT NESTED": "comments",
    "VERBOSE REGEX": "strings",
    "VERBOSE REGEX COMMENT": "comments",
    "PREDEFINED": "constants",
    "DELIMITER": "operators",
    "CHARACTER": "numbers",
    "CHAR": "numbers",
    "SPECIAL CHAR": "operators",
    "COMMAND OPTIONAL ARGUMENT": "params",
    "SHORT COMMAND": "keywords",
    "VERBATIM SEGMENT": "strings",
    "TAG": "tags",
    "CLASS NAME": "classes",
    "DEF NAME": "functions",
    "FUNC NAME": "functions",
    "MODULE NAME": "namespace",
    "INSTANCE VAR": "params",
    "CLASS VAR": "params",
    "GLOBAL": "namespace",
    "SYMBOL": "constants",
    "BACKTICKS": "strings",
    "DATA SECTION": "comments",
    "STRING Q": "strings",
    "BLOCKQUOTE": "comments",
    "HRULE": "operators",
    "LINK": "tags",
    "CODE": "strings",
    "CODE2": "strings",
    "CODEBLOCK": "strings",
    "OPTION": "keywords",
    "POSTPROC": "keywords",
    "PRECHAR": "operators",
    "ULIST": "operators",
    "OLIST": "operators",
    "STRIKEOUT": "operators",
    "STRONG": "keywords",
    "STRONG 2 (NOT USED)": "keywords",
    "EM1 (ITALIC)": "decorator",
    "EM2 (UNDERLINE)": "decorator",
    "H1": "keywords",
    "H2": "keywords",
    "H3": "keywords",
    "H4": "keywords",
    "H5": "keywords",
    "H6": "keywords",
    "PREPROC": "keywords",
    "SPECIAL": "operators",
}

# Lexer-specific overrides
LEXER_OVERRIDES = {
    "escseq": {
        # ANSI escape sequences - keep as terminal colors (like errorlist)
        "DEFAULT on DEFAULT": "fg",
        "BLACK on DEFAULT": "errors",
        "RED on DEFAULT": "errors",
        "GREEN on DEFAULT": "functions",
        "YELLOW on DEFAULT": "strings",
        "BLUE on DEFAULT": "keywords",
        "MAGENTA on DEFAULT": "decorator",
        "CYAN on DEFAULT": "operators",
        "WHITE on DEFAULT": "fg",
    },
    "ihex": {
        "RECSTART": "operators",
        "RECTYPE": "keywords",
        "RECTYPE_UNKNOWN": "errors",
        "BYTECOUNT": "numbers",
        "BYTECOUNT_WRONG": "errors",
        "NOADDRESS": "errors",
        "DATAADDRESS": "numbers",
        "STARTADDRESS": "numbers",
        "ADDRESSFIELD_UNKNOWN": "errors",
        "EXTENDEDADDRESS": "numbers",
        "DATA_ODD": "numbers",
        "DATA_EVEN": "numbers",
        "DATA_UNKNOWN": "errors",
        "DATA_EMPTY": "comments",
        "CHECKSUM": "numbers",
        "CHECKSUM_WRONG": "errors",
        "GARBAGE": "errors",
    },
    "srec": {
        "RECSTART": "operators",
        "RECTYPE": "keywords",
        "RECTYPE_UNKNOWN": "errors",
        "BYTECOUNT": "numbers",
        "BYTECOUNT_WRONG": "errors",
        "NOADDRESS": "errors",
        "DATAADDRESS": "numbers",
        "RECCOUNT": "numbers",
        "STARTADDRESS": "numbers",
        "ADDRESSFIELD_UNKNOWN": "errors",
        "DATA_ODD": "numbers",
        "DATA_EVEN": "numbers",
        "DATA_UNKNOWN": "errors",
        "DATA_EMPTY": "comments",
        "CHECKSUM": "numbers",
        "CHECKSUM_WRONG": "errors",
        "GARBAGE": "errors",
    },
    "tehex": {
        "RECSTART": "operators",
        "RECTYPE": "keywords",
        "RECTYPE_UNKNOWN": "errors",
        "BYTECOUNT": "numbers",
        "BYTECOUNT_WRONG": "errors",
        "DATAADDRESS": "numbers",
        "STARTADDRESS": "numbers",
        "ADDRESSFIELD_UNKNOWN": "errors",
        "DATA_ODD": "numbers",
        "DATA_EVEN": "numbers",
        "CHECKSUM": "numbers",
        "CHECKSUM_WRONG": "errors",
        "GARBAGE": "errors",
    },
    "registry": {
        "DEFAULT STYLE": "fg",
        "DEFAULT": "fg",
        "COMMENT": "comments",
        "VALUE NAME": "props",
        "STRING": "strings",
        "HEX DIGIT": "numbers",
        "VALUE TYPE": "classes",
        "ADDED KEY": "functions",
        "REMOVED KEY": "errors",
        "ESCAPED CHARACTERS IN STRINGS": "errors",
        "GUID IN KEY PATH": "constants",
        "GUID IN STRING": "constants",
        "PARAMETER": "params",
        "OPERATORS": "operators",
    },
}


def get_color_for_style(lexer_name: str, style_name: str) -> str:
    """Get the palette color for a given style."""
    # Check lexer-specific overrides first
    if lexer_name in LEXER_OVERRIDES and style_name in LEXER_OVERRIDES[lexer_name]:
        return PALETTE[LEXER_OVERRIDES[lexer_name][style_name]]

    # Check common map
    if style_name in STYLE_COLOR_MAP:
        return PALETTE[STYLE_COLOR_MAP[style_name]]

    # Fallback: try partial matches
    style_lower = style_name.upper()
    if "COMMENT" in style_lower:
        return PALETTE["comments"]
    if "NUMBER" in style_lower or "HEX" in style_lower or "BIN" in style_lower or "OCT" in style_lower:
        return PALETTE["numbers"]
    if "STRING" in style_lower or "QUOTE" in style_lower or "HEREDOC" in style_lower or "TEMPLATE" in style_lower or "REGEX" in style_lower or "BACKTICK" in style_lower:
        return PALETTE["strings"]
    if "KEYWORD" in style_lower or "INSTRUCTION" in style_lower or "COMMAND" in style_lower or "STATEMENT" in style_lower or "DECLARATION" in style_lower or "RESERVED" in style_lower:
        return PALETTE["keywords"]
    if "TYPE" in style_lower or "CLASS" in style_lower or "STRUCT" in style_lower or "ENUM" in style_lower or "INTERFACE" in style_lower:
        return PALETTE["classes"]
    if "FUNCTION" in style_lower or "METHOD" in style_lower or "FUNC" in style_lower or "DEF" in style_lower or "CMDLET" in style_lower or "ALIAS" in style_lower or "OPCODE" in style_lower:
        return PALETTE["functions"]
    if "OPERATOR" in style_lower or "SYMBOL" in style_lower or "DELIMITER" in style_lower or "BRACE" in style_lower or "PAREN" in style_lower:
        return PALETTE["operators"]
    if "IDENTIFIER" in style_lower or "VARIABLE" in style_lower or "CONSTANT" in style_lower or "PARAMETER" in style_lower or "ARGUMENT" in style_lower or "ATTRIBUTE" in style_lower or "PROPERTY" in style_lower or "FIELD" in style_lower or "MEMBER" in style_lower:
        return PALETTE["params"]
    if "ERROR" in style_lower or "ILLEGAL" in style_lower or "UNKNOWN" in style_lower or "INVALID" in style_lower or "WRONG" in style_lower or "BAD" in style_lower or "ESCAPE" in style_lower:
        return PALETTE["errors"]
    if "PREPROCESSOR" in style_lower or "PRAGMA" in style_lower or "MACRO" in style_lower or "DIRECTIVE" in style_lower:
        return PALETTE["keywords"]
    if "USER" in style_lower or "DECORATOR" in style_lower or "ANNOTATION" in style_lower:
        return PALETTE["decorator"]
    if "TAG" in style_lower or "SGML" in style_lower or "XML" in style_lower or "HTML" in style_lower or "ENTITY" in style_lower or "CDATA" in style_lower:
        return PALETTE["tags"]
    if "LABEL" in style_lower or "LINE" in style_lower or "GOTO" in style_lower:
        return PALETTE["props"]
    if "NAMESPACE" in style_lower or "MODULE" in style_lower or "IMPORT" in style_lower or "PACKAGE" in style_lower:
        return PALETTE["namespace"]

    # Default fallback
    return PALETTE["fg"]


def generate_lexer_block(lexer_name: str, styles: list, desc: str, ext: str) -> ET.Element:
    """Generate a LexerType element for a lexer."""
    lexer_elem = ET.Element("LexerType")
    lexer_elem.set("name", lexer_name)
    lexer_elem.set("desc", desc)
    lexer_elem.set("ext", ext)

    for style_id, style_name in styles:
        ws = ET.SubElement(lexer_elem, "WordsStyle")
        ws.set("name", style_name)
        ws.set("styleID", str(style_id))

        fg_color = get_color_for_style(lexer_name, style_name)
        ws.set("fgColor", fg_color)
        ws.set("bgColor", PALETTE["bg"])
        ws.set("fontName", "")
        ws.set("fontStyle", "0")
        ws.set("fontSize", "")

        # Add keywordClass for known keyword styles
        if "KEYWORD" in style_name.upper() and "USER" not in style_name.upper():
            if "1" in style_name and "KEYWORD" in style_name:
                ws.set("keywordClass", "instre1")
            elif "2" in style_name and "KEYWORD" in style_name:
                ws.set("keywordClass", "instre2")
            elif "TYPE" in style_name.upper() or "DATA TYPE" in style_name.upper():
                ws.set("keywordClass", "type1")

    return lexer_elem


def main():
    # Load model
    with open(MODEL_PATH, "r", encoding="utf-8") as f:
        model = json.load(f)

    # Parse theme
    tree = ET.parse(THEME_PATH)
    root = tree.getroot()
    lexer_styles = root.find(".//LexerStyles")

    # Get unthemed lexers
    themed = {lt.get("name") for lt in lexer_styles.findall("LexerType")}
    unthemed = [name for name in model.keys() if name not in themed]

    print(f"Adding {len(unthemed)} missing lexers...")

    # Generate and insert each lexer (in alphabetical order, before </LexerStyles>)
    for lexer_name in sorted(unthemed):
        if lexer_name not in model:
            print(f"  WARNING: {lexer_name} not in model, skipping")
            continue

        styles = model[lexer_name]
        parsed_styles = []
        for s in styles:
            if isinstance(s, list) and len(s) >= 2:
                parsed_styles.append((str(s[0]), s[1]))

        desc, ext = LEXER_META.get(lexer_name, (lexer_name.capitalize(), lexer_name))
        lexer_elem = generate_lexer_block(lexer_name, parsed_styles, desc, ext)

        # Insert before GlobalStyles (which is after LexerStyles end)
        lexer_styles.append(lexer_elem)
        print(f"  Added: {lexer_name} ({len(parsed_styles)} styles)")

    # Write back with formatting
    ET.indent(tree, space="    ")
    tree.write(THEME_PATH, encoding="utf-8", xml_declaration=True)
    print(f"\nTheme written to {THEME_PATH}")


if __name__ == "__main__":
    main()
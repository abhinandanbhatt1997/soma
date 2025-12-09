# soma/lexer.py

import re

TOKEN_SPEC = [
    ("COMMENT", r"#.*"),
    ("STRING", r'"(?:[^"\\]|\\.)*"'),  # String literals
    ("NUMBER", r"\d+"),
    ("IDENT",  r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("LAMBDA", r"\\"),
    ("ARROW",  r"->"),
    ("EQUAL",  r"="),
    ("PLUS",   r"\+"),
    ("MINUS",  r"-"),
    ("MUL",    r"\*"),
    ("DIV",    r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("COMMA",  r","),
    ("NEWLINE",r"\n"),
    ("SKIP",   r"[ \t]+"),
    ("MISMATCH", r"."),
]

MASTER = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))

def tokenize(code):
    tokens = []
    KEYWORDS = {"if": "IF", "then": "THEN", "else": "ELSE"}

    for m in MASTER.finditer(code):
        kind = m.lastgroup
        value = m.group()

        if kind == "NUMBER":
            tokens.append(("NUMBER", int(value)))
        elif kind == "STRING":
            # Strip quotes and handle simple escapes
            unquoted = value[1:-1]
            unquoted = unquoted.replace('\\"', '"')
            tokens.append(("STRING", unquoted))
        elif kind == "IDENT":
            token_type = KEYWORDS.get(value, "IDENT")
            tokens.append((token_type, value))
        elif kind == "SKIP":
            continue
        elif kind == "NEWLINE":
            tokens.append(("NEWLINE", None))
        elif kind == "COMMENT":
            continue
        elif kind == "MISMATCH":
            raise SyntaxError(f"Illegal char {value}")
        else:
            tokens.append((kind, value))

    tokens.append(("EOF", None))
    return tokens

import re

class Lexer:
    def __init__(self, source):
        self.source = source

    def tokenize(self):
        TOKEN_SPEC = [
            ("NUMBER",   r"\d+"),
            ("LET",      r"let\b"),
            ("IF",       r"if\b"),
            ("ELSE",     r"else\b"),
            ("WHILE",    r"while\b"),
            ("FN",       r"fn\b"),
            ("EQEQ",     r"=="),
            ("NOTEQ",    r"!="),
            ("GT",       r">"),
            ("LT",       r"<"),
            ("IDENT",    r"[a-zA-Z_]\w*"),
            ("PLUS",     r"\+"),
            ("MINUS",    r"-"),
            ("STAR",     r"\*"),
            ("SLASH",    r"/"),
            ("EQUAL",    r"="),
            ("LPAREN",   r"\("),
            ("RPAREN",   r"\)"),
            ("LBRACE",   r"\{"),
            ("RBRACE",   r"\}"),
            ("COMMA",    r","),
            ("NEWLINE",  r"\n"),
            ("SKIP",     r"[ \t]+"),
            ("MISMATCH", r"."),
        ]

        tokens = []
        regex = "|".join(f"(?P<{n}>{p})" for n, p in TOKEN_SPEC)

        for m in re.finditer(regex, self.source):
            kind = m.lastgroup
            value = m.group()
            if kind == "NUMBER":
                tokens.append(("NUMBER", int(value)))
            elif kind in {
                "LET","IF","ELSE","WHILE","FN","IDENT",
                "PLUS","MINUS","STAR","SLASH",
                "EQUAL","EQEQ","NOTEQ","GT","LT",
                "LPAREN","RPAREN","LBRACE","RBRACE","COMMA"
            }:
                tokens.append((kind, value))
            elif kind in ("NEWLINE", "SKIP"):
                continue
            else:
                raise SyntaxError(f"Illegal character {value}")

        tokens.append(("EOF", None))
        return tokens

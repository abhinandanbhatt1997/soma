class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, kind):
        tok = self.peek()
        if tok[0] != kind:
            raise SyntaxError(f"Expected {kind}, got {tok}")
        return self.advance()

    def parse(self):
        stmts = []
        while self.peek()[0] != "EOF":
            stmts.append(self.statement())
        return stmts

    # ---------- statements ----------

    def statement(self):
        tok = self.peek()[0]

        if tok == "LET":
            return self.let_stmt()
        if tok == "IF":
            return self.if_stmt()
        if tok == "WHILE":
            return self.while_stmt()
        if tok == "FN":
            return self.fn_stmt()

        return ("expr", self.expr())

    def let_stmt(self):
        self.expect("LET")
        name = self.expect("IDENT")[1]
        self.expect("EQUAL")
        value = self.expr()
        return ("let", name, value)

    def if_stmt(self):
        self.expect("IF")
        cond = self.expr()
        then_block = self.block()
        else_block = None
        if self.peek()[0] == "ELSE":
            self.advance()
            else_block = self.block()
        return ("if", cond, then_block, else_block)

    def while_stmt(self):
        self.expect("WHILE")
        cond = self.expr()
        body = self.block()
        return ("while", cond, body)

    def fn_stmt(self):
        self.expect("FN")
        name = self.expect("IDENT")[1]
        self.expect("LPAREN")

        # parse arguments
        args = []
        if self.peek()[0] != "RPAREN":
            while True:
                args.append(self.expect("IDENT")[1])
                if self.peek()[0] == "RPAREN":
                    break
                self.expect("COMMA")
        self.expect("RPAREN")

        body = self.block()
        return ("fn", name, args, body)

    def block(self):
        self.expect("LBRACE")
        stmts = []
        while self.peek()[0] != "RBRACE":
            stmts.append(self.statement())
        self.expect("RBRACE")
        return stmts

    # ---------- expressions ----------

    def expr(self):
        return self.compare()

    def compare(self):
        node = self.add()
        while self.peek()[0] in ("GT", "LT", "EQEQ", "NOTEQ"):
            op = self.advance()[0]
            right = self.add()
            node = (op, node, right)
        return node

    def add(self):
        node = self.term()
        while self.peek()[0] in ("PLUS", "MINUS"):
            op = self.advance()[0]
            right = self.term()
            node = (op, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.peek()[0] in ("STAR", "SLASH"):
            op = self.advance()[0]
            right = self.factor()
            node = (op, node, right)
        return node

    def factor(self):
        tok = self.peek()

        if tok[0] == "NUMBER":
            return ("number", self.advance()[1])

        if tok[0] == "IDENT":
            name = self.advance()[1]
            # check for function call
            if self.peek()[0] == "LPAREN":
                self.advance()
                args = []
                if self.peek()[0] != "RPAREN":
                    while True:
                        args.append(self.expr())
                        if self.peek()[0] == "RPAREN":
                            break
                        self.expect("COMMA")
                self.expect("RPAREN")
                return ("call", name, args)
            return ("var", name)

        if tok[0] == "LPAREN":
            self.advance()
            node = self.expr()
            self.expect("RPAREN")
            return node

        raise SyntaxError(f"Unexpected token {tok}")

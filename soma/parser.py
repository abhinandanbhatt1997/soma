from soma.lexer import tokenize

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', None)

    def eat(self, kind):
        tok = self.peek()
        if tok[0] != kind:
            raise SyntaxError(f"Expected {kind}, got {tok}")
        self.pos += 1
        return tok

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            tok_type, tok_val = self.tokens[self.pos]
            if tok_type == "NEWLINE":
                self.pos += 1
                continue
            if tok_type == "EOF":
                break
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.peek()[0] == 'IDENT' and self._lookahead_kind(1) == 'EQUAL':
            name = self.eat('IDENT')[1]
            self.eat('EQUAL')
            value = self.expr()
            return ("assign", name, value)
        return ("expr", self.expr())

    def _lookahead_kind(self, n):
        if self.pos + n < len(self.tokens):
            return self.tokens[self.pos + n][0]
        return 'EOF'

    def expr(self):
        return self.if_expr()

    def if_expr(self):
        if self.peek()[0] == 'IF':
            self.eat('IF')
            cond = self.expr()
            self.eat('THEN')
            then_branch = self.expr()
            self.eat('ELSE')
            else_branch = self.expr()
            return ("if", cond, then_branch, else_branch)
        return self.lambda_expr()

    def lambda_expr(self):
        if self.peek()[0] == 'LAMBDA':
            self.eat('LAMBDA')
            arg = self.eat('IDENT')[1]
            self.eat('ARROW')
            body = self.expr()
            return ("lambda", arg, body)
        return self.add()

    def add(self):
        node = self.term()
        while self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.eat(self.peek()[0])[0]
            node2 = self.term()
            node = ("bin", op, node, node2)
        return node

    def term(self):
        node = self.factor()
        while self.peek()[0] in ('MUL', 'DIV'):
            op = self.eat(self.peek()[0])[0]
            node2 = self.factor()
            node = ("bin", op, node, node2)
        return node

    def factor(self):
        node = self.primary()

        while self.peek()[0] == 'LPAREN':
            self.eat('LPAREN')
            args = []
            if self.peek()[0] != 'RPAREN':
                args.append(self.expr())
                while self.peek()[0] == 'COMMA':
                    self.eat('COMMA')
                    args.append(self.expr())
            self.eat('RPAREN')
            node = ("call", node, args)

        return node

    def primary(self):
        tok = self.peek()

        if tok[0] == 'NUMBER':
            return self.eat('NUMBER')[1]
        if tok[0] == 'STRING':
            return self.eat('STRING')[1]
        if tok[0] == 'IDENT':
            return ("var", self.eat('IDENT')[1])
        if tok[0] == 'LPAREN':
            self.eat('LPAREN')
            expr = self.expr()
            self.eat('RPAREN')
            return expr
        if tok[0] == 'LAMBDA':
            return self.lambda_expr()
        if tok[0] == 'IF':
            return self.if_expr()
        if tok[0] == 'EOF':
            raise SyntaxError(f"Unexpected end of input at pos {self.pos}")
        raise SyntaxError(f"Unexpected token {tok} at pos {self.pos}")

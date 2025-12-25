class Interpreter:
    def __init__(self):
        self.env_stack = [{}]
        self.functions = {}

    def env(self):
        return self.env_stack[-1]

    def push(self):
        self.env_stack.append({})

    def pop(self):
        self.env_stack.pop()

    def run(self, ast):
        result = None
        for stmt in ast:
            result = self.exec_stmt(stmt)
        if result is not None:
            print(result)

    # ---------- STATEMENTS ----------
    def exec_stmt(self, stmt):
        kind = stmt[0]

        # let x = expr
        if kind == "let":
            _, name, expr = stmt
            value = self.eval(expr)

            # assign to nearest existing variable
            for env in reversed(self.env_stack):
                if name in env:
                    env[name] = value
                    return value

            self.env()[name] = value
            return value

        # expression
        if kind == "expr":
            return self.eval(stmt[1])

        # if
        if kind == "if":
            _, cond, then_body, else_body = stmt
            if self.eval(cond):
                self.push()
                result = None
                for s in then_body:
                    result = self.exec_stmt(s)
                self.pop()
                return result
            else:
                self.push()
                result = None
                for s in else_body:
                    result = self.exec_stmt(s)
                self.pop()
                return result

        # while (NO new scope)
        if kind == "while":
            _, cond, body = stmt
            result = None
            while self.eval(cond):
                for s in body:
                    result = self.exec_stmt(s)
            return result

        # function definition
        if kind == "fn":
            _, name, args, body = stmt
            self.functions[name] = (args, body)
            return None

        raise RuntimeError(f"Unknown statement {stmt}")

    # ---------- EXPRESSIONS ----------
    def eval(self, node):
        kind = node[0]

        if kind == "number":
            return node[1]

        if kind == "var":
            name = node[1]
            for env in reversed(self.env_stack):
                if name in env:
                    return env[name]
            raise NameError(f"Undefined variable '{name}'")

        if kind == "call":
            _, name, call_args = node
            if name not in self.functions:
                raise NameError(f"Undefined function '{name}'")

            params, body = self.functions[name]
            if len(params) != len(call_args):
                raise TypeError("Argument count mismatch")

            values = [self.eval(a) for a in call_args]

            self.push()
            for p, v in zip(params, values):
                self.env()[p] = v

            result = None
            for stmt in body:
                result = self.exec_stmt(stmt)

            self.pop()
            return result

        left = self.eval(node[1])
        right = self.eval(node[2])

        if kind == "SLASH":
            if right == 0:
                raise ZeroDivisionError("Division by zero in Soma")
            return left // right

        return {
            "PLUS": left + right,
            "MINUS": left - right,
            "STAR": left * right,
            "GT": left > right,
            "LT": left < right,
            "EQEQ": left == right,
            "NOTEQ": left != right,
        }[kind]

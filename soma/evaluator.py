# soma/evaluator.py

class Environment:
    """
    Lexical scoped environment with parent chaining.
    """
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise NameError(f"Undefined variable: '{name}'")

    def set(self, name, value):
        self.vars[name] = value


class Evaluator:
    def __init__(self):
        self.builtins = {
            "print": self._builtin_print,
        }
        self.global_env = Environment()
        for name, fn in self.builtins.items():
            self.global_env.set(name, fn)

    def _builtin_print(self, *args):
        print(*args)
        return None

    def eval(self, ast):
        result = None
        for stmt in ast:
            result = self.eval_stmt(stmt, self.global_env)
        return result

    def eval_stmt(self, stmt, env):
        tag = stmt[0]

        if tag == "assign":
            _, name, expr = stmt
            value = self.eval_expr(expr, env)
            env.set(name, value)
            return None

        elif tag == "expr":
            return self.eval_expr(stmt[1], env)

        else:
            raise RuntimeError(f"Unknown statement: {tag}")

    def eval_expr(self, expr, env):
        # literals
        if isinstance(expr, (int, float, str)):
            return expr

        # variable lookup
        if isinstance(expr, str):
            try:
                return env.get(expr)
            except NameError:
                pass
            if expr in self.builtins:
                return self.builtins[expr]
            raise NameError(f"Undefined variable: {expr}")

        if not isinstance(expr, tuple):
            raise RuntimeError(f"Invalid expression: {expr}")

        tag = expr[0]

        if tag == "var":
            name = expr[1]
            try:
                return env.get(name)
            except NameError:
                pass
            if name in self.builtins:
                return self.builtins[name]
            raise NameError(f"Undefined variable: {name}")

        elif tag == "bin":
            _, op, left, right = expr
            l = self.eval_expr(left, env)
            r = self.eval_expr(right, env)
            if op == "PLUS": return l + r
            if op == "MINUS": return l - r
            if op == "MUL": return l * r
            if op == "DIV": return l / r
            raise ValueError(f"Unknown operator: {op}")

        elif tag == "call":
            _, func_node, args = expr
            func = self.eval_expr(func_node, env)
            if not callable(func):
                raise TypeError(f"Object '{func}' is not callable")
            arg_vals = [self.eval_expr(a, env) for a in args]
            return func(*arg_vals)

        elif tag == "if":
            _, cond, then_b, else_b = expr
            if self.eval_expr(cond, env):
                return self.eval_expr(then_b, env)
            return self.eval_expr(else_b, env)

        elif tag == "lambda":
            _, arg_name, body = expr

            def closure(arg_val):
                local = Environment(parent=env)
                local.set(arg_name, arg_val)
                return self.eval_expr(body, local)

            return closure

        else:
            raise RuntimeError(f"Unknown expr tag: {tag}")

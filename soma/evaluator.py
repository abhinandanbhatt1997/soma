# soma/evaluator.py

class Evaluator:
    def __init__(self):
        self.builtins = {
            "print": self._builtin_print,
        }

    def _builtin_print(self, *args):
        print(*args)
        return None

    def eval(self, ast):
        global_env = dict(self.builtins)
        result = None
        for stmt in ast:
            result = self.eval_stmt(stmt, global_env)
        return result

    def eval_stmt(self, stmt, env):
        tag = stmt[0]
        if tag == "assign":
            _, name, expr = stmt
            value = self.eval_expr(expr, env)
            env[name] = value
            return None  # ← No output for assignments
        elif tag == "expr":
            return self.eval_expr(stmt[1], env)
        else:
            raise RuntimeError(f"Unknown statement: {tag}")

    def eval_expr(self, expr, env):
        # Literals: number, string
        if isinstance(expr, (int, float, str)):
            return expr

        # Variable names (e.g., "print", "x")
        if isinstance(expr, str):
            if expr in env:
                return env[expr]
            if expr in self.builtins:
                return self.builtins[expr]
            raise NameError(f"Undefined variable: {expr}")

        if not isinstance(expr, tuple):
            raise RuntimeError(f"Invalid expression: {expr}")

        tag = expr[0]

        if tag == "var":
            name = expr[1]
            if name in env:
                return env[name]
            if name in self.builtins:
                return self.builtins[name]
            raise NameError(f"Undefined variable: {name}")

        elif tag == "bin":
            _, op, left, right = expr
            lval = self.eval_expr(left, env)
            rval = self.eval_expr(right, env)
            if op == "PLUS": return lval + rval
            if op == "MINUS": return lval - rval
            if op == "MUL": return lval * rval
            if op == "DIV": return lval / rval
            raise ValueError(f"Unknown operator: {op}")

        elif tag == "call":
            _, func_node, args = expr
            func = self.eval_expr(func_node, env)
            if not callable(func):
                raise TypeError(f"Object {func} is not callable")
            arg_vals = [self.eval_expr(arg, env) for arg in args]
            return func(*arg_vals)

        elif tag == "if":
            _, cond, then_branch, else_branch = expr
            cond_val = self.eval_expr(cond, env)
            if cond_val:
                return self.eval_expr(then_branch, env)
            else:
                return self.eval_expr(else_branch, env)

        elif tag == "lambda":
            _, arg_name, body = expr
            def closure(*args):
                if len(args) != 1:
                    raise TypeError(f"Lambda takes exactly 1 argument, got {len(args)}")
                new_env = {arg_name: args[0]}
                full_env = {**env, **new_env}
                return self.eval_expr(body, full_env)
            return closure

        else:
            raise RuntimeError(f"Unknown expression tag: {tag}")

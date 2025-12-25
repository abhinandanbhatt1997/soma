# soma/evaluator.py
class Environment:
    def __init__(self, parent=None):
        self.data = {}
        self.parent = parent

    def get(self, k):
        if k in self.data:
            return self.data[k]
        if self.parent:
            return self.parent.get(k)
        raise NameError(k)

    def set(self, k, v):
        self.data[k] = v

def eval_node(node, env):
    kind = node[0]

    if kind == "program":
        val = None
        for s in node[1]:
            val = eval_node(s, env)
        return val

    if kind == "assign":
        val = eval_node(node[2], env)
        env.set(node[1], val)
        return val

    if kind == "expr":
        return eval_node(node[1], env)

    if kind == "num":
        return node[1]

    if kind == "str":
        return node[1]

    if kind == "var":
        return env.get(node[1])

    if kind == "list":
        return [eval_node(x, env) for x in node[1]]

    if kind == "map":
        return {eval_node(k, env): eval_node(v, env) for k, v in node[1]}

    if kind == "bin":
        a = eval_node(node[2], env)
        b = eval_node(node[3], env)
        return {
            "PLUS": a + b,
            "MINUS": a - b,
            "STAR": a * b,
            "SLASH": a // b,
        }[node[1]]

    if kind == "call":
        if node[1] == "print":
            val = eval_node(node[2], env)
            print(val)
            return val
        raise NameError(node[1])

    if kind == "try":
        try:
            return eval_node(node[1], env)
        except Exception as e:
            new = Environment(env)
            new.set(node[2], str(e))
            return eval_node(node[3], new)

    if kind == "match":
        subj = eval_node(node[1], env)
        for pat, body in node[2]:
            res = match_pattern(pat, subj)
            if res is not None:
                new = Environment(env)
                for k, v in res.items():
                    new.set(k, v)
                return eval_node(body, new)
        raise ValueError("No match")

    raise Exception(f"Unknown node {node}")

def match_pattern(pat, val):
    if pat[0] == "pat_any":
        return {}

    if pat[0] == "pat_lit":
        return {} if pat[1] == val else None

    if pat[0] == "pat_var":
        return {pat[1]: val}

    if pat[0] == "pat_empty":
        return {} if val == [] else None

    if pat[0] == "pat_cons":
        if not val:
            return None
        return {pat[1]: val[0], pat[2]: val[1:]}

    return None

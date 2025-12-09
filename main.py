# main.py
from soma.lexer import tokenize
from soma.parser import Parser
from soma.evaluator import Evaluator

def repl():
    print("Soma REPL — type expressions or 'exit' to quit.")
    print(r"Example: (\x -> x * 2)(5)")
    evaluator = Evaluator()
    
    # Create global environment with built-ins
    from soma.evaluator import Environment
    global_env = Environment()
    for name, func in evaluator.builtins.items():
        global_env.set(name, func)

    while True:
        try:
            line = input("soma> ").strip()
            if line.lower() in ("exit", "quit"):
                break
            if not line:
                continue

            tokens = tokenize(line)
            ast = Parser(tokens).parse()

            if not ast:
                continue

            # Evaluate in persistent global environment
            for stmt in ast:
                result = evaluator.eval_stmt(stmt, global_env)
                if stmt[0] == "expr" and result is not None:
                    print("=>", result)

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            code = f.read()
        tokens = tokenize(code)
        ast = Parser(tokens).parse()
        evaluator = Evaluator()
        evaluator.eval(ast)
    else:
        repl()

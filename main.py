# main.py
from soma.lexer import tokenize
from soma.parser import Parser
from soma.evaluator import Evaluator

def repl():
    print("Soma REPL — type expressions or 'exit' to quit.")
    print(r"Example: (\x -> x * 2)(5)")

    evaluator = Evaluator()
    global_env = evaluator.global_env

    while True:
        try:
            line = input("soma> ").strip()
            if line.lower() in ("exit", "quit"):
                break
            if not line:
                continue

            tokens = tokenize(line)
            ast = Parser(tokens).parse()

            for stmt in ast:
                result = evaluator.eval_stmt(stmt, global_env)
                if stmt[0] == "expr" and result is not None:
                    print("=>", result)

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def run_file(path):
    code = open(path).read()
    tokens = tokenize(code)
    ast = Parser(tokens).parse()
    evaluator = Evaluator()
    evaluator.eval(ast)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()

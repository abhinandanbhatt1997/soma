import sys
from soma.lexer import Lexer
from soma.parser import Parser
from soma.interpreter import Interpreter

def run_file(path):
    with open(path) as f:
        source = f.read()

    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    interp = Interpreter()
    interp.run(ast)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <file.soma>")
        sys.exit(1)

    run_file(sys.argv[1])

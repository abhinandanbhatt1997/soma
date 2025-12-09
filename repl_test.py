#!/usr/bin/env python3
# repl_test.py

import pexpect
import sys
import os

TEST_CASES = [
    # (input, expected_output_substring or None)
    ("2 + 3", "=> 5"),
    ("10 - 4 * 2", "=> 2"),
    ("x = 10", None),
    ("x", "=> 10"),
    ("square = \\x -> x * x", None),
    ("square(5)", "=> 25"),
    ("(\\n -> n + 100)(1)", "=> 101"),
    ('if 1 then print("yes") else print("no")', "yes"),
    ("make_adder = \\a -> \\b -> a + b", None),
    ("add10 = make_adder(10)", None),
    ("add10(5)", "=> 15"),
    ("undefined_var", "Undefined variable"),
]

def run_repl_test():
    print("🧪 Running Soma REPL Tests...\n")
    
    # Start Soma REPL
    child = pexpect.spawn(f"{sys.executable} main.py", timeout=5)
    child.logfile_read = sys.stdout.buffer  # Optional: see output in real-time (remove for clean logs)
    
    # Wait for initial prompt
    try:
        child.expect(r"soma> ", timeout=5)
    except pexpect.TIMEOUT:
        print("❌ Failed to start REPL — no prompt received.")
        return False

    passed = 0
    failed = 0

    for i, (inp, expected) in enumerate(TEST_CASES, 1):
        try:
            # Send input
            child.sendline(inp)
            
            if expected is None:
                # Should return to prompt with no extra output
                child.expect(r"soma> ", timeout=2)
                print(f"✅ Test {i}: PASS (no output for '{inp}')")
                passed += 1
            else:
                # Wait for output + prompt
                child.expect([expected, pexpect.TIMEOUT], timeout=2)
                if child.match:
                    child.expect(r"soma> ", timeout=1)
                    print(f"✅ Test {i}: PASS ('{expected}' found)")
                    passed += 1
                else:
                    print(f"❌ Test {i}: FAIL - expected '{expected}', not found")
                    failed += 1
                    
        except pexpect.exceptions.TIMEOUT:
            print(f"❌ Test {i}: FAIL - timeout on input: {inp}")
            failed += 1
            # Try to recover
            child.sendline("exit")
            break

    # Clean exit
    child.sendline("exit")
    child.close()

    print(f"\n📊 Results: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    if not os.path.exists("main.py"):
        print("❌ Run from Soma root directory!")
        sys.exit(1)
        
    success = run_repl_test()
    sys.exit(0 if success else 1)

#!/usr/bin/env python
import sys
import py_compile

try:
    py_compile.compile(r'd:\shree gopal traders\app.py', doraise=True)
    print("✓ app.py syntax is valid")
    sys.exit(0)
except py_compile.PyCompileError as e:
    print(f"✗ Syntax error in app.py:\n{e}")
    sys.exit(1)

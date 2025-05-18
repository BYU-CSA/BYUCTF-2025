# LLIR
Description:
```markdown
Checker? I hardly know her!

[checker?.ll]
```

**Author**: `overllama`

## Writeup
There are a few ways to solve this. Either you can reverse the LLIR to determine what is happening or use that file to then compile it to C code with `llvm` command line and reverse it from there.

The challenge is one big flag checker with a MASSIVE check statement with all kinds of conditions to determine whether or not your flag is correct. It should be deterministic and solvable pretty simply with z3 👍 (see `solve.py`).

LLVM commands to compile:
```bash
llvm-as checker\?.ll -o tmp.bc
clang tmp.bc -o prog
```

**Flag** - `byuctf{lL1r_not_str41ght_to_4sm_458d}`
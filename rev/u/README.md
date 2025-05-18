# u
Description:
```markdown
u

[u.py]
```

**Author**: `overllama`

## Writeup
Just reverse it, it isn't actually that bad once you start renaming things. Just checks it against precomputed values

This program checks the flag by first generating a list of values (powers of 3 mod 256) exactly the length of the flag, which is also the length of the list of stored values. It takes user input, then checks that `powerofthreelist[i] * input[i] == stored[i]`

**Flag** - `byuctf{uuuuuuu_uuuu_uuu_34845}`
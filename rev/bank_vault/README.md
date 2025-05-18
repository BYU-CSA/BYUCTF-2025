# Bank Vault
Description:
```markdown
This bank is totally secure. No way you can break your way into the vault or recover the password. We have a special key system that is unbreakable.

[bank]
```

**Author**: `overllama`

## Writeup
When reversing the challenge, you'll see an array of boolean values and an array of 32 bit integers (these are stored initially in the data section). The logic of checking the flag against these integers is reversible, and that generates a bool array. When finished, that array is reversed and checked against the original array used. You just need to pass the checks that correlate with the original array to get the flag. This just means whenever you're stepping through the binary and you run into a `1` from the bool array, that comparison actually matters.

**Flag** - `byuctf{3v3n_v3ct0rs_4pp34r_1n_m3m0ry}`
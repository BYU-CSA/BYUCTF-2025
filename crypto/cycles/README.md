# Cycles
Description:
```markdown
I heard through the grapevine that you can't take a discrete log under a large enough, good prime. Well I made sure to pick a good prime, go ahead and try

[main.py] [cycles.txt]
```

**Author**: `overllama`

## Writeup
This challenge only involves knowing fermat's little theorem, which says that the number, given `g` being prime and `p` being prime, any `a` such that `g^a=1%p` must be a multiple of `p-1`. A little experimentation reveals this when poking around with it. `a-1` doesn't work, so you know it needs to be a multiple. The actual multiple is under 50, though I'm unsure which it is. See my solve script for more details. Running the solve takes less than 5 seconds.

See `solve.py`.

**Flag** - `byuctf{1t_4lw4ys_c0m3s_b4ck_t0_1_21bcd6}`
# Goat
Description:
```markdown
To prevent excessive brute forcing for those experiencing a skissue, I made sure to add a PoW.

`nc goat.chal.cyberjousting.com 1349`

[goat.zip]
```

**Author**: `Legoclones`

## Writeup
This challenge gives you a single format string vulnerability through your name. This can leak information or give you an arbitrary write primitive, but not both. The problem here is that ASLR is enabled, so arbitrary write only works in the executable section of memory because PIE is disabled (meaning no libc/stack writing). Leaking stuff won't do anything because there's no way to use it afterwards. 

The solution is a partial GOT overwrite - since RELRO is only partially enabled, you can overwrite GOT entries that have been initialized. The intended GOT entry to overwrite is `snprintf` because it's < 0xffff bytes away from `system`, meaning `system` and `snprintf` will have all but the last 2 bytes of their addresses overlapping. Their distance is also far enough away that when that 1/16 chance happens, the first nibble is either 0 or 1, and the last 3 are the nibbles of the address of `system` in this libc. That's just a long way of saying the partial overwrite has approximately a 1/16 or 1/32 chance of working (idk I can't do math), which is doable. 

Once a format string is used to change the GOT address for `snprintf` to `system`, the confirmation gets stored in the same buffer passed in as the first argument to `snprintf()` (which is actually `system()`), so using `/bin/sh` as your confirmation will cause it to run `system("/bin/sh")`. 

I've automated solving the PoW and exploiting the vulnerability in `solve.py`. Due to the low brute force, just run it until you don't see EOF (should take like 30 seconds max). 

**Flag** - `byuctf{n0w_y0u're_the_g0at!}`

## Hosting
`goat` was compiled with the command `gcc -o goat -fstack-protector-all -no-pie goat.c`.

This challenge should be a Docker container that runs `goat` on port 5000. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
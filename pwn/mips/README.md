# MIPS
Description:
```markdown
Pwn mains need to learn more about other architectures.

`nc mips.chal.cyberjousting.com 1357`

[mips.zip]
```

**Author**: `Legoclones`

## Writeup
In x64, stack canaries are referenced as an offset to the `fs` register and I think are stored in TLS near the linker. However, in MIPS, the Global Offset Table contains a pointer to the stack canary. This is a stripped mipsel32 execute without PIE that contains a buffer overflow and 2 arbitrary reads (they specify the address and I print out the bytes). However, stack canaries are enabled, so the buffer overflow will fail without knowing the canary. They would probably think of doing GOT -> libc `environ` -> stack, but that requires **3** reads, not 2. Doing GOT -> canary will give them what they need, then they can exploit the overflow and go to the `win()` function.

Note that exploit dev tooling kinda sucks for MIPS, and if they have the latest version of Unicorn installed (2.1.3), then any pwntools commands will cause Python to segfault. They'll get over it. I'm pulling the libraries from my own Docker container which they can see in the `Dockerfile`. There, they'll see what libc is being used, what qemu version is being used, that qemu has ASLR on, etc. A PoW was added to prevent brute forcing the canary address. Half of solving the problem is just figuring out how to run it on their own machine and learn what's going on.

The solution is automated in `solve.py`.

**Flag** - `byuctf{h0p3_y0u_d1dnt_h4v3_un1c0rn_2.1.3_cuz_M1PS_s3gf4ultz_th3r3}`

## Hosting
`mips` was compiled with the command `make` (see `Makefile`).

This challenge should be a Docker container that runs `mips` on port 5003. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
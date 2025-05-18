# Game of Yap
Description:
```markdown
yap yap yap

`nc yap.chal.cyberjousting.com 1355`

[game-of-yap.zip]
```

**Author**: `deltabluejay`

## Writeup
This challenge gives you two chances to perform a buffer overflow in the `play` function. However, PIE is enabled (no other protections besides NX). For the first BOF, you need to perform a partial overwrite to jump to the `yap` function, which will leak a binary address for you. For the second BOF, you'll use that leak to write a small ROP chain. You can write a ROP chain to jump to the provided `mov rdi, rsi` gadget, which will conveniently move the pointer to the buffer (which you control) into `rdi`, and then call `printf`. You can leverage this to leak a libc address from the stack. The ROP chain will finally return back into `play` in order to provide one last chance to exploit the binary. In this final BOF, you can use the libc leak to ret2system.

See [solve.py](./solve.py) for a PoC.

**Flag** - `byuctf{heres_your_yap_plus_certification_c13abe01}`

## Hosting
`game-of-yap` was compiled with the command `gcc -fPIE -pie -masm=intel -fno-stack-protector -o game-of-yap game-of-yap.c`.

This challenge should be a Docker container that runs `game-of-yap` on port 5002. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
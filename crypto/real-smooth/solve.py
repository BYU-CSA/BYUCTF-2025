from pwn import *

p = remote('smooth.chal.cyberjousting.com', 1350)

c1 = p.recvline().decode().rstrip()
c2 = p.recvline().decode().rstrip()
ciphertexts = bytes.fromhex(c1+c2)
ogplaintext = b'Slide to the leftSlide to the right'
newplaintext = b'Criss cross, criss cross'

print("Forged ciphertext = ", forged:=xor(xor(ciphertexts, ogplaintext), newplaintext).hex()[:len(newplaintext.hex())])
p.sendline(forged.encode())

p.interactive()
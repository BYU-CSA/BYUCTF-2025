from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from pwn import *
import sys
sys.setrecursionlimit(1000000)


### REMOTE INTERACTION ###
p = remote('choose.chal.cyberjousting.com', 1348)
p.recvline()
enc = p.recvline().strip().decode()
print(f'enc: {enc}')
p.recvline()
p.sendline(b"2 3 6") # use these e values

for _ in range(6):
    exec(p.recvline().decode().strip())


# crt code from https://www.geeksforgeeks.org/chinese-remainder-theorem-in-python/
def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def chinese_remainder_thm(num, rem):
    prod = 1
    for n in num:
        prod *= n

    result = 0
    for i in range(len(num)):
        prod_i = prod // num[i]
        _, inv_i, _ = gcd_extended(prod_i, num[i])
        result += rem[i] * prod_i * inv_i
    return result % prod

def getIntRoot(n, root):
    low = 10**(len(str(n))//root)
    high = 10*low
    while True:
        guess = (low+high)//2
        if guess**root == n:
            return guess
        if high==low:
            return high
        if guess**root < n:
            low = guess+1
        if guess**root > n:
            high = guess - 1

# n0-3 and c0-3 are set during the exec() above (hacky solution ik)
key = chinese_remainder_thm([n0, n1, n2], [pow(c0, 3, n0), pow(c1, 2, n1), c2])
key = long_to_bytes(getIntRoot(key, 6))
cipher = AES.new(key[:16], AES.MODE_ECB)
print(cipher.decrypt(bytes.fromhex(enc)))
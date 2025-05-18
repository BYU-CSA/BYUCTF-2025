from Crypto.Util.number import getPrime
import random

flag = b'byuctf{1t_4lw4ys_c0m3s_b4ck_t0_1_21bcd6}'
N = 1024
p = getPrime(N)
g = 3
a = p-1
a=a*random.randint(5, 50)
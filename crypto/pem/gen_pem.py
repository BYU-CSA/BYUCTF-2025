from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long
from base64 import b64encode

flag = b"fjagkdflgfkdsjgfdltyugvjcbghjqfsdjvfdhbjfd byuctf{P3M_f0rm4t_1s_k1ng} cmxvblalsfiuqeuipplvdldbnmjzxydhjgfdgppsksjq"
n = bytes_to_long(flag)
n = n ** 2
e = 0x10001

key = RSA.construct((n, e))

pem_key = key.publickey().exportKey(format='PEM')
print(pem_key.decode())

# make sure to specify that flag = sqrt(n)
from pwn import *
    
##### Solve #####

def split_into_blocks(string : bytes, blocksize=16):
    blocks = []
    for i in range(0, len(string), blocksize):
        block = string[i:i+blocksize]
        blocks.append(block)
    return blocks

def crack_block(p, ct: bytes, block_len, iteration):
    zero_iv = b''
    for j in range(1,len(ct)+1):
        for i in range(255):
            new_iv = bytes((block_len*iteration)) # pad to the current block
            new_iv += bytes((block_len-j)) # pad the current block
            new_iv += bytes([i]) # current byte
            new_iv += bytes([byt ^ j for byt in zero_iv]) # known bytes
            p.recvuntil(b"> ")
            payload = bytes.hex(new_iv).encode()
            # print(len(payload))
            # print(payload)
            p.sendline(payload)
            error = p.recvline()
            if b'Padding error' not in error:
                print(error)
                zero_iv = bytes([new_iv[-j]^j]) + zero_iv
                break
            else:
                # print(error)
                pass
        # print(zero_iv)
    return zero_iv

def break_repeating(p, ciphertext: bytes, block_len):
    result = b''
    print(p.recvuntil(b" > "))
    p.sendline(b'00'*20)
    print(p.recvline())
    for ct in ciphertext:
        zeroiv = crack_block(p, ct, block_len, 1) # I had to increment this manually but it worked lol
        return zeroiv


if __name__ == "__main__":
    p = remote('hash.chal.cyberjousting.com', 1351)
    print(p.recvlines(2))
    ct = p.recvline().strip().decode()
    print(ct)
    flag = bytes.fromhex(ct)
    zeroiv = break_repeating(p, [ct[:20]], 20)
    zeroiv = b'T\x1b^:sd\\\xd0\xf6O\x07\xa5\xc9l\x0cz\xa1\x88\x7f\xdc'+zeroiv
    # zeroiv = b'T\x1b^:sd\\\xd0\xf6O\x07\xa5\xc9l\x0cz\xa1\x88\x7f\xdcC\x11\xb0\xd4\x19X-\xe2\xa4\x06\xc9F=\xcd<\x7f\xc1\rZ\xfc'+zeroiv
    print(zeroiv)
    print(bytes([byt ^ j for byt, j in zip(zeroiv,bytes.fromhex(ct)[:40])]))
    print(f"Zero IV: {str(zeroiv)}")

# byuctf{my_k3y_4nd_m3ss4g3_w3r3_th3_s4m3}
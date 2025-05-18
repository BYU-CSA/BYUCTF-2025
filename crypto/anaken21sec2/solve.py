import encrypt
from itertools import combinations
from time import time

plaintext = input("What is the plaintext?\n")
ciphertext = input("What is ciphertext?\n")
order = input("what is the order of the 11-digit key\n").split(" ")
order = [int(i)-1 for i in order]
numbers = [chr(i) for i in range(97, 97+25)]
start = time()

for comb in combinations(numbers, 11):
    key = ""
    for i in range(11):
        key += comb[order[i]]
    if encrypt.encrypt(plaintext, key) == ciphertext:
        print(key, time()-start)
print("complete", time()-start)
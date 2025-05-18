# Anaken21sec2
Description:
```markdown
I made this custom encryption algorithm for my crypto class and decided to share it with you guys! Let's see if you can break it without knowing the key...

*Note - wrap the flag in `byuctf{}`*

`nc anaken21sec2.chal.cyberjousting.com 1347`

[encrypt.py] [break.py]
```

**Author**: `Anaken21sec1`

## Writeup
To break the encryption, you can exploit the fact that the same key is used to mix up the 6x6 box as is used to shuffle the letters at the end. This leaves the encryption vulnerable to a chosen plaintext attack. By using a chosen plaintext attack, you can figure out the alphabetical order of the key. Then, you can use that to reduce the brute force space to a matter of minutes instead of days. You can do this as follows:

1. Encrypt several (at least 10) different 12-letter plaintexts and keep track of their encryptions
2. Encrypt the concatenation of the plaintexts
3. Using the output of the long plaintext and comparing it to the short outputs, you can deduce the alphabetical order of the key.
4. Using the alphabetical order of the key, you can brute force the key much faster than trying all 25^11 combinations.

Here is an example. We start by encrypting the following plaintexts on the left and we get the ciphertexts on the right.
```
aaaaaaaaaaaa    frqccahtwirw
rrrrrrrrrrrr    gjmfkputacxz
zzzzzzzzzzzz    qxkonxnjghvf
dddddddddddd    fehu0hztzrlm
uuuuuuuuuuuu    gudxqnltdlip
llllllllllll    yunrvnt0ivzj
gggggggggggg    fpzlfcqtt0fc
tttttttttttt    qbbfkvejaqpz
cccccccccccc    puuu0ngjzedm
yyyyyyyyyyyy    xpfoncv0gjnf
```

Then we encrypt the concatenation and get the following ciphertext.
```
aaaaaaaaaaaarrrrrrrrrrrrzzzzzzzzzzzzdddddddddddduuuuuuuuuuuullllllllllllggggggggggggttttttttttttccccccccccccyyyyyyyyyyyy
frfjhiv0ezcqxnrliczpuoctklqvqanfccnznjfpfjfazqxutnfkevhaxmgurtbdntmv0lttvmxpwpffex0zp0jiughpyuljunrkhzdncqbu0wgjotdzfqgg
```

We can split up the cipher text by the letters in the first plaintext (each split should be with in 1 letter of length from the others)
```
frfjhiv0ezc qxnrliczpuo ctklqvqanf ccnznjfpfjf azqxutnfkev haxmgurtbdn tmv0lttvmxp wpffex0zp0j iughpyuljun rkhzdncqbu0 wgjotdzfqgg
```

From here we can split each of the chunks into letters based off the ciphertexts. Note that each line represents a letter of the key. Since each message is 11 letters long and the cipher is done in blocks of 12, each letter will take 1 or 2 letters (but usually 1) from each of the individual ciphertexts. We can use this to discover the order of the key. For example, the first line has 2 letters from the first ciphertext. Thus, it is the first to come alphabetically from the key. The last letter comes next alphabetically and so on. (Sometimes it gives ambiguous results, but it usually causes errors later on so you can go back and check your work)
```
1  fr f  j  h  i  v  0  e  z  c
2  q  x  n  r  l  i  c  z  pu o
3  c  t  k  l  q  v  q  a  n  f
4  c  c  n  z  n  j  fp f  j  f
5  a  z  qx u  t  n  f  k  e  v
6  h  a  x  m  gu r  t  b  d  n
7  t  m  v  0  l  t  t  v  m  xp
8  w  p  f  fe x  0  z  p  0  j
9  i  u  g  h  p  yu l  j  u  n
10 r  k  h  z  d  n  c qb  u  0
11 w  gj o  t  d  z  f  q  g  g
```

From this we know that the order must go 
```
1 11 5 8 6 9 4 10 2 7 3
```

Now, we can use this to brute force any plaintext. My code to brute force is in `brute.py`. I used the plaintext `"abcdefghijkl"` with corresponding ciphertext `"gsswpplcfyjn"`. This yields 2 potential keys in less than 12 minutes:
```
cxjqksgwdlf
cxjqkriwdlf
```

These are actually both valid keys that perform the same encryption (on every plaintext that I tried at least). Using either key, we can now decrypt the ciphertext to find the flag.

**Flag** - `byuctf{cryptonerdsgobrrrrrrweneedmoreofthem}`

## Hosting
This challenge should be a Docker container that runs `break.py` on port 5000. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
# Choose Your RSA
Description:
```markdown
My RSA is so secure, I will even let you choose what value of `e` to use for 3 different encryptions! Of course, they have to be different values of `e`. Can't make it too easy.

`nc choose.chal.cyberjousting.com 1348`

[server.py]
```

**Author**: `Anaken21sec1`

## Writeup
The idea behind this challenge is that you can use `e=2`, `e=3`, and `e=6` (in the real world, an even `e` would not work, but you never have to actually use an RSA decryption). Using the 3 cipher texts, you can use the Chinese Remainder theorem to find `m^6 mod (n0*n1*n2)` where `m` is the AES key. The size of the key and the primes are chosen so that `m^6<(n0*n1*n2)`, so that this yields the key directly. However, the key needed to be large enough so that `m^2 > n0`, `m^3>n1`, and `m^4>n2`, to avoid trivially revealing the key. The different AES key each time prevents using interactions from a previous connection to help in a current connection.

See `solve.py`.

**Flag** - `byuctf{Chin3s3_rema1nd3r_th30r3m_is_Sup3r_H3lpful}`

## Hosting
This challenge should be a Docker container that runs `server.py` on port 5001. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
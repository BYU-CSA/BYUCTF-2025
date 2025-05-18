# Hash Psycho
Description:
```markdown
Brand new authentication server, zero security vulnerabilities

`nc psycho.chal.cyberjousting.com 1353`

[hash_psycho.py]
```

**Author**: `overllama`

## Writeup
Python default `int` `hash()` actually is equivalent to `% (2**61-1)`. You can therefore forge a hash value that is just `1337+(2**61-1)` (`2305843009213695288`) and voila, flag.
```python
>>> 1337 == hash(1337+(2**61-1))
True
```

**Flag** - `byuctf{wh0_kn3w_h4sh_w4snt_h4sh}`

## Hosting
This challenge should be a Docker container that runs `server.py` on port 5001. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
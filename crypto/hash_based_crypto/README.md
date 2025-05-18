# Hash Based Cryptography
Description:
```markdown
I wrote this code for class; hopefully it's not insecure

`nc hash.chal.cyberjousting.com 1351`

[server.py]
```

**Author**: `overllama`

## Writeup
The idea of this solve is to perform a padding attack on the cipher. See `solve.py`.

**Flag** - `byuctf{my_k3y_4nd_m3ss4g3_w3r3_th3_s4m3}`

## Hosting
This challenge should be a Docker container that runs `server.py` on port 5002. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
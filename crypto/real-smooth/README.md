# Real Smooth
Description:
```markdown
Just do the dance, that's the solve

`nc smooth.chal.cyberjousting.com 1350`

[real-smooth.py]
```

**Author**: `overllama`

## Writeup
ChaCha without Poly is vulnerable to a bit flip attack, so you can just flip bits across the board knowing the plaintexts and profit.

See `solve.py`.

**Flag** - `byuctf{ch4ch4_sl1d3?...n0,ch4ch4_b1tfl1p}`

## Hosting
This challenge should be a Docker container that runs `real-smooth.py` on port 5003. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
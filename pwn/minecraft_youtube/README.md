# Minecraft YouTuber
Description:
```markdown
Oh boy, I hit a million subscribers on YouTube, what do I do now?

`nc minecraft.chal.cyberjousting.com 1354`

[minecraft] [minecraft.c] [Dockerfile]
```

**Author**: `overllama`

## Writeup
Basically the idea here is that it's an uninitialized data use vulnerability and you can "groom" the Heap to make the keycard value be what you want it to be (0x1337). The uid is kind of a red herring. You just have to spam gear until you get a name tag, set it to what you want it to be, and then win.

See `solve.py`.

**Flag** - `byuctf{th3_3xpl01t_n4m3_1s_l1t3r4lly_gr00m1ng}`

## Hosting
This challenge should be a Docker container that runs `minecraft` on port 5001. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
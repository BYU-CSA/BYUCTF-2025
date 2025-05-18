# moooo
Description:
```markdown
Moo, mooo mooo mooo. Mooo mooo moooo moo moo moooooooooo moo moooo

(When you have the flag, the program will run printing "gotem")

[main.cow]
```

**Author**: `overllama`

## Writeup
So this is in a language called COW, which is documented on the [esolang wiki](https://esolangs.org/wiki/COW) and is just awful. I had to write my own interpreter since there isn't really anything out there that can interpret this well lol. I mean there are a few that can [interpret](https://frank-buss.de/cow.html) but none that do stdin in the way I wanted.

That interpreter is in [moo.py](./moo.py), and the intended solve is static rev of the commands until you realize that it will only run successfully under one potential flag

**Flag** - `byuctf{moo_mooo_moooo_mooooooo_moo_lol}`
# JWTF
Description:
```markdown
Unfortunately one of our JWTs was compromised by attackers, so we created a JWT Revocation List to ensure they can't use it anymore.

https://jwtf.chal.cyberjousting.com

[jwtf.zip]
```

**Author**: `Legoclones`

## Writeup
The way to get around this is by taking advantage of the fact that the signature is base64-encoded. Let's take a token like `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6dHJ1ZSwidWlkIjoiMTMzNyJ9.TYXuhKJG6sb3ck9UZgzbIFaZ2WLK2JeN8Q5Mj_UnvZk`. The last section, `TYXuhKJG6sb3ck9UZgzbIFaZ2WLK2JeN8Q5Mj_UnvZk` [is decoded to](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)To_Hex('Space',0)&input=VFlYdWhLSkc2c2IzY2s5VVpnemJJRmFaMldMSzJKZU44UTVNal9VbnZaaw&oeol=FF) `4d 85 ee 84 a2 46 ea c6 f7 72 4f 54 66 0c db 20 56 99 d9 62 ca d8 97 8d f1 0e 4c 8d 49 ef 66`. However, if you change the last character `k` to the next letter in the base64 alphabet, `l`, it [ALSO decodes to the same thing](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)To_Hex('Space',0)&input=VFlYdWhLSkc2c2IzY2s5VVpnemJJRmFaMldMSzJKZU44UTVNal9VbnZabA&oeol=FF). Therefore you can change the last letter of the signature and it will be base64-decoded into the same signature.

`curl http://localhost:5002/flag -H 'Cookie: session=<insert_jrl_token_but_change_last_char>`

Note that adding whitespace or equal signs won't work because those are specifically filtered out. Also, changing any bytes of the other two sections will also not work because the signature is based on the hash of `section1.section2` in their base64-encoded forms.

**Flag** - `byuctf{idk_if_this_means_anything_but_maybe_its_useful_somewhere_97ba5a70d94d}`

## Hosting
This challenge should be a Docker container that runs a Flask server on port 5002. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
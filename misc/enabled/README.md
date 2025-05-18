# Enabled
Description:
```markdown
We're doing a little bit of sanitizing and a whole lot of restriction on what you can run. Good luck.

`nc enabled.chal.cyberjousting.com 1352`

[jail.sh]
```

**Author**: `overllama`

## Writeup
This challenge involves just knowing bash internals really well. I'm sure there are a couple of solves, but the intended is using `pushd` to navigate to the flag directory and then you can run `source` and the error message will give you the flag. Who knows what other solve paths are available, though.

```bash
pushd ..
pushd flag
source flag.txt
```

**Flag** - `byuctf{enable_can_do_some_funky_stuff_huh?_488h33d}`

## Hosting
This challenge should be a Docker container that runs `jail.sh` on port 5000. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
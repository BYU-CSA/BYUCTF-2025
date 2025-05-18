# TCL
Description:
```markdown
I created my own Tiny Config Language and even a little parser for it - you should try it out!

`nc tcl.chal.cyberjousting.com 1358`

[tcl.zip]
```

**Author**: `Legoclones`

## Writeup
The whole thing here is that there's a garbage collector that frees memory no longer used. It runs every 5 seconds and loops through the global variable of "objects" and frees anything not `NULL` with `refcount == 0` and sets it to `NULL`. One problem is a race condition - the program will let you use an object with refcount that's 0 as long as it's not `NULL`. The garbage collector runs through all global variables and makes a list of indexes. It then frees all the indexes in a row, then sets all them to `NULL`. However, there's a small section of time in between the freeing and setting to `NULL` where the attacker can reference that object (which was a freed chunk but is now reallocated) and change the `refcount`. Then, when the garbage collector sees `refcount` for the freed object is not 0, it will assume a mistake and not set it to NULL. This reallocated chunk will also be pushed onto the end of the objects array, leaving **two** references to same chunk in the objects array. 

Once the second config file is finished, `clear_objects()` will set the `refcount` to 0 for both instances of the same chunk, and the garbage collector will end up freeing + setting both references to `NULL`. The race condition is having some line of the second config file allocate a chunk that just got freed but not yet set to `NULL`.

The outline for the solution is as follows:
- Create a config file with 50 objects (25x key/value string pairs)
- Finish the config file
- Start a second config file
- Wait *x* amount of seconds (to time race condition) for the garbage collector thread to start to free the objects
- Send a config line
    - This will take the last freed chunk and use it, setting `refcount` to a non-0 value
- When the garbage collector goes to nullify each freed chunk, it will run into the one allocated from the config line above and ignore it, leaving **two instances of the same chunk** in globals
- Send more config lines to fill up all the `NULL`s in between the two references
- Finish the config file
- Wait at least 5 seconds for the garbage collector to do the double free
- Start a third config file with a bunch of ints for the same key and have one of the ints end up overwriting the first instance with the GOT address of some function (to create a fake chunk there)
- Send a bunch more lines with ints and have one of the float objects end up overwriting the fake chunk that got pushed on with the address for `win()` so you get a shell when it's called next

Not at all complicated :)

This is automated in `solve.py`, but the network jitter will have to be resolved with the random delay once it's actually deployed on the REAL infra.

**Flag** - `byuctf{ok4y_y34h_th4t_d3fin1t3ly_suck3d}`

## Hosting
`tcl` was compiled with the command `gcc -pthread -o tcl -fstack-protector-all -no-pie tcl.c`.

This challenge should be a Docker container that runs `tcl` on port 5004. All the proper files are included in here. The command to build the docker container is (when located inside of this directory):

```bash
docker compose up -d
```

To stop the challenge:
```bash
docker compose down
```
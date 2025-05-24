# moooo

### Description

Moo, mooo mooo mooo. Mooo mooo moooo moo moo moooooooooo moo moooo
(When you have the flag, the program will run printing "gotem")

Files:
- [main.cow](./main.cow)

### Solve

This challenge is in a language called COW, which is documented on the [esolang wiki](https://esolangs.org/wiki/COW) and is just awful. I had a deep dive into it because I found it on a google spiral and decided to really dive into it. There are only 12 instructions in the whole language, as documented on the site:

| Opcode | Description |
| ------ | ----------- |
| moo | | This command is connected to the MOO command. When encountered during normal execution, it searches the program code in reverse looking for a matching MOO command and begins executing again starting from the found MOO command. When searching, it skips the instruction that is immediately before it (see MOO). |
| mOo | Moves current memory position back one block. |
| moO | Moves current memory position forward one block. |
| mOO | Execute value in current memory block as if it were an instruction. The command executed is based on the instruction code value (for example, if the current memory block contains a 2, then the moO command is executed). An invalid command exits the running program. Value 3 is invalid as it would cause an infinite loop. |
| Moo | If current memory block has a 0 in it, read a single ASCII character from STDIN and store it in the current memory block. If the current memory block is not 0, then print the ASCII character that corresponds to the value in the current memory block to STDOUT. |
| MOo | Decrement current memory block value by 1. |
| MoO | Increment current memory block value by 1. |
| MOO | If current memory block value is 0, skip next command and resume execution after the next matching moo command. If current memory block value is not 0, then continue with next command. Note that the fact that it skips the command immediately following it has interesting ramifications for where the matching moo command really is. For example, the following will match the second and not the first moo: OOO MOO moo moo |
| OOO | Set current memory block value to 0. |
| MMM | If no current value in register, copy current memory block value. If there is a value in the register, then paste that value into the current memory block and clear the register. |
| OOM | Print value of current memory block to STDOUT as an integer. |
| oom | Read an integer from STDIN and put it into the current memory block. |

My personal approach with a challenge like this is starting to redefine the opcodes as something that I can understand. There's a file in this directory ([`main-commented`](./main-commented)) that contains the commented original code before it was turned into an amalgamous blob. For a dynamic approach, it's really useful to have a small interpreter such that you can print debug information. Usually, I'll reverse the program until I understand it enough to debug and that will take me the rest of the way there.

For the process of static RE, I usually start with separating the program on useful lines. The program starts with this: `MoO MoO MoO MoO MoO MoO MoO MoO MoO MoO MoO MOO`. This increments the first space of memory by 11 and starts a loop.

That loop processes these commands (skipping the first the first time):
```
moO MoO MoO MoO MoO MoO MoO MoO moO MoO MoO MoO MoO MoO MoO MoO MoO MoO MoO moO 
MoO MoO MoO MoO MoO MoO MoO MoO MoO MoO moO MoO MoO MoO MoO moO MoO MoO MoO moO MoO mOo mOo mOo mOo mOo mOo MOo
```

Each piece of this can be separated on `moO`, which moves +1 memory block:
```
moO MoO MoO MoO MoO MoO MoO MoO
moO MoO MoO MoO MoO MoO MoO MoO MoO MoO MoO
moO MoO MoO MoO MoO MoO MoO MoO MoO MoO MoO
moO MoO MoO MoO MoO
moO MoO MoO MoO
moO MoO
mOo mOo mOo mOo mOo mOo MOo
```
The loop will increment each space of memory by a certain amount in a loop. `MOO` will loop until the memory address it's on is 0. So it'll loop 11 times, since that's what our first piece set. So memory after the loop is finished will be:
`0 77 110 110 44 33 11`

After that, we have another section of commands, before we get to the OOO: 
```
moO Moo moO 
MoO Moo Moo moO moO MoO MoO Moo moO MOo Moo mOo mOo mOo mOo Moo moO Moo Moo moO moO moO Moo mOo mOo MOo Moo mOo Moo Moo moO moO 
moO Moo mOo mOo Moo mOo Moo Moo Moo moO moO moO MoO Moo moO MOo Moo moO
```

This can be split up by the print statements (`Moo`) and memory moves (`moO`/`mOo`) as follows:
```
moO Moo ; 77
moO MoO - Moo Moo ; 111 111
moO moO MoO MoO - Moo ; 46
moO MOo - Moo ; 32
mOo mOo mOo mOo - Moo ; 77
moO - Moo Moo ; 111 111
moO moO moO - Moo ; 32
mOo mOo MOo - Moo ; 109
mOo - Moo Moo ; 111 111
moO moO moO - Moo ; 32
mOo mOo - Moo ; 109
mOo - Moo Moo Moo ; 111 111 111
moO moO moO MoO - Moo ; 33
moO MOo - Moo ; 10
moO
```

Tracking from our original memory of `0 77 110 110 44 33 11`, this prints `77 111 111 46 32 77 111 111 32 109 111 111 32 109 111 111 111 33 10` as their ascii values. In a Python repl, we can print that out ourself!

```sh
➜  moo > python 
>>> values = '77 111 111 46 32 77 111 111 32 109 111 111 32 109 111 111 111 33 10'.split()
>>> ''.join([chr(int(i)) for i in values])
'Moo. Moo moo mooo!\n'
```

That's more or less the static reverse engineering side of things! You can just continue that process until you find the flag, paying attention to those 'break spots', especially as you understand the language more.

For the dynamic side, I spent a long time looking for a good online interpreter, and there are a few that can [interpret](https://frank-buss.de/cow.html) but none that do stdin in the way I wanted (allowing you to input more than one character at a time) as far as I could find. Luckily, there are only 12 opcodes so actually implementing an interpreter myself was pretty easy, though I'll change it to use `sys.stdin` in Python for input if I ever go back and edit it. That interpreter is in [moo.py](./moo.py), and you can add debug statements to it so that you can visualize what the program is actually doing.

The program itself is designed to only complete all the way to the end under one flag. It'll run by taking your input into various memory slots and then subtract a lot off each spot followed by the `mOO` opcode to 'execute' whatever value is in memory at that location. This would only allow the program to finish if `moO` or `3` was in that memory location, so you can statically reverse the program to add 3 to the number of subtraction operators at each check OR many people in the actual CTF side channelled the program since it would kill itself if the input was not correct. There is a Moo compiler somewhere online so people used that to output an actual program and then side channeled that binary. I was also told that AI could make a pretty decent little interpreter, too.

All in all, a fun challenge, and it will print `gotem` when you get the actual flag! It was a fun one to make and to work through to solve as well.

Flag : `byuctf{moo_mooo_moooo_mooooooo_moo_lol}`

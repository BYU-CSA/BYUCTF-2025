#!/usr/bin/env python3
 
"""
A python interpreter for moo, so i can use stdin
"""

import sys

class COWRuntimeException(Exception):
    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)

def search_back(instructions, rip):
    while instructions[rip] != "MOO":
        rip -= 1
        if rip < 0:
            raise COWRuntimeException("Error: couldn't find a valid MOO")
    return rip

def search_forward(instructions, rip):
    rip += 2 # this will cover the case of MOO moo moo where it skips the first moo
    while instructions[rip] != "moo":
        rip += 1
        if rip > len(instructions):
            raise COWRuntimeException("Error: couldn't find a valid moo")
    rip += 1
    return rip

def main(instructions, stdin):
    try:
        instructions = [instruction for instruction in instructions.split(' ') if instruction != '']
        memory = [0]        
        rsp = 0
        rip = 0
        stdout = ""
        register = 0
        while True:
            if rip == len(instructions):
                if stdout != "":
                    print(stdout)
                return
            elif instructions[rip] == "moo":
                rip = search_back(instructions, rip)
            elif instructions[rip] == "mOo":
                if rsp == 0:
                    raise COWRuntimeException("Error: Tried to decrement memory down from 0")
                rsp -= 1
                rip += 1
            elif instructions[rip] == "moO":
                if rsp == len(memory)-1:
                    memory.append(0)
                rsp += 1
                rip += 1
            elif instructions[rip] == "mOO":
                if memory[rsp] == 3 or memory[rsp] > 11:
                    raise COWRuntimeException("Error: tried to run invalid command")
                if memory[rsp] == 0:
                    rip = search_back(instructions, rip)
                elif memory[rsp] == 1:
                    if rsp == 0:
                        raise COWRuntimeException("Error: Tried to decrement memory down from 0")
                    rsp -= 1
                    rip += 1
                elif memory[rsp] == 2:
                    if rsp == len(memory)-1:
                        memory.append(0)
                    rsp += 1
                    rip += 1
                elif memory[rsp] == 4:
                    if memory[rsp] == 0:
                        if stdin == "":
                            print("STDIN empty, please input character(s)")
                            stdin = input(" > ").rstrip("\n")
                            if stdin == "":
                                raise COWRuntimeException("Error: no stdin after user input")
                        memory[rsp] = ord(stdin[0])
                        stdin = stdin[1:]
                    else:
                        stdout += chr(memory[rsp])
                    rip += 1
                elif memory[rsp] == 5:
                    if memory[rsp] == 0:
                        raise COWRuntimeException
                    else:
                        memory[rsp] -= 1
                        rip += 1
                elif memory[rsp] == 6:
                    memory[rsp] += 1
                    rip += 1
                elif memory[rsp] == 7:
                    if memory[rsp] == 0:
                        rip = search_forward(instructions, rip)
                    else:
                        rip += 1
                elif memory[rsp] == 8:
                    memory[rsp] = 0
                    rip += 1
                elif memory[rsp] == 9:
                    if register == 0:
                        register = memory[rsp]
                    else:
                        memory[rsp] = register
                        register = 0
                    rip += 1
                elif memory[rsp] == 10:
                    stdout += str(memory[rsp])
                    rip += 1
                elif memory[rsp] == 11:
                    print("Enter an integer to place in a register")
                    try:
                        stdin_num = int(input(" > ").rstrip("\n"))
                    except Exception as e:
                        raise COWRuntimeException("Error: " + str(e))
                    rip += 1
                else:
                    raise COWRuntimeException("Error: instruction in memory out of range")
                # TODO: Finish up these instructions after everything else has been coded
            elif instructions[rip] == "Moo":
                if memory[rsp] == 0:
                    if stdin == "":
                        print("STDIN empty, please input character(s)")
                        stdin = input(" > ").rstrip("\n")
                        if stdin == "":
                            raise COWRuntimeException("Error: no stdin after user input")
                    memory[rsp] = ord(stdin[0])
                    stdin = stdin[1:]
                else:
                    stdout += chr(memory[rsp])
                rip += 1
            elif instructions[rip] == "MOo":
                if memory[rsp] == 0:
                    raise COWRuntimeException
                else:
                    memory[rsp] -= 1
                    rip += 1
            elif instructions[rip] == "MoO":
                memory[rsp] += 1
                rip += 1
            elif instructions[rip] == "MOO":
                if memory[rsp] == 0:
                    rip = search_forward(instructions, rip)
                else:
                    rip += 1
            elif instructions[rip] == "OOO":
                memory[rsp] = 0
                rip += 1
            elif instructions[rip] == "MMM":
                if register == 0:
                    register = memory[rsp]
                else:
                    memory[rsp] = register
                    register = 0
                rip += 1
            elif instructions[rip] == "OOM":
                stdout += str(memory[rsp])
                rip += 1
            elif instructions[rip] == "oom":
                print("Enter an integer to place in a register")
                try:
                    stdin_num = int(input(" > ").rstrip("\n"))
                except Exception as e:
                    raise COWRuntimeException("Error: " + str(e))
                rip += 1
            else:
                raise COWRuntimeException("Error: bad instruction")
    except COWRuntimeException as e:
        print(e.message)
        print("Debug dump: ")
        print("rip = ", str(rip))
        print("Current instruction = ", repr(instructions[rip]))
        print("Stack: ", str(memory))
        print(f"RSP: {str(rsp)}, stack[RSP]: {str(memory[rsp])}")
        print("STDOUT: ", stdout)


if __name__ == "__main__":
    if (len(sys.argv)) < 2:
        print("Usage: python3 moo.py <instructions.txt>")
        print("A third argument can be added in the place of STDIN")
        sys.exit(1)
    
    try:
        with open(sys.argv[1]) as f:
            instructions = f.read().replace('\n', '')
    except FileNotFoundError:
        print("File not found")
        print("Usage: python3 moo.py <instructions.txt>")
        print("A third argument can be added in the place of STDIN")
    except PermissionError:
        print("Permissions denied")
        print("Usage: python3 moo.py <instructions.txt>")
        print("A third argument can be added in the place of STDIN")
    except Exception as e:
        print("Error: ", e)
        print("Usage: python3 moo.py <instructions.txt>")
        print("A third argument can be added in the place of STDIN")

    stdin = ''
    if (len(sys.argv) >= 3):
        stdin = sys.argv[2]

    main(instructions, stdin)
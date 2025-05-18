from z3 import *

# Initialize 37 symbolic bytes for the flag
flag = [BitVec(f'flag_{i}', 8) for i in range(0x25)]

s = Solver()

# All characters must be printable ASCII
for c in flag:
    s.add(c >= 0x20, c <= 0x7d)


s.add(flag[4]==flag[0xe])
s.add(flag[0xe]==flag[0x11])
s.add(flag[0x11]==flag[0x17])
s.add(flag[0x17]==flag[0x19])
s.add(flag[9]==flag[0x14])
s.add(flag[10]==flag[0x12])
s.add(flag[0xb]==flag[0xf])
s.add(flag[0xf]==flag[0x18])
s.add(flag[0x18]==flag[0x1f])
s.add(flag[0x1f]==flag[0x1b])
s.add(flag[0xd]==flag[0x1a])
s.add(flag[0x10]==flag[0x1d])
s.add(flag[0x13]==flag[0x1c])
s.add(flag[0x1c]==flag[0x20])
s.add(flag[0x24]==ord('}'))
s.add(flag[6]==ord('{'))
s.add(flag[8]==flag[7]+-0x20)
s.add(flag[0]==ord('b'))
s.add(flag[1]==ord('y'))
s.add(flag[2]==ord('u'))
s.add(flag[3]==ord('c'))
s.add(flag[4]==ord('t'))
s.add(flag[5]==ord('f'))
s.add(flag[9] +flag[0x14] == flag[0x1f] + 3)
s.add(flag[0x1f] + 3 == flag[0])
s.add(flag[10] == flag[7] + 6)
s.add(flag[8] == flag[9] + 0x1b)
s.add(flag[0xc] == flag[0xd] + -1)
s.add(flag[0xd] == flag[10] + -3)
s.add(flag[10] == flag[0x10] + -1)
s.add(flag[0x10] == flag[0xe] + -1)
s.add(flag[0x23] == flag[5] + -2)
s.add(flag[5] == flag[0x15] + -1)
s.add(flag[0x15] == flag[0x16] + -1)
s.add(flag[0x16] == flag[0x1c] * 2)
s.add(flag[0x21] == flag[0x20] + 1)
s.add(flag[0x20] + 1 == flag[0x22] + -3)
s.add(flag[0x1e] == flag[7] + 1)



if s.check() == sat:
    print('SAT')
    m = s.model()
    result = ''.join([chr(m[c].as_long()) for c in flag])
    print(f"Flag: {result}")
else:
    print("No solution found.")
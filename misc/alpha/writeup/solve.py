bytes = [
    0x78, 0x20,
    0x0c, 0x20,
    0x1c, 0x00,
    0xd8, 0x00,
    0x78, 0x00,
    0x71, 0x00,
    0x49, 0x09,
    0xE6, 0x00,
    0x50, 0x00,
    0x8F, 0x00,
    0x50, 0x10,
    0x07, 0x00,
    0x08, 0x00,
    0x70, 0x10,
    0xE6, 0x00,
    0x50, 0x00,
    0x8E, 0x08,
    0x14, 0x28,
    0xE6, 0x00,
    0x50, 0x00,
    0x8F, 0x00,
    0X08, 0X00,
    0X70, 0X01,
    0X50, 0X00,
    0X3F, 0X0C,
    0X07, 0X00,
    0X3F, 0X0C,
    0XD8, 0X00,
    0X3F, 0X0C,
    0X30, 0X00,
    0X69, 0X20,
    0X08, 0X00,
    0XD8, 0X00,
    0X3F, 0X0C,
    0X3F, 0X0C,
    0X30, 0X00,
    0X83, 0X10,
    0X89, 0X24,
]

segments = {
    'A':  0b0000000000000001,
    'B':  0b0000000000000010,
    'C':  0b0000000000000100,
    'D':  0b0000000000001000,
    'E':  0b0000000000010000,
    'F':  0b0000000000100000,
    'G1': 0b0000000001000000,
    'G2': 0b0000000010000000,
    'H':  0b0000000100000000,
    'J':  0b0000001000000000,
    'K':  0b0000010000000000,
    'L':  0b0000100000000000,
    'M':  0b0001000000000000,
    'N':  0b0010000000000000,
    'DP': 0b0100000000000000,
}

def print_digit(A, B, C, D, E, F, G1, G2, H, J, K, L, M, N, DP):

    print(' ___ ') if A else print('     ')

    print('|', end='') if F else print(' ', end='')
    print('\\', end='') if H else print(' ', end='')
    print('|', end='') if J else print(' ', end='')
    print('/', end='') if K else print(' ', end='')
    print('|') if B else print(' ')

    print(' _', end='') if G1 else print('  ', end='')
    print('__ ') if G2 else print('   ')

    print('|', end='') if E else print(' ', end='')
    print('/', end='') if L else print(' ', end='')
    print('|', end='') if M else print(' ', end='')
    print('\\', end='') if N else print(' ', end='')
    print('|') if C else print(' ')

    print(' ___ ') if D else print('     ')


for i in range(0, len(bytes), 2):
    digit = (bytes[i + 1] << 8) + bytes[i]
    matching_segments = {'A': False, 'B': False, 'C': False, 'D': False, 'E': False, 'F': False, 'G1': False, 'G2': False, 'H': False, 'J': False, 'K': False, 'L': False, 'M': False, 'N': False, 'DP': False}
    for segment, mask in segments.items():
        if digit & mask:
            matching_segments[segment] = True
    print()
    print(int(i/2)+1)
    print('#'*8)
    print_digit(**matching_segments)
    print('#'*8)
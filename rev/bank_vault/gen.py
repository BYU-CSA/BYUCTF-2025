import random 
flag = b"byuctf{3v3n_v3ct0rs_4pp34r_1n_m3m0ry}"
binarr = [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1]
hexarr = [0xf16285bd, 0x4d79b336, 0x3607c041, 0x4f757c48, 0x63634432, 0x8474be64, 0x2f66bfed, 
          0x8c8ba74b, 0xcb7bb04c, 0x29aa35bb, 0xdc33e9f9, 0xb37642ea, 0x1133f4df, 0x6819b1cf, 
          0xac1b2111, 0x797e383b, 0xe46e41f5, 0x38e144f9, 0xaa5f25b7, 0x36e31d2b, 0x17cd4129, 
          0xcf9276a9, 0x9675f6, 0xed76e994, 0x1e33fc99, 0x75157513, 0x996d3e0c, 0x5b633cab, 
          0x60d22379, 0xfc740809, 0xcb43d953, 0xf9cfead5, 0xb1304006, 0xca841431, 0x2aece666, 
          0xdb72fb63, 0x73862a0f, 0x21ff2a98, 0x3b73281b, 0x1322483e, 0x565f373a, 0xbf32aa3e, 
          0x9d345021, 0xc003dd66, 0xfb08399c, 0x677070f7, 0x96d4f926, 0x5aad004, 0x465a312a, 
          0xcea1f556, 0xa9706fd9, 0x31330bd6, 0x4241cfa0, 0xfc340a7a, 0x1724268, 0x41e06d3e, 
          0xd9111112, 0x635f1af6, 0xeff71436, 0x82311dc8, 0xb56e65d1, 0x98e00125, 0xfe5faeb5, 
          0x4d53dae2, 0x980bcea2, 0xb98118bd, 0x8421652d, 0xf76d1209, 0xa4339088, 0xb98085f8, 
          0x6f6dea30, 0x2110d58e, 0x443b9947, 0x4529fd1d, 0xf0e27c3e, 0x8530b126, 0x8f72c719, 
          0xca794f90, 0x3e7dbb1d, 0xe57c7778, 0x18f32f9e, 0x4d2a5666, 0xe8e18692, 0x9a987ce8]

count = 0
for i in range(len(hexarr)):
    print(f"hexarr[{i}] = {hex(hexarr[i])} = {binarr[-(i+1)]}")
    if binarr[-(i+1)] == 1:
        print(hex(flag[count]))
        count += 1


# count = 0
# hexarr = []
# while count < len(binarr):
#     ran = random.randint(0,0xffffffff)
#     hexarr.append(hex(ran))
#     count += 1

# print(hexarr)


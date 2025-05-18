import numpy as np
from encrypt import permutes




def unPermute(blockM, count):
    finalBlockM = np.zeros((6,6))
    for i in range(6):
        for j in range(6):
            index = int(permutes[count][i,j]-1)
            finalBlockM[index//6,index%6] = blockM[i,j]
    return finalBlockM


def unAdd(blockM, count):
    if count == 0:
        for i in range(6):
            for j in range(6):
                if (i+j)%2 == 0:
                    blockM[i,j] +=2
    elif count == 1:
        blockM[3:,3:] = blockM[3:,3:]+2*blockM[:3,:3]
    elif count == 2:
        blockM[:3,:3] = 2*blockM[3:,3:]+blockM[:3,:3]
    elif count == 3:
        blockM[3:,:3] = blockM[3:,:3]+2*blockM[:3,3:]
    else:
        blockM[:3,3:] = 2*blockM[3:,:3]+blockM[:3,3:]
    return np.mod(blockM, 3)


def decrypt(ciphertext, key):
    #rearrange the ciphertext according to the key
    keyNums = [ord(key[i])-97 for i in range(len(key))]
    reducedKeyNums = []
    [reducedKeyNums.append(x) for x in keyNums if x not in reducedKeyNums]
    letterBoxes = [[] for i in reducedKeyNums]
    amountToTakeOff = len(ciphertext)//len(reducedKeyNums)
    remainder = len(ciphertext)%len(reducedKeyNums)
    for i in range(len(reducedKeyNums)):
        nextLowest = reducedKeyNums.index(min(reducedKeyNums))
        letterBoxes[nextLowest] = [ciphertext[i] for i in range(amountToTakeOff)]
        ciphertext = ciphertext[amountToTakeOff:]
        if nextLowest<remainder:
            letterBoxes[nextLowest].append(ciphertext[0])
            ciphertext = ciphertext[1:]
        reducedKeyNums[nextLowest]+=26
    intermediateText = ""
    i=0
    while sum([len(box) for box in letterBoxes]) != 0:
        intermediateText += letterBoxes[i].pop(0)
        i = (i+1)%len(letterBoxes)
    
    #do the block permutations and additions
    blocks = [intermediateText[12*i:12*(i+1)] for i in range(0,len(intermediateText)//12)]
    plaintext = ""
    for block in blocks:
        #make 6 by 6 matrix
        blockM =np.zeros((6,6))
        for (i,letter) in enumerate(block[0:6]):
            if letter == "0":
                letter = "`"
            letterNum = ord(letter)-96
            blockM[i,0] = letterNum//9
            blockM[i,1] = (letterNum%9)//3
            blockM[i,2] = letterNum%3
        for (i,letter) in enumerate(block[6:]):
            if letter == "0":
                letter = "`"
            letterNum = ord(letter)-96
            blockM[i,3] = letterNum//9
            blockM[i,4] = (letterNum%9)//3
            blockM[i,5] = letterNum%3
            
        #unscramble matrix
        for keyNum in reversed(keyNums):
            blockM = unAdd(blockM, keyNum%5)
            blockM = unPermute(blockM,(keyNum//5)%5)

        #get resulting letters from matrix
        for i in range(6):
            resultLetterNum = int(9*blockM[0,i]+3*blockM[1,i]+blockM[2,i])
            if resultLetterNum == 0:
                plaintext += "0"
            else:
                plaintext += chr(resultLetterNum+96)
        for i in range(6):
            resultLetterNum = int(9*blockM[3,i]+3*blockM[4,i]+blockM[5,i])
            if resultLetterNum == 0:
                plaintext += "0"
            else:
                plaintext += chr(resultLetterNum+96)
    return plaintext

if __name__ == "__main__":
    ciphertext =  input("What would you like to decrypt?\n")
    key = input("Enter the encryption key. \n")

    if len(ciphertext)%12 ==0:
        print(decrypt(ciphertext, key))
    else:
        print("Sorry, invalid ciphertext.")

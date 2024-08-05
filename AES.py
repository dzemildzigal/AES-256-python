"""
From: https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf

Terms and Acronyms
    
Affine Transformation - A transformation consisting of multiplication by a matrix followed by the addition of a vector.
Array - An enumerated collection of identical entities (e.g., an array of bytes).
Block - Sequence of binary bits that comprise the input, output, State, and Round Key. The length of a sequence is the number of bits it contains. Blocks are also interpreted as arrays of bytes.
Cipher - Series of transformations that converts plaintext to ciphertext using the Cipher Key.
Inverse Cipher - Series of transformations that converts ciphertext to plaintext using the Cipher Key.
Cipher Key - Secret, cryptographic key that is used by the Key Expansion routine to generate a set of Round Keys; can be pictured as a rectangular array of bytes, having four rows and Nk columns.
Round Key - Round keys are values derived from the Cipher Key using the Key Expansion routine; they are applied to the State in the Cipher and Inverse Cipher.
Key Expansion - Routine used to generate a series of Round Keys from the Cipher Key.
State - Intermediate Cipher result that can be pictured as a rectangular array of bytes, having four rows and Nb columns.
S-Box - Non-linear substitution table used in several byte substitution transformations and in the Key Expansion routine to perform a one-for-one substitution of a byte value.
Word - A group of 32 bits that is treated either as a single entity or as an array of 4 bytes. (32b = 4B = WORD)

Algorithms and Parameters

AddRoundKey() - Transformation in the Cipher and Inverse Cipher in which a Round Key is added to the State using an XOR operation. The length of a Round Key equals the size of the State (i.e., for Nb = 4, the Round Key length equals 128 bits/16 bytes).
InvMixColumns() - Transformation in the Inverse Cipher that is the inverse of MixColumns().
MixColumns() - Transformation in the Cipher that takes all of the columns of the State and mixes their data (independently of one another) to produce new columns.
InvShiftRows() - Transformation in the Inverse Cipher that is the inverse of ShiftRows().
ShiftRows() - Transformation in the Cipher that processes the State by cyclically shifting the last three rows of the State by different offsets.
InvSubBytes() - Transformation in the Inverse Cipher that is the inverse of SubBytes().
SubBytes() - Transformation in the Cipher that processes the State using a non linear byte substitution table (S-Box) that operates on each of the State bytes independently.
SubWord() - Function used in the Key Expansion routine that takes a four-byte input word and applies an S-box to each of the four bytes to produce an output word.
RotWord() Function used in the Key Expansion routine that takes a four-byte input word and performs a cyclic permutation.
K - Cipher key (masterkey). For AES-256 it is 256b long.
Nb - Number of columns (32b words, 4B words) comprising the state. For this standard Nb = 4.
Nk - Number of columns (32b words, 4B words) comprising the Cipher Key. For this standard (AES-256) Nk=8 (alternatives are 6 and 4).
Nr - Number of rounds which is a function of Nb and Nk. For this standard (AES-256) Nr = 14 (alternatives are 12 and 10).
Rcon[] - The round constant word array.
w[] - The Key Schedule (array of all round keys).
XOR - Exclusive or.
+ - Exclusive or.
* - Multiplication in a finite field.
(*) - Multiplication of two polynomials (each with degree < 4) modulo X^4+1. 


Inputs and Outputs

The input and output for the AES algorithm each consist of sequences of 128 bits (digits with values of 0 or 1). These sequences will sometimes be referred to as blocks and the number of bits they contain will be referred to as their length. 
The Cipher Key for the AES algorithm is a sequence of 128, 192 or 256 bits. Other input, output and Cipher Key lengths are not permitted by this standard.

The State

Internally, the AES algorithm's operations are performed on a two-dimensional array of bytes called the State. The State consists of four rows of bytes, each containing Nb bytes, where Nb is the block length divided by 32. Nb = 4, 4*32 = 128
In the State array denoted by the symbol s, each individual byte has two indices, with its row number r in the range 0 <= r < 4 and its column number c in the range 0 <= c < Nb. This allows an individual byte of the State to be referred to as either s r,c or s[r,c]. For this standard, Nb=4, i.e., 0 <= c < 4 (also see Sec. 6.3).
With respect to the input, the state's r,c-th element is: s[r,c] = input[r + 4c] for 0 <= r < 4 && 0 <= c < Nb (4).
With respect to the state, the output's r+4c-th element is: output[r + 4c] = s[r,c] for 0<= r < 4 && 0 <= c < Nb (4).

The Cipher

At the start of the Cipher, the input is copied to the State array. After an initial Round Key addition, the State array is transformed by implementing a Round Function 14 times (AES-256, Nr=14) with the final round differing slightly from the first Nr-1 rounds.
The Round Function is parametrized using the Key Schedule (w[]) which is a one-dimensional array of 4B words derived from the Key Expansion routine.
The Cipher is described by: The individual transformations, SubBytes(), ShiftRows(), MixColumns(), and AddRoundKey() - process the State for Nr rounds, with the exception of the final round where MixColumns() is omited!


Pseudocode of Cipher:

Nb = 4
Nk = 8
Nr = 14
byte === 1B === 8b
word === 4B === 32b
Cipher(byte in[4*Nb (bytes) = 128b], byte out[4*Nb (bytes) = 128b], word w[Nb*(Nr+1) words = 4*(15)*4B = 240b = 30B]):
    byte state[4, Nb]; # For us it's [4, 4]
    state = in

    AddRoundKey(state, w[0, Nb-1]) # words 0 to 3 from w = 4 words, 1 word = 32b, 0 to 3 words is 128b

    for round in range(1, Nr-1):
        SubBytes(state)
        ShiftRows(state)
        MixColumns(state)
        AddRoundKey(state, w[round*Nb, (round+1)*Nb - 1]) # w[round * 4, (round + 1) * 4 - 1] # words round * 4 to (round+1) * 4 - 1 which is 4 words which is 128b
    
    SubBytes(state)
    ShiftRows(state)
    AddRoundKey(state, w[Nr*Nb, (Nr+1)*Nb - 1]) # w[14*4, 15*4 - 1] = w[56, 60 - 1] = w[56, 59] which is 4 words which is 128b.

    out = state

SubBytes - > use S-Box and change values to one from S-Box.
ShiftRows - Go through state row-by-row (1 row is 4B). O-th row is not affected, 1-st row wrap around lshift 1B, 2-nd row wrap around lshift 2B, 3-rd row wrap around lshift 3B. Ex for ABCD:EFGH:IJKL:MNOP -> ABCD:FGHE:KLIJ:PMNO
MixColumns - Go through state column-by-column and perform the following matrix multiplication:
                |S'0,c|     | 02  03  01  01 | |S0,c|
                |S'1,c|  =  | 01  02  03  01 | |S1,c|   for 0 <= c < Nb (number of columns of state, for us is 4)
                |S'2,c|  =  | 01  01  02  03 | |S2,c|
                |S'3,c|     | 03  01  01  02 | |S3,c|

                
Key Expansion

The AES algorithm takes the Cipher Key, K, and performs a Key Expansion routine to generate a key schedule. The Key Expansion generates a total of Nb(Nr+1) (4*(14+1) = 60) 4B words.
The algorithm requires an initial set of Nb=4, 4B words (128b), and each of the Nr=14 rounds requires Nb=4, 4B words (128b) of key data.
The resulting key schedule consists of a linear array of 4B words, denoted [w_i], where i is in the range of 0 <= i < Nb(Nr+1) | 4(14+1)=60, 60 * 4B = 240B


Pseudocode for Key Expansion:

Nb = 4
Nk = 8
Nr = 14
KeyExpansion(byte key[4*Nk = 4*8B=256b for AES-256], word w[Nb*(Nr+1) = 4*(14+1)words = 60words = 240B], Nk = 8 (8words = 8*4B*8=256b)):
    word temp;
    i = 0;

    while (i<Nk):
        w[i] = word(key[4*i], key[4*i + 1], key[4*i + 2], key[4*i + 3]);
        i+=1;
    
    i = Nk

    while (i < Nb * (Nr + 1)):
        temp = w[i-1]
        if (i % Nk == 0):
            temp = SubWord(RotWord(temp)) XOR Rcon[int(i/Nk)]
        elif (Nk > 6 and i % Nk == 4):
            temp = SubWord(temp)
        
        w[i] = w[i-Nk] XOR temp
        i+=1
    
    

"""
class AES_256():
    
    s_box = ( 
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76, 
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0, 
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15, 
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75, 
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84, 
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF, 
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8, 
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2, 
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73, 
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB, 
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, 
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08, 
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A, 
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E, 
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF, 
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16, 
    ) 

    inv_s_box = ( 
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB, 
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB, 
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E, 
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25, 
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92, 
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84, 
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06, 
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B, 
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73, 
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E, 
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B, 
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4, 
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F, 
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF, 
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61, 
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
    )

    r_con = (
        b'\x00\x00\x00\x00', b'\x01\x00\x00\x00', b'\x02\x00\x00\x00', b'\x04\x00\x00\x00', b'\x08\x00\x00\x00', b'\x10\x00\x00\x00', b'\x20\x00\x00\x00', b'\x40\x00\x00\x00',
        b'\x80\x00\x00\x00', b'\x1B\x00\x00\x00', b'\x36\x00\x00\x00', b'\x6C\x00\x00\x00', b'\xD8\x00\x00\x00', b'\xAB\x00\x00\x00', b'\x4D\x00\x00\x00', b'\x9A\x00\x00\x00',
        b'\x2F\x00\x00\x00', b'\x5E\x00\x00\x00', b'\xBC\x00\x00\x00', b'\x63\x00\x00\x00', b'\xC6\x00\x00\x00', b'\x97\x00\x00\x00', b'\x35\x00\x00\x00', b'\x6A\x00\x00\x00',
        b'\xD4\x00\x00\x00', b'\xB3\x00\x00\x00', b'\x7D\x00\x00\x00', b'\xFA\x00\x00\x00', b'\xEF\x00\x00\x00', b'\xC5\x00\x00\x00', b'\x91\x00\x00\x00', b'\x39\x00\x00\x00',
    )

    def SubWord(self, word:bytearray):
        retval = [0, 0, 0, 0]

        for i in range(len(word)):
            retval[i] = self.s_box[word[i]]
        
        return retval

    def RotWord(self, word:bytearray):
        temp = word[0]
        word[0] = word[1]
        word[1] = word[2]
        word[2] = word[3]
        word[3] = temp
        return word

    def XOR_BITWISE(self, a:bytearray,b:bytearray):
        assert(len(a) == len(b))
        bytes_a = bytes(a)
        result = [0, 0, 0, 0]
        
        for i in range(len(a)):
            result[i] = bytes_a[i] ^ b[i]
        
        return result

    def KeyExpansion(self, key:bytearray, w:bytearray, Nk:int=8, Nb:int=4, Nr:int=14, verbose:bool=False):
        if(verbose):
            print("key: ", key.hex(' '))
        temp = b'\x00'*4 #4 bytes = 1 word
        w_list = list(w)
        key_list = list(key)
        temp_list = list(temp)
        assert(len(w) == 240) #240 bytes to expand and 16 to start with from masterkey (key)
        i = 0

        while (i < Nk):
            w_list[i*4:i*4+4] = key_list[4*i:4*i+4]
            if(verbose):
                print(f'w[{i}]: ', bytes(w_list[i*4:i*4+4]).hex(' '))
            i+=1
        
        while (i < Nb * (Nr + 1)):
            temp_list = w_list[(i-1)*4:i*4]
            if(verbose):
                print(f'For i={i}, temp={bytes(temp_list).hex()}')
            if (i % Nk == 0):
                temp_list =  self.XOR_BITWISE(self.SubWord(self.RotWord(temp_list)),bytes(self.r_con[int(i/Nk)]))
            elif (Nk > 6 and i % Nk == 4):
                temp_list = self.SubWord(temp_list)
            
            w_list[i*4:i*4+4] = self.XOR_BITWISE(w_list[(i-Nk)*4:(i-Nk)*4+4], temp_list)
            i+=1
        
        w = bytearray(w_list)
        return w

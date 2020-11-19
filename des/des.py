from Crypto.Random.random import getrandbits

PERMUTED_CHOICE_1 = [
    56, 48, 40, 32, 24, 16,  8,
     0, 57, 49, 41, 33, 25, 17,
     9,  1, 58, 50, 42, 34, 26,
    18, 10,  2, 59, 51, 43, 35,
    62, 54, 46, 38, 30, 22, 14,
     6, 61, 53, 45, 37, 29, 21,
    13,  5, 60, 52, 44, 36, 28,
    20, 12,  4, 27, 19, 11,  3
]

PERMUTED_CHOICE_2 = [
    13, 16, 10, 23,  0,  4,
     2, 27, 14,  5, 20,  9,
    22, 18, 11,  3, 25,  7,
    15,  6, 26, 19, 12,  1,
    40, 51, 30, 36, 46, 54,
    29, 39, 50, 44, 32, 47,
    43, 48, 38, 55, 33, 52,
    45, 41, 49, 35, 28, 31
]

LEFT_SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

INITIAL_PERMUTATION = [
    57, 49, 41, 33, 25, 17,  9,  1,
    59, 51, 43, 35, 27, 19, 11,  3,
    61, 53, 45, 37, 29, 21, 13,  5,
    63, 55, 47, 39, 31, 23, 15,  7,
    56, 48, 40, 32, 24, 16,  8,  0,
    58, 50, 42, 34, 26, 18, 10,  2,
    60, 52, 44, 36, 28, 20, 12,  4,
    62, 54, 46, 38, 30, 22, 14,  6
]

INVERSE_INITIAL_PERMUTATION = [
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25,
    32,  0, 40,  8, 48, 16, 56, 24
]

EXPANSION_TABLE = [
    31,  0,  1,  2,  3,  4,
     3,  4,  5,  6,  7,  8,
     7,  8,  9, 10, 11, 12,
    11, 12, 13, 14, 15, 16,
    15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24,
    23, 24, 25, 26, 27, 28,
    27, 28, 29, 30, 31,  0
]

SBOXES = [
    # S0
    [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
      0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
      4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
     15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13],

    # S2
    [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
      3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
      0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
     13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9],

    # S3
    [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
     13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
     13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
      1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12],

    # S4
    [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
     13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
     10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
      3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14],

    # S5
    [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
     14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
      4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
     11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3],

    # S6
    [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
     10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
      9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
      4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13],

    # S7
    [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
     13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
      1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
      6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12],

    # S8
    [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
      1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
      7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
      2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11],
]

CIPHER_PERMUTATION = [
    15,  6, 19, 20, 28, 11,
    27, 16,  0, 14, 22, 25,
     4, 17, 30,  9,  1,  7,
    23, 13, 31, 26,  2,  8,
    18, 12, 29,  5, 21, 10,
     3, 24
]



def encrypt(block, key):
    return cipher(block, key_schedule(key))

def decrypt(block, key):
    keys = key_schedule(key)
    keys.reverse()
    return cipher(block, keys)

def cipher(block, keys):
    permuted_block = initial_permutation(block)
    [left, right] = get_blocks(permuted_block, 64, 32)

    for i in range(0,14, 2):
        (left, right) = double_round(left, right, keys[i], keys[i + 1])

    final_left = left ^ cipher_function(right, keys[14])
    final_right = right ^ cipher_function(final_left, keys[15])

    return final_permutation(combine([final_right, final_left], 32))

def initial_permutation(block):
    return permute(block, INITIAL_PERMUTATION, 64)

def final_permutation(block):
    return permute(block, INVERSE_INITIAL_PERMUTATION, 64)

## ROUND FUNCTION

def double_round(left0, right0, key0, key1):
    right1 = left0 ^ cipher_function(right0, key0)
    right2 = right0 ^ cipher_function(right1, key1)

    return (right1, right2)


def cipher_function(block, key):
    expanded_block = expand(block) ^ key
    blocks = get_blocks(expanded_block, 48, 6)

    sbox_result = 0
    for i in range(len(blocks)):
        sbox_result = (sbox_result << 4) | sbox(blocks[i], i)

    output = cipher_permutation(sbox_result)
    return output

def expand(block):
    return permute(block, EXPANSION_TABLE, 32)

def cipher_permutation(block):
    return permute(block, CIPHER_PERMUTATION, 32)

def sbox(block, box):
    row = (block & 0x20) >> 4 | (block & 0x1)
    col = (block & 0x1E) >> 1

    return SBOXES[box][16 * row + col]

## KEY SCHEDULE

# verified
def key_schedule(key):
    keys = [0] * 16
    permuted_key = permute(key, PERMUTED_CHOICE_1, 64)
    [C, D] = get_blocks(permuted_key, 56, 28)
    for i in range(len(keys)):
        C = rotl(C, 28, LEFT_SHIFTS[i])
        D = rotl(D, 28, LEFT_SHIFTS[i])
        keys[i] = permute(combine([C, D], 28), PERMUTED_CHOICE_2, 56)

    return keys

# verified
def generate_key():
    key = getrandbits(56)
    blocks = get_blocks(key, 56, 7)
    key_parity = combine([add_odd_parity_bit(x) for x in blocks], 8)
    return key_parity

# verified
def add_odd_parity_bit(block):
    bit = 0x0
    for i in range(7):
        if (block & (1 << i)) == 0:
            bit ^=0x1

    return (block << 1) | bit

## UTILS

#verified
# Permute: int, int[] -> int
# Permute takes an integer and permutes the first 64 bits of it according
# to the permutation given. Bits are numbered 0..63 from left to right.
def permute(block, permutation, block_length):
    permuted_block = 0

    for index in permutation:
        bit = (block & (1 << (block_length - index - 1))) >> (block_length - index - 1)
        permuted_block = (permuted_block << 1) | bit

    return permuted_block

#verified
def rotl(block, block_length, rotation):
    mask = ((2 ** rotation) - 1) << (block_length - rotation)
    rot_bits = (block & mask) >> (block_length - rotation)
    return ((block << rotation) | rot_bits) & (2 ** block_length - 1)

#verified
def get_blocks(input, input_length, block_size):
    num_blocks = input_length // block_size

    blocks = [0] * num_blocks
    mask = (2 ** block_size) - 1

    for i in range(num_blocks):
        shift = (num_blocks - 1 - i) * block_size
        blocks[i] = (input & (mask << shift)) >> shift

    return blocks

# Combintes b0, b1, ..., bn into b0||b1||...||bn
def combine(blocks, block_length):
    output = 0
    for b in blocks:
        output = (output << block_length) | b

    return output

def main():
    key = 0x1046913489980131
    plain = 0x0000000000000000

    encrypted = encrypt(plain, key)
    print(hex(encrypted))
    print(hex(decrypt(encrypted, key)))

if __name__ == "__main__":
    main()
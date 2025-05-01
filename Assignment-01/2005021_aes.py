from BitVector import *
import sys
sys.path.append("./BitVector-3.5.0/BitVector")

LEFT = 0
RIGHT = 1
WORD_SIZE = 4
WORD_PER_KEY = 4
BLOCK_SIZE = 16
AES_modulus = BitVector(bitstring='100011011') # AES modulus

Sbox = (
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

InvSbox = (
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

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]

# Function to convert a string to a bit vector
def convet_to_bitvector(key: str):
    # Convert key to bytes
    return [BitVector(textstring=char) for char in key]

# Function to convert a bit vector to a string
def print_bitvector_as_ascii(key: list):
    for bitvector in key:
        # Convert each byte to its ASCII representation
        print(bitvector.get_bitvector_in_ascii(), end="")
    print()

# Function to convert a bit vector to a hex string
def print_bitvector_as_hex(key: list):
    for bitvector in key:
        # Convert each byte to its hex representation
        print(bitvector.get_bitvector_in_hex(), end=" ")
    print()

# Padding function to ensure the key is a multiple of 16 bytes
def pad_text(plain_text: list):
    # Pad the text to be a multiple of 16 bytes
    block_size = 16
    padding_length = block_size - (len(plain_text) % block_size)
    # If the length is already a multiple of 16, padding_length is 16
    if padding_length == 0:
        padding_length = block_size
    # Pad with the length of the padding
    padding = [BitVector(intVal=padding_length, size=8)] * padding_length
    # Append the padding to the plaintext
    text = plain_text + padding

    return text

# Take input key and plaintext
def input_and_preprocess(padding: bool = False):
    # key = input("Key:\nIn ASCII: ")
    key = "Thats my Kung Fu"
    print("Key:\nIn ASCII: ", key)
    # Check if the key length is valid
    if len(key) * 8 != 128 and len(key) != 192 and len(key) != 256:
        raise ValueError("Key length must be 128, 192, or 256 bits.")
    # Convert key to bytes
    key = convet_to_bitvector(key)
    print("In HEX:", end=" ")
    print_bitvector_as_hex(key)
    print()
    # plain_text = input("Plain Text:\nIn ASCII: ")
    plain_text = "Two One Nine Two"
    print("Plain Text:\nIn ASCII: ", plain_text)
    plain_text = convet_to_bitvector(plain_text)
    print("In HEX:", end=" ")
    print_bitvector_as_hex(plain_text)
    # Pad the plaintext
    if padding:
        plain_text = pad_text(plain_text)
        print("In ASCII(after padding):", end=" ")
        print_bitvector_as_ascii(plain_text)
        print("In HEX(after padding):", end=" ")
        print_bitvector_as_hex(plain_text)
        print()
    return key, plain_text

# Function to get the number of rounds for AES based on key length
def get_round_counts(key_length: int):
    # Determine the number of rounds based on key length
    if key_length == 128:
        round_counts = 10
    elif key_length == 192:
        round_counts = 12
    elif key_length == 256:
        round_counts = 14
    else:
        raise ValueError("Invalid key length. Must be 128, 192, or 256 bits.")
    return round_counts

# This function generates the round constants for AES key schedule.
def generate_round_constants(count: int):
    # Generate round constants
    constants = [BitVector(intVal=1, size=8)]
    for i in range(1, count):
        constants.append(constants[i-1].deep_copy())
        # Left shift the value by 1
        constants[i].shift_left_by_one()
        # If the value is greater than or equal to 128, XOR with 0x11B
        if constants[i-1] >= BitVector(intVal=128, size=8):
            constants[i] = constants[i] ^ BitVector(intVal=0x1B, size=8)

    # Convert constants to round constants
    # Initialize with 0 at index 0 to match the AES standard
    round_constants = [[BitVector(size=8), BitVector(size=8),
                        BitVector(size=8), BitVector(size=8)]]
    for i in range(count):
        round_constants.append([constants[i], BitVector(size=8),
                        BitVector(size=8), BitVector(size=8)])

    return round_constants

def rotate_word(word: list[BitVector], n: int, direction: int):
    # Rotate left a word by n byes
    if direction == LEFT:
        return word[n:] + word[:n]
    elif direction == RIGHT:
        return word[-n:] + word[:-n]
    else:
        raise ValueError("Invalid direction. Use LEFT or RIGHT.")

def substitute_word(word: list[BitVector]):
    # Substitute each byte in the word using Sbox
    result = []
    for b in word:
        # Convert to int if it's a character
        result.append(BitVector(intVal=Sbox[b.intValue()], size=8))
    return result

def XOR(a: list[BitVector], b: list[BitVector]):
    # XOR two lists of bytes
    return [a[i] ^ b[i] for i in range(len(a))]

# Key schedule function
def key_schedule(key: list[BitVector], round_key_count: int, round_constants: list[list[BitVector]]):
    original_key_word_count = len(key) // WORD_SIZE

    # Convert key to 4-byte words
    original_key_words = []
    for i in range(original_key_word_count):
        word = []
        for j in range(WORD_SIZE):
            word.append(key[WORD_SIZE * i + j])
        original_key_words.append(word)

    # Generate round keys
    extended_key_words = []

    # Extend the keys
    for i in range(round_key_count * WORD_PER_KEY):
        if i < original_key_word_count:
            extended_key_words.append(original_key_words[i])
        else:
            # Generate new word
            temp = extended_key_words[i - 1]
            if i % original_key_word_count == 0:
                # Rotate and substitute
                temp = rotate_word(temp, 1, LEFT)
                temp = substitute_word(temp)
                temp = XOR(temp, extended_key_words[i - original_key_word_count])
                temp = XOR(temp, round_constants[i // original_key_word_count])
            elif original_key_word_count > 6 and i % original_key_word_count == 4:
                # Substitute
                temp = substitute_word(temp)
                temp = XOR(temp, extended_key_words[i - original_key_word_count])
            else:
                # Just XOR with previous word
                temp = XOR(temp, extended_key_words[i - original_key_word_count])
            extended_key_words.append(temp)

    # Convert extended key words to round keys
    round_keys = []
    for i in range(round_key_count):
        round_key = []
        for j in range(WORD_PER_KEY):
            round_key.append(extended_key_words[i * WORD_PER_KEY + j])
        # transpose the round key
        round_key = [list(x) for x in zip(*round_key)]
        round_keys.append(round_key)

    return round_keys

# Function to print a block
def print_block(block: list[list[BitVector]]):
    for row in block:
        for b in row:
            print(b.get_bitvector_in_hex(), end=" ")
        print()
    print()

# Function to perform the SubBytes step
def sub_bytes(plain_tex_blockt: list[list[BitVector]]):
    # Substitute each byte in the block using Sbox
    for i in range(WORD_PER_KEY):
        for j in range(WORD_SIZE):
            plain_tex_blockt[i][j] = BitVector(intVal=Sbox[plain_tex_blockt[i][j].intValue()], size=8)
    return plain_tex_blockt

# Function to perform the ShiftRows step
def shift_rows(plain_tex_blockt: list[list[BitVector]]):
    # Shift rows of the block
    for i in range(1, WORD_PER_KEY):
        plain_tex_blockt[i] = rotate_word(plain_tex_blockt[i], i, LEFT)
    return plain_tex_blockt

# Function to perform the MixColumns step
def mix_columns(plain_tex_blockt: list[list[BitVector]]):
    result = []
    # Mix columns of the block
    for i in range(WORD_PER_KEY):
        temp = [BitVector(size=8) for _ in range(WORD_PER_KEY)]
        for j in range(WORD_SIZE):
            for k in range(WORD_SIZE):
                temp[j] ^= Mixer[i][k].gf_multiply_modular(plain_tex_blockt[k][j], AES_modulus, 8)
        result.append(temp)
    return result

# Function to add round keys to the plaintext
def add_round_key(plain_tex_blockt: list[list[BitVector]], round_key: list[list[BitVector]]):
    # XOR the plaintext with the round key
    for i in range(WORD_PER_KEY):
        for j in range(WORD_SIZE):
            plain_tex_blockt[i][j] = plain_tex_blockt[i][j] ^ round_key[i][j]
    # print_block(plain_tex_blockt)
    return plain_tex_blockt

# Function to encrypt a 128-block of plaintext
def encrypt_block(block: list[list[BitVector]], round_keys: list[list[list[BitVector]]]):
    # Add round key initially
    block = add_round_key(block, round_keys[0])

    round_count = len(round_keys)
    # Perform 9 rounds of encryption
    for i in range(1, round_count - 1):
        block = sub_bytes(block)
        block = shift_rows(block)
        block = mix_columns(block)
        block = add_round_key(block, round_keys[i])

    # Perform the last round without MixColumns
    block = sub_bytes(block)
    block = shift_rows(block)
    block = add_round_key(block, round_keys[round_count - 1])

    return block

# Function to convet text to 4x4 blocks
def convert_text_to_blocks(text: list[BitVector]):
    # Divide the plaintext into 4x4 blocks
    text_blocks = []
    for i in range(0, len(text), BLOCK_SIZE):
        block = []
        for j in range(WORD_PER_KEY):
            word = []
            for k in range(WORD_SIZE):
                word.append(text[i + WORD_SIZE * j + k])
            block.append(word)
        # transpose the block
        block = [list(x) for x in zip(*block)]
        text_blocks.append(block)

    return text_blocks

# Function to convert 4x4 blocks to plain text
def convert_blocks_to_text(blocks: list[list[list[BitVector]]]):
    # Convert the blocks to text
    text = []
    for block in blocks:
        # transpose the block
        block = [list(x) for x in zip(*block)]
        for i in range(WORD_PER_KEY):
            for j in range(WORD_SIZE):
                text.append(block[i][j])

    return text


# Function to encrypt the plaintext using the round keys
def encrypt_plain_text(plain_text: list[BitVector], round_keys: list[list[list[BitVector]]]):
    # Divide the plaintext into 4x4 blocks
    plain_text_blocks = convert_text_to_blocks(plain_text)

    # store the encrypted blocks
    encrypted_blocks = []

    # Encrypt each block
    for block in plain_text_blocks:
        encrypted_block = encrypt_block(block, round_keys)
        encrypted_blocks.append(encrypted_block)

    cypher_text = convert_blocks_to_text(encrypted_blocks)

    return cypher_text
        
if __name__ == "__main__":
    key, plain_text = input_and_preprocess()
    key_length = len(key) * 8
    round_count = get_round_counts(key_length)
    round_key_count = round_count + 1
    round_constants_count = (round_count * 4) // (key_length // 32)
    round_constants = generate_round_constants(round_constants_count)

    round_keys = key_schedule(key, round_key_count, round_constants)

    cipher_text = encrypt_plain_text(plain_text, round_keys)

    print("Cipher Text:", end=" ")
    print_bitvector_as_hex(cipher_text)

# Cipher Text: 29 c3 50 5f 57 14 20 f6 40 22 99 b3 1a 02 d7 3a 
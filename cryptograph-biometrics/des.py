# des.py
# Pure Python implementation of DES (Data Encryption Standard)
# Supports block-by-block operations, key schedule, S-Boxes, and CBC mode for files.

# --- DES Permutation Tables and Constants ---

# Initial Permutation (IP)
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Final Permutation (IP^-1)
IP_INV = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9,  49, 17, 57, 25
]

# Expansion Function (E)
E = [
    32, 1,  2,  3,  4,  5,
    4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# Permutation P
P = [
    16, 7,  20, 21,
    29, 12, 28, 17,
    1,  15, 23, 26,
    5,  18, 31, 10,
    2,  8,  24, 14,
    32, 27, 3,  9,
    19, 13, 30, 6,
    22, 11, 4,  25
]

# Permuted Choice 1 (PC-1)
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
]

# Permuted Choice 2 (PC-2)
PC2 = [
    14, 17, 11, 24, 1,  5,
    3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,
    16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Left Shift Schedule
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# S-Boxes (1 to 8)
S_BOXES = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 8, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]


# --- Helper functions for Bit manipulation ---

def permute(block, table):
    """Permute a block (list of bits or integer) using a table."""
    return [block[x - 1] for x in table]


def text_to_bits(text):
    """Convert string of characters into a list of 0s and 1s."""
    bits = []
    for char in text.encode('utf-8'):
        for i in range(8):
            bits.append((char >> (7 - i)) & 1)
    return bits


def bits_to_text(bits):
    """Convert a list of bits back into a string."""
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        bytes_list.append(byte)
    return bytes(bytes_list).decode('utf-8', errors='ignore')


def bytes_to_bits(data):
    """Convert bytes into a list of bits."""
    bits = []
    for byte in data:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
    return bits


def bits_to_bytes(bits):
    """Convert a list of bits into bytes."""
    byte_arr = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        byte_arr.append(byte)
    return bytes(byte_arr)


def hex_to_bits(hex_str):
    """Convert a hexadecimal string to a list of bits."""
    bits = []
    for char in hex_str:
        val = int(char, 16)
        for i in range(4):
            bits.append((val >> (3 - i)) & 1)
    return bits


def bits_to_hex(bits):
    """Convert a list of bits to a hexadecimal string."""
    hex_chars = []
    for i in range(0, len(bits), 4):
        val = 0
        for j in range(4):
            val = (val << 1) | bits[i + j]
        hex_chars.append(f"{val:X}")
    return "".join(hex_chars)


# --- Core DES Round Functionality ---

def shift_left(key_half, n):
    """Circular left shift on key half (28 bits)."""
    return key_half[n:] + key_half[:n]


def generate_round_keys(key_bits):
    """Generate sixteen 48-bit round keys from a 64-bit key."""
    # Apply PC-1 to reduce key from 64-bit to 56-bit
    pc1_key = permute(key_bits, PC1)
    
    # Split into two 28-bit halves
    c0 = pc1_key[:28]
    d0 = pc1_key[28:]
    
    round_keys = []
    c, d = c0, d0
    for shift_amount in SHIFT_SCHEDULE:
        c = shift_left(c, shift_amount)
        d = shift_left(d, shift_amount)
        # Apply PC-2 to compress combined 56 bits into 48 bits
        round_keys.append(permute(c + d, PC2))
    return round_keys


def feistel_f(r_half, round_key):
    """The Feistel function (f)."""
    # 1. Expand 32 bits to 48 bits using Expansion Table E
    expanded = permute(r_half, E)
    
    # 2. XOR with Round Key
    xored = [bit ^ key_bit for bit, key_bit in zip(expanded, round_key)]
    
    # 3. Put through 8 S-Boxes (each takes 6 bits, yields 4 bits)
    s_output = []
    for i in range(8):
        # Extract 6 bits for S-Box i
        s_input = xored[i * 6 : (i + 1) * 6]
        # Row is determined by 1st and 6th bit
        row = (s_input[0] << 1) | s_input[5]
        # Column is determined by middle 4 bits (2nd, 3rd, 4th, 5th)
        col = (s_input[1] << 3) | (s_input[2] << 2) | (s_input[3] << 1) | s_input[4]
        
        val = S_BOXES[i][row][col]
        # Convert val (0-15) to 4 bits
        for j in range(4):
            s_output.append((val >> (3 - j)) & 1)
            
    # 4. Permute with table P
    return permute(s_output, P)


def des_block_encrypt(block_bits, round_keys):
    """Encrypt a single 64-bit block."""
    # 1. Initial Permutation
    ip_block = permute(block_bits, IP)
    
    # Split into 32-bit halves
    l_half = ip_block[:32]
    r_half = ip_block[32:]
    
    # 16 Rounds
    for i in range(16):
        temp_l = r_half
        # f(R_i, K_i) XOR L_i
        f_out = feistel_f(r_half, round_keys[i])
        temp_r = [a ^ b for a, b in zip(l_half, f_out)]
        
        l_half = temp_l
        r_half = temp_r
        
    # Combine (R_16 + L_16) - Note the swap at the final round
    combined = r_half + l_half
    
    # Final Permutation (IP^-1)
    return permute(combined, IP_INV)


def des_block_decrypt(block_bits, round_keys):
    """Decrypt a single 64-bit block (uses round keys in reverse)."""
    # Simply reverse the round keys
    return des_block_encrypt(block_bits, round_keys[::-1])


# --- Block Cipher Modes and Padding ---

def pkcs7_pad(data, block_size=8):
    """PKCS#7 Padding."""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def pkcs7_unpad(data):
    """PKCS#7 Unpadding."""
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 8:
        raise ValueError("Invalid padding bytes")
    # Verify all padding bytes are matching
    for i in range(len(data) - pad_len, len(data)):
        if data[i] != pad_len:
            raise ValueError("Padding mismatch")
    return data[:-pad_len]


# CBC (Cipher Block Chaining) Mode
# IV is set to a fixed 64-bit block for simplicity in the lab, but can be customized.
DEFAULT_IV_HEX = "0123456789ABCDEF"

def des_cbc_encrypt(plaintext_bytes, key_hex, iv_hex=DEFAULT_IV_HEX):
    """Encrypt arbitrary bytes using DES in CBC mode."""
    # 1. Pad plaintext
    padded = pkcs7_pad(plaintext_bytes)
    
    key_bits = hex_to_bits(key_hex)
    iv_bits = hex_to_bits(iv_hex)
    round_keys = generate_round_keys(key_bits)
    
    ciphertext_bits = []
    prev_cipher_block = iv_bits
    
    # Process 8 bytes (64 bits) at a time
    for i in range(0, len(padded), 8):
        block_bytes = padded[i : i + 8]
        block_bits = bytes_to_bits(block_bytes)
        
        # XOR with previous ciphertext block (CBC Mode)
        xored_bits = [b ^ prev for b, prev in zip(block_bits, prev_cipher_block)]
        
        # Encrypt block
        cipher_block = des_block_encrypt(xored_bits, round_keys)
        
        # Store block
        ciphertext_bits.extend(cipher_block)
        prev_cipher_block = cipher_block
        
    return bits_to_bytes(ciphertext_bits)


def des_cbc_decrypt(ciphertext_bytes, key_hex, iv_hex=DEFAULT_IV_HEX):
    """Decrypt arbitrary bytes using DES in CBC mode."""
    if len(ciphertext_bytes) % 8 != 0:
        raise ValueError("Ciphertext length must be a multiple of 8 bytes")
        
    key_bits = hex_to_bits(key_hex)
    iv_bits = hex_to_bits(iv_hex)
    round_keys = generate_round_keys(key_bits)
    
    plaintext_bits = []
    prev_cipher_block = iv_bits
    
    # Convert ciphertext to bits
    cipher_bits = bytes_to_bits(ciphertext_bytes)
    
    for i in range(0, len(cipher_bits), 64):
        cipher_block = cipher_bits[i : i + 64]
        
        # Decrypt block
        decrypted_block = des_block_decrypt(cipher_block, round_keys)
        
        # XOR with previous ciphertext block
        plain_block = [b ^ prev for b, prev in zip(decrypted_block, prev_cipher_block)]
        
        plaintext_bits.extend(plain_block)
        prev_cipher_block = cipher_block
        
    plaintext_bytes = bits_to_bytes(plaintext_bits)
    return pkcs7_unpad(plaintext_bytes)


# --- File Utilities ---

def encrypt_file(input_path, output_path, key_hex):
    """Reads a file, encrypts it with DES, and writes it to another file."""
    with open(input_path, 'rb') as f:
        plaintext = f.read()
    ciphertext = des_cbc_encrypt(plaintext, key_hex)
    with open(output_path, 'wb') as f:
        f.write(ciphertext)


def decrypt_file(input_path, output_path, key_hex):
    """Reads an encrypted file, decrypts it with DES, and writes it back."""
    with open(input_path, 'rb') as f:
        ciphertext = f.read()
    plaintext = des_cbc_decrypt(ciphertext, key_hex)
    with open(output_path, 'wb') as f:
        f.write(plaintext)


# --- Basic verification test when executed directly ---
if __name__ == "__main__":
    # Test key (64 bits, i.e., 16 hex characters)
    test_key = "133457799BBCDFF1"
    
    message = b"This is a secret message. Cryptography is fun!"
    print(f"Original: {message.decode()}")
    
    # Encrypt
    encrypted = des_cbc_encrypt(message, test_key)
    print(f"Encrypted (Hex): {encrypted.hex().upper()}")
    
    # Decrypt
    decrypted = des_cbc_decrypt(encrypted, test_key)
    print(f"Decrypted: {decrypted.decode()}")
    
    assert decrypted == message, "DES test failed!"
    print("DES implementation is fully working and correct!")

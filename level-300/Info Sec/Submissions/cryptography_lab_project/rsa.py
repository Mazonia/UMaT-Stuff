# rsa.py
# Pure Python implementation of RSA cryptography.
# Supports generating primes (via Miller-Rabin), key generation, modular arithmetic,
# and encryption/decryption of text strings.

import random

# --- Mathematical Helpers ---

def gcd(a, b):
    """Euclidean algorithm to find the greatest common divisor."""
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    """Extended Euclidean algorithm to find Bezout coefficients."""
    old_s, s = 1, 0
    old_t, t = 0, 1
    old_r, r = a, b
    
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
        
    return old_r, old_s, old_t


def mod_inverse(e, phi):
    """Find modular inverse of e modulo phi."""
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % phi


def is_prime_miller_rabin(n, k=20):
    """Miller-Rabin primality test. Returns True if n is probably prime."""
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
        
    # Write n - 1 as 2^r * d
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
        
    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
            
        is_composite = True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                is_composite = False
                break
        if is_composite:
            return False
            
    return True


def generate_prime(bits):
    """Generate a random prime number of the specified bit length."""
    if bits < 3:
        raise ValueError("Bit size must be at least 3 to generate a prime.")
    while True:
        # Ensure it has the correct bit length and is odd
        num = random.getrandbits(bits)
        num |= (1 << (bits - 1)) | 1
        if is_prime_miller_rabin(num):
            return num


# --- Core RSA Key Generation ---

def generate_keypair(bits):
    """Generate RSA public and private keypairs."""
    # Bits represents the bit-size of each prime (p and q)
    # Total key size N will be approximately 2 * bits
    p = generate_prime(bits)
    q = generate_prime(bits)
    
    # Ensure p and q are not identical
    while q == p:
        q = generate_prime(bits)
        
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose E. Commonly 65537 is used.
    # If 65537 is larger than phi or shares factors with phi, find another coprime.
    e = 65537
    if e >= phi or gcd(e, phi) != 1:
        # Search for a suitable small odd coprime
        e = 3
        while gcd(e, phi) != 1:
            e += 2
            
    d = mod_inverse(e, phi)
    
    # Public key is (e, n), Private key is (d, n)
    # Returns (p, q, n, e, d)
    return p, q, n, e, d


# --- RSA Encryption / Decryption ---

def rsa_encrypt(plaintext, e, n):
    """
    Encrypt text using RSA.
    Performs byte-by-byte encryption to match the school lab specification.
    For each byte m, calculates c = m^e mod n.
    """
    bytes_data = plaintext.encode('utf-8')
    ciphertext = [pow(m, e, n) for m in bytes_data]
    return ciphertext


def rsa_decrypt(ciphertext, d, n):
    """
    Decrypt RSA ciphertext back to text.
    For each encrypted integer c, calculates m = c^d mod n.
    """
    decrypted_bytes = bytearray(pow(c, d, n) for c in ciphertext)
    return decrypted_bytes.decode('utf-8', errors='ignore')


# --- Verification Test ---
if __name__ == "__main__":
    print("Testing RSA Key Generation for different bit sizes...")
    for bit_size in [8, 16, 32, 64, 128]:
        p, q, n, e, d = generate_keypair(bit_size)
        print(f"\nBit size: {bit_size}")
        print(f"p: {p}")
        print(f"q: {q}")
        print(f"N (p*q): {n}")
        print(f"E (public exponent): {e}")
        print(f"D (private exponent): {d}")
        
        # Verify encryption/decryption
        msg = "Hello RSA!"
        cipher = rsa_encrypt(msg, e, n)
        decrypted = rsa_decrypt(cipher, d, n)
        print(f"Ciphertext list: {cipher}")
        print(f"Decrypted: '{decrypted}'")
        assert decrypted == msg, f"RSA failed for bit size {bit_size}"
        
    print("\nRSA implementation is fully working and correct!")

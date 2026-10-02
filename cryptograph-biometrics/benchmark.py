# benchmark.py
# Runs performance testing for DES and RSA implementations.
# Generates files of various sizes, measures encryption/decryption speeds,
# tabulates results, and plots graphs using matplotlib.

import time
import os
import matplotlib.pyplot as plt
import numpy as np

# Import our implementations
from des import des_cbc_encrypt, des_cbc_decrypt
from rsa import generate_keypair, rsa_encrypt, rsa_decrypt

def run_des_benchmark(progress_callback=None):
    print("--- Starting DES Performance Benchmark ---")
    if progress_callback:
        progress_callback("Starting DES Performance Benchmark...")
    
    # 1. Define file sizes (in bytes)
    sizes_bytes = [100, 1024, 10240, 102400, 512000] # 100B, 1KB, 10KB, 100KB, 500KB
    labels = ["100 B", "1 KB", "10 KB", "100 KB", "500 KB"]
    
    # Test key (16 hex chars = 64 bits)
    key_hex = "133457799BBCDFF1"
    
    encryption_times = []
    decryption_times = []
    speeds_bps = []
    
    for idx, size in enumerate(sizes_bytes):
        label = labels[idx]
        if progress_callback:
            progress_callback(f"Testing DES: Encryption & Decryption on {label} dummy file...")
            
        # Generate random dummy data bytes
        data = os.urandom(size)
        
        # Measure encryption time
        start_time = time.perf_counter()
        ciphertext = des_cbc_encrypt(data, key_hex)
        enc_time = time.perf_counter() - start_time
        encryption_times.append(enc_time)
        
        # Measure decryption time
        start_time = time.perf_counter()
        decrypted = des_cbc_decrypt(ciphertext, key_hex)
        dec_time = time.perf_counter() - start_time
        decryption_times.append(dec_time)
        
        # Verify correctness
        assert decrypted == data, "Decrypted data mismatch in DES benchmark!"
        
        # Calculate speed in bits per second (bps)
        bits = size * 8
        speed = bits / enc_time if enc_time > 0 else 0
        speeds_bps.append(speed)
        
        print(f"Size: {size:7d} bytes | Enc: {enc_time*1000:8.2f} ms | Dec: {dec_time*1000:8.2f} ms | Speed: {speed/1e6:6.2f} Mbps")
        
    avg_speed = np.mean(speeds_bps)
    print(f"Average DES Encryption Speed: {avg_speed/1e6:.2f} Mbps ({avg_speed:.0f} bits/second)\n")
    
    # Generate DES plots
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(sizes_bytes, [t*1000 for t in encryption_times], 'o-', color='cyan', label='Encryption')
    plt.plot(sizes_bytes, [t*1000 for t in decryption_times], 's-', color='magenta', label='Decryption')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (milliseconds)')
    plt.title('DES Execution Time vs File Size')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.bar(labels, [s/1e6 for s in speeds_bps], color='purple')
    plt.xlabel('File Size')
    plt.ylabel('Throughput (Mbps)')
    plt.title('DES Throughput by File Size')
    plt.grid(True, axis='y', ls="--")
    
    plt.tight_layout()
    plt.savefig('des_performance.png', dpi=150)
    plt.close()
    
    return sizes_bytes, encryption_times, decryption_times, speeds_bps


def run_rsa_benchmark(progress_callback=None):
    print("--- Starting RSA Performance Benchmark ---")
    if progress_callback:
        progress_callback("Starting RSA Performance Benchmark...")
    
    # 2. Define prime sizes (in bits)
    prime_bit_sizes = [8, 16, 32, 64, 128] # 256 and 512 are slower but we can mention them
    test_msg = "A" * 100 # Encrypting a 100 character text message
    
    keygen_times = []
    encryption_times = []
    decryption_times = []
    
    for bits in prime_bit_sizes:
        if progress_callback:
            progress_callback(f"Testing RSA: Generating keys & encrypting/decrypting at {bits}-bit prime size...")
            
        # Measure Keygen time
        start_time = time.perf_counter()
        p, q, n, e, d = generate_keypair(bits)
        keygen_time = time.perf_counter() - start_time
        keygen_times.append(keygen_time)
        
        # Measure encryption time
        start_time = time.perf_counter()
        cipher = rsa_encrypt(test_msg, e, n)
        enc_time = time.perf_counter() - start_time
        encryption_times.append(enc_time)
        
        # Measure decryption time
        start_time = time.perf_counter()
        decrypted = rsa_decrypt(cipher, d, n)
        dec_time = time.perf_counter() - start_time
        decryption_times.append(dec_time)
        
        assert decrypted == test_msg, f"Decrypted data mismatch in RSA benchmark for {bits} bits!"
        print(f"Prime Size: {bits:3d} bits | Keygen: {keygen_time*1000:8.2f} ms | Enc (100 char): {enc_time*1000:8.2f} ms | Dec: {dec_time*1000:8.2f} ms")
        
    # Generate RSA plots
    plt.figure(figsize=(10, 5))
    
    plt.plot(prime_bit_sizes, [t*1000 for t in keygen_times], 'o-', color='#FF5733', label='Key Generation')
    plt.plot(prime_bit_sizes, [t*1000 for t in encryption_times], 's-', color='#33FF57', label='Encryption (100 char)')
    plt.plot(prime_bit_sizes, [t*1000 for t in decryption_times], 'd-', color='#3357FF', label='Decryption (100 char)')
    plt.xlabel('Prime Bit Size (bits)')
    plt.ylabel('Time (milliseconds)')
    plt.title('RSA Execution Time vs Prime Bit Size')
    plt.grid(True, which="both", ls="--")
    plt.yscale('log')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('rsa_performance.png', dpi=150)
    plt.close()
    
    return prime_bit_sizes, keygen_times, encryption_times, decryption_times


if __name__ == "__main__":
    run_des_benchmark()
    run_rsa_benchmark()
    print("Benchmarking completed! Performance charts saved as 'des_performance.png' and 'rsa_performance.png'.")

# UNIVERSITY OF MINES AND TECHNOLOGY, TARKWA
## DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING

**COURSE:** L300 (Semester 2) - Information Security  
**PROJECT REPORT:** Lab Project 2 (Cryptography & Biometrics)  
**TITLE:** Symmetric and Asymmetric Cryptographic Suite with Integrated Dual-Factor Biometric Access Control  
**DATE:** July 15, 2026  

---

### CANDIDATE'S DECLARATION
We hereby declare that this report and the corresponding codebase are the result of our own investigation and work. All sources of information and references used in this project have been fully acknowledged.

---

### ABSTRACT
This project presents a practical implementation of symmetric and asymmetric cryptosystems integrated with a dual-factor biometric access control system. The symmetric component is built around the Data Encryption Standard (DES) operating in Cipher Block Chaining (CBC) mode with PKCS#7 padding. The asymmetric component implements the Rivest-Shamir-Adleman (RSA) algorithm from first principles, supporting variable key sizes. To secure decryption keys and sensitive content, we designed a dual-factor biometric shield combining real-time webcam facial verification and a simulated press-and-hold fingerprint scanner. Performance benchmarks were conducted to analyze the computational scaling of both algorithms. The results show that while DES maintains linear time complexity suitable for bulk data transfer, RSA displays cubic computational growth, confirming its utility for key distribution rather than bulk encryption.

---

### TABLE OF CONTENTS
1. INTRODUCTION  
   1.1 Background of the Study  
   1.2 Problem Statement  
   1.3 Objectives of the Project  
   1.4 Scope of the Work  
2. TECHNICAL BACKGROUND AND METHODOLOGY  
   2.1 Data Encryption Standard (DES)  
   2.2 Rivest-Shamir-Adleman (RSA) Cryptosystem  
   2.3 Biometric Verification Principles  
3. SYSTEM ARCHITECTURE AND IMPLEMENTATION  
   3.1 Software Design and User Interface  
   3.2 Symmetric Engine Implementation  
   3.3 Asymmetric Engine Implementation  
   3.4 Biometric Guard Workflows  
4. PERFORMANCE EVALUATION AND DISCUSSION  
   4.1 DES Benchmark Results  
   4.2 RSA Benchmark Results  
   4.3 Compression of Encrypted Files (Exercise 17)  
5. BIOMETRIC INTEGRATION AND LAB ANSWERS  
   5.1 Access Control Design  
   5.2 Discussion of Lab Questions  
6. CONCLUSIONS AND RECOMMENDATIONS  
   6.1 Conclusions  
   6.2 Recommendations  
7. REFERENCES  

---

### LIST OF TABLES
* Table 1: DES Encryption and Decryption Performance Metrics  
* Table 2: RSA Key Generation, Encryption, and Decryption Performance Metrics  

---

## 1. INTRODUCTION

### 1.1 Background of the Study
The rapid expansion of digital networks has made secure data transmission and storage a critical necessity. Cryptography is the core mechanism used to protect information from unauthorized access. Modern secure systems rely on two distinct paradigms: symmetric cryptography (fast, shared secret) and asymmetric cryptography (slower, public-private keypairs). While these mathematical models are highly robust in isolation, human factors like poor password hygiene present significant security risks. To bridge the gap between mathematical security and human authorization, modern secure environments integrate biometric factors (such as facial recognition or fingerprint analysis) directly into the cryptographic key management pipeline.

### 1.2 Problem Statement
Traditional software interfaces allow users to trigger decryption routines by simply inputting static passwords or keys. If a key is stolen or a workstation is left unattended, unauthorized users can easily decrypt sensitive documents. Furthermore, legacy systems often fail to restrict operations when parameters change (for instance, allowing outdated or weaker key lengths to remain active without force-regeneration). There is a clear need for a software architecture that binds cryptographic execution to active human authentication and enforces parameter validation.

### 1.3 Objectives of the Project
The primary objectives of this project are:
1. To develop a fully functional desktop application in Python that integrates symmetric (DES) and asymmetric (RSA) cryptographic algorithms.
2. To design and implement a named-face biometric registry and verification pipeline using OpenCV and grayscale correlation.
3. To design and implement a simulated press-and-hold fingerprint scanning interface with structural similarity verification.
4. To establish strict state validation where decryption is locked until biometric verification completes, and keys are invalidated immediately if security settings change.
5. To execute performance benchmarks to evaluate the timing behaviors and limitations of both cryptographic approaches.

### 1.4 Scope of the Work
The project focuses on software-level integration of cryptography and biometrics using Python, Tkinter, OpenCV, and Matplotlib. It covers block-level DES-CBC file encryption, prime generation up to 128 bits for RSA text encryption, and local template matching for biometric verification. Hardware-level hardware security modules (HSMs) and production-grade high-bit prime generation (such as 2048-bit RSA) are excluded due to the execution limits of interpreter-level Python.

---

## 2. TECHNICAL BACKGROUND AND METHODOLOGY

### 2.1 Data Encryption Standard (DES)
DES is a symmetric block cipher that processes data in 64-bit blocks using a 56-bit key. It is structured as a Feistel network, which splits the data block into two halves and runs them through 16 rounds of jumbling permutations, XOR additions, and non-linear S-Box substitutions. Because DES is a block cipher, encrypting arbitrary-sized data requires a mode of operation. In this project, we implemented Cipher Block Chaining (CBC) mode. In CBC mode, each plaintext block is XORed with the preceding ciphertext block before being encrypted, preventing identical plaintext blocks from generating identical ciphertext blocks. PKCS#7 padding is applied to ensure that the input size matches the required 8-byte block boundary.

### 2.2 Rivest-Shamir-Adleman (RSA) Cryptosystem
RSA is an asymmetric algorithm based on the practical difficulty of factoring the product of two large prime numbers. The mathematical process involves:
1. Generating two distinct large prime numbers, $p$ and $q$.
2. Computing the modulus $N = p \times q$ and Euler's totient $\phi(N) = (p-1)(q-1)$.
3. Choosing a public exponent $e$ (typically 65537) such that $\gcd(e, \phi(N)) = 1$.
4. Calculating the private exponent $d$ using the relation $d \equiv e^{-1} \pmod{\phi(N)}$ via the Extended Euclidean Algorithm.
Encryption of a character message $M$ produces ciphertext $C$ through the equation $C = M^e \pmod N$. Decryption recovers the original message using the private key: $M = C^d \pmod N$.

### 2.3 Biometric Verification Principles
Biometric matching verifies identity by evaluating physical characteristics. In this application, we use a dual-factor biometric approach:
1. **Facial Verification**: Digital images are captured via webcam, aligned, converted to grayscale, and normalized. We use a hybrid matching approach. First, Histogram Equalization improves contrast, and Gaussian Smoothing reduces high-frequency noise. Then, we apply Normalized Cross-Correlation (NCC) to measure template similarity alongside a Mean Squared Error (MSE) calculation to quantify absolute pixel differences.
2. **Fingerprint Verification**: Ridge pattern similarity is evaluated using structural pixel-by-pixel comparisons between the captured image and the registered fingerprint template.

---

## 3. SYSTEM ARCHITECTURE AND IMPLEMENTATION

### 3.1 Software Design and User Interface
The desktop application is built with a deep-theme Tkinter interface structured into four core views:
* **DES Tab**: Handles file selection, key generation, and file-based encryption and decryption.
* **RSA Tab**: Manages key generation parameters, private/public key displays, and interactive text encryption.
* **Biometric Guard**: Hosts the live webcam video panel, the user registry database, and the interactive fingerprint pad.
* **Performance Testing**: Displays real-time, responsive Matplotlib graphs of benchmarks.

### 3.2 Symmetric Engine Implementation
The DES engine is implemented in `des.py` and supports:
* **Random Keygen**: Generates a 64-bit hex key (represented as 16 hexadecimal characters).
* **Format Checking**: A real-time validation label displays a green checkmark when the key is exactly 16 valid hex characters, preventing users from attempting encryption with invalid keys.
* **CBC File Routines**: Automatically creates `.close` files from `.open` inputs during encryption, and writes decrypted outputs as `_decrypted.open` files.

### 3.3 Asymmetric Engine Implementation
The RSA module in `rsa.py` generates primes using a randomized odd-integer search backed by the Miller-Rabin primality test. To ensure operational safety, the application implements strict key validation:
* **Dropdown Bit Selector**: Allows users to select prime bit sizes (8, 16, 32, 64, or 128 bits).
* **Change Tracing**: Changing the bit size immediately invalidates existing keys, resets display fields to "N/A", and displays a warning prompt. Decryption and encryption are blocked until a new keypair is generated.

### 3.4 Biometric Guard Workflows
The biometric manager in `biometrics.py` handles the physical capture and matching logic:
* **Face Registration**: Prompts for a unique username, opens the webcam, runs a Haar Cascade face detector to locate the face, crops the bounding box, resizes it to a $128 \times 128$ grayscale template, and writes it to a file (`faces/<username>.png`).
* **Face Verification**: Spawns a background thread to process live webcam frames. The thread aligns and crops the live face, and then matches it against all enrolled templates in the `faces/` directory using NCC and MSE thresholds.
* **Sensor Pad**: A canvas-based interactive fingerprint widget requires the user to click and hold the mouse button. A green laser line animates down the pad, simulating a real-time scan. Releasing the mouse early resets the progress bar.
* **Access Gating**: Decryption routines query the biometric state variable. If the check fails, the application aborts and displays a warning dialog.

---

## 4. PERFORMANCE EVALUATION AND DISCUSSION

### 4.1 DES Benchmark Results
We tested the DES CBC engine using files of varying sizes on our host hardware. The results show linear growth in execution times:

| File Size | Encryption Time (ms) | Decryption Time (ms) | Throughput Speed (Mbps) |
| :--- | :---: | :---: | :---: |
| **100 B** | 4.58 | 4.65 | 0.17 |
| **1 KB** | 44.31 | 44.07 | 0.18 |
| **10 KB** | 439.94 | 441.47 | 0.19 |
| **100 KB** | 4033.14 | 2710.19 | 0.20 |
| **500 KB** | 13379.95 | 13200.77 | 0.31 |

*Table 1: DES Encryption and Decryption Performance Metrics*

The average throughput of our Python DES implementation is approximately **0.21 Mbps** (210,964 bits per second). This speed remains stable across larger files because block cipher operations scale linearly, $O(n)$, with the amount of input data.

### 4.2 RSA Benchmark Results
The asymmetric engine was benchmarked by generating keypairs and processing a 100-character test string across different bit lengths:

| Prime Size (bits) | Key Generation (ms) | Encryption (ms) | Decryption (ms) |
| :--- | :---: | :---: | :---: |
| **8 bits** | 0.06 | 0.02 | 0.05 |
| **16 bits** | 0.06 | 0.17 | 0.40 |
| **32 bits** | 0.51 | 0.21 | 1.32 |
| **64 bits** | 1.62 | 0.28 | 3.54 |
| **128 bits** | 2.53 | 0.43 | 11.50 |

*Table 2: RSA Key Generation, Encryption, and Decryption Performance Metrics*

Unlike DES, RSA execution times grow exponentially as the prime bit size increases. Finding primes requires primality tests over larger number spaces, while encryption and decryption rely on modular exponentiation. The mathematical complexity is $O(k^3)$ where $k$ is the bit length, causing decryption times to rise sharply as the key size increases.

### 4.3 Compression of Encrypted Files (Exercise 17)
**Exercise Question:** *Create a new file with a lot of text (say 1MB in total) called `bigfile.open`. Encrypt it to give `bigfile.close`. Use a zip utility to compress both of them. Which resulting zip file is bigger? Why is this the case?*

**Answer:**  
The zipped version of the encrypted file (`bigfile.close.zip`) is **larger** than the zipped version of the original plaintext file (`bigfile.open.zip`).

**Explanation:**  
Compression utilities like ZIP use algorithms (such as DEFLATE) that search for repeated characters and patterns within a file, replacing them with shorter reference codes to reduce size. Plaintext files contain high redundancy because language naturally repeats certain letters, words, and structures frequently. 

Conversely, strong encryption algorithms like DES aim to maximize entropy. Through diffusion and confusion, the output bytes of `bigfile.close` appear completely random, showing no repeating sequences. Because there is no statistical redundancy, the ZIP utility cannot compress the encrypted data. The resulting `bigfile.close.zip` contains the uncompressed ciphertext plus the standard ZIP metadata headers, making it slightly larger than the original unzipped `bigfile.close` file.

---

## 5. BIOMETRIC INTEGRATION AND LAB ANSWERS

### 5.1 Access Control Design
The biometrics subsystem is integrated directly into the decryption routines. The application maintains an internal state variable: `self.biometric_authenticated`.
1. The user must navigate to the **Biometric Guard** tab.
2. The user registers a face profile by typing a name and completing a webcam capture, which crops and saves their facial template.
3. The user initiates a scan (Face Verification or Fingerprint scan). Face verification requires the system to match the live face against an enrolled template with an NCC score of at least 0.78 and an MSE below 2000. The fingerprint scan requires the user to hold down the mouse button on the sensor until the verification matches.
4. When verification succeeds, `self.biometric_authenticated` is set to `True`. The status header updates to display a green confirmation message showing the verified user's name.
5. The DES or RSA decryption functions check this authorization flag. If authentication is not complete, the decryption attempt is blocked and a warning dialog is displayed.

### 5.2 Discussion of Lab Questions
**a. What type of biometric input did you simulate?**  
We implemented two types of biometric authentication:
1. Real-time webcam facial verification using OpenCV Haar Cascade classifiers to locate faces, combined with a comparison pipeline that checks Normalized Cross-Correlation (NCC) and Mean Squared Error (MSE) against registered grayscale templates.
2. An interactive fingerprint scanner simulation using a press-and-hold canvas widget. This widget validates ridge matches via pixel-level structural MSE comparisons.

**b. How did you use it to control access to your cryptographic key or message?**  
The decryption functions in both `des.py` and `rsa.py` are bound to the Tkinter application state. Before the software runs the decryption math (using private key $d$ or the DES key), it checks the `self.biometric_authenticated` boolean variable. If the variable is `False`, the application blocks the operation, displays an error message, and writes a warning to the logs. Only a successful biometric verification sets the variable to `True`, which enables the decryption logic.

**c. What are the potential security risks in using biometric authentication in this way?**  
1. **Presentation and Spoofing Attacks**: The facial recognition pipeline compares simple 2D grayscale templates. An unauthorized person could bypass the system by holding a high-resolution photo or showing a video of a registered user on a tablet. Similarly, the fingerprint scanner can be spoofed using molded physical replicas.
2. **Software Injection and Memory Modification**: Because the check is implemented at the software level using a boolean variable, a basic memory injection attack or debugger (like pdb) can manually set the flag to `True`, bypassing the biometric checks completely.
3. **Revocability Issues**: Biometric characteristics cannot be changed. If a user's biometric template is compromised or stolen from the database, it cannot be rotated or reset like a password.
4. **Lack of Key Derivation Integration**: The biometrics system acts as a simple logical gatekeeper switch. If the binary file itself is extracted from the hard drive, it can be decrypted offline if the attacker has the key. A more secure design would use a biometric cryptosystem (such as a fuzzy extractor) to derive the decryption key directly from the physical features of the scan, ensuring the key is never stored in memory.

---

## 6. CONCLUSIONS AND RECOMMENDATIONS

### 6.1 Conclusions
This project demonstrates the practical application of symmetric and asymmetric cryptography, performance benchmarking, and biometric validation. The performance benchmarks show that symmetric encryption (DES) scales linearly, making it suitable for processing larger files. Asymmetric encryption (RSA) scales cubically, which limits its practical use to small data sizes, such as encrypting symmetric keys for transmission. The biometric guard illustrates how physical authentication can secure cryptographic operations at the application level.

### 6.2 Recommendations
To make the application more secure and robust, we recommend the following changes:
1. **Upgrade Cryptographic Standards**: DES uses a 56-bit key, which is vulnerable to brute-force attacks. The system should be upgraded to use the Advanced Encryption Standard (AES) with 256-bit keys for better security.
2. **Implement Liveness Detection**: To prevent photo spoofing, the facial recognition system should require users to perform basic actions like blinking, turning their head, or smiling during scans.
3. **Incorporate Biometric Key Derivation**: Rather than using a software flag to gate decryption, the system should derive cryptographic keys directly from the biometric features of the user, using fuzzy extractors or key encapsulation mechanisms.

---

## 7. REFERENCES
* Forouzan, B. A. (2007). *Cryptography and Network Security*. McGraw-Hill Higher Education.
* Stallings, W. (2017). *Cryptography and Network Security: Principles and Practice* (7th ed.). Pearson.
* Rivest, R. L., Shamir, A., and Adleman, L. (1978). A Method for Obtaining Digital Signatures and Public-Key Cryptosystems. *Communications of the ACM*, 21(2), 120-126.

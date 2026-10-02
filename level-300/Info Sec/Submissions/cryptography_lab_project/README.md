# Cryptography Lab Project: Symmetric & Asymmetric Encryption with Biometric Guard

This project is a comprehensive educational implementation of symmetric and asymmetric cryptography, performance benchmarking, and biometric access control. The application features a graphical user interface (GUI) built with Python and Tkinter.

## Features

### 1. Symmetric Cryptography (DES)
- Full Python implementation of the Data Encryption Standard (DES) using Cipher Block Chaining (CBC) mode.
- Supports encrypting `.open` files and decrypting `.close` files.
- Includes a 64-bit random key generator and live key format validation.

### 2. Asymmetric Cryptography (RSA)
- Custom RSA implementation supporting variable prime bit sizes (8, 16, 32, 64, 128 bits).
- Demonstrates prime number generation (Miller-Rabin primality test) and keypair mathematics ($p, q, N, e, d$).
- Text-based interactive encryption and decryption.

### 3. Biometric Security Guard
- **Facial Registration & Matching**: Uses OpenCV and Haar Cascades for real-time face enrollment. Supports a multi-user registry where faces are saved with unique names and verified using a hybrid matching approach (Histogram Equalization, Gaussian Smoothing, Normalized Cross-Correlation, and Mean Squared Error).
- **Interactive Fingerprint Scanner**: A simulated GUI sensor pad that requires a press-and-hold action.
- **Cryptographic Hook**: Decryption engines for both DES and RSA remain locked until a biometric challenge is successfully passed.

### 4. Performance Benchmarking
- Live Matplotlib integrations to graph and benchmark the throughput speed of DES across varying file sizes.
- Benchmarks RSA execution speeds (Key Generation, Encryption, Decryption) as prime bit sizes scale exponentially.

## Prerequisites

Ensure you have Python 3 installed. You will need the following Python libraries:
- `opencv-python` (cv2)
- `numpy`
- `Pillow` (PIL)
- `matplotlib`

You can install them via pip:
```bash
pip install opencv-python numpy Pillow matplotlib
```

## How to Run

1. Clone the repository to your local machine.
2. Open a terminal or command prompt in the project directory.
3. Run the application:
   ```bash
   python app.py
   ```
4. Navigate through the tabs (DES, RSA, Biometrics, Benchmarks) to explore the features. Note that you must register a face or complete a fingerprint scan in the "Biometric Guard" tab before you can unlock decryption functionalities in the DES and RSA tabs.

## Project Structure
- `app.py`: The main GUI application.
- `des.py`: DES encryption and decryption algorithms.
- `rsa.py`: RSA key generation and encryption/decryption routines.
- `biometrics.py`: Logic for facial recognition and fingerprint simulation.
- `benchmark.py`: Automation scripts for testing and plotting performance data.
- `report.md`: Detailed project report covering mathematical background, testing results, and lab questions.

# format_report.py
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os

def build_report(toc_pages=None):
    doc = docx.Document()
    
    # ----------------------------------------------------
    # SECTION 1: FRONT MATTER (Pages 1 to 3)
    # ----------------------------------------------------
    section1 = doc.sections[0]
    section1.page_width = Inches(8.5)
    section1.page_height = Inches(11.0)
    section1.top_margin = Inches(1.0)
    section1.bottom_margin = Inches(1.0)
    section1.left_margin = Inches(1.0)
    section1.right_margin = Inches(1.0)
    section1.different_first_page_header_footer = True
    
    # Clear default header/footer for section 1
    section1.header.is_linked_to_previous = False
    section1.footer.is_linked_to_previous = False
    section1.header.paragraphs[0].text = ""
    section1.footer.paragraphs[0].text = ""

    # Helpers for paragraph addition
    def add_p(text="", style='Normal', bold=False, italic=False, size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(size)
            run.bold = bold
            run.italic = italic
        return p

    def add_heading(text, level, space_before=12, space_after=6):
        align = WD_ALIGN_PARAGRAPH.LEFT
        size = 14 if level == 1 else (12 if level == 2 else 11)
        p = add_p(text, bold=True, size=size, align=align, space_before=space_before, space_after=space_after)
        p.paragraph_format.keep_with_next = True
        return p

    # --- Page 1: COVER PAGE ---
    add_p("\n\n", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    add_p("UNIVERSITY OF MINES AND TECHNOLOGY, TARKWA", bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", bold=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    
    add_p("PROJECT REPORT: LAB PROJECT 2", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("(CRYPTOGRAPHY & BIOMETRICS)", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    
    add_p("TITLE:", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("SYMMETRIC AND ASYMMETRIC CRYPTOGRAPHIC SUITE WITH INTEGRATED DUAL-FACTOR BIOMETRIC ACCESS CONTROL", 
          bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)
    
    add_p("COURSE: L300 (Semester 2) - Information Security", size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("DATE: JULY 2026", size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=60)
    
    add_p("..................................................", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p("Project Group Candidates", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    
    doc.add_page_break() # End Page 1
    
    # --- Page 2: DECLARATION & ABSTRACT ---
    add_heading("CANDIDATE'S DECLARATION", level=1, space_before=12, space_after=12)
    add_p("We hereby declare that this report and the corresponding codebase are the result of our own investigation and work. "
          "All sources of information and references used in this project have been fully acknowledged.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    add_p("\n\n..................................................\nProject Group Candidates\n\n", align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=36)
    
    add_heading("ABSTRACT", level=1, space_before=24, space_after=12)
    add_p("This project presents a practical implementation of symmetric and asymmetric cryptosystems integrated with a dual-factor biometric access control system. "
          "The symmetric component is built around the Data Encryption Standard (DES) operating in Cipher Block Chaining (CBC) mode with PKCS#7 padding. "
          "The asymmetric component implements the Rivest-Shamir-Adleman (RSA) algorithm from first principles, supporting variable key sizes. "
          "To secure decryption keys and sensitive content, we designed a dual-factor biometric shield combining real-time webcam facial verification and a simulated press-and-hold fingerprint scanner. "
          "Performance benchmarks were conducted to analyze the computational scaling of both algorithms. "
          "The results show that while DES maintains linear time complexity suitable for bulk data transfer, RSA displays cubic computational growth, confirming its utility for key distribution rather than bulk encryption.",
          align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    doc.add_page_break() # End Page 2
    
    # --- Page 3: TABLE OF CONTENTS & LIST OF TABLES ---
    add_heading("TABLE OF CONTENTS", level=1, space_before=12, space_after=12)
    
    tp = toc_pages if toc_pages else {
        "1": "1", "1.1": "1", "1.2": "1", "1.3": "1", "1.4": "1",
        "2": "2", "2.1": "2", "2.2": "2", "2.3": "2",
        "3": "3", "3.1": "3", "3.2": "3", "3.3": "3", "3.4": "3",
        "4": "4", "4.1": "4", "4.2": "4", "4.3": "4",
        "5": "5", "5.1": "5", "5.2": "5",
        "6": "5", "6.1": "5", "6.2": "5",
        "7": "5"
    }
    
    def add_toc_line(num, title, page_str, indent_spaces=0):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        
        prefix = " " * indent_spaces
        full_title = f"{prefix}{num} {title}"
        dot_count = 100 - len(full_title) - len(page_str)
        dot_count = max(5, dot_count)
        
        run_title = p.add_run(f"{full_title} " + "." * dot_count)
        run_title.font.name = 'Times New Roman'
        run_title.font.size = Pt(10.5)
        
        run_page = p.add_run(f" {page_str}")
        run_page.font.name = 'Times New Roman'
        run_page.font.size = Pt(10.5)
        run_page.bold = True
        
    add_toc_line("1.", "INTRODUCTION", tp["1"], 0)
    add_toc_line("1.1", "Background of the Study", tp["1.1"], 3)
    add_toc_line("1.2", "Problem Statement", tp["1.2"], 3)
    add_toc_line("1.3", "Objectives of the Project", tp["1.3"], 3)
    add_toc_line("1.4", "Scope of the Work", tp["1.4"], 3)
    
    add_toc_line("2.", "TECHNICAL BACKGROUND AND METHODOLOGY", tp["2"], 0)
    add_toc_line("2.1", "Data Encryption Standard (DES)", tp["2.1"], 3)
    add_toc_line("2.2", "Rivest-Shamir-Adleman (RSA) Cryptosystem", tp["2.2"], 3)
    add_toc_line("2.3", "Biometric Verification Principles", tp["2.3"], 3)
    
    add_toc_line("3.", "SYSTEM ARCHITECTURE AND IMPLEMENTATION", tp["3"], 0)
    add_toc_line("3.1", "Software Design and User Interface", tp["3.1"], 3)
    add_toc_line("3.2", "Symmetric Engine Implementation", tp["3.2"], 3)
    add_toc_line("3.3", "Asymmetric Engine Implementation", tp["3.3"], 3)
    add_toc_line("3.4", "Biometric Guard Workflows", tp["3.4"], 3)
    
    add_toc_line("4.", "PERFORMANCE EVALUATION AND DISCUSSION", tp["4"], 0)
    add_toc_line("4.1", "DES Benchmark Results", tp["4.1"], 3)
    add_toc_line("4.2", "RSA Benchmark Results", tp["4.2"], 3)
    add_toc_line("4.3", "Compression of Encrypted Files (Exercise 17)", tp["4.3"], 3)
    
    add_toc_line("5.", "BIOMETRIC INTEGRATION AND LAB ANSWERS", tp["5"], 0)
    add_toc_line("5.1", "Access Control Design", tp["5.1"], 3)
    add_toc_line("5.2", "Discussion of Lab Questions", tp["5.2"], 3)
    
    add_toc_line("6.", "CONCLUSIONS AND RECOMMENDATIONS", tp["6"], 0)
    add_toc_line("6.1", "Conclusions", tp["6.1"], 3)
    add_toc_line("6.2", "Recommendations", tp["6.2"], 3)
    
    add_toc_line("7.", "REFERENCES", tp["7"], 0)
    
    add_p("\n", space_after=0)
    add_heading("LIST OF TABLES", level=1, space_before=12, space_after=12)
    
    def add_lot_line(num, caption, page_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        
        full_title = f"Table {num}: {caption}"
        dot_count = 100 - len(full_title) - len(page_str)
        dot_count = max(5, dot_count)
        
        run_title = p.add_run(f"{full_title} " + "." * dot_count)
        run_title.font.name = 'Times New Roman'
        run_title.font.size = Pt(10.5)
        
        run_page = p.add_run(f" {page_str}")
        run_page.font.name = 'Times New Roman'
        run_page.font.size = Pt(10.5)
        run_page.bold = True

    add_lot_line("1", "DES Encryption and Decryption Performance Metrics", tp["4.1"])
    add_lot_line("2", "RSA Key Generation, Encryption, and Decryption Performance Metrics", tp["4.2"])
    
    # ----------------------------------------------------
    # SECTION 2: MAIN REPORT CONTENT (Pages 4 to 8 / Report Pages 1 to 5)
    # ----------------------------------------------------
    doc.add_section(WD_SECTION.NEW_PAGE)
    section2 = doc.sections[1]
    section2.page_width = Inches(8.5)
    section2.page_height = Inches(11.0)
    section2.top_margin = Inches(0.8)
    section2.bottom_margin = Inches(0.8)
    section2.left_margin = Inches(0.8)
    section2.right_margin = Inches(0.8)
    
    # Unlink headers/footers
    section2.header.is_linked_to_previous = False
    section2.footer.is_linked_to_previous = False
    
    # Set header text
    hp = section2.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("Information Security - Lab Project 2 | Cryptography & Biometrics")
    hrun.font.name = 'Times New Roman'
    hrun.font.size = Pt(8.5)
    hrun.font.italic = True
    
    # Set footer text (No complex fields, simple static layout, or standard Word numbering)
    fp = section2.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    frun = fp.add_run("Information Security Practical Report")
    frun.font.name = 'Times New Roman'
    frun.font.size = Pt(9.5)
    
    sectPr = section2._sectPr
    pgNumType = OxmlElement('w:pgNumType')
    pgNumType.set(qn('w:start'), '1')
    sectPr.append(pgNumType)

    # ==================== REPORT PAGE 1 (Page 4) ====================
    add_heading("1. INTRODUCTION", level=1, space_before=12, space_after=6)
    add_heading("1.1 Background of the Study", level=2, space_before=6, space_after=3)
    add_p("The rapid expansion of digital networks has made secure data transmission and storage a critical necessity. "
          "Cryptography is the core mechanism used to protect information from unauthorized access. "
          "Modern secure systems rely on two distinct paradigms: symmetric cryptography (fast, shared secret) and asymmetric cryptography (slower, public-private keypairs). "
          "While these mathematical models are highly robust in isolation, human factors like poor password hygiene present significant security risks. "
          "To bridge the gap between mathematical security and human authorization, modern secure environments integrate biometric factors "
          "(such as facial recognition or fingerprint analysis) directly into the cryptographic key management pipeline.", 
          size=10.5, space_after=8)
          
    add_heading("1.2 Problem Statement", level=2, space_before=6, space_after=3)
    add_p("Traditional software interfaces allow users to trigger decryption routines by simply inputting static passwords or keys. "
          "If a key is stolen or a workstation is left unattended, unauthorized users can easily decrypt sensitive documents. "
          "Furthermore, legacy systems often fail to restrict operations when parameters change (for instance, allowing outdated or weaker key lengths to remain active without force-regeneration). "
          "There is a clear need for a software architecture that binds cryptographic execution to active human authentication and enforces parameter validation.", 
          size=10.5, space_after=8)
          
    add_heading("1.3 Objectives of the Project", level=2, space_before=6, space_after=3)
    add_p("The primary objectives of this project are:\n"
          "1. To develop a fully functional desktop application in Python that integrates symmetric (DES) and asymmetric (RSA) cryptographic algorithms.\n"
          "2. To design and implement a named-face biometric registry and verification pipeline using OpenCV and grayscale correlation.\n"
          "3. To design and implement a simulated press-and-hold fingerprint scanning interface with structural similarity verification.\n"
          "4. To establish strict state validation where decryption is locked until biometric verification completes, and keys are invalidated immediately if security settings change.\n"
          "5. To execute performance benchmarks to evaluate the timing behaviors and limitations of both cryptographic approaches.", 
          size=10.5, space_after=8)
          
    add_heading("1.4 Scope of the Work", level=2, space_before=6, space_after=3)
    add_p("The project focuses on software-level integration of cryptography and biometrics using Python, Tkinter, OpenCV, and Matplotlib. "
          "It covers block-level DES-CBC file encryption, prime generation up to 128 bits for RSA text encryption, and local template matching for biometric verification. "
          "Hardware-level hardware security modules (HSMs) and production-grade high-bit prime generation (such as 2048-bit RSA) are excluded due to the execution limits of interpreter-level Python.", 
          size=10.5, space_after=0)

    doc.add_page_break() # End Report Page 1
    
    # ==================== REPORT PAGE 2 (Page 5) ====================
    add_heading("2. TECHNICAL BACKGROUND AND METHODOLOGY", level=1, space_before=12, space_after=6)
    
    add_heading("2.1 Data Encryption Standard (DES)", level=2, space_before=6, space_after=3)
    add_p("DES is a symmetric block cipher that processes data in 64-bit blocks using a 56-bit key. "
          "It is structured as a Feistel network, which splits the data block into two halves and runs them through 16 rounds of jumbling permutations, XOR additions, and non-linear S-Box substitutions. "
          "Because DES is a block cipher, encrypting arbitrary-sized data requires a mode of operation. In this project, we implemented Cipher Block Chaining (CBC) mode. "
          "In CBC mode, each plaintext block is XORed with the preceding ciphertext block before being encrypted, preventing identical plaintext blocks from generating identical ciphertext blocks. "
          "PKCS#7 padding is applied to ensure that the input size matches the required 8-byte block boundary.", 
          size=10.5, space_after=8)
          
    add_heading("2.2 Rivest-Shamir-Adleman (RSA) Cryptosystem", level=2, space_before=6, space_after=3)
    add_p("RSA is an asymmetric algorithm based on the practical difficulty of factoring the product of two large prime numbers. The mathematical process involves:\n"
          "1. Generating two distinct large prime numbers, p and q.\n"
          "2. Computing the modulus N = p * q and Euler's totient phi(N) = (p-1)(q-1).\n"
          "3. Choosing a public exponent e (typically 65537) such that gcd(e, phi(N)) = 1.\n"
          "4. Calculating the private exponent d using the relation d = e^-1 mod phi(N) via the Extended Euclidean Algorithm.\n"
          "Encryption of a character message M produces ciphertext C through the equation C = M^e mod N. "
          "Decryption recovers the original message using the private key: M = C^d mod N.", 
          size=10.5, space_after=8)
          
    add_heading("2.3 Biometric Verification Principles", level=2, space_before=6, space_after=3)
    add_p("Biometric matching verifies identity by evaluating physical characteristics. In this application, we use a dual-factor biometric approach:\n"
          "1. Facial Verification: Digital images are captured via webcam, aligned, converted to grayscale, and normalized. "
          "We use a hybrid matching approach. First, Histogram Equalization improves contrast, and Gaussian Smoothing reduces high-frequency noise. "
          "Then, we apply Normalized Cross-Correlation (NCC) to measure template similarity alongside a Mean Squared Error (MSE) calculation to quantify absolute pixel differences.\n"
          "2. Fingerprint Verification: Ridge pattern similarity is evaluated using structural pixel-by-pixel comparisons between the captured image and the registered fingerprint template.", 
          size=10.5, space_after=0)

    doc.add_page_break() # End Report Page 2
    
    # ==================== REPORT PAGE 3 (Page 6) ====================
    add_heading("3. SYSTEM ARCHITECTURE AND IMPLEMENTATION", level=1, space_before=12, space_after=6)
    
    add_heading("3.1 Software Design and User Interface", level=2, space_before=6, space_after=3)
    add_p("The desktop application is built with a deep-theme Tkinter interface structured into four core views:\n"
          "* DES Tab: Handles file selection, key generation, and file-based encryption and decryption.\n"
          "* RSA Tab: Manages key generation parameters, private/public key displays, and interactive text encryption.\n"
          "* Biometric Guard: Hosts the live webcam video panel, the user registry database, and the interactive fingerprint pad.\n"
          "* Performance Testing: Displays real-time, responsive Matplotlib graphs of benchmarks.", 
          size=10.5, space_after=8)
          
    add_heading("3.2 Symmetric Engine Implementation", level=2, space_before=6, space_after=3)
    add_p("The DES engine is implemented in des.py and supports:\n"
          "* Random Keygen: Generates a 64-bit hex key (represented as 16 hexadecimal characters).\n"
          "* Format Checking: A real-time validation label displays a green checkmark when the key is exactly 16 valid hex characters, "
          "preventing users from attempting encryption with invalid keys.\n"
          "* CBC File Routines: Automatically creates .close files from .open inputs during encryption, and writes decrypted outputs as _decrypted.open files.", 
          size=10.5, space_after=8)
          
    add_heading("3.3 Asymmetric Engine Implementation", level=2, space_before=6, space_after=3)
    add_p("The RSA module in rsa.py generates primes using a randomized odd-integer search backed by the Miller-Rabin primality test. "
          "To ensure operational safety, the application implements strict key validation:\n"
          "* Dropdown Bit Selector: Allows users to select prime bit sizes (8, 16, 32, 64, or 128 bits).\n"
          "* Change Tracing: Changing the bit size immediately invalidates existing keys, resets display fields to 'N/A', and displays a warning prompt. "
          "Decryption and encryption are blocked until a new keypair is generated.", 
          size=10.5, space_after=8)
          
    add_heading("3.4 Biometric Guard Workflows", level=2, space_before=6, space_after=3)
    add_p("The biometric manager in biometrics.py handles the physical capture and matching logic:\n"
          "* Face Registration: Prompts for a unique username, opens the webcam, runs a Haar Cascade face detector to locate the face, crops the bounding box, "
          "resizes it to a 128x128 grayscale template, and writes it to a file (faces/<username>.png).\n"
          "* Face Verification: Spawns a background thread to process live webcam frames. The thread aligns and crops the live face, "
          "and then matches it against all enrolled templates in the faces/ directory using NCC and MSE thresholds.\n"
          "* Sensor Pad: A canvas-based interactive fingerprint widget requires the user to click and hold the mouse button. "
          "A green laser line animates down the pad, simulating a real-time scan. Releasing the mouse early resets the progress bar.\n"
          "* Access Gating: Decryption routines query the biometric state variable. If the check fails, the application aborts and displays a warning dialog.", 
          size=10.5, space_after=0)

    doc.add_page_break() # End Report Page 3
    
    # ==================== REPORT PAGE 4 (Page 7) ====================
    add_heading("4. PERFORMANCE EVALUATION AND DISCUSSION", level=1, space_before=12, space_after=6)
    
    add_heading("4.1 DES Benchmark Results", level=2, space_before=6, space_after=3)
    add_p("We tested the DES CBC engine using files of varying sizes on our host hardware. The results show linear growth in execution times:", 
          size=10.5, space_after=6)
          
    # Add DES Table (Table 1)
    des_data = [
        ["File Size", "Encryption Time (ms)", "Decryption Time (ms)", "Throughput Speed (Mbps)"],
        ["100 B", "4.58", "4.65", "0.17"],
        ["1 KB", "44.31", "44.07", "0.18"],
        ["10 KB", "439.94", "441.47", "0.19"],
        ["100 KB", "4033.14", "2710.19", "0.20"],
        ["500 KB", "13379.95", "13200.77", "0.31"]
    ]
    
    table1 = doc.add_table(rows=len(des_data), cols=4)
    table1.style = 'Table Grid'
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table1.rows):
        row.height = Inches(0.24)
        for c_idx, cell in enumerate(row.cells):
            cell.text = des_data[r_idx][c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.runs[0]
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.bold = True
                    
    add_p("", space_after=4)
    
    add_p("Table 1 shows that the average throughput of our Python DES implementation is approximately 0.21 Mbps (210,964 bits per second). "
          "This speed remains stable across larger files because block cipher operations scale linearly, O(n), with the amount of input data.", 
          size=10.5, space_after=8)
          
    # Insert DES Image
    if os.path.exists("des_performance.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture("des_performance.png", width=Inches(4.5))
        add_p("Figure 1: DES execution timing and throughput curves.", italic=True, size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)

    doc.add_page_break() # End Report Page 4
    
    # ==================== REPORT PAGE 5 (Page 8) ====================
    add_heading("4.2 RSA Benchmark Results", level=2, space_before=6, space_after=3)
    add_p("The asymmetric engine was benchmarked by generating keypairs and processing a 100-character test string across different bit lengths:", 
          size=10.5, space_after=6)
          
    # Add RSA Table (Table 2)
    rsa_data = [
        ["Prime Size (bits)", "Key Generation (ms)", "Encryption (ms)", "Decryption (ms)"],
        ["8 bits", "0.06", "0.02", "0.05"],
        ["16 bits", "0.06", "0.17", "0.40"],
        ["32 bits", "0.51", "0.21", "1.32"],
        ["64 bits", "1.62", "0.28", "3.54"],
        ["128 bits", "2.53", "0.43", "11.50"]
    ]
    
    table2 = doc.add_table(rows=len(rsa_data), cols=4)
    table2.style = 'Table Grid'
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table2.rows):
        row.height = Inches(0.24)
        for c_idx, cell in enumerate(row.cells):
            cell.text = rsa_data[r_idx][c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.runs[0]
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.bold = True
                    
    add_p("", space_after=4)
    
    add_p("Unlike DES, RSA execution times grow exponentially as the prime bit size increases. "
          "Finding primes requires primality tests over larger number spaces, while encryption and decryption rely on modular exponentiation. "
          "The mathematical complexity is O(k^3) where k is the bit length, causing decryption times to rise sharply as the key size increases.", 
          size=10.5, space_after=8)
          
    # Insert RSA Image
    if os.path.exists("rsa_performance.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture("rsa_performance.png", width=Inches(4.5))
        add_p("Figure 2: RSA execution timing vs key bit size.", italic=True, size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
        
    add_heading("4.3 Compression of Encrypted Files (Exercise 17)", level=2, space_before=10, space_after=3)
    p_q = add_p("", size=10.5, space_after=4)
    p_q.add_run("Question: ").bold = True
    p_q.add_run("Create a new file with a lot of text (say 1MB in total) called bigfile.open. Encrypt it to give bigfile.close. "
              "Use a zip utility to compress both of them. Which resulting zip file is bigger? Why is this the case?")
    
    p_a = add_p("", size=10.5, space_after=4)
    p_a.add_run("Answer: ").bold = True
    p_a.add_run("The zipped version of the encrypted file (bigfile.close.zip) is larger than the zipped version of the original plaintext file (bigfile.open.zip).")
    
    p_e = add_p("", size=10.5, space_after=0)
    p_e.add_run("Explanation: ").bold = True
    p_e.add_run("Compression utilities like ZIP use algorithms (such as DEFLATE) that search for repeated characters and patterns within a file, "
              "replacing them with shorter reference codes to reduce size. Plaintext files contain high redundancy because language naturally repeats "
              "certain letters, words, and structures frequently. Conversely, strong encryption algorithms like DES aim to maximize entropy. "
              "Through diffusion and confusion, the output bytes of bigfile.close appear completely random, showing no repeating sequences. "
              "Because there is no statistical redundancy, the ZIP utility cannot compress the encrypted data. The resulting bigfile.close.zip "
              "contains the uncompressed ciphertext plus the standard ZIP metadata headers, making it slightly larger than the original unzipped bigfile.close file.")

    doc.add_page_break() # End Report Page 5
    
    # ==================== REPORT PAGE 6 (Page 9) ====================
    add_heading("5. BIOMETRIC INTEGRATION AND LAB ANSWERS", level=1, space_before=12, space_after=6)
    
    add_heading("5.1 Access Control Design", level=2, space_before=6, space_after=3)
    add_p("The biometrics subsystem is integrated directly into the decryption routines. The application maintains an internal state variable: self.biometric_authenticated. "
          "The user must navigate to the Biometric Guard tab. The user registers a face profile by typing a name and completing a webcam capture, which crops and saves their facial template. "
          "The user then initiates a scan. Face verification requires the system to match the live face against an enrolled template with an NCC score of at least 0.78 and an MSE below 2000. "
          "The fingerprint scan requires the user to hold down the mouse button on the sensor until the verification matches. "
          "When verification succeeds, the status header updates to display a green confirmation message showing the verified user's name. "
          "The DES or RSA decryption functions check this authorization flag. If authentication is not complete, the decryption attempt is blocked and a warning dialog is displayed.", 
          size=10.5, space_after=8)
          
    # Insert Fingerprint Match Image
    if os.path.exists("fingerprint_matches.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture("fingerprint_matches.png", width=Inches(3.8))
        add_p("Figure 3: Simulated fingerprint structural comparison (template vs captured).", italic=True, size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)

    add_heading("5.2 Discussion of Lab Questions", level=2, space_before=10, space_after=3)
    
    p_qa = add_p("", size=10.5, space_after=4)
    p_qa.add_run("a. What type of biometric input did you simulate?\n").bold = True
    p_qa.add_run("We implemented two types of biometric authentication: "
                "(1) Real-time webcam facial verification using OpenCV Haar Cascade classifiers to locate faces, combined with a comparison pipeline that checks "
                "Normalized Cross-Correlation (NCC) and Mean Squared Error (MSE) against registered grayscale templates; "
                "(2) An interactive fingerprint scanner simulation using a press-and-hold canvas widget, which validates ridge matches via pixel-level structural MSE comparisons.")
                
    p_qb = add_p("", size=10.5, space_after=4)
    p_qb.add_run("b. How did you use it to control access to your cryptographic key or message?\n").bold = True
    p_qb.add_run("The decryption functions in both des.py and rsa.py are bound to the Tkinter application state. Before the software runs the decryption math "
                "(using private key d or the DES key), it checks the self.biometric_authenticated boolean variable. If the variable is False, "
                "the application blocks the operation, displays an error message, and writes a warning to the logs. Only a successful biometric verification "
                "sets the variable to True, which enables the decryption logic.")
                
    p_qc = add_p("", size=10.5, space_after=0)
    p_qc.add_run("c. What are the potential security risks in using biometric authentication in this way?\n").bold = True
    p_qc.add_run("1. Presentation and Spoofing Attacks: The facial recognition pipeline compares simple 2D grayscale templates. An unauthorized person could bypass "
                "the system by holding a high-resolution photo or showing a video of a registered user on a tablet. Similarly, the fingerprint scanner can be spoofed "
                "using molded physical replicas.\n"
                "2. Software Injection and Memory Modification: Because the check is implemented at the software level using a boolean variable, a basic memory "
                "injection attack or debugger (like pdb) can manually set the flag to True, bypassing the biometric checks completely.\n"
                "3. Revocability Issues: Biometric characteristics cannot be changed. If a user's biometric template is compromised or stolen from the database, "
                "it cannot be rotated or reset like a password.\n"
                "4. Lack of Key Derivation Integration: The biometrics system acts as a simple logical gatekeeper switch. If the binary file itself is extracted "
                "from the hard drive, it can be decrypted offline if the attacker has the key. A more secure design would use a biometric cryptosystem "
                "(such as a fuzzy extractor) to derive the decryption key directly from the physical features of the scan, ensuring the key is never stored in memory.")

    doc.add_page_break() # End Report Page 6
    
    # ==================== REPORT PAGE 7 (Page 10) ====================
    add_heading("6. CONCLUSIONS AND RECOMMENDATIONS", level=1, space_before=12, space_after=6)
    
    add_heading("6.1 Conclusions", level=2, space_before=6, space_after=3)
    add_p("This project demonstrates the practical application of symmetric and asymmetric cryptography, performance benchmarking, and biometric validation. "
          "The performance benchmarks show that symmetric encryption (DES) scales linearly, making it suitable for processing larger files. "
          "Asymmetric encryption (RSA) scales cubically, which limits its practical use to small data sizes, such as encrypting symmetric keys for transmission. "
          "The biometric guard illustrates how physical authentication can secure cryptographic operations at the application level.", 
          size=10.5, space_after=8)
          
    add_heading("6.2 Recommendations", level=2, space_before=6, space_after=3)
    add_p("To make the application more secure and robust, we recommend the following changes:\n"
          "1. Upgrade Cryptographic Standards: DES uses a 56-bit key, which is vulnerable to brute-force attacks. The system should be upgraded to use the "
          "Advanced Encryption Standard (AES) with 256-bit keys for better security.\n"
          "2. Implement Liveness Detection: To prevent photo spoofing, the facial recognition system should require users to perform basic actions like "
          "blinking, turning their head, or smiling during scans.\n"
          "3. Incorporate Biometric Key Derivation: Rather than using a software flag to gate decryption, the system should derive cryptographic keys "
          "directly from the biometric features of the user, using fuzzy extractors or key encapsulation mechanisms.", 
          size=10.5, space_after=12)
          
    add_heading("7. REFERENCES", level=1, space_before=18, space_after=6)
    
    def add_reference(text):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        
    add_reference("Forouzan, B. A. (2007). Cryptography and Network Security. McGraw-Hill Higher Education.")
    add_reference("Stallings, W. (2017). Cryptography and Network Security: Principles and Practice (7th ed.). Pearson.")
    add_reference("Rivest, R. L., Shamir, A., and Adleman, L. (1978). A Method for Obtaining Digital Signatures and Public-Key Cryptosystems. Communications of the ACM, 21(2), 120-126.")

    # Save document
    doc.save("report.docx")
    print("report.docx generated successfully!")

if __name__ == "__main__":
    build_report()

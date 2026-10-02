# format_report_v2.py
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os

def build_report():
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
    
    section1.header.is_linked_to_previous = False
    section1.footer.is_linked_to_previous = False
    section1.header.paragraphs[0].text = ""
    section1.footer.paragraphs[0].text = ""

    def add_p(text="", bold=False, italic=False, size=10, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            run = p.add_run(text)
            run.font.name = 'Calibri'
            run.font.size = Pt(size)
            run.bold = bold
            run.italic = italic
        return p

    def add_heading(text, level, space_before=10, space_after=4):
        align = WD_ALIGN_PARAGRAPH.LEFT
        size = 13 if level == 1 else (11.5 if level == 2 else 10.5)
        p = add_p(text, bold=True, size=size, align=align, space_before=space_before, space_after=space_after)
        p.paragraph_format.keep_with_next = True
        return p

    # --- Page 1: COVER PAGE ---
    add_p("\n\n", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    add_p("UNIVERSITY OF MINES AND TECHNOLOGY, TARKWA", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    
    add_p("PROJECT REPORT: LAB PROJECT 2", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("(CRYPTOGRAPHY & BIOMETRICS)", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    
    add_p("TITLE:", bold=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("SYMMETRIC AND ASYMMETRIC CRYPTOGRAPHIC SUITE WITH INTEGRATED DUAL-FACTOR BIOMETRIC ACCESS CONTROL", 
          bold=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)
    
    add_p("COURSE: L300 (Semester 2) - Information Security", size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("DATE: JULY 2026", size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=60)
    
    add_p("..................................................", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p("Project Group Candidates", bold=True, size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    
    doc.add_page_break() # End Page 1
    
    # --- Page 2: DECLARATION & ABSTRACT ---
    add_heading("CANDIDATE'S DECLARATION", level=1, space_before=10, space_after=10)
    add_p("We hereby declare that this report and the corresponding codebase are the result of our own investigation and work. "
          "All sources of information and references used in this project have been fully acknowledged.", align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    add_p("\n\n..................................................\nProject Group Candidates\n\n", align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=30)
    
    add_heading("ABSTRACT", level=1, space_before=20, space_after=10)
    add_p("This project presents a practical implementation of symmetric and asymmetric cryptosystems integrated with a dual-factor biometric access control system. "
          "The symmetric component is built around the Data Encryption Standard (DES) operating in Cipher Block Chaining (CBC) mode with PKCS#7 padding. "
          "The asymmetric component implements the Rivest-Shamir-Adleman (RSA) algorithm from first principles, supporting variable key sizes. "
          "To secure decryption keys and sensitive content, we designed a dual-factor biometric shield combining real-time webcam facial verification and a simulated press-and-hold fingerprint scanner. "
          "Performance benchmarks were conducted to analyze the computational scaling of both algorithms. "
          "The results show that while DES maintains linear time complexity suitable for bulk data transfer, RSA displays cubic computational growth, confirming its utility for key distribution rather than bulk encryption.",
          align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    doc.add_page_break() # End Page 2
    
    # --- Page 3: TABLE OF CONTENTS & LIST OF TABLES ---
    add_heading("TABLE OF CONTENTS", level=1, space_before=10, space_after=10)
    
    tp = {
        "1": "1", "1.1": "1", "1.2": "1", "1.3": "1", "1.4": "1",
        "2": "1", "2.1": "1", "2.2": "2", "2.3": "2",
        "3": "2", "3.1": "2", "3.2": "2", "3.3": "2", "3.4": "3",
        "4": "3", "4.1": "3", "4.2": "4", "4.3": "4",
        "5": "4", "5.1": "4", "5.2": "5",
        "6": "5", "6.1": "5", "6.2": "5",
        "7": "5"
    }
    
    def add_toc_line(num, title, page_str, indent_spaces=0):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.1
        
        prefix = " " * indent_spaces
        full_title = f"{prefix}{num} {title}"
        dot_count = 100 - len(full_title) - len(page_str)
        dot_count = max(5, dot_count)
        
        run_title = p.add_run(f"{full_title} " + "." * dot_count)
        run_title.font.name = 'Calibri'
        run_title.font.size = Pt(10)
        
        run_page = p.add_run(f" {page_str}")
        run_page.font.name = 'Calibri'
        run_page.font.size = Pt(10)
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
    add_heading("LIST OF TABLES", level=1, space_before=10, space_after=10)
    
    def add_lot_line(num, caption, page_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.1
        
        full_title = f"Table {num}: {caption}"
        dot_count = 100 - len(full_title) - len(page_str)
        dot_count = max(5, dot_count)
        
        run_title = p.add_run(f"{full_title} " + "." * dot_count)
        run_title.font.name = 'Calibri'
        run_title.font.size = Pt(10)
        
        run_page = p.add_run(f" {page_str}")
        run_page.font.name = 'Calibri'
        run_page.font.size = Pt(10)
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
    section2.top_margin = Inches(0.7)
    section2.bottom_margin = Inches(0.7)
    section2.left_margin = Inches(0.75)
    section2.right_margin = Inches(0.75)
    
    section2.header.is_linked_to_previous = False
    section2.footer.is_linked_to_previous = False
    
    hp = section2.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("Information Security - Lab Project 2 | Cryptography & Biometrics")
    hrun.font.name = 'Calibri'
    hrun.font.size = Pt(8.5)
    hrun.font.italic = True
    
    fp = section2.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    frun = fp.add_run("Information Security Practical Report")
    frun.font.name = 'Calibri'
    frun.font.size = Pt(9)
    
    sectPr = section2._sectPr
    pgNumType = OxmlElement('w:pgNumType')
    pgNumType.set(qn('w:start'), '1')
    sectPr.append(pgNumType)

    # ==================== REPORT PAGE 1 (Page 4) ====================
    add_heading("1. INTRODUCTION", level=1, space_before=10, space_after=4)
    add_heading("1.1 Background of the Study", level=2, space_before=5, space_after=2)
    add_p("Modern data networks require cryptography to ensure security. Symmetric cryptography uses a shared secret key for fast encryption, "
          "while asymmetric cryptography uses public-private keypairs for key distribution. Integrating biometric factors directly "
          "into cryptographic workflows bridges the gap between digital security and physical user authentication.", size=10, space_after=6)
          
    add_heading("1.2 Problem Statement", level=2, space_before=5, space_after=2)
    add_p("Standard decryption systems rely on static keys, which are vulnerable to theft or unauthorized workstation access. "
          "Legacy systems also fail to restrict decryption if settings change. This project implements a system where decryption keys "
          "are gated by real-time biometric verification.", size=10, space_after=6)
          
    add_heading("1.3 Objectives of the Project", level=2, space_before=5, space_after=2)
    add_p("The objectives are: (1) Develop a desktop dashboard integrating DES and RSA cryptosystems; "
          "(2) Implement face and fingerprint biometric verification using OpenCV; "
          "(3) Enforce access control where decryption is locked until biometric verification succeeds; "
          "(4) Benchmark performance timings across key sizes.", size=10, space_after=6)
          
    add_heading("1.4 Scope of the Work", level=2, space_before=5, space_after=2)
    add_p("The work covers software-level implementations of DES-CBC, variable-bit RSA (8 to 128 bits), local biometric template matching, "
          "and live performance graphing. Hardware-level security modules and production-grade high-bit RSA are excluded.", size=10, space_after=10)

    add_heading("2. TECHNICAL BACKGROUND AND METHODOLOGY", level=1, space_before=12, space_after=4)
    add_heading("2.1 Data Encryption Standard (DES)", level=2, space_before=5, space_after=2)
    add_p("DES is a symmetric Feistel block cipher processing 64-bit blocks with a 56-bit key through 16 rounds of permutations, XORs, "
          "and S-Box substitutions. We implement Cipher Block Chaining (CBC) mode with PKCS#7 padding to ensure secure multi-block file encryption.", size=10, space_after=0)

    doc.add_page_break() # End Report Page 1
    
    # ==================== REPORT PAGE 2 (Page 5) ====================
    add_heading("2.2 Rivest-Shamir-Adleman (RSA) Cryptosystem", level=2, space_before=5, space_after=2)
    add_p("RSA is an asymmetric cipher based on prime factorization. Modulus N is the product of primes p and q. "
          "The public exponent e and totient phi(N) are coprime, and private key d is the modular inverse of e modulo phi(N). "
          "Encryption is C = M^e mod N, and decryption is M = C^d mod N.", size=10, space_after=6)
          
    add_heading("2.3 Biometric Verification Principles", level=2, space_before=5, space_after=2)
    add_p("Facial verification uses webcam captures processed via Haar Cascade detection, histogram equalization, and Gaussian smoothing, "
          "matched against templates using Normalized Cross-Correlation (NCC) and Mean Squared Error (MSE). "
          "Fingerprint verification evaluates ridge structure similarity using grayscale MSE.", size=10, space_after=10)

    add_heading("3. SYSTEM ARCHITECTURE AND IMPLEMENTATION", level=1, space_before=12, space_after=4)
    add_heading("3.1 Software Design and User Interface", level=2, space_before=5, space_after=2)
    add_p("The Tkinter GUI features a deep-themed sidebar menu and four tabs: DES file encryption, RSA text encryption, "
          "Biometric Guard, and Performance Benchmarks. The dashboard handles parameter changes and gates decryption status.", size=10, space_after=6)
          
    add_heading("3.2 Symmetric Engine Implementation", level=2, space_before=5, space_after=2)
    add_p("The DES module in des.py generates a 64-bit key, performs character-format checking, and executes CBC mode encryption. "
          "It automatically generates .close ciphertext files from .open plaintext files.", size=10, space_after=6)
          
    add_heading("3.3 Asymmetric Engine Implementation", level=2, space_before=5, space_after=2)
    add_p("The RSA module in rsa.py uses Miller-Rabin tests for prime generation. A dropdown controls prime size (8 to 128 bits). "
          "Changing this parameter invalidates existing keys, resets display fields, and locks decryption.", size=10, space_after=0)

    doc.add_page_break() # End Report Page 2
    
    # ==================== REPORT PAGE 3 (Page 6) ====================
    add_heading("3.4 Biometric Guard Workflows", level=2, space_before=5, space_after=2)
    add_p("The biometric system in biometrics.py registers user faces as cropped 128x128 grayscale templates. "
          "Live verification runs in a background thread using NCC (threshold >= 0.78) and MSE (threshold < 2000). "
          "The fingerprint pad requires a press-and-hold action verified by ridge MSE.", size=10, space_after=10)

    add_heading("4. PERFORMANCE EVALUATION AND DISCUSSION", level=1, space_before=12, space_after=4)
    add_heading("4.1 DES Benchmark Results", level=2, space_before=5, space_after=2)
    add_p("We evaluated the DES-CBC engine using dummy files up to 500KB. Execution times grow linearly, O(n), with file size, maintaining stable throughput.", size=10, space_after=6)
          
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
        row.height = Inches(0.2)
        for c_idx, cell in enumerate(row.cells):
            cell.text = des_data[r_idx][c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.runs[0]
            run.font.name = 'Calibri'
            run.font.size = Pt(9)
            if r_idx == 0:
                run.bold = True
                    
    add_p("", space_after=4)
    add_p("Table 1 shows that the average throughput of our Python DES implementation is approximately 0.21 Mbps. "
          "This speed remains stable across larger files because block cipher operations scale linearly, O(n), with the amount of input data.", size=10, space_after=6)
          
    # Insert DES Image
    if os.path.exists("des_performance.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        run = p_img.add_run()
        run.add_picture("des_performance.png", width=Inches(3.8))
        add_p("Figure 1: DES execution timing and throughput curves.", italic=True, size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)

    doc.add_page_break() # End Report Page 3
    
    # ==================== REPORT PAGE 4 (Page 7) ====================
    add_heading("4.2 RSA Benchmark Results", level=2, space_before=5, space_after=2)
    add_p("We benchmarked RSA key generation and text encryption. Execution times scale cubically, O(k^3), with prime bit size due to modular exponentiation.", size=10, space_after=6)
          
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
        row.height = Inches(0.2)
        for c_idx, cell in enumerate(row.cells):
            cell.text = rsa_data[r_idx][c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.runs[0]
            run.font.name = 'Calibri'
            run.font.size = Pt(9)
            if r_idx == 0:
                run.bold = True
                    
    add_p("", space_after=4)
    
    # Insert RSA Image
    if os.path.exists("rsa_performance.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        run = p_img.add_run()
        run.add_picture("rsa_performance.png", width=Inches(3.8))
        add_p("Figure 2: RSA execution timing vs key bit size.", italic=True, size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
        
    add_heading("4.3 Compression of Encrypted Files (Exercise 17)", level=2, space_before=8, space_after=2)
    p_q = add_p("", size=10, space_after=2)
    p_q.add_run("Question: ").bold = True
    p_q.add_run("Create a new file with text called bigfile.open, encrypt it to bigfile.close, and zip both. Which is larger and why?")
    
    p_a = add_p("", size=10, space_after=2)
    p_a.add_run("Answer: ").bold = True
    p_a.add_run("The zipped encrypted file (bigfile.close.zip) is larger than the zipped plaintext (bigfile.open.zip).")
    
    p_e = add_p("", size=10, space_after=0)
    p_e.add_run("Explanation: ").bold = True
    p_e.add_run("ZIP compression relies on finding repeating patterns (redundancy). Plaintext contains high redundancy. "
              "In contrast, DES encryption maximizes entropy, making the ciphertext bytes appear completely random. "
              "Since there is no redundancy, the ZIP utility cannot compress the encrypted data, resulting in a larger zip file due to ZIP header overhead.")

    doc.add_page_break() # End Report Page 4
    
    # ==================== REPORT PAGE 5 (Page 8) ====================
    add_heading("5. BIOMETRIC INTEGRATION AND LAB ANSWERS", level=1, space_before=10, space_after=4)
    add_heading("5.1 Access Control Design", level=2, space_before=5, space_after=2)
    add_p("Decryption functions check the boolean self.biometric_authenticated. The user registers a face via webcam, "
          "and verifies identity using the webcam scanner or simulated fingerprint pad. Successful verification updates the UI and enables decryption.", size=10, space_after=6)
          
    # Insert Fingerprint Match Image
    if os.path.exists("fingerprint_matches.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(2)
        p_img.paragraph_format.space_after = Pt(2)
        run = p_img.add_run()
        run.add_picture("fingerprint_matches.png", width=Inches(3.2))
        add_p("Figure 3: Simulated fingerprint match comparison HUD.", italic=True, size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)

    add_heading("5.2 Discussion of Lab Questions", level=2, space_before=8, space_after=2)
    
    p_qa = add_p("", size=10, space_after=3)
    p_qa.add_run("a. What type of biometric input did you simulate?\n").bold = True
    p_qa.add_run("We simulated real-time webcam facial matching (using Haar Cascade, NCC, and MSE) and interactive fingerprint ridge matching (using a press-and-hold canvas and structural MSE).")
                
    p_qb = add_p("", size=10, space_after=3)
    p_qb.add_run("b. How did you use it to control access to your cryptographic key or message?\n").bold = True
    p_qb.add_run("Decryption functions check the self.biometric_authenticated state. If False, the operation is blocked, displaying a warning dialog. "
                "Only successful biometric matching sets the flag to True.")
                
    p_qc = add_p("", size=10, space_after=6)
    p_qc.add_run("c. What are the potential security risks in using biometric authentication in this way?\n").bold = True
    p_qc.add_run("1. Spoofing: Simple 2D grayscale facial templates can be bypassed using photos or tablet screens. Ridge patterns can be copied using molded physical replicas.\n"
                "2. Software bypass: Since authentication is gated by a boolean flag in memory, a debugger or memory injector can toggle the flag to bypass biometric checks.\n"
                "3. Non-revocability: Stolen biometric templates cannot be rotated or reset like passwords.\n"
                "4. Lack of Cryptographic Binding: Gating acts as a simple switch. A secure design would derive decryption keys directly from the biometric features using fuzzy extractors.")

    add_heading("6. CONCLUSIONS AND RECOMMENDATIONS", level=1, space_before=10, space_after=4)
    add_heading("6.1 Conclusions", level=2, space_before=4, space_after=2)
    add_p("This lab successfully demonstrates symmetric and asymmetric cryptosystems integrated with biometrics. Benchmarks confirm that DES is suitable "
          "for bulk data transfer due to linear scaling, while RSA is limited to key exchange due to cubic scaling.", size=10, space_after=4)
          
    add_heading("6.2 Recommendations", level=2, space_before=4, space_after=2)
    add_p("We recommend: (1) Upgrade from 56-bit DES to 256-bit AES; (2) Implement liveness checks during facial scans to prevent photo spoofing; "
          "(3) Derive cryptographic keys directly from biometrics using fuzzy extractors.", size=10, space_after=6)
          
    add_heading("7. REFERENCES", level=1, space_before=10, space_after=4)
    
    def add_reference(text):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.first_line_indent = Inches(-0.2)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.1
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(9.5)
        
    add_reference("Forouzan, B. A. (2007). Cryptography and Network Security. McGraw-Hill Higher Education.")
    add_reference("Stallings, W. (2017). Cryptography and Network Security: Principles and Practice (7th ed.). Pearson.")
    add_reference("Rivest, R. L., Shamir, A., and Adleman, L. (1978). A Method for Obtaining Digital Signatures and Public-Key Cryptosystems. Communications of the ACM, 21(2), 120-126.")

    doc.save("report.docx")
    print("report.docx generated successfully!")

if __name__ == "__main__":
    build_report()

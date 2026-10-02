# app.py
# Cryptoshield Labs - Cryptography Lab Project Desktop Application
# Integrates DES, RSA, Biometric Verification, and Performance Benchmarking.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import time
import threading

# Import core modules
import des
import rsa
import biometrics
import benchmark

# Import Matplotlib for embedded responsive plots
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Define Theme Colors
BG_COLOR = "#0C111A"       # Deep dark blue/gray
CARD_BG = "#161F30"        # Lighter dark blue for panels
TEXT_MAIN = "#FFFFFF"      # White
TEXT_MUTED = "#8A99AD"     # Muted gray-blue
ACCENT_BLUE = "#00D2FF"    # Neon blue
ACCENT_GREEN = "#00E676"   # Neon green
ACCENT_RED = "#FF1744"     # Neon red
BORDER_COLOR = "#223147"   # Panel borders
BTN_HOVER = "#00A3C4"      # Hover state for accent blue


class Tooltip:
    """
    Lightweight hover tooltip for any Tkinter widget.
    Shows a dark-themed popup with a short help text after a short delay.
    """
    DELAY_MS = 600

    def __init__(self, widget, text: str):
        self.widget = widget
        self.text = text
        self._tip_win = None
        self._after_id = None
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _schedule(self, event=None):
        self._cancel()
        self._after_id = self.widget.after(self.DELAY_MS, self._show)

    def _cancel(self):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

    def _show(self, event=None):
        if self._tip_win or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self._tip_win = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)
        lbl = tk.Label(
            tw, text=self.text, justify="left",
            background="#1E2D45", foreground="#00D2FF",
            relief="solid", bd=1, padx=8, pady=4,
            font=("Segoe UI", 9), wraplength=320
        )
        lbl.pack()

    def _hide(self, event=None):
        self._cancel()
        if self._tip_win:
            self._tip_win.destroy()
            self._tip_win = None

class CryptoShieldApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CryptoShield Labs - Cryptography & Biometrics Dashboard")
        self.geometry("1150x750")
        self.configure(bg=BG_COLOR)
        self.resizable(True, True)
        
        # State Variables
        self.biometric_authenticated = False
        self.des_key = tk.StringVar(value="133457799BBCDFF1")
        self.rsa_bit_size = tk.IntVar(value=64)
        self._last_rsa_bit_size = 64  # Track last generated bit size
        
        # RSA Key State
        self.rsa_keys = {
            "p": "", "q": "", "n": "", "e": "", "d": ""
        }
        self.rsa_keys_valid = False   # True only after successful keygen at current bit size
        
        # Initialize biometric verifier
        self.verifier = biometrics.BiometricVerifier()
        
        # For webcam thread tracking
        self.webcam_running = False
        self.webcam_thread = None
        
        # Interactive Fingerprint Scanner State Variables
        self.finger_scanning = False
        self.finger_progress = 0
        self.finger_laser_y = 10
        self.finger_laser_direction = 1
        self.fingerprint_profile = tk.StringVar(value="authorized")
        
        # Trace RSA bit-size changes to invalidate stale keys
        self.rsa_bit_size.trace_add("write", self._on_rsa_bitsize_changed)
        
        # Apply style definitions
        self.setup_styles()
        
        # Build UI layout
        self.build_ui()
        
        # Set initial tab
        self.show_frame("des")
        
    def setup_styles(self):
        # Configure fonts and general widget appearances
        self.option_add("*Font", "SegoeUI 10")
        self.style = ttk.Style()
        self.style.theme_use('default')
        
        # Set ttk widget style settings
        self.style.configure("TFrame", background=BG_COLOR)
        self.style.configure("Card.TFrame", background=CARD_BG, borderwidth=1, relief="solid", bordercolor=BORDER_COLOR)
        
        # Scrollbars
        self.style.configure("Vertical.TScrollbar", background=BORDER_COLOR, troughcolor=BG_COLOR, arrowcolor=TEXT_MAIN)
        
    def build_ui(self):
        # Create Split Screen: Left Sidebar (Menu) and Right Content Area
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # --- LEFT SIDEBAR PANEL ---
        sidebar = tk.Frame(self, bg=CARD_BG, width=250, bd=0, highlightthickness=1, highlightbackground=BORDER_COLOR)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(5, weight=1) # Push bottom items down
        
        # Logo and Branding
        logo_label = tk.Label(sidebar, text="🛡️ CRYPTOSHIELD", font=("Segoe UI", 16, "bold"), fg=ACCENT_BLUE, bg=CARD_BG)
        logo_label.pack(pady=(30, 5), padx=20, anchor="w")
        
        sublogo_label = tk.Label(sidebar, text="Information Security Lab", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=CARD_BG)
        sublogo_label.pack(pady=(0, 30), padx=20, anchor="w")
        
        # Sidebar Menu Buttons
        self.menu_buttons = {}
        menu_items = [
            ("des", "🔐 Symmetric DES"),
            ("rsa", "🔑 Asymmetric RSA"),
            ("biometrics", "👤 Biometric Guard"),
            ("benchmark", "📊 Benchmarks"),
        ]
        
        for frame_id, text in menu_items:
            btn = tk.Button(sidebar, text=f"  {text}", font=("Segoe UI", 11, "bold"), 
                            fg=TEXT_MAIN, bg=CARD_BG, activeforeground=ACCENT_BLUE, activebackground=BG_COLOR,
                            bd=0, anchor="w", cursor="hand2", padx=20, pady=12,
                            command=lambda fid=frame_id: self.show_frame(fid))
            btn.pack(fill="x", padx=10, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=BG_COLOR, fg=ACCENT_BLUE))
            btn.bind("<Leave>", lambda e, b=btn, fid=frame_id: self.on_btn_leave(b, fid))
            self.menu_buttons[frame_id] = btn
            
        # Security Guard Indicator at bottom of Sidebar
        self.guard_frame = tk.Frame(sidebar, bg=BG_COLOR, bd=1, relief="solid", highlightthickness=0)
        self.guard_frame.pack(fill="x", padx=15, pady=20, side="bottom")
        
        self.guard_icon = tk.Label(self.guard_frame, text="🔒 SYSTEM LOCKED", font=("Segoe UI", 10, "bold"), fg=ACCENT_RED, bg=BG_COLOR)
        self.guard_icon.pack(pady=10)
        
        self.guard_desc = tk.Label(self.guard_frame, text="Decryption key access requires\nbiometric authentication.", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_COLOR)
        self.guard_desc.pack(pady=(0, 10))
        
        # --- RIGHT CONTENT PANEL ---
        self.content_container = tk.Frame(self, bg=BG_COLOR)
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)
        
        # Initialize dynamically swapped frames
        self.frames = {}
        self.frames["des"] = self.create_des_frame()
        self.frames["rsa"] = self.create_rsa_frame()
        self.frames["biometrics"] = self.create_biometric_frame()
        self.frames["benchmark"] = self.create_benchmark_frame()
        
        # Grid all frames in the container
        for fid, frame in self.frames.items():
            frame.grid(row=0, column=0, sticky="nsew")

    def on_btn_leave(self, button, frame_id):
        if frame_id != self.current_frame_id:
            button.configure(bg=CARD_BG, fg=TEXT_MAIN)
        else:
            button.configure(bg=BG_COLOR, fg=ACCENT_BLUE)

    def show_frame(self, frame_id):
        # Stop webcam if moving away from biometrics tab
        if hasattr(self, 'current_frame_id') and self.current_frame_id == "biometrics" and frame_id != "biometrics":
            self.stop_webcam()
            
        self.current_frame_id = frame_id
        
        # Visual selection update
        for fid, btn in self.menu_buttons.items():
            if fid == frame_id:
                btn.configure(bg=BG_COLOR, fg=ACCENT_BLUE)
            else:
                btn.configure(bg=CARD_BG, fg=TEXT_MAIN)
                
        # Raise selected frame
        self.frames[frame_id].tkraise()
        
        # Refresh graphs on benchmark page if opened
        if frame_id == "benchmark":
            self.load_benchmark_graphs()

    def update_security_status(self):
        if self.biometric_authenticated:
            self.guard_frame.configure(highlightbackground=ACCENT_GREEN)
            self.guard_icon.configure(text="🔓 SYSTEM UNLOCKED", fg=ACCENT_GREEN)
            self.guard_desc.configure(text="Decryption keys active.\nAccess granted to private data.")
            # Unlock widgets in tabs if necessary
        else:
            self.guard_frame.configure(highlightbackground=BORDER_COLOR)
            self.guard_icon.configure(text="🔒 SYSTEM LOCKED", fg=ACCENT_RED)
            self.guard_desc.configure(text="Decryption key access requires\nbiometric authentication.")
            
    def check_biometric_access(self):
        """Helper to prompt for authentication if locked."""
        if not self.biometric_authenticated:
            messagebox.showwarning(
                "Access Denied", 
                "SECURITY GUARD ALERT:\n\nPrivate key storage is LOCKED. "
                "You must verify your identity on the 'Biometric Guard' tab before decrypting data."
            )
            self.show_frame("biometrics")
            return False
        return True

    # =========================================================================
    # TAB 1: DES IMPLEMENTATION VIEW
    # =========================================================================
    def create_des_frame(self):
        frame = tk.Frame(self.content_container, bg=BG_COLOR)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure((0, 1), weight=1)
        
        # Tab Title
        header = tk.Label(frame, text="Symmetric Cryptography: Data Encryption Standard (DES)", 
                          font=("Segoe UI", 16, "bold"), fg=TEXT_MAIN, bg=BG_COLOR)
        header.grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(20, 10))
        
        # Common Configuration (Key Panel)
        key_panel = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        key_panel.grid(row=1, column=0, columnspan=2, sticky="ew", padx=30, pady=10)
        
        key_lbl = tk.Label(key_panel, text="Hexadecimal Key (64-bit / 16 hex chars):", font=("Segoe UI", 10, "bold"), fg=ACCENT_BLUE, bg=CARD_BG)
        key_lbl.pack(side="left", padx=(20, 10), pady=15)
        Tooltip(key_lbl, "DES requires a 64-bit key expressed as exactly 16 hexadecimal characters (0-9, A-F).\nExample: 133457799BBCDFF1")
        
        key_entry = tk.Entry(key_panel, textvariable=self.des_key, font=("Courier New", 12, "bold"),
                             bg=BG_COLOR, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, bd=1, relief="solid", width=25)
        key_entry.pack(side="left", padx=10, pady=15)
        Tooltip(key_entry, "Type or paste your 16-character hex key here.\nThe key must be exactly 16 hex chars before encrypting or decrypting.")
        
        # Live key-length indicator
        self.des_key_indicator = tk.Label(key_panel, text="✔ 16/16", font=("Segoe UI", 9, "bold"), fg=ACCENT_GREEN, bg=CARD_BG)
        self.des_key_indicator.pack(side="left", padx=(0, 5), pady=15)
        
        def _update_key_indicator(*_):
            val = self.des_key.get().strip()
            length = len(val)
            valid = length == 16 and all(c in "0123456789ABCDEFabcdef" for c in val)
            self.des_key_indicator.configure(
                text=f"{'✔' if valid else '✘'} {length}/16",
                fg=ACCENT_GREEN if valid else ACCENT_RED
            )
        self.des_key.trace_add("write", _update_key_indicator)
        _update_key_indicator()  # Initial render
        
        def gen_random_key():
            import secrets
            random_key = secrets.token_hex(8).upper()
            self.des_key.set(random_key)
            self.log_des(f"Generated random 64-bit key: {random_key}")
            
        gen_btn = tk.Button(key_panel, text="🎲 Generate Key", font=("Segoe UI", 9, "bold"),
                            bg=ACCENT_BLUE, fg=BG_COLOR, activebackground=BTN_HOVER, bd=0, padx=15, cursor="hand2", command=gen_random_key)
        gen_btn.pack(side="left", padx=10, pady=15)
        Tooltip(gen_btn, "Generate a cryptographically secure random 64-bit DES key.")
        
        # Left Side Card: Encryption
        enc_card = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        enc_card.grid(row=2, column=0, sticky="nsew", padx=(30, 15), pady=15)
        
        tk.Label(enc_card, text="🔒 Encryption Engine", font=("Segoe UI", 13, "bold"), fg=TEXT_MAIN, bg=CARD_BG).pack(anchor="w", padx=20, pady=15)
        
        # File selector block
        file_frame = tk.Frame(enc_card, bg=CARD_BG)
        file_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(file_frame, text="Select File to Encrypt (.open):", fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w")
        
        self.des_enc_filepath = tk.StringVar()
        fe_entry = tk.Entry(file_frame, textvariable=self.des_enc_filepath, bg=BG_COLOR, fg=TEXT_MAIN, bd=1, relief="solid", font=("Segoe UI", 9))
        fe_entry.pack(side="left", fill="x", expand=True, pady=5)
        Tooltip(fe_entry, "Select a .open file to encrypt. The output will be saved alongside it as a .close file.")
        
        def browse_open_file():
            path = filedialog.askopenfilename(filetypes=[("Open Files", "*.open"), ("All Files", "*.*")])
            if path:
                self.des_enc_filepath.set(path)
                self.log_des(f"Selected file for encryption: {os.path.basename(path)}")
                
        fb_btn = tk.Button(file_frame, text="Browse...", bg=BORDER_COLOR, fg=TEXT_MAIN, bd=0, padx=12, command=browse_open_file, cursor="hand2")
        fb_btn.pack(side="right", padx=(5, 0), pady=5)
        Tooltip(fb_btn, "Browse your filesystem for a .open file to encrypt.")
        
        # Text selector block
        text_frame = tk.Frame(enc_card, bg=CARD_BG)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(text_frame, text="Or input Plaintext directly:", fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w")
        self.des_plain_text = tk.Text(text_frame, height=6, bg=BG_COLOR, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, bd=1, relief="solid", font=("Segoe UI", 10))
        self.des_plain_text.pack(fill="both", expand=True, pady=5)
        
        def execute_des_encrypt():
            key = self.des_key.get().strip()
            if len(key) != 16:
                messagebox.showerror("Key Error", "DES key must be exactly 16 hex characters (64 bits).")
                return
            
            # File mode
            file_path = self.des_enc_filepath.get().strip()
            if file_path:
                if not os.path.exists(file_path):
                    messagebox.showerror("File Error", "Selected file does not exist.")
                    return
                # Create output filename (.close)
                base, ext = os.path.splitext(file_path)
                out_path = base + ".close"
                
                try:
                    start = time.perf_counter()
                    des.encrypt_file(file_path, out_path, key)
                    elapsed = time.perf_counter() - start
                    self.log_des(f"SUCCESS: Encrypted file successfully!\n"
                                 f"Input: {os.path.basename(file_path)}\n"
                                 f"Output: {os.path.basename(out_path)}\n"
                                 f"Time Taken: {elapsed*1000:.2f} ms")
                    messagebox.showinfo("Success", f"File encrypted successfully!\nSaved to: {os.path.basename(out_path)}")
                except Exception as e:
                    self.log_des(f"ENCRYPTION ERROR: {str(e)}")
                    messagebox.showerror("Encryption Error", str(e))
            else:
                # Text mode
                plaintext = self.des_plain_text.get("1.0", "end-1c")
                if not plaintext:
                    messagebox.showwarning("Input Empty", "Please browse a file or input plaintext.")
                    return
                try:
                    start = time.perf_counter()
                    cipher_bytes = des.des_cbc_encrypt(plaintext.encode('utf-8'), key)
                    elapsed = time.perf_counter() - start
                    hex_cipher = cipher_bytes.hex().upper()
                    
                    self.des_cipher_text.delete("1.0", "end")
                    self.des_cipher_text.insert("1.0", hex_cipher)
                    
                    self.log_des(f"SUCCESS: Encrypted text input.\n"
                                 f"Ciphertext (Hex): {hex_cipher[:40]}...\n"
                                 f"Time Taken: {elapsed*1000:.2f} ms")
                except Exception as e:
                    self.log_des(f"ENCRYPTION ERROR: {str(e)}")
                    messagebox.showerror("Encryption Error", str(e))

        enc_btn = tk.Button(enc_card, text="🛡️ Run DES Encryption", font=("Segoe UI", 11, "bold"),
                            bg=ACCENT_BLUE, fg=BG_COLOR, activebackground=BTN_HOVER, bd=0, pady=10, cursor="hand2", command=execute_des_encrypt)
        enc_btn.pack(fill="x", padx=20, pady=(0, 20))
        Tooltip(enc_btn, "Encrypt the selected file or plaintext using DES-CBC.\nRequires a valid 16-character hex key above.")
        
        # Right Side Card: Decryption
        dec_card = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        dec_card.grid(row=2, column=1, sticky="nsew", padx=(15, 30), pady=15)
        
        tk.Label(dec_card, text="🔓 Decryption Engine (Biometric Shielded)", font=("Segoe UI", 13, "bold"), fg=TEXT_MAIN, bg=CARD_BG).pack(anchor="w", padx=20, pady=15)
        
        # File selector block
        file_frame_dec = tk.Frame(dec_card, bg=CARD_BG)
        file_frame_dec.pack(fill="x", padx=20, pady=5)
        tk.Label(file_frame_dec, text="Select File to Decrypt (.close):", fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w")
        
        self.des_dec_filepath = tk.StringVar()
        fd_entry = tk.Entry(file_frame_dec, textvariable=self.des_dec_filepath, bg=BG_COLOR, fg=TEXT_MAIN, bd=1, relief="solid", font=("Segoe UI", 9))
        fd_entry.pack(side="left", fill="x", expand=True, pady=5)
        
        def browse_close_file():
            path = filedialog.askopenfilename(filetypes=[("Close Files", "*.close"), ("All Files", "*.*")])
            if path:
                self.des_dec_filepath.set(path)
                self.log_des(f"Selected file for decryption: {os.path.basename(path)}")
                
        fb_dec_btn = tk.Button(file_frame_dec, text="Browse...", bg=BORDER_COLOR, fg=TEXT_MAIN, bd=0, padx=12, command=browse_close_file, cursor="hand2")
        fb_dec_btn.pack(side="right", padx=(5, 0), pady=5)
        
        # Text selector block
        text_frame_dec = tk.Frame(dec_card, bg=CARD_BG)
        text_frame_dec.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(text_frame_dec, text="Or input Ciphertext (Hex):", fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w")
        self.des_cipher_text = tk.Text(text_frame_dec, height=6, bg=BG_COLOR, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, bd=1, relief="solid", font=("Segoe UI", 10))
        self.des_cipher_text.pack(fill="both", expand=True, pady=5)
        
        def execute_des_decrypt():
            # Apply Biometric lock
            if not self.check_biometric_access():
                return
                
            key = self.des_key.get().strip()
            if len(key) != 16:
                messagebox.showerror("Key Error", "DES key must be exactly 16 hex characters (64 bits).")
                return
            
            # File mode
            file_path = self.des_dec_filepath.get().strip()
            if file_path:
                if not os.path.exists(file_path):
                    messagebox.showerror("File Error", "Selected file does not exist.")
                    return
                # Create output filename (.open)
                base, ext = os.path.splitext(file_path)
                # Ensure we write a decrypted file
                out_path = base + "_decrypted.open"
                
                try:
                    start = time.perf_counter()
                    des.decrypt_file(file_path, out_path, key)
                    elapsed = time.perf_counter() - start
                    self.log_des(f"SUCCESS: Decrypted file successfully!\n"
                                 f"Input: {os.path.basename(file_path)}\n"
                                 f"Output: {os.path.basename(out_path)}\n"
                                 f"Time Taken: {elapsed*1000:.2f} ms")
                    messagebox.showinfo("Success", f"File decrypted successfully!\nSaved to: {os.path.basename(out_path)}")
                except Exception as e:
                    self.log_des(f"DECRYPTION ERROR: {str(e)}")
                    messagebox.showerror("Decryption Error", str(e))
            else:
                # Text mode
                hex_cipher = self.des_cipher_text.get("1.0", "end-1c").strip()
                if not hex_cipher:
                    messagebox.showwarning("Input Empty", "Please browse a file or input hex ciphertext.")
                    return
                try:
                    start = time.perf_counter()
                    cipher_bytes = bytes.fromhex(hex_cipher)
                    decrypted_bytes = des.des_cbc_decrypt(cipher_bytes, key)
                    elapsed = time.perf_counter() - start
                    plaintext = decrypted_bytes.decode('utf-8', errors='ignore')
                    
                    self.des_plain_text.delete("1.0", "end")
                    self.des_plain_text.insert("1.0", plaintext)
                    
                    self.log_des(f"SUCCESS: Decrypted hex ciphertext.\n"
                                 f"Decrypted: '{plaintext}'\n"
                                 f"Time Taken: {elapsed*1000:.2f} ms")
                except Exception as e:
                    self.log_des(f"DECRYPTION ERROR: {str(e)}")
                    messagebox.showerror("Decryption Error", "Decryption failed. Please check key validity and integrity.")

        dec_btn = tk.Button(dec_card, text="🔓 Run DES Decryption", font=("Segoe UI", 11, "bold"),
                            bg=ACCENT_GREEN, fg=BG_COLOR, activebackground=BTN_HOVER, bd=0, pady=10, cursor="hand2", command=execute_des_decrypt)
        dec_btn.pack(fill="x", padx=20, pady=(0, 20))
        Tooltip(dec_btn, "Decrypt a .close file or hex ciphertext using DES-CBC.\n⚠ Biometric authentication is required to unlock decryption.")
        
        # Bottom Console Log Card
        log_card = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        log_card.grid(row=3, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 20))
        
        tk.Label(log_card, text="📁 Execution Logs:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w", padx=15, pady=(5, 0))
        
        self.des_log = tk.Text(log_card, height=4, bg=CARD_BG, fg=ACCENT_GREEN, bd=0, font=("Courier New", 9))
        self.des_log.pack(fill="both", expand=True, padx=15, pady=5)
        
        return frame
        
    def log_des(self, message):
        self.des_log.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.des_log.see("end")

    # =========================================================================
    # TAB 2: RSA IMPLEMENTATION VIEW
    # =========================================================================
    def create_rsa_frame(self):
        frame = tk.Frame(self.content_container, bg=BG_COLOR)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure((0, 1), weight=1)
        
        # Title
        header = tk.Label(frame, text="Asymmetric Cryptography: RSA Cryptosystem", 
                          font=("Segoe UI", 16, "bold"), fg=TEXT_MAIN, bg=BG_COLOR)
        header.grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(20, 10))
        
        # Top Card: RSA Key Generation Panel
        key_card = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        key_card.grid(row=1, column=0, columnspan=2, sticky="ew", padx=30, pady=10)
        
        bit_lbl = tk.Label(key_card, text="Key Bit Size:", font=("Segoe UI", 10, "bold"), fg=ACCENT_BLUE, bg=CARD_BG)
        bit_lbl.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        Tooltip(bit_lbl, "Prime bit size controls RSA key strength.\nLarger sizes are more secure but slower to generate.\n⚠ Changing this will invalidate any existing keypair — regenerate before encrypting.")
        
        bit_selector = ttk.Combobox(key_card, values=[8, 16, 32, 64, 128], textvariable=self.rsa_bit_size, width=8, state="readonly")
        bit_selector.grid(row=0, column=1, padx=5, pady=15)
        Tooltip(bit_selector, "Select the prime bit size.\n⚠ After changing, click 'Generate Keypair' before encrypting or decrypting.")
        
        # Key status indicator label (shows stale/ready state)
        self.rsa_key_status_lbl = tk.Label(key_card, text="⚠ No Keys", font=("Segoe UI", 9, "bold"), fg=ACCENT_RED, bg=CARD_BG)
        self.rsa_key_status_lbl.grid(row=1, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="w")
        
        # Fields for p, q, N, e, d
        display_frame = tk.Frame(key_card, bg=CARD_BG)
        display_frame.grid(row=0, column=3, rowspan=2, padx=25, pady=10, sticky="ew")
        
        self.rsa_entries = {}
        vars_to_show = [("p", "Prime p"), ("q", "Prime q"), ("n", "Modulus N (p*q)"), ("e", "Public E"), ("d", "Private D")]
        for idx, (var_id, name) in enumerate(vars_to_show):
            tk.Label(display_frame, text=f"{name}:", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=CARD_BG).grid(row=idx, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(display_frame, font=("Courier New", 8, "bold"), fg=TEXT_MAIN, bg=BG_COLOR, insertbackground=TEXT_MAIN, width=65, bd=1, relief="solid")
            entry.grid(row=idx, column=1, sticky="w", padx=5, pady=2)
            self.rsa_entries[var_id] = entry
            
        def generate_rsa_keys():
            bits = self.rsa_bit_size.get()
            self.log_rsa(f"Generating primes and keys for bit size {bits}...")
            self.rsa_key_status_lbl.configure(text="⏳ Generating...", fg=ACCENT_BLUE)
            gen_btn.configure(state="disabled")
            
            def run_keygen():
                start = time.perf_counter()
                p, q, n, e, d = rsa.generate_keypair(bits)
                elapsed = time.perf_counter() - start
                self.rsa_keys.update({"p": p, "q": q, "n": n, "e": e, "d": d})
                self._last_rsa_bit_size = bits
                self.rsa_keys_valid = True
                self.after(0, lambda: self.update_rsa_key_ui(elapsed))
                self.after(0, lambda: gen_btn.configure(state="normal"))
                
            threading.Thread(target=run_keygen, daemon=True).start()
            
        gen_btn = tk.Button(key_card, text="🔑 Generate Keypair", font=("Segoe UI", 10, "bold"),
                            bg=ACCENT_BLUE, fg=BG_COLOR, activebackground=BTN_HOVER, bd=0, padx=15, pady=8, cursor="hand2", command=generate_rsa_keys)
        gen_btn.grid(row=0, column=2, padx=15, pady=15)
        Tooltip(gen_btn, "Generate a fresh RSA keypair at the selected bit size.\nAlternatively, you can manually type or paste E, D, and N into the fields.")
        
        # Left Side Panel: Encryption
        enc_card = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        enc_card.grid(row=2, column=0, sticky="nsew", padx=(30, 15), pady=15)
        
        tk.Label(enc_card, text="🔒 RSA Encryption Engine", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=CARD_BG).pack(anchor="w", padx=20, pady=15)
        
        tk.Label(enc_card, text="Enter Plaintext Message:", fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w", padx=20)
        self.rsa_plain_text = tk.Text(enc_card, height=6, bg=BG_COLOR, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, bd=1, relief="solid", font=("Segoe UI", 10))
        self.rsa_plain_text.pack(fill="both", expand=True, padx=20, pady=5)
        
        def execute_rsa_encrypt():
            e_str = self.rsa_entries["e"].get().strip()
            n_str = self.rsa_entries["n"].get().strip()
            if not e_str or not n_str:
                messagebox.showerror(
                    "Key Required",
                    "⚠ Public Key (E) and Modulus (N) are required for encryption.\n\n"
                    "Please click 'Generate Keypair' or manually enter/paste Public E and Modulus N above."
                )
                return
            try:
                e = int(e_str)
                n = int(n_str)
            except ValueError:
                messagebox.showerror("Invalid Key", "Public E and Modulus N must be valid integers.")
                return
            
            plaintext = self.rsa_plain_text.get("1.0", "end-1c")
            if not plaintext:
                messagebox.showwarning("Input Empty", "Please enter message to encrypt.")
                return
                
            try:
                start = time.perf_counter()
                cipher = rsa.rsa_encrypt(plaintext, e, n)
                elapsed = time.perf_counter() - start
                
                # Format ciphertext list
                cipher_str = ",".join(map(str, cipher))
                self.rsa_cipher_text.delete("1.0", "end")
                self.rsa_cipher_text.insert("1.0", cipher_str)
                
                self.log_rsa(f"SUCCESS: Encrypted plaintext using Public Key (E={e}, N={n}).\nTime Taken: {elapsed*1000:.2f} ms")
            except Exception as e_err:
                self.log_rsa(f"ENCRYPTION ERROR: {str(e_err)}")
                messagebox.showerror("Encryption Error", str(e_err))
                
        self.rsa_enc_btn = tk.Button(enc_card, text="🔒 Run RSA Encryption", font=("Segoe UI", 11, "bold"),
                            bg=ACCENT_BLUE, fg=BG_COLOR, activebackground=BTN_HOVER, bd=0, pady=10, cursor="hand2", command=execute_rsa_encrypt)
        self.rsa_enc_btn.pack(fill="x", padx=20, pady=20)
        Tooltip(self.rsa_enc_btn, "Encrypt the plaintext message with the current RSA public key (E, N).")
        
        # Right Side Panel: Decryption
        dec_card = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        dec_card.grid(row=2, column=1, sticky="nsew", padx=(15, 30), pady=15)
        
        tk.Label(dec_card, text="🔓 RSA Decryption Engine (Biometric Shielded)", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=CARD_BG).pack(anchor="w", padx=20, pady=15)
        
        tk.Label(dec_card, text="Enter Ciphertext Integer List (comma-separated):", fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w", padx=20)
        self.rsa_cipher_text = tk.Text(dec_card, height=6, bg=BG_COLOR, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, bd=1, relief="solid", font=("Segoe UI", 10))
        self.rsa_cipher_text.pack(fill="both", expand=True, padx=20, pady=5)
        
        def execute_rsa_decrypt():
            # Apply Biometric lock
            if not self.check_biometric_access():
                return
                
            d_str = self.rsa_entries["d"].get().strip()
            n_str = self.rsa_entries["n"].get().strip()
            if not d_str or not n_str:
                messagebox.showerror(
                    "Key Required",
                    "⚠ Private Key (D) and Modulus (N) are required for decryption.\n\n"
                    "Please click 'Generate Keypair' or manually enter/paste Private D and Modulus N above."
                )
                return
            try:
                d = int(d_str)
                n = int(n_str)
            except ValueError:
                messagebox.showerror("Invalid Key", "Private D and Modulus N must be valid integers.")
                return
                
            cipher_str = self.rsa_cipher_text.get("1.0", "end-1c").strip()
            if not cipher_str:
                messagebox.showwarning("Input Empty", "Please input ciphertext integer list.")
                return
                
            try:
                # Convert comma-separated string to integers
                cipher = list(map(int, cipher_str.split(",")))
                
                start = time.perf_counter()
                decrypted = rsa.rsa_decrypt(cipher, d, n)
                elapsed = time.perf_counter() - start
                
                self.rsa_plain_text.delete("1.0", "end")
                self.rsa_plain_text.insert("1.0", decrypted)
                
                self.log_rsa(f"SUCCESS: Decrypted ciphertext using Private Key (D={d}, N={n}).\nDecrypted: '{decrypted}'\nTime Taken: {elapsed*1000:.2f} ms")
            except Exception as e_err:
                self.log_rsa(f"DECRYPTION ERROR: {str(e_err)}")
                messagebox.showerror("Decryption Error", "Failed to decrypt. Verify integer list formatting or check if private key matches public key.")
                
        self.rsa_dec_btn = tk.Button(dec_card, text="🔓 Run RSA Decryption", font=("Segoe UI", 11, "bold"),
                            bg=ACCENT_GREEN, fg=BG_COLOR, activebackground=BTN_HOVER, bd=0, pady=10, cursor="hand2", command=execute_rsa_decrypt)
        self.rsa_dec_btn.pack(fill="x", padx=20, pady=20)
        Tooltip(self.rsa_dec_btn, "Decrypt the ciphertext list using the current RSA private key (D, N).\n⚠ Biometric authentication is required.")
        
        # Bottom Logs Console
        log_card = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        log_card.grid(row=3, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 20))
        
        tk.Label(log_card, text="📁 Execution Logs:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w", padx=15, pady=(5, 0))
        
        self.rsa_log = tk.Text(log_card, height=4, bg=CARD_BG, fg=ACCENT_GREEN, bd=0, font=("Courier New", 9))
        self.rsa_log.pack(fill="both", expand=True, padx=15, pady=5)
        
        return frame
        
    def update_rsa_key_ui(self, time_elapsed):
        for var_id, entry in self.rsa_entries.items():
            val = self.rsa_keys[var_id]
            entry.delete(0, "end")
            entry.insert(0, str(val))
        bits = self._last_rsa_bit_size
        self.rsa_key_status_lbl.configure(
            text=f"✔ Keys Ready ({bits}-bit) — Generated in {time_elapsed*1000:.1f} ms", fg=ACCENT_GREEN)
        self.log_rsa(f"Keypair generated successfully in {time_elapsed*1000:.2f} ms!\n"
                     f"p = {self.rsa_keys['p']}\n"
                     f"q = {self.rsa_keys['q']}")

    def _on_rsa_bitsize_changed(self, *_):
        """Called whenever the user changes the RSA bit-size dropdown."""
        try:
            new_bits = self.rsa_bit_size.get()
        except Exception:
            return
        if new_bits != self._last_rsa_bit_size:
            self.rsa_keys_valid = False
            self.rsa_keys = {"p": "", "q": "", "n": "", "e": "", "d": ""}
            if hasattr(self, "rsa_key_status_lbl"):
                self.rsa_key_status_lbl.configure(
                    text=f"⚠ Bit size set to {new_bits} — Click 'Generate Keypair' or enter custom keys.",
                    fg=ACCENT_RED
                )

    def log_rsa(self, message):
        self.rsa_log.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.rsa_log.see("end")

    # =========================================================================
    # TAB 3: BIOMETRIC GUARD (ACCESS CONTROL)
    # =========================================================================
    def create_biometric_frame(self):
        frame = tk.Frame(self.content_container, bg=BG_COLOR)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure((0, 1), weight=1)
        
        # Title
        header = tk.Label(frame, text="Biometric Guard: Identity Access Control System",
                          font=("Segoe UI", 16, "bold"), fg=TEXT_MAIN, bg=BG_COLOR)
        header.grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(20, 10))
        
        # Top Overview Card
        status_panel = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        status_panel.grid(row=1, column=0, columnspan=2, sticky="ew", padx=30, pady=10)
        
        self.bio_status_label = tk.Label(status_panel, text="🔒 BIOMETRICS ACTIVE: DECRYPTION CORE SECURED",
                                         font=("Segoe UI", 12, "bold"), fg=ACCENT_RED, bg=CARD_BG)
        self.bio_status_label.pack(side="left", padx=25, pady=20)
        
        def reset_biometric_lock():
            self.biometric_authenticated = False
            self.update_security_status()
            self.bio_status_label.configure(text="🔒 BIOMETRICS ACTIVE: DECRYPTION CORE SECURED", fg=ACCENT_RED)
            messagebox.showinfo("Security Lock Active", "Decryption features are now re-secured under biometric lock.")
            
        reset_btn = tk.Button(status_panel, text="🔒 Re-lock Cryptocore", font=("Segoe UI", 9, "bold"),
                              bg=ACCENT_RED, fg=TEXT_MAIN, activebackground=BTN_HOVER, bd=0, padx=15, pady=5,
                              cursor="hand2", command=reset_biometric_lock)
        reset_btn.pack(side="right", padx=25, pady=20)
        
        # Left Panel: Webcam Face Recognition Scanner
        cam_card = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        cam_card.grid(row=2, column=0, sticky="nsew", padx=(30, 15), pady=15)
        
        tk.Label(cam_card, text="👤 Live Facial Recognition & Registration",
                 font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=CARD_BG).pack(anchor="w", padx=20, pady=15)
        
        # Status details
        face_info_frame = tk.Frame(cam_card, bg=CARD_BG)
        face_info_frame.pack(fill="x", padx=20, pady=2)
        
        self.face_status_lbl = tk.Label(face_info_frame, text="🔵 Face Enrolled: CHECKING...",
                                        font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG)
        self.face_status_lbl.pack(side="left")
        Tooltip(self.face_status_lbl, "Shows how many face identities are currently enrolled.\nAt least one face must be registered before identity verification is available.")
        
        # Webcam Feed Canvas Label
        self.cam_canvas = tk.Label(cam_card, bg=BG_COLOR, text="[ WEBCAM SCANNER DISCONNECTED ]",
                                   fg=TEXT_MUTED, font=("Courier New", 10), bd=1, relief="solid")
        self.cam_canvas.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Name entry for registration
        name_frame = tk.Frame(cam_card, bg=CARD_BG)
        name_frame.pack(fill="x", padx=20, pady=(5, 2))
        name_lbl = tk.Label(name_frame, text="Name for Registration:", fg=TEXT_MUTED, bg=CARD_BG,
                 font=("Segoe UI", 9))
        name_lbl.pack(side="left")
        Tooltip(name_lbl, "Enter a unique name for the person being registered.\nThis name will be displayed when their face is verified later.")
        self.reg_name_var = tk.StringVar()
        self.reg_name_entry = tk.Entry(name_frame, textvariable=self.reg_name_var,
                                       font=("Segoe UI", 10), bg=BG_COLOR, fg=TEXT_MAIN,
                                       insertbackground=TEXT_MAIN, bd=1, relief="solid", width=18)
        self.reg_name_entry.pack(side="left", padx=(8, 0), ipady=3)
        Tooltip(self.reg_name_entry, "Type the name to associate with the face being registered.\nRequired before clicking 'Register Face'.")
        
        # Face control buttons
        face_btn_frame = tk.Frame(cam_card, bg=CARD_BG)
        face_btn_frame.pack(fill="x", padx=20, pady=(6, 20))
        face_btn_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.webcam_btn_register = tk.Button(face_btn_frame, text="👤 Register Face",
                                             bg=ACCENT_BLUE, fg=BG_COLOR, font=("Segoe UI", 9, "bold"),
                                             bd=0, pady=8, cursor="hand2",
                                             command=lambda: self.start_webcam(mode="register"))
        self.webcam_btn_register.grid(row=0, column=0, padx=(0, 3), sticky="ew")
        Tooltip(self.webcam_btn_register, "Open webcam and capture your face under the entered name.\nFill in the Name field above first.")
        
        self.webcam_btn_verify = tk.Button(face_btn_frame, text="🟢 Verify Identity",
                                           bg=ACCENT_GREEN, fg=BG_COLOR, font=("Segoe UI", 9, "bold"),
                                           bd=0, pady=8, cursor="hand2",
                                           command=lambda: self.start_webcam(mode="verify"))
        self.webcam_btn_verify.grid(row=0, column=1, padx=3, sticky="ew")
        Tooltip(self.webcam_btn_verify, "Start facial verification against all registered identities.\nHold your face steady for 2.5 seconds to grant access.\n⚠ At least one face must be registered first.")
        
        self.webcam_btn_abort = tk.Button(face_btn_frame, text="🛑 Abort Scan",
                                          bg=BORDER_COLOR, fg=TEXT_MAIN, font=("Segoe UI", 9, "bold"),
                                          bd=0, pady=8, cursor="hand2", state="disabled",
                                          command=self.stop_webcam)
        self.webcam_btn_abort.grid(row=0, column=2, padx=(3, 0), sticky="ew")
        Tooltip(self.webcam_btn_abort, "Stop the live webcam scan immediately.")
        
        # Right Panel: split into Registered Faces list (top) + Fingerprint scanner (bottom)
        right_panel = tk.Frame(frame, bg=BG_COLOR)
        right_panel.grid(row=2, column=1, sticky="nsew", padx=(15, 30), pady=15)
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=2)
        right_panel.grid_columnconfigure(0, weight=1)
        
        # --- Registered Faces Card ---
        faces_card = tk.Frame(right_panel, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        faces_card.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        
        tk.Label(faces_card, text="🗂️ Registered Face Identities",
                 font=("Segoe UI", 11, "bold"), fg=TEXT_MAIN, bg=CARD_BG).pack(anchor="w", padx=15, pady=(12, 6))
        
        list_frame = tk.Frame(faces_card, bg=CARD_BG)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 5))
        
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", bg=BORDER_COLOR, troughcolor=BG_COLOR)
        self.faces_listbox = tk.Listbox(
            list_frame, yscrollcommand=scrollbar.set,
            bg=BG_COLOR, fg=TEXT_MAIN, selectbackground=ACCENT_BLUE,
            selectforeground=BG_COLOR, font=("Segoe UI", 10), bd=0,
            highlightthickness=1, highlightbackground=BORDER_COLOR,
            activestyle="none", height=4
        )
        scrollbar.config(command=self.faces_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.faces_listbox.pack(side="left", fill="both", expand=True)
        
        def delete_selected_face():
            sel = self.faces_listbox.curselection()
            if not sel:
                messagebox.showwarning("No Selection", "Please select a face profile to delete.")
                return
            name = self.faces_listbox.get(sel[0])
            if messagebox.askyesno("Confirm Delete", f"Delete face profile for '{name}'?"):
                self.verifier.delete_face(name)
                self.update_face_status_ui()
        
        del_btn = tk.Button(faces_card, text="🗑 Delete Selected", font=("Segoe UI", 8, "bold"),
                            bg=ACCENT_RED, fg=TEXT_MAIN, bd=0, pady=5, cursor="hand2",
                            command=delete_selected_face)
        del_btn.pack(fill="x", padx=15, pady=(2, 12))
        
        # --- Fingerprint Scanner Card ---
        finger_card = tk.Frame(right_panel, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        finger_card.grid(row=1, column=0, sticky="nsew")
        
        tk.Label(finger_card, text="🌀 Interactive Fingerprint Ridge Scanner",
                 font=("Segoe UI", 11, "bold"), fg=TEXT_MAIN, bg=CARD_BG).pack(anchor="w", padx=20, pady=(12, 8))
        
        profile_frame = tk.Frame(finger_card, bg=CARD_BG)
        profile_frame.pack(fill="x", padx=20, pady=3)
        
        tk.Label(profile_frame, text="Input Fingerprint Profile:", fg=TEXT_MUTED, bg=CARD_BG,
                 font=("Segoe UI", 9, "bold")).pack(side="left")
        
        authorized_rb = tk.Radiobutton(profile_frame, text="Authorized User (Match)",
                                       variable=self.fingerprint_profile, value="authorized",
                                       bg=CARD_BG, fg=TEXT_MAIN, selectcolor=BG_COLOR,
                                       activebackground=CARD_BG, activeforeground=TEXT_MAIN, font=("Segoe UI", 8))
        authorized_rb.pack(side="left", padx=10)
        
        intruder_rb = tk.Radiobutton(profile_frame, text="Intruder (Mismatch)",
                                     variable=self.fingerprint_profile, value="intruder",
                                     bg=CARD_BG, fg=TEXT_MAIN, selectcolor=BG_COLOR,
                                     activebackground=CARD_BG, activeforeground=TEXT_MAIN, font=("Segoe UI", 8))
        intruder_rb.pack(side="left", padx=5)
        
        sensor_display_frame = tk.Frame(finger_card, bg=CARD_BG)
        sensor_display_frame.pack(fill="both", expand=True, padx=20, pady=5)
        sensor_display_frame.grid_columnconfigure((0, 1), weight=1)
        sensor_display_frame.grid_rowconfigure(0, weight=1)
        
        sensor_pad_card = tk.Frame(sensor_display_frame, bg=BG_COLOR, bd=1, relief="solid", highlightcolor=BORDER_COLOR)
        sensor_pad_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        tk.Label(sensor_pad_card, text="TOUCH SENSOR PAD", font=("Segoe UI", 8, "bold"),
                 fg=TEXT_MUTED, bg=BG_COLOR).pack(pady=(10, 5))
        
        self.finger_sensor = tk.Canvas(sensor_pad_card, width=150, height=150, bg=CARD_BG,
                                       highlightthickness=1, highlightbackground=BORDER_COLOR)
        self.finger_sensor.pack(pady=5)
        self.finger_sensor.create_oval(30, 30, 120, 120, outline=TEXT_MUTED, width=1)
        self.finger_sensor.create_oval(45, 20, 105, 130, outline=TEXT_MUTED, width=1)
        self.finger_sensor.create_oval(60, 10, 90, 140, outline=TEXT_MUTED, width=1)
        self.finger_sensor.create_oval(15, 45, 135, 105, outline=TEXT_MUTED, width=1)
        self.finger_laser_line = self.finger_sensor.create_line(5, 10, 145, 10, fill=ACCENT_GREEN, width=2, state="hidden")
        self.finger_sensor.bind("<ButtonPress-1>", self.start_fingerprint_scan)
        self.finger_sensor.bind("<ButtonRelease-1>", self.abort_fingerprint_scan)
        
        self.finger_sensor_status = tk.Label(sensor_pad_card, text="CLICK & HOLD MOUSE TO SCAN",
                                             font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_COLOR)
        self.finger_sensor_status.pack(pady=5)
        self.finger_progress_bar = ttk.Progressbar(sensor_pad_card, orient="horizontal", length=130, mode="determinate")
        self.finger_progress_bar.pack(pady=(0, 10))
        
        self.finger_canvas = tk.Label(sensor_display_frame, bg=BG_COLOR, text="[ COMPARISON VIEWER ]",
                                      fg=TEXT_MUTED, font=("Courier New", 9), bd=1, relief="solid")
        self.finger_canvas.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        self.finger_expl = tk.Label(finger_card, text="Press and hold sensor to run biometric pattern matching.",
                                    font=("Segoe UI", 9), fg=TEXT_MUTED, bg=CARD_BG, justify="left")
        self.finger_expl.pack(fill="x", padx=20, pady=10)
        
        # Initial status check
        self.update_face_status_ui()
        
        return frame
        
    def update_face_status_ui(self):
        """Refresh face-enrollment status label and registered-faces listbox."""
        registered = self.verifier.list_registered_faces()
        # Refresh listbox
        self.faces_listbox.delete(0, "end")
        for name in registered:
            self.faces_listbox.insert("end", name)
        # Update status label and verify button
        if registered:
            count = len(registered)
            self.face_status_lbl.configure(
                text=f"🟢 {count} Face Profile{'s' if count != 1 else ''} Enrolled", fg=ACCENT_GREEN)
            self.webcam_btn_verify.configure(state="normal")
        else:
            self.face_status_lbl.configure(text="🔵 No Face Profiles Registered", fg=ACCENT_BLUE)
            self.webcam_btn_verify.configure(state="disabled")

    def start_webcam(self, mode="verify"):
        if mode == "register":
            name = self.reg_name_var.get().strip()
            if not name:
                messagebox.showwarning("Name Required",
                                       "Please enter a name in the 'Name for Registration' field before registering.")
                return

        self.webcam_running = True
        self.webcam_btn_verify.configure(state="disabled")
        self.webcam_btn_register.configure(state="disabled")
        self.webcam_btn_abort.configure(state="normal")
        self.cam_canvas.configure(text="[ INITIALIZING CAMERA... ]")
        
        def on_frame(frame):
            if not self.webcam_running:
                return False
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            img = img.resize((420, 260), Image.Resampling.LANCZOS)
            self.after(0, lambda: self.update_cam_canvas(img))
            return True
            
        def on_complete(success, name=None):
            if success:
                if mode == "register":
                    self.after(0, lambda: self.handle_register_success(name))
                else:
                    self.biometric_authenticated = True
                    self.after(0, lambda: self.handle_auth_success(name))
                    
        def on_error(err_msg):
            self.after(0, lambda: messagebox.showerror("Camera Error", err_msg))
            self.after(0, self.stop_webcam)
            
        if mode == "register":
            reg_name = self.reg_name_var.get().strip()
            self.webcam_thread = threading.Thread(
                target=self.verifier.register_face_via_webcam,
                args=(reg_name, on_frame, on_complete, on_error),
                daemon=True
            )
        else:
            self.webcam_thread = threading.Thread(
                target=self.verifier.scan_face_via_webcam,
                args=(on_frame, on_complete, on_error),
                daemon=True
            )
        self.webcam_thread.start()
        
    def update_cam_canvas(self, img):
        if not self.webcam_running:
            return
        photo = ImageTk.PhotoImage(img)
        self.cam_canvas.configure(image=photo, text="")
        self.cam_canvas.image = photo
        
    def handle_register_success(self, name):
        self.stop_webcam()
        self.reg_name_var.set("")  # Clear name field after successful registration
        self.update_face_status_ui()
        messagebox.showinfo("Registration Success",
                            f"✅ '{name}' has been successfully enrolled as a secure identity!")
        
    def handle_auth_success(self, name):
        self.stop_webcam()
        self.update_security_status()
        self.bio_status_label.configure(
            text=f"🔓 IDENTITY VERIFIED: {name.upper()} — DECRYPTION SHIELD DISABLED", fg=ACCENT_GREEN)
        messagebox.showinfo("Authentication Success",
                            f"✅ Identity confirmed: {name}\nDecryption functionalities are now unlocked.")
        
    def stop_webcam(self):
        self.webcam_running = False
        self.webcam_btn_verify.configure(state="normal" if self.verifier.is_face_registered() else "disabled")
        self.webcam_btn_register.configure(state="normal")
        self.webcam_btn_abort.configure(state="disabled")
        self.cam_canvas.configure(image="", text="[ WEBCAM SCANNER DISCONNECTED ]")
        self.cam_canvas.image = None
        
    # --- Fingerprint Scanner Controls ---
    def start_fingerprint_scan(self, event):
        if self.finger_scanning:
            return
            
        # Reset matching display elements
        self.finger_canvas.configure(image="", text="[ SCANNING COMPARING... ]")
        self.finger_canvas.image = None
        self.finger_expl.configure(text="Analyzing fingerprint structure... Keep your finger on pad.", fg=TEXT_MUTED)
        
        self.finger_scanning = True
        self.finger_progress = 0
        self.finger_laser_y = 10
        self.finger_laser_direction = 1
        
        # Visually light up sensor pad border
        self.finger_sensor.configure(highlightbackground=ACCENT_BLUE)
        self.finger_sensor.itemconfig(self.finger_laser_line, state="normal")
        self.finger_sensor_status.configure(text="🚨 READING RIDGES...", fg=ACCENT_BLUE)
        
        # Start update timer loop
        self.update_fingerprint_scan()
        
    def abort_fingerprint_scan(self, event):
        if not self.finger_scanning:
            return
            
        if self.finger_progress < 100:
            self.finger_scanning = False
            self.finger_sensor.configure(highlightbackground=BORDER_COLOR)
            self.finger_sensor.itemconfig(self.finger_laser_line, state="hidden")
            self.finger_sensor_status.configure(text="❌ SCAN ABORTED - PRESS PAD TO RE-TRY", fg=ACCENT_RED)
            self.finger_progress_bar.configure(value=0)
            
    def update_fingerprint_scan(self):
        if not self.finger_scanning:
            return
            
        # Increment progress
        self.finger_progress += 4
        self.finger_progress_bar.configure(value=self.finger_progress)
        
        # Sweeping Laser Animation
        self.finger_laser_y += self.finger_laser_direction * 10
        if self.finger_laser_y >= 140:
            self.finger_laser_y = 140
            self.finger_laser_direction = -1
        elif self.finger_laser_y <= 10:
            self.finger_laser_y = 10
            self.finger_laser_direction = 1
            
        self.finger_sensor.coords(self.finger_laser_line, 5, self.finger_laser_y, 145, self.finger_laser_y)
        
        # Update text stages
        if self.finger_progress < 25:
            diag_text = f"🔄 Reading ridges... {self.finger_progress}%"
        elif self.finger_progress < 50:
            diag_text = f"⚙️ Mapping minutiae... {self.finger_progress}%"
        elif self.finger_progress < 75:
            diag_text = f"🔍 Verifying template... {self.finger_progress}%"
        elif self.finger_progress < 100:
            diag_text = f"🔓 Loading keys... {self.finger_progress}%"
        else:
            diag_text = "✅ Scan complete!"
            
        self.finger_sensor_status.configure(text=diag_text, fg=ACCENT_BLUE)
        
        if self.finger_progress >= 100:
            self.finger_scanning = False
            self.finger_sensor.configure(highlightbackground=ACCENT_GREEN)
            self.finger_sensor.itemconfig(self.finger_laser_line, state="hidden")
            self.finger_sensor_status.configure(text="✅ SCAN COMPLETE", fg=ACCENT_GREEN)
            self.after(300, self.execute_fingerprint_verification)
        else:
            self.after(40, self.update_fingerprint_scan)
            
    def execute_fingerprint_verification(self):
        profile = self.fingerprint_profile.get()
        if profile == "authorized":
            biometrics.generate_mock_fingerprint("test_positive.png", seed=101, noise=True)
            path = "test_positive.png"
        else:
            biometrics.generate_mock_fingerprint("test_negative.png", seed=202, noise=False)
            path = "test_negative.png"
            
        success, match_path, score, explanation = self.verifier.verify_fingerprint(path)
        
        # Display comparison image
        if match_path and os.path.exists(match_path):
            img = Image.open(match_path)
            # Resize image to fit right panel canvas (approx 280x200)
            img = img.resize((260, 160), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.finger_canvas.configure(image=photo, text="")
            self.finger_canvas.image = photo
            
        self.finger_expl.configure(text=explanation, fg=ACCENT_GREEN if success else ACCENT_RED)
        
        if success:
            self.biometric_authenticated = True
            self.update_security_status()
            self.bio_status_label.configure(text="🔓 BIOMETRICS PASSED: DECRYPTION SHIELD DISABLED", fg=ACCENT_GREEN)
            messagebox.showinfo("Authentication Success", "Fingerprint verified! Decryption core is now active.")
        else:
            self.biometric_authenticated = False
            self.update_security_status()
            self.bio_status_label.configure(text="🔒 BIOMETRICS ACTIVE: DECRYPTION CORE SECURED", fg=ACCENT_RED)
            messagebox.showerror("Authentication Failed", "Fingerprint mismatch. Access Rejection.")
        
    # =========================================================================
    # TAB 4: PERFORMANCE BENCHMARKS
    # =========================================================================
    def style_figure(self, fig):
        fig.patch.set_facecolor(CARD_BG)
        for ax in fig.axes:
            ax.set_facecolor(BG_COLOR)
            ax.tick_params(colors=TEXT_MUTED, which='both', labelsize=8)
            ax.xaxis.label.set_color(TEXT_MUTED)
            ax.yaxis.label.set_color(TEXT_MUTED)
            ax.title.set_color(TEXT_MAIN)
            for spine in ax.spines.values():
                spine.set_color(BORDER_COLOR)
            ax.grid(True, which="both", ls="--", color=BORDER_COLOR, alpha=0.3)

    def create_benchmark_frame(self):
        frame = tk.Frame(self.content_container, bg=BG_COLOR)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure((0, 1), weight=1)
        
        # Title
        header = tk.Label(frame, text="Performance Testing & Execution Benchmarks", 
                          font=("Segoe UI", 16, "bold"), fg=TEXT_MAIN, bg=BG_COLOR)
        header.grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(20, 10))
        
        # Top Control Card
        control_panel = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        control_panel.grid(row=1, column=0, columnspan=2, sticky="ew", padx=30, pady=10)
        
        self.bench_status_lbl = tk.Label(control_panel, text="Run Benchmarks to measure implementation speeds on your hardware.", 
                                         fg=TEXT_MUTED, bg=CARD_BG, justify="left")
        self.bench_status_lbl.pack(side="left", padx=25, pady=20)
                 
        def run_benchmarks():
            self.bench_btn.configure(state="disabled", text="⚡ Running Benchmarks...")
            
            def update_progress(msg):
                self.after(0, lambda: self.bench_status_lbl.configure(text=msg, fg=ACCENT_BLUE))
            
            def run_thread():
                try:
                    des_data = benchmark.run_des_benchmark(progress_callback=update_progress)
                    rsa_data = benchmark.run_rsa_benchmark(progress_callback=update_progress)
                    self.after(0, lambda: self.handle_bench_complete(des_data, rsa_data))
                except Exception as e:
                    self.after(0, lambda: messagebox.showerror("Benchmark Error", str(e)))
                    self.after(0, lambda: self.bench_btn.configure(state="normal", text="⚡ Run Full Benchmark Suite"))
                    self.after(0, lambda: self.bench_status_lbl.configure(text="Benchmark failed. Please try again.", fg=ACCENT_RED))
                    
            threading.Thread(target=run_thread, daemon=True).start()
            
        self.bench_btn = tk.Button(control_panel, text="⚡ Run Full Benchmark Suite", font=("Segoe UI", 10, "bold"),
                                   bg=ACCENT_BLUE, fg=BG_COLOR, activebackground=BTN_HOVER, bd=0, padx=20, pady=10, cursor="hand2", command=run_benchmarks)
        self.bench_btn.pack(side="right", padx=25, pady=20)
        
        # Left Panel: DES performance graph
        self.graph1_panel = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        self.graph1_panel.grid(row=2, column=0, sticky="nsew", padx=(30, 15), pady=15)
        
        tk.Label(self.graph1_panel, text="Symmetric: DES Performance Chart", font=("Segoe UI", 11, "bold"), fg=TEXT_MAIN, bg=CARD_BG).pack(anchor="w", padx=20, pady=10)
        
        # Create DES Figure and Axes
        self.des_fig = plt.Figure(figsize=(5, 3), dpi=100, facecolor=CARD_BG)
        self.des_ax1 = self.des_fig.add_subplot(121)
        self.des_ax2 = self.des_fig.add_subplot(122)
        
        # Embed DES Figure
        self.des_canvas = FigureCanvasTkAgg(self.des_fig, master=self.graph1_panel)
        self.des_canvas_widget = self.des_canvas.get_tk_widget()
        self.des_canvas_widget.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.des_canvas_widget.configure(bg=BG_COLOR)
        
        # Right Panel: RSA performance graph
        self.graph2_panel = tk.Frame(frame, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        self.graph2_panel.grid(row=2, column=1, sticky="nsew", padx=(15, 30), pady=15)
        
        tk.Label(self.graph2_panel, text="Asymmetric: RSA Performance Chart", font=("Segoe UI", 11, "bold"), fg=TEXT_MAIN, bg=CARD_BG).pack(anchor="w", padx=20, pady=10)
        
        # Create RSA Figure and Axes
        self.rsa_fig = plt.Figure(figsize=(5, 3), dpi=100, facecolor=CARD_BG)
        self.rsa_ax = self.rsa_fig.add_subplot(111)
        
        # Embed RSA Figure
        self.rsa_canvas = FigureCanvasTkAgg(self.rsa_fig, master=self.graph2_panel)
        self.rsa_canvas_widget = self.rsa_canvas.get_tk_widget()
        self.rsa_canvas_widget.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.rsa_canvas_widget.configure(bg=BG_COLOR)
        
        # Initialize plots with baseline data
        initial_des = (
            [100, 1024, 10240, 102400, 512000],
            [0.0001, 0.0008, 0.0075, 0.0720, 0.3600],
            [0.0001, 0.0008, 0.0072, 0.0710, 0.3500],
            [8.0 * 1e6, 10.2 * 1e6, 10.9 * 1e6, 11.4 * 1e6, 11.4 * 1e6]
        )
        initial_rsa = (
            [8, 16, 32, 64, 128],
            [0.002, 0.008, 0.045, 0.320, 2.500],
            [0.0001, 0.0003, 0.0008, 0.0025, 0.0090],
            [0.0002, 0.0005, 0.0015, 0.0055, 0.0220]
        )
        self.update_plots(initial_des, initial_rsa)
        
        return frame
        
    def handle_bench_complete(self, des_data, rsa_data):
        self.bench_btn.configure(state="normal", text="⚡ Run Full Benchmark Suite")
        self.bench_status_lbl.configure(text="Benchmark Complete! Charts updated.", fg=ACCENT_GREEN)
        self.update_plots(des_data, rsa_data)
        messagebox.showinfo("Benchmark Complete", "Performance benchmarking completed! Execution speed charts have been updated.")
        
    def load_benchmark_graphs(self):
        # Refresh the embedded matplotlib figures when tab is loaded
        if hasattr(self, 'des_canvas') and hasattr(self, 'rsa_canvas'):
            self.des_canvas.draw()
            self.rsa_canvas.draw()

    def update_plots(self, des_data, rsa_data):
        # 1. Update DES plots
        sizes_bytes, des_enc_times, des_dec_times, des_speeds_bps = des_data
        
        self.des_ax1.clear()
        self.des_ax2.clear()
        
        # Plot execution times (log-log scale)
        self.des_ax1.plot(sizes_bytes, [t*1000 for t in des_enc_times], 'o-', color=ACCENT_BLUE, label='Encryption')
        self.des_ax1.plot(sizes_bytes, [t*1000 for t in des_dec_times], 's-', color=ACCENT_RED, label='Decryption')
        self.des_ax1.set_xscale('log')
        self.des_ax1.set_yscale('log')
        self.des_ax1.set_xlabel('File Size (bytes)', color=TEXT_MUTED, fontsize=8)
        self.des_ax1.set_ylabel('Time (milliseconds)', color=TEXT_MUTED, fontsize=8)
        self.des_ax1.set_title('DES Execution Time vs File Size', color=TEXT_MAIN, fontsize=9)
        self.des_ax1.legend(facecolor=CARD_BG, edgecolor=BORDER_COLOR, labelcolor=TEXT_MAIN, fontsize=8)
        
        # Plot throughput (bar chart)
        labels = ["100 B", "1 KB", "10 KB", "100 KB", "500 KB"]
        self.des_ax2.bar(labels, [s/1e6 for s in des_speeds_bps], color=ACCENT_GREEN)
        self.des_ax2.set_xlabel('File Size', color=TEXT_MUTED, fontsize=8)
        self.des_ax2.set_ylabel('Throughput (Mbps)', color=TEXT_MUTED, fontsize=8)
        self.des_ax2.set_title('DES Throughput by File Size', color=TEXT_MAIN, fontsize=9)
        
        self.style_figure(self.des_fig)
        self.des_fig.tight_layout()
        self.des_canvas.draw()
        
        # 2. Update RSA plots
        prime_bit_sizes, rsa_keygen_times, rsa_enc_times, rsa_dec_times = rsa_data
        
        self.rsa_ax.clear()
        self.rsa_ax.plot(prime_bit_sizes, [t*1000 for t in rsa_keygen_times], 'o-', color=ACCENT_BLUE, label='Key Generation')
        self.rsa_ax.plot(prime_bit_sizes, [t*1000 for t in rsa_enc_times], 's-', color=ACCENT_GREEN, label='Encryption (100 char)')
        self.rsa_ax.plot(prime_bit_sizes, [t*1000 for t in rsa_dec_times], 'd-', color=ACCENT_RED, label='Decryption (100 char)')
        self.rsa_ax.set_xscale('linear')
        self.rsa_ax.set_yscale('log')
        self.rsa_ax.set_xlabel('Prime Bit Size (bits)', color=TEXT_MUTED, fontsize=8)
        self.rsa_ax.set_ylabel('Time (milliseconds)', color=TEXT_MUTED, fontsize=8)
        self.rsa_ax.set_title('RSA Execution Time vs Prime Bit Size', color=TEXT_MAIN, fontsize=9)
        self.rsa_ax.legend(facecolor=CARD_BG, edgecolor=BORDER_COLOR, labelcolor=TEXT_MAIN, fontsize=8)
        
        self.style_figure(self.rsa_fig)
        self.rsa_fig.tight_layout()
        self.rsa_canvas.draw()


if __name__ == "__main__":
    app = CryptoShieldApp()
    app.mainloop()

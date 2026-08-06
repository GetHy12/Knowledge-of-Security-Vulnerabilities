import os
import re
import subprocess

# FIX 1: Menghapus hardcoded credentials. 
# Menggunakan environment variables agar password tidak terlihat di dalam kode.
ADMIN_USER = os.environ.get("ADMIN_USER")
ADMIN_PASS = os.environ.get("ADMIN_PASS")

def login():
    print("=== Network Status Checker (Secure Version) ===")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    # Pengecekan jika environment variables belum disetel di server
    if not ADMIN_USER or not ADMIN_PASS:
        print("[-] Server configuration error: Credentials not set in environment.")
        return False

    if username == ADMIN_USER and password == ADMIN_PASS:
        print("[+] Login Successful!\n")
        return True
    else:
        print("[-] Invalid credentials!")
        return False

def is_valid_ip(ip):
    # FIX 2: Input validation menggunakan Regex.
    # Memastikan input dari pengguna benar-benar murni berformat IPv4.
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip) is not None

def check_network():
    target_ip = input("Enter target IP to ping (e.g., 8.8.8.8): ")
    
    # Mengeksekusi validasi sebelum melangkah lebih jauh
    if not is_valid_ip(target_ip):
        print("[-] Invalid IP format detected. Aborting.")
        return

    print(f"Pinging {target_ip}...")
    
    # FIX 3: Mencegah Command Injection.
    # Menggunakan subprocess.run dengan format list argumen alih-alih os.system string raw.
    try:
        subprocess.run(["ping", "-c", "3", target_ip], check=True)
    except subprocess.CalledProcessError:
        print("[-] Ping command failed.")

if __name__ == "__main__":
    if login():
        check_network()
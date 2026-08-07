import os
import re
import subprocess

# FIX 1: Remove hardcoded credentials.
# Credentials are now loaded from environment variables so they never appear in source.
ADMIN_USER = os.environ.get("ADMIN_USER")
ADMIN_PASS = os.environ.get("ADMIN_PASS")


def login():
    print("=== Network Status Checker (Secure Version) ===")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    # Fail safely if the server/environment was never configured
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
    # FIX 2: Input validation using Regex.
    # Each octet is bounded to 0-255 (not just "1-3 digits") so values like
    # 999.999.999.999 are correctly rejected as invalid IPv4 addresses.
    octet = r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])"
    pattern = re.compile(rf"^{octet}(\.{octet}){{3}}$")
    return pattern.match(ip) is not None


def check_network():
    target_ip = input("Enter target IP to ping (e.g., 8.8.8.8): ")

    if not is_valid_ip(target_ip):
        print("[-] Invalid IP format detected. Aborting.")
        return

    print(f"Pinging {target_ip}...")

    # FIX 3: Prevent Command Injection.
    # subprocess.run() is called with an argument list (no shell=True), so the
    # OS shell never parses the string and cannot execute chained/injected commands.
    try:
        subprocess.run(["ping", "-c", "3", target_ip], check=True)
    except subprocess.CalledProcessError:
        print("[-] Ping command failed.")


if __name__ == "__main__":
    if login():
        check_network()

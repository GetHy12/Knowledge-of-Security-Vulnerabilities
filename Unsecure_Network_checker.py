import os

# Vulnerability 1: Hardcoded credentials
# Admin credentials stored in plaintext inside the source code
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def login():
    print("=== Network Status Checker ===")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if username == ADMIN_USER and password == ADMIN_PASS:
        print("[+] Login Successful!\n")
        return True
    else:
        print("[-] Invalid credentials!")
        return False

def check_network():
    # Vulnerability 2: Missing input validation
    # The script accepts any string from the user without sanitizing it
    target_ip = input("Enter target IP or Domain to ping (e.g., 8.8.8.8): ")
    
    print(f"Pinging {target_ip}...")
    
    # Vulnerability 3: Command injection example
    # The unsanitized input is passed directly to the system shell
    # An attacker can input: 8.8.8.8; ls -la
    os.system(f"ping -c 3 {target_ip}")

if __name__ == "__main__":
    if login():
        check_network()
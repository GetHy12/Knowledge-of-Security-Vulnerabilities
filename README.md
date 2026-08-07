# Knowledge-of-Security-Vulnerabilities

## What the script does

This is a simple Python Command Line Interface (CLI) application designed to check network
connectivity. It requires the user to log in securely and then prompts the user to enter a
target IP address to execute a system `ping` command.

## Vulnerabilities Included (in `Unsecure_Network_checker.py`)

This script intentionally includes 3 common security vulnerabilities:

1. **Hardcoded Credentials**
   - **What it is:** The admin username and password are saved as plain text directly inside
     the source code.
   - **Why it's a risk:** Anyone who can read the code (such as in a public repository) can
     immediately see the password and gain unauthorized access.

2. **Missing Input Validation**
   - **What it is:** The application asks for an IP address but does not verify if the user
     actually typed a valid IP format before processing it.
   - **Why it's a risk:** It allows attackers to input malicious characters or system commands
     instead of a normal IP address.

3. **Command Injection**
   - **What it is:** The script takes the unsanitized user input and passes it directly to the
     system shell using the `os.system()` function.
   - **Why it's a risk:** An attacker can input something like `8.8.8.8; cat /etc/passwd`. The
     system will execute the ping, and then execute the dangerous `cat` command, potentially
     taking over the system or leaking sensitive server data.

## How to Fix It (in `Secure_Network_checker.py`)

1. **Environment Variables:** Credentials are removed from the code and are now loaded safely
   from the server's environment variables (`os.environ.get`).
2. **Input Validation (Regex):** The script now uses a Regular Expression (Regex) to verify
   that the user's input strictly matches a valid IPv4 format — including bounding each octet
   to the 0–255 range — before proceeding.
3. **Safe Subprocess Execution:** Replaced `os.system()` with
   `subprocess.run(["ping", "-c", "3", target_ip])`. Passing arguments as an array/list instead
   of a raw shell string prevents the shell from executing any chained or injected commands.

## How to Run

Requires Python 3.8+ and a Unix-like environment with `ping` on the PATH (Linux/macOS; on
Windows adjust the `ping` flag from `-c` to `-n` in the script).

### 1. Clone the repository

```bash
git clone https://github.com/GetHy12/Knowledge-of-Security-Vulnerabilities.git
cd Knowledge-of-Security-Vulnerabilities
```

### 2. Set the required credentials as environment variables

The secure version reads credentials from the environment — it will refuse to start if these
are not set.

```bash
# Linux / macOS
export ADMIN_USER="admin"
export ADMIN_PASS="your-chosen-password"

# Windows PowerShell
$Env:ADMIN_USER = "admin"
$Env:ADMIN_PASS = "your-chosen-password"
```

### 3. Run the secure version

```bash
python3 Secure_Network_checker.py
```

Log in with the username/password you exported above, then enter a target IP (e.g. `8.8.8.8`)
when prompted.

### 4. (Optional, for comparison only) Run the vulnerable version

Only run this in an isolated/sandboxed environment — it contains intentional vulnerabilities,
including a hardcoded login (`admin` / `admin123` in the source) and unsanitized shell
execution.

```bash
python3 Unsecure_Network_checker.py
```

To see the command-injection flaw in action, log in and enter an IP such as:

```text
8.8.8.8; echo INJECTED
```

In the unsecure version this executes the extra `echo` command; in the secure version the
regex rejects the input outright.

# Knowledge-of-Security-Vulnerabilities

## What the script does
This is a simple Python Command Line Interface (CLI) application designed to check network connectivity. It requires the user to log in securely and then prompts the user to enter a target IP address to execute a system `ping` command.

## Vulnerabilities Included (in `Unsecure_network_checker.py`)
This script intentionally includes 3 common security vulnerabilities:

1. **Hardcoded Credentials**
   * **What it is:** The admin username and password are saved as plain text directly inside the source code.
   * **Why it's a risk:** Anyone who can read the code (such as in a public repository) can immediately see the password and gain unauthorized access.

2. **Missing Input Validation**
   * **What it is:** The application asks for an IP address but does not verify if the user actually typed a valid IP format before processing it.
   * **Why it's a risk:** It allows attackers to input malicious characters or system commands instead of a normal IP address.

3. **Command Injection**
   * **What it is:** The script takes the unsanitized user input and passes it directly to the system shell using the `os.system()` function.
   * **Why it's a risk:** An attacker can input something like `8.8.8.8; cat /etc/passwd`. The system will execute the ping, and then execute the dangerous `cat` command, potentially taking over the system or leaking sensitive server data.

## How to Fix It (in `secure_network_checker.py`)
To fix these vulnerabilities, a secure version has been created with the following mitigations:

1. **Environment Variables:** Credentials are removed from the code and are now loaded safely from the server's environment variables (`os.environ.get`).
2. **Input Validation (Regex):** The script now uses a Regular Expression (Regex) to verify that the user's input strictly matches an IPv4 format before proceeding.
3. **Safe Subprocess Execution:** Replaced `os.system()` with `subprocess.run(["ping", "-c", "3", target_ip])`. Passing arguments as an array list prevents the shell from executing any chained or injected commands.

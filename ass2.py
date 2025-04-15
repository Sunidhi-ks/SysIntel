import os
import re
import time
import heapq
from collections import defaultdict
from logger import logger

def run_log_inspector():
    logger.info("Running Log Inspector")
    print("Log Inspector Output")
    


def analyze_auth_log(log_path="/var/log/auth.log"):
    print("\n--- Unauthorized Access Report ---")
    failed_logins = []
    sudo_misuse = []
    brute_force_ips = defaultdict(int)

    try:
        with open(log_path, "r") as f:
            for line in f:
                if "Failed password" in line:
                    failed_logins.append(line)
                    ip_match = re.search(r'from\s+(\d+\.\d+\.\d+\.\d+)', line)
                    if ip_match:
                        ip = ip_match.group(1)
                        brute_force_ips[ip] += 1

                if "sudo" in line and "authentication failure" in line:
                    sudo_misuse.append(line)

    except FileNotFoundError:
        print(f"Log file not found: {log_path}")
        return

    print("\nFailed Login Attempts:")
    if failed_logins:
        for entry in failed_logins[-5:]:
            print(entry.strip())
    else:
        print("No failed login attempts found.")

    print("\nSudo Misuse Attempts:")
    if sudo_misuse:
        for entry in sudo_misuse[-5:]:
            print(entry.strip())
    else:
        print("No sudo misuse attempts found.")

    print("\nPotential Brute Force IPs:")
    printed = False
    for ip, count in brute_force_ips.items():
        if count > 5:
            print(f"{ip} -> {count} attempts")
            printed = True
    if not printed:
        print("No brute force IPs detected.")

    print("\n✅ Log analysis completed.\n")


def get_top_10_largest_files(start_path='/'):
    large_files = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            try:
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                heapq.heappush(large_files, (-size, filepath))
            except:
                continue

    print("\n 10 Largest Files")
    for i in range(min(10, len(large_files))):
        size, filepath = heapq.heappop(large_files)
        print(f"{filepath} - {abs(size)/1024/1024:.2f} MB")

def get_files_modified_last_24_hours(start_path='/', max_files=10):
    now = time.time()
    recent_files = []

    for root, dirs, files in os.walk(start_path):
        for file in files:
            try:
                filepath = os.path.join(root, file)
                if os.path.getmtime(filepath) >= now - 86400:
                    recent_files.append(filepath)
            except:
                continue

    print(f"\n Files Modified({max_files})")
    for f in recent_files[:max_files]:
        print(f)

def list_hidden_files_in_home(max_files=10):
    home = os.path.expanduser("~")
    hidden = []

    for root, dirs, files in os.walk(home):
        for name in files:
            if name.startswith("."):
                hidden.append(os.path.join(root, name))

    print(f"\n Hidden Files({max_files})")
    for f in hidden[:max_files]:
        print(f)

def main():
    analyze_auth_log()
    get_top_10_largest_files('/')
    get_files_modified_last_24_hours('/', max_files=10)
    list_hidden_files_in_home(max_files=10)

if __name__ == "__main__":
    main()


def run_log_inspector():
    log_file = "/var/log/syslog"  # For Ubuntu/Debian
    if not os.path.exists(log_file):
        log_file = "/var/log/messages"  # Fallback (CentOS/RHEL)

    try:
        with open(log_file, "r") as file:
            lines = file.readlines()[-20:]  # Get last 20 lines

        print("Recent Log Entries with WARN/ERROR:\n")
        for line in lines:
            if "error" in line.lower() or "warn" in line.lower():
                print(line.strip())
    except PermissionError:
        print("Permission denied. Try running as sudo to read system logs.")
    except FileNotFoundError:
        print("Log file not found.")
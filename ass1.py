import subprocess
import psutil
import json
from datetime import datetime
from logger import logger

def run_system_monitor():
    logger.info("Running System Monitor")
    print("System Monitor Output")



# ---------- Utility to run shell commands ----------
def run_command(command_list):
    try:
        return subprocess.check_output(command_list, text=True)
    except Exception as e:
        return f"Error running {' '.join(command_list)}: {e}"

# ---------- Collect Monitoring Data ----------
def collect_data():
    data = {}

    # CPU Usage (via top)
    data["CPU_Usage"] = run_command(["top", "-bn1"])

    # RAM Usage
    data["RAM_Usage"] = run_command(["free", "-h"])

    # Disk Usage
    data["Disk_Usage"] = run_command(["df", "-h"])

    # Disk I/O (iostat)
    # iostat may not be installed by default
    data["Disk_IO"] = run_command(["iostat"])  # If error, install via sudo apt install sysstat

    # Network I/O
    data["Network_IO"] = run_command(["ifconfig"])

    # System Uptime + Load Average
    data["Uptime_Load"] = run_command(["uptime"])

    # Running Services
    data["Running_Services"] = run_command(["systemctl", "list-units", "--type=service", "--state=running"])

    return data

# ---------- Display Human-Readable ----------
def print_human(data):
    print("SYSTEM MONITOR REPORT")
    for key, value in data.items():
        print(f"--- {key.replace('_', ' ')} ---")
        print(value)
        print("\n")

# ---------- Save as JSON with timestamp ----------
def save_as_json(data):
    timestamp = datetime.now().isoformat(timespec='seconds').replace(":", "-")
    filename = f"log_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[✓] JSON log saved as: {filename}")

# ---------- Main ---------#


if __name__ == "__main__":
    print("[*] Monitoring system...")
    monitoring_data = collect_data()
    
    print_human(monitoring_data)
    save_as_json(monitoring_data)


def run_system_monitor():
    print("CPU Usage:", psutil.cpu_percent(interval=1), "%")
    print("Memory Usage:", psutil.virtual_memory().percent, "%")
    print("Disk Usage:", psutil.disk_usage('/').percent, "%")
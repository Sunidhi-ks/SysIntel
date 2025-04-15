import psutil
import socket
import subprocess
from logger import logger

def run_network_intel():
    logger.info("Running Network Intel")
    print("Network Intel Output")
    # Your actual code goes here


def scan_active_connections():
    print("\n--- Active Network Connections ---")
    connections = psutil.net_connections(kind='inet')

    listening = []
    external_ips = set()

    for conn in connections:
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else ""
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else ""
        status = conn.status

        if status == "LISTEN":
            listening.append(laddr)
        elif conn.raddr and conn.raddr.ip not in ("127.0.0.1", "::1"):
            external_ips.add(conn.raddr.ip)

    print("\nListening Ports:")
    for port in listening:
        print(port)

    print("\nExternal IPs Connected:")
    for ip in external_ips:
        print(ip)


def check_local_open_ports(ports):
    print("\n--- Port Check on Localhost ---")
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', port))
            if result == 0:
                print(f"Port {port} is OPEN")
            else:
                print(f"Port {port} is CLOSED")


def ping_host(host="8.8.8.8"):
    print(f"\n--- Pinging {host} ---")
    try:
        subprocess.run(["ping", "-c", "4", host], check=True)
    except subprocess.CalledProcessError:
        print("Ping failed.")


def traceroute_host(host="8.8.8.8"):
    print(f"\n--- Traceroute to {host} ---")
    try:
        subprocess.run(["traceroute", host])
    except FileNotFoundError:
        print("Traceroute utility not found. Install using: sudo apt install traceroute")


# === MAIN CALLS ===
if __name__ == "__main__":
    scan_active_connections()
    check_local_open_ports([22, 80, 443])  # SSH, HTTP, HTTPS
    traceroute_host("8.8.8.8")             # Bonus traceroute

def run_network_intel():
    print("Host Name:", socket.gethostname())
    print("Local IP Address:", socket.gethostbyname(socket.gethostname()))
    
    print("\nActive Network Connections:")
    connections = psutil.net_connections(kind='inet')
    for conn in connections[:10]:  # Just show top 10
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
        print(f"Type: {conn.type} | Status: {conn.status} | Local: {laddr} | Remote: {raddr}")

import socket
import sys
from datetime import datetime

def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Could not resolve hostname: {target}")
        sys.exit(1)

def log_scan_result(port, status):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_now} - Port {port}: {status}")
    return f"{time_now} - Port {port}: {status}"

def scan_port(target, port, results):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                results.append(log_scan_result(port, "Open"))
    except Exception as e:
        results.append(log_scan_result(port, f"Error - {e}"))

def scan_ports(target, start_port, end_port):
    results = []
    print(f"Scanning {target} from port {start_port} to {end_port}")
    for port in range(start_port, end_port + 1):
        scan_port(target, port, results)
    return results

def save_results(target, results):
    filename = f"scan_results_{target}.txt"
    with open(filename, "w") as f:
        for result in results:
            f.write(result + "\n")
    print(f"Results saved to {filename}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python port_scanner.py <target> <start_port> <end_port>")
        sys.exit(1)

    target = resolve_target(sys.argv[1])
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("Please provide a valid port range (1-65535).")
        sys.exit(1)

    results = scan_ports(target, start_port, end_port)
    save_results(target, results)

if __name__ == "_main_":
    main()
import socket
import threading
import subprocess
import re

def discover_targets():
    """
    Discover available targets on the local network using the arp -a command.
    """
    try:
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        targets = re.findall(r"(\d+\.\d+\.\d+\.\d+)", result.stdout)
        return targets
    except Exception as e:
        print(f"Error discovering targets: {e}")
        return []

def scan_port(target, port):
    """
    Scan a single port on the target.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Timeout for the connection
            result = s.connect_ex((target, port))
            if result == 0:  # Port is open
                print(f"[+] Port {port} is open")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

def thread_worker(target, ports):
    """
    Worker function for scanning a range of ports in a thread.
    """
    for port in ports:
        scan_port(target, port)

def divide_ports(start_port, end_port, num_threads):
    """
    Divide the range of ports into chunks for multithreaded processing.
    """
    port_range = list(range(start_port, end_port + 1))
    chunk_size = len(port_range) // num_threads
    return [port_range[i:i + chunk_size] for i in range(0, len(port_range), chunk_size)]

def scan_ports_multithreaded(target, start_port, end_port, num_threads):
    """
    Perform a multithreaded scan on the target within the specified port range.
    """
    port_chunks = divide_ports(start_port, end_port, num_threads)
    threads = []

    for chunk in port_chunks:
        thread = threading.Thread(target=thread_worker, args=(target, chunk))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def main():
    """
    Main function to prompt the user for input or list discovered targets.
    """
    print("Available targets:")
    targets = discover_targets()
    for i, target in enumerate(targets, start=1):
        print(f"{i}. {target}")

    # Prompt user to select or enter a target
    target_choice = input("\nEnter the target number (or type an IP/hostname): ").strip()
    if target_choice.isdigit() and 1 <= int(target_choice) <= len(targets):
        target = targets[int(target_choice) - 1]
    else:
        target = target_choice

    # Prompt for port range and number of threads
    try:
        start_port = int(input("Enter the start port: "))
        end_port = int(input("Enter the end port: "))
        num_threads = int(input("Enter the number of threads: "))

        if start_port < 1 or end_port > 65535 or start_port > end_port:
            print("Invalid port range. Ports must be between 1 and 65535.")
            return

        if num_threads < 1:
            print("Number of threads must be at least 1.")
            return

        print(f"Scanning {target} from port {start_port} to {end_port} using {num_threads} threads.")
        scan_ports_multithreaded(target, start_port, end_port, num_threads)

    except ValueError:
        print("Invalid input. Please enter numbers for ports and threads.")
        return

if __name__ == "_main_":
    main()
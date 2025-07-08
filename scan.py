from datetime import datetime
from sync_scan import scan_ports_sync
from async_scan import run_tcp_connect_scan, run_nmap_scan
import asyncio
import socket

def print_nmap_style(results, ip):
    print(f"\nNmap scan report for {ip}")
    print(f"{'PORT':<9} {'STATE':<14} {'SERVICE'}")
    open_ports = []
    closed_or_filtered_count = 0
    for port in sorted(results):
        merged_status = None
        for _, status in results[port].items():
            merged_status = status
        proto = "udp" if "U" in results[port] else "tcp"
        try:
            service = socket.getservbyport(port, proto)
        except:
            service = "unknown"
        if merged_status.lower() == "open":
            open_ports.append((f"{port}/{proto}", merged_status, service))
        else:
            closed_or_filtered_count += 1
    for port_proto, state, service in open_ports:
        print(f"{port_proto:<9} {state:<14} {service}")
    if closed_or_filtered_count > 0:
        print(f"\nNot shown: {closed_or_filtered_count} closed or filtered ports")

def main():
    ip = input("Target IP: ").strip()
    mode = input("Scan Mode (sync/async): ").strip().lower()
    scan_type = input("Scan Type (S, U, X, N, A, C): ").strip().upper()
    ports_input = input("Ports (comma-separated): ").strip()
    ports = []
    for part in ports_input.split(","):
        part = part.strip()
        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))

    start_time = datetime.now()

    if mode == "sync":
        results = scan_ports_sync(ip, ports, scan_type)
    elif mode == "async":
        if scan_type == "C":
            results = asyncio.run(run_tcp_connect_scan(ip, ports))
        else:
            results = asyncio.run(run_nmap_scan(ip, ports, scan_type))
    else:
        print("Invalid mode")
        return

    print_nmap_style(results, ip)

    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\nScan completed in {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()

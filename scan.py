from datetime import datetime
from sync_scan import scan_ports_sync
from async_scan import run_tcp_connect_scan, run_nmap_scan
import asyncio
import socket
import ipaddress

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

def choose_mode(ip_list, ports):
    ip_count = len(ip_list)
    port_count = len(ports)
    target_count = ip_count * port_count
    if ip_count > 1 or port_count > 10 or target_count > 20:
        return "async"
    else:
        return "sync"

def expand_ip_input(ip_str):
    ip_str = ip_str.strip()
    result = []

    if '/' in ip_str:
        # CIDR 표기법
        net = ipaddress.IPv4Network(ip_str, strict=False)
        result = [str(ip) for ip in net.hosts()]
    elif '-' in ip_str:
        # 범위
        start, end = ip_str.split('-')
        start = start.strip()
        end = end.strip()
        if '.' in end:
            # ex) 192.168.56.1-192.168.56.10
            start_ip = ipaddress.IPv4Address(start)
            end_ip = ipaddress.IPv4Address(end)
        else:
            # ex) 192.168.56.1-10
            parts = start.split('.')
            base = '.'.join(parts[:3])
            start_num = int(parts[3])
            end_num = int(end)
            start_ip = ipaddress.IPv4Address(f"{base}.{start_num}")
            end_ip = ipaddress.IPv4Address(f"{base}.{end_num}")
        result = [str(ipaddress.IPv4Address(ip))
                  for ip in range(int(start_ip), int(end_ip) + 1)]
    else:
        result = [ip_str]

    return result

def main():
    ip_input = input("Target IP(s) (comma, space, range, CIDR): ").strip()
    raw_ip_parts = []
    if ',' in ip_input:
        raw_ip_parts = [ip.strip() for ip in ip_input.split(',')]
    else:
        raw_ip_parts = ip_input.split()

    ip_list = []
    for part in raw_ip_parts:
        ip_list.extend(expand_ip_input(part))

    ports_input = input("Ports (e.g. 22, 80, 1000-1010): ").strip()
    ports = []
    for part in ports_input.split(","):
        part = part.strip()
        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))

    scan_type = input("Scan Type (S, U, X, N, A, C): ").strip().upper()

    mode = choose_mode(ip_list, ports)
    print(f"\n[INFO] Auto-selected scan mode: {mode.upper()}")

    start_time = datetime.now()

    for ip in ip_list:
        # CIDR 입력일 경우 nmap이 알아서 처리하므로 리스트 대신 원본 IP 사용
        if '/' in ip_input and scan_type != 'C' and mode == 'async':
            results = asyncio.run(run_nmap_scan(ip_input, ports, scan_type))
            print_nmap_style(results, ip_input)
            break  # CIDR은 한 번만 처리
        else:
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

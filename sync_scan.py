from scapy.all import IP, TCP, UDP, ICMP, sr, sr1

def scan_ports_sync(ip, ports, scan_type="S"):
    results = {}
    flag_map = {'S': 'S', 'A': 'A', 'N': '', 'X': 'FPU'}
    if scan_type == 'U':
        for port in ports:
            pkt = IP(dst=ip)/UDP(dport=port)
            resp = sr1(pkt, timeout=2, verbose=0)
            results[port] = {"U": analyze_udp(resp)}
    else:
        flags = flag_map.get(scan_type)
        packets = [IP(dst=ip)/TCP(dport=port, flags=flags) for port in ports]
        answered, unanswered = sr(packets, timeout=2, verbose=0)
        for send, recv in answered:
            port = send.dport
            tcp_flags = recv.getlayer(TCP).flags if recv.haslayer(TCP) else None
            results.setdefault(port, {})
            results[port][scan_type] = analyze_tcp(scan_type, tcp_flags)
        for send in unanswered:
            port = send.dport
            results.setdefault(port, {})
            results[port][scan_type] = "Open|Filtered" if scan_type in ['X', 'N'] else "Filtered"
    return results

def analyze_tcp(scan_type, tcp_flags):
    if scan_type == 'S':
        if tcp_flags == 0x12: return "Open"
        elif tcp_flags == 0x14: return "Closed"
    elif scan_type == 'A':
        if tcp_flags == 0x4 or tcp_flags == 0x14: return "Unfiltered"
    elif scan_type in ['X', 'N']:
        if tcp_flags == 0x14: return "Closed"
    return "Open|Filtered"

def analyze_udp(resp):
    if resp is None: return "Open|Filtered"
    elif resp.haslayer(UDP): return "Open"
    elif resp.haslayer(ICMP):
        icmp = resp.getlayer(ICMP)
        if icmp.type == 3 and icmp.code in [1, 2, 3, 9, 10, 13]: return "Closed"
    return "Unknown"

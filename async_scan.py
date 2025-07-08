import asyncio
import re

async def run_tcp_connect_single(ip, port):
    try:
        conn = asyncio.open_connection(ip, port)
        reader, writer = await asyncio.wait_for(conn, timeout=1)
        writer.close()
        await writer.wait_closed()
        return port, {"C": "Open"}
    except:
        return port, {"C": "Closed"}

async def run_tcp_connect_scan(ip, ports):
    tasks = [run_tcp_connect_single(ip, port) for port in ports]
    results = await asyncio.gather(*tasks)
    return dict(results)

async def run_nmap_scan(ip, ports, scan_type):
    scan_flags = {"S": "-sS", "A": "-sA", "X": "-sX", "N": "-sN", "U": "-sU"}
    flag = scan_flags.get(scan_type, "-sS")
    port_arg = ",".join(str(p) for p in ports)
    cmd = ["nmap", flag, "-p", port_arg, ip, "-oG", "-"]

    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    output = stdout.decode()

    results = {}
    for line in output.splitlines():
        if "Ports:" in line:
            parts = line.split("Ports:")[1].strip().split(",")
            for part in parts:
                match = re.search(r"(\d+)/(\w+)/(\w+)/", part)
                if match:
                    port = int(match.group(1))
                    state = match.group(2)
                    results[port] = {scan_type: state}
    return results

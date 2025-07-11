import asyncio # Event loop, Coroutines, Non blocking networking
import argparse # Simplifies command-line argument parsing for user input
from datetime import datetime

""" 
We choose asyncio because: port scanning involves many concurrent network I/O
argparse lets us expose --targets --ports flags easily
datetime: Measure per-probe durations
"""

async def scan_port(ip, port, timeout=1.0):
    """
    attempts an asynchronous TCP connection to (ip, port)
    Returns (ip, port, Bool)
    """
    start = datetime.now()
    is_open = False
    try:
        # Open a connection; under the hood this sends a SYN and awaits response
        # Aborts connection if no response within 'timeout' seconds
        conn_coro = asyncio.open_connection(ip, port)
        reader, writer = await asyncio.wait_for(conn_coro, timeout)
        is_open = True
        writer.close() # close cleanly if successful
        await writer.wait_closed()
    except asyncio.TimeoutError:
        print(f"{ip}:{port} TIMEOUT after {timeout}s")
    except Exception as e:
        print(e)
    
    duration = (datetime.now() - start).total_seconds()
    print(f"{ip}:{port} {'OPEN' if is_open else 'CLOSED'}")
    return ip, port, is_open, duration

async def main(targets, ports, timeout):
    # Build a list of coroutines; one per target-port pair
    tasks = [scan_port(ip, port, timeout)
             for ip in targets for port in ports
            ]
    
    # Run them concurrently and wait for all to finish
    await asyncio.gather(*tasks)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Async SYN Scanner v1")
    parser.add_argument('--targets', nargs='+', required = True,
                        help = 'List of IPs to scan')
    parser.add_argument('--ports', nargs='+', type = int, required= True,
                        help = 'List of ports to scan')
    parser.add_argument('--timeout', type=float, default = 1.0,
                        help = 'Give up on a probe after x seconds')
    args = parser.parse_args()

    # Start the asyncio event loop
    asyncio.run(main(args.targets, args.ports, args.timeout))
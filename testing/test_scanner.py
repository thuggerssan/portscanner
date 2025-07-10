import asyncio # Event loop, Coroutines, Non blocking networking
import argparse # Simplifies command-line argument parsing for user input

""" 
We choose asyncio because: port scanning involves many concurrent network I/O
argparse lets us expose --targets --ports flags easily
"""

async def scan_port(ip, port):
    """
    attempts an asynchronous TCP connection to (ip, port)
    Returns (ip, port, Bool)
    """
    try:
        # Open a connection; under the hood this sends a SYN and awaits response
        reader, writer = await asyncio.open_connection(ip, port)
        writer.close() # close cleanly if successful
        await writer.wait_closed()

        return ip, port, True
    except Exception as e:
        print(e)
        return ip, port, False

async def main(targets, ports):
    # Build a list of coroutines; one per target-port pair
    tasks = [scan_port(ip, port) for ip in targets for port in ports]
    
    # Run them concurrently and wait for all to finish
    results = await asyncio.gather(*tasks)

    for ip, port, is_open in results:
        status = 'OPEN' if is_open else 'CLOSED'
        print(f"{ip}:{port} {status}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Async SYN Scanner v1")
    parser.add_argument('--targets', nargs='+', required = True,
                        help = 'List of IPs to scan')
    parser.add_argument('--ports', nargs='+', type = int, required= True,
                        help = 'List of ports to scan')
    args = parser.parse_args()

    # Start the asyncio event loop
    asyncio.run(main(args.targets, args.ports))

import socket


BANNER = """
  _   _            _       __             
 | \ | |          | |     /_ |            
 |  \| | ___ _   _| |_ _ __| |_ __   ___  
 | . ` |/ _ \ | | | __| '__| | '_ \ / _ \ 
 | |\  |  __/ |_| | |_| |  | | | | | (_) |
 |_| \_|\___|\__,_|\__|_|  |_|_| |_|\___/                                                                             
"""
formatted_banner = "-"*60 + "\n" + BANNER + "-"*60


def print_usage():
    """
    prints usage instructions
    """

    print(formatted_banner)
    print("Usage: python Neutr1no_.py [options]")
    print("Options:")
    print("  -h, --help       Show this help message and exit")
    print("  -ip <address>    Specify an IP address to scan")
    print("  -host <name>     Specify a hostname to resolve and scan")
    """print("\nExample:")
    print("  python Neutr1no.py -ip 192.168.1.1")
    print("  python Neutr1no.py -host example.com")"""


def is_valid_ip(ip_str):
    """
    Checks if the given string is a valid IPv4 address format.
    """

    try:
        socket.inet_pton(socket.AF_INET, ip_str)
        return True
    except socket.error:
        return False

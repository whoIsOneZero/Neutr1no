import sys

from network.dns_lookup import get_ip_address
from network.os_discovery import os_discovery
from network.port_scanner import scan_ports
from utils.helpers import is_valid_ip, print_usage
from vulnerability.vulnerability_scan import vulnerability_scan


"""def main(host):
    print(f"Got the host: {host}")"""


def main():

    # argument parsing
    if len(sys.argv) < 3:
        if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
            print_usage()
            sys.exit(1)

        print_usage()
        sys.exit(1)

    # valid args
    if sys.argv[1] == '-ip' and len(sys.argv) == 3:
        ip_str = sys.argv[2]
        if is_valid_ip(ip_str):
            ip = ip_str
            print(f"Got the IP: {ip}")
        else:
            print("Invalid IP address")
            sys.exit(1)
    elif sys.argv[1] == "-host" and len(sys.argv) == 3:
        hostname = sys.argv[2]
        ip_address = get_ip_address(hostname)
        if ip_address:
            ip = ip_address
            print(f"Got the IP: {ip}")
        else:
            print("Could not resolve hostname")
            sys.exit(1)

    # Perform port scanning, OS discovery, and vulnerability scanning
    services = os_discovery(ip)
    scan_ports(ip)
    vulnerabilities = vulnerability_scan(services)
    print(vulnerabilities)

    """# invalid arg
    else:
        print("Invalid options")
        print_usage()
        sys.exit(1)"""


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import socket
import sys
from colorama import init, Fore
from threading import Thread, Lock
from queue import Queue
import dns.resolver
import vulners
import subprocess

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


def get_ip_address(hostname):
    """
    Performs a DNS lookup using the dnspython library.
    """

    resolver = dns.resolver.Resolver()
    try:
        answers = resolver.resolve(hostname, "A")  # Query for A records
        return str(answers[0].address)  # Return the first IP address
    except dns.resolver.ResolverError as e:
        print(f"DNS lookup error: {e}")
        return None


def main(host):
    print(f"Got the host: {host}")


if __name__ == "__main__":
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
            main(ip)
        else:
            print("Invalid IP address")
            sys.exit(1)
    elif sys.argv[1] == "-host" and len(sys.argv) == 3:
        hostname = sys.argv[2]
        ip_address = get_ip_address(hostname)
        if ip_address:
            ip = ip_address
            main(ip)
        else:
            print("Could not resolve hostname")
            sys.exit(1)

    # invalid arg
    else:
        print("Invalid options")
        print_usage()
        sys.exit(1)

# some colors
init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX
RED = Fore.LIGHTRED_EX
# number of threads, feel free to tune this parameter as you wish
N_THREADS = 100
# thread queue
q = Queue()
print_lock = Lock()
Host = ip or hostname


def port_scan(port):
    """
    Scan a port on the global variable `host`
    """
    try:
        s = socket.socket()
        s.connect((Host, port))
    except:
        with print_lock:
            print(f"{GRAY}{Host:15}:{port:5} is closed  {RESET}", end='\r')
    else:
        with print_lock:
            print(f"{GREEN}{Host:15}:{port:5} is open    {RESET}")
    finally:
        s.close()


def scan_thread():
    """
    worker thread for port scanning
    """
    global q
    while True:
        # get the port number from the queue
        worker = q.get()
        # scan that port number
        port_scan(worker)
        # tells the queue that the scanning for that port
        # is done
        q.task_done()


def main(Host, ports):
    global q
    ports = range(1025)
    try:
        for t in range(N_THREADS):
            # for each thread, start it
            t = Thread(target=scan_thread)
            # when we set daemon to true, that thread will end when the main thread ends
            t.daemon = True
            # start the daemon thread
            t.start()
        for worker in ports:
            # for each port, put that port into the queue
            # to start scanning
            q.put(worker)
            # wait the threads ( port scanners ) to finish
        q.join()
    except socket.gaierror as e:
        print(f"Error: Could not resolve hostname {ip}")


ports = [range(1025)]
main(Host, ports)
print(main)


# OS detection
def os_discovery():

    # More secure than check_call
    service = f"nmap {Host} -sV -version-intensity 8 -T4 --host-timeout 120"
    oS = f"nmap {Host} -O -T4 --host-timeout 120"
    output = subprocess.check_output(service, shell=True).decode('utf-8')
    services = []
    for line in output.splitlines():
        if "open" in line:
            parts = line.split()
            service_name = parts[2]
            services.append(service_name)
    return services


services = os_discovery()


def vulnerability_scan(service):
    all_vulnerabilities = []
    vulners_api = vulners.VulnersApi(api_key="Insert your API key here")

    for service in services:
        print(f"\n\nVulnerabilities found for service: {service}\n\n")
        vulnerabilities = []

        try:
            # Search for vulnerabilities using the Vulners API
            results = vulners_api.find_exploit_all(service)
            filtered_results = [
                result for result in results if service in result['description']]

            # Check if vulnerabilities were found
            if filtered_results:
                for result in filtered_results:
                    vulnerability = {
                        "CVE ID": result.get('id'),
                        "Title": result.get('title'),
                        "Description": result.get('description'),
                        "Severity": result.get('cvss'),
                        "CVSS Score": result.get('cvss', {}).get('score', 'N/A')
                    }
                    vulnerabilities.append(vulnerability)

                    # Print vulnerability details
                    print(f"{GRAY}[+] CVE ID: {result.get('id')}{RESET}")
                    print(f"{GREEN}- Title: {result.get('title')} {RESET}")
                    print(
                        f"{GREEN}- Description: {result.get('description')}{RESET}")
                    print(
                        f"{RED}- CVSS Score: {vulnerability.get('CVSS Score', 'N/A')}{RESET}")
            else:
                print("No vulnerabilities found for this service.")
        except Exception as e:
            print(
                f"Error searching for vulnerabilities for service {service}:", e)

    return all_vulnerabilities


vulnerabilities = vulnerability_scan(services)
print(vulnerabilities)

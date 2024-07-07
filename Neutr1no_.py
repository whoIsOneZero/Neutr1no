import socket
from colorama import init, Fore
from threading import Thread, Lock
from queue import Queue
import dns.resolver
import vulners
import subprocess


def mainMenu():
    """Prints a menu and returns the user's choice."""
    print("-"*80)
    print("NEUTR1NO")
    print("-"*80)
    print()
    print("\t\t\t1---> IP address")
    print("\t\t\t2---> Host Name")
    print()

    while True:
        try:
            choice = int(input("Select Your Option : "))
            return choice
        except ValueError:
            print("Invalid choice. Please enter 1 or 2.")


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
  choice = mainMenu()
  if choice == 1:
    ip_str = input("Enter IP Address: ")
    if is_valid_ip(ip_str):
      ip = ip_str
      main(ip)
    else:
      print("Invalid IP address")
      mainMenu()
  elif choice == 2:
    hostname = input('Enter Host Name: ')
    ip_address = get_ip_address(hostname)
    if ip_address:
      ip = ip_address
      main(ip)
    else:
      mainMenu()
  else:
    print("Invalid Choice :(")
    mainMenu()

# some colors
init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

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
        print (f"Error: Could not resolve hostname {ip}")
ports = [range(1025)]
main(Host,ports)
print(main)

#OS detection
import os

def os_discovery():
    
    # Construct the nmap command using string formatting
    service = f"nmap {Host} -sV -version-intensity 8 -T4 --host-timeout 120"  # More secure than check_call
    oS = f"nmap {Host} -O -T4 --host-timeout 120"
    output = subprocess.check_output(service, shell=True).decode('utf-8')
    services = []
    for line in output.splitlines():
        if "open" in line:
            service = line.split()[2]
            services.append(service)
    return services
services = os_discovery()

def vulnerability_scan(service):
    all_vulnerabilities = []
    vulners_api = vulners.VulnersApi(api_key="QRDTHXAEX2ID16HG561UEFPDDTDJC9GPMKIATCMQ6DWNN3L8V993XUZIC42927I4")

    for service in services:
        print(f"\n\nVulnerabilities found for service: {service}\n\n")
        vulnerabilities = []

        try:
            # Search for vulnerabilities using the Vulners API
            results = vulners_api.find_exploit_all(service)

            # Check if vulnerabilities were found
            if results:
                for result in results:
                    vulnerability = {
                        "CVE ID": result.get('id'),
                        "Title": result.get('title'),
                        "Description": result.get('description')
                    }
                    vulnerabilities.append(vulnerability)

                    # Print vulnerability details
                    print(f"{GRAY}[+] CVE ID: {result.get('id')}{RESET}")
                    print(f"{GREEN}- Title: {result.get('title')} {RESET}")
                    print(f"{GREEN}- Description: {result.get('description')}{RESET}")
            else:
                print("No vulnerabilities found for this service.")
        except Exception as e:
            print(f"Error searching for vulnerabilities for service {service}:", e)

    return all_vulnerabilities
vulnerabilities = vulnerability_scan(services)
print(vulnerabilities)


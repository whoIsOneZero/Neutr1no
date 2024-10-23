import socket
from threading import Thread, Lock
from queue import Queue
from colorama import Fore, init

# Init colors
init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

N_THREADS = 100
q = Queue()
print_lock = Lock()

def port_scan(Host, port):
    """
    Scan a port on the given host.
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

def scan_thread(Host):
    global q
    while True:
        worker = q.get()
        port_scan(Host, worker)
        q.task_done()

def scan_ports(Host):
    global q
    ports = range(1025)
    try:
        for t in range(N_THREADS):
            t = Thread(target=scan_thread, args=(Host,))
            t.daemon = True
            t.start()
        for worker in ports:
            q.put(worker)
        q.join()
    except socket.gaierror as e:
        print(f"Error: Could not resolve hostname {Host}")

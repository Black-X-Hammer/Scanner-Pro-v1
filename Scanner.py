
import socket
import threading
import argparse
from datetime import datetime

print("="*50)
print("""                                                                   Schanner *                                                                          
██████╗ ██╗      █████╗  ██████╗██╗  ██╗    ██╗  ██╗     ██╗  ██╗ █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝    ╚██╗██╔╝     ██║  ██║██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
██████╔╝██║     ███████║██║     █████╔╝█████╗╚███╔╝█████╗███████║███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
██╔══██╗██║     ██╔══██║██║     ██╔═██╗╚════╝██╔██╗╚════╝██╔══██║██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
██████╔╝███████╗██║  ██║╚██████╗██║  ██╗    ██╔╝ ██╗     ██║  ██║██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝

""")
print("="*50)

# Argument Parser
parser = argparse.ArgumentParser(description="Simple Network Scanner")
parser.add_argument("-t", "--target", required=True, help="Target IP or domain")
parser.add_argument("-p", "--ports", help="Ports (e.g. 20-100)")
args = parser.parse_args()

target = socket.gethostbyname(args.target)

# Port Range
if args.ports:
    start_port, end_port = map(int, args.ports.split("-"))
else:
    start_port, end_port = 1, 1024

print(f"Scanning Target: {target}")
print(f"Ports: {start_port} - {end_port}")
print(f"Start Time: {datetime.now()}")
print("-"*50)

lock = threading.Lock()

def scan(port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        
        result = s.connect_ex((target, port))
        
        if result == 0:
            try:
                banner = s.recv(1024).decode().strip()
            except:
                banner = "Unknown Service"
            
            with lock:
                print(f"[OPEN] Port {port} | {banner}")
        
        s.close()
    except:
        pass

# Threads
threads = []

for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("-"*50)
print(f"Finished at: {datetime.now()}")

```
15.Check which ports are open on a host (socket)?


import socket

host = "127.0.0.1"

start_port = 1
end_port = 1024

print(f"Scanning host: {host}")

for port in range(start_port, end_port + 1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((host, port))

    if result == 0:
        print(f"Port {port} is OPEN")

    sock.close()

print("Port scanning completed.")

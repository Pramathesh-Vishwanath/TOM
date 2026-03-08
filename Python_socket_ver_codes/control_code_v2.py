import socket

HOST = "127.0.0.1"
WEB_PORT  = 7001
BRIDGE_PORT = 6001

# connect to bridge
bridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bridge.connect((HOST, BRIDGE_PORT))

# listen to web
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind((HOST, WEB_PORT))
srv.listen(1)
conn, _ = srv.accept()

print("Control mode 1 running")

while True:
    cmd = conn.recv(1024).decode().strip()
    if cmd:
        print("Control got:", cmd)
        bridge.sendall(cmd.encode())
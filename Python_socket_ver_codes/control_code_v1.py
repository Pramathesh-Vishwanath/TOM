import socket

HOST = "127.0.0.1"
PORT = 6001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print("Type ON or OFF")

while True:
    cmd = input("> ").strip().upper()
    if cmd in ["ON", "OFF"]:
        sock.sendall((cmd + "\n").encode())
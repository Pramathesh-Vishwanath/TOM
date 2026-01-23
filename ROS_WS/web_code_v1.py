import socket

HOST = "127.0.0.1"
PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print("Web connected")

while True:
    data = sock.recv(1024).decode()
    if not data:
        break
    print("WEB:", data.strip())


    """Test succesful"""
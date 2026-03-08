import socket, time, serial, threading

HOST = "0.0.0.0"
CTRL_PORT = 6001
WEB_PORT  = 6002

# ESP serial
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)

counter = 0

def control_receiver():
    global ser
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((HOST, CTRL_PORT))
    srv.listen(1)
    conn, _ = srv.accept()

    while True:
        data = conn.recv(1024).decode().strip()
        if data:
            print("Bridge got:", data)
            ser.write((data + "\n").encode())

def web_sender():
    global counter
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((HOST, WEB_PORT))
    srv.listen(1)
    conn, _ = srv.accept()

    while True:
        counter += 1
        conn.sendall(str(counter).encode())
        time.sleep(1)

print("Bridge started")

threading.Thread(target=control_receiver, daemon=True).start()
threading.Thread(target=web_sender, daemon=True).start()

while True:
    time.sleep(1)
# bridge_code.py
import socket
import threading
import time
import serial

HOST = "127.0.0.1"
CTRL_PORT = 6001
WEB_PORT = 6002

# change if needed
SERIAL_PORT = "/dev/ttyUSB0"
BAUD = 115200

esp = serial.Serial(SERIAL_PORT, BAUD, timeout=1)

counter = 0
current_cmd = "STOP"

def control_listener():
    global current_cmd
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((HOST, CTRL_PORT))
    srv.listen(1)

    conn, _ = srv.accept()
    while True:
        data = conn.recv(1024).decode()
        if data:
            current_cmd = data.strip()
            esp.write((current_cmd + "\n").encode())

def web_sender():
    global counter
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((HOST, WEB_PORT))
    srv.listen(1)

    conn, _ = srv.accept()
    while True:
        counter += 1
        conn.sendall(f"{counter}\n".encode())
        time.sleep(0.5)

print("Bridge started")

threading.Thread(target=control_listener, daemon=True).start()
threading.Thread(target=web_sender, daemon=True).start()

while True:
    time.sleep(1)

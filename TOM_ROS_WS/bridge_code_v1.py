import socket
import serial
import threading
import time

# -------- Serial --------
ESP_PORT = "/dev/ttyUSB0"
BAUD = 115200
ser = serial.Serial(ESP_PORT, BAUD, timeout=1)

# -------- Socket ports --------
WEB_PORT = 6000
CTRL_PORT = 6001
HOST = "127.0.0.1"

counter = 0
led_state = "OFF"

print("Bridge started")

# ---------- Web sender ----------
def web_sender():
    global counter
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((HOST, WEB_PORT))
    srv.listen(1)

    conn, _ = srv.accept()
    print("Web connected")

    while True:
        counter += 1
        conn.sendall(f"{counter}\n".encode())
        time.sleep(1)

# ---------- Control receiver ----------
def control_receiver():
    global led_state
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((HOST, CTRL_PORT))
    srv.listen(1)

    conn, _ = srv.accept()
    print("Control connected")

    while True:
        cmd = conn.recv(1024).decode().strip()
        if not cmd:
            continue

        print("CMD:", cmd)
        led_state = cmd
        ser.write((cmd + "\n").encode())

# ---------- Main ----------
threading.Thread(target=web_sender, daemon=True).start()
threading.Thread(target=control_receiver, daemon=True).start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    ser.close()
    print("Bridge stopped")

# control_code.py
import socket

HOST = "127.0.0.1"
CTRL_PORT = 6001
WEB_CMD_PORT = 6003

gear_map = {
    "N": 0,
    "1": 129,
    "2": 255,
    "R": 129
}

current_gear = "N"

bridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bridge.connect((HOST, CTRL_PORT))

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind((HOST, WEB_CMD_PORT))
srv.listen(1)

conn, _ = srv.accept()

print("Control code running")
while True:
    cmd = conn.recv(1024).decode().strip()

    if cmd == "UP":
        if current_gear == "N":
            current_gear = "1"
        elif current_gear == "1":
            current_gear = "2"

    elif cmd == "DOWN":
        if current_gear == "2":
            current_gear = "1"
        elif current_gear == "1":
            current_gear = "N"

    elif cmd in ["L", "R"]:
        bridge.sendall(f"TURN_{cmd}\n".encode())
        continue

    pwm = gear_map[current_gear]
    direction = "REV" if current_gear == "R" else "FWD"

    bridge.sendall(f"{direction}:{pwm}\n".encode())

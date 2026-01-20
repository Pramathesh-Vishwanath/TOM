# control_code.py
import socket
import time

HOST = "127.0.0.1"
BRIDGE_PORT = 6001      # bridge listens here
WEB_CMD_PORT = 6003     # web sends commands here

GEARS = ["R", "N", "1", "2"]
GEAR_PWM = {
    "R": 129,
    "N": 0,
    "1": 129,
    "2": 255
}

gear_index = GEARS.index("N")
current_gear = "N"

# ---- connect to bridge (retry) ----
bridge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        bridge.connect((HOST, BRIDGE_PORT))
        print("Control → connected to bridge")
        break
    except:
        print("Control → waiting for bridge...")
        time.sleep(1)

# ---- listen for web commands ----
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST, WEB_CMD_PORT))
srv.listen(1)

print("Control → waiting for web")
conn, _ = srv.accept()
print("Web connected to control")

while True:
    cmd = conn.recv(1024).decode().strip()
    if not cmd:
        continue

    if cmd == "UP":
        if gear_index < len(GEARS) - 1:
            gear_index += 1
        current_gear = GEARS[gear_index]
        conn.sendall(f"GEAR:{current_gear}\n".encode())
    elif cmd == "DOWN":
        if gear_index > 0:
            gear_index -= 1
        current_gear = GEARS[gear_index]
        conn.sendall(f"GEAR:{current_gear}\n".encode())
    elif cmd == "LEFT":
        gear_index = GEARS.index("N")
        current_gear = "N"
        bridge.sendall(b"LEFT\n")
        print("Turn LEFT → Gear N")
        conn.sendall(f"GEAR:{current_gear}\n".encode())
        continue

    elif cmd == "RIGHT":
        gear_index = GEARS.index("N")
        current_gear = "N"
        bridge.sendall(b"RIGHT\n")
        print("Turn RIGHT → Gear N")
        conn.sendall(f"GEAR:{current_gear}\n".encode())
        continue

    pwm = GEAR_PWM[current_gear]

    if current_gear == "R":
        bridge.sendall(f"REV:{pwm}\n".encode())
    elif current_gear == "N":
        bridge.sendall(b"STOP\n")
    else:
        bridge.sendall(f"FWD:{pwm}\n".encode())

    print("Current gear:", current_gear)


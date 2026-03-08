# web_code.py
import socket
import threading
import time
from flask import Flask, render_template_string

HOST = "127.0.0.1"
CTRL_PORT = 6003
BRIDGE_PORT = 6002
WEB_PORT = 8080

ctrl_sock = None
latest_num = "—"
current_gear = "N"

app = Flask(__name__)
HTML = """
<!DOCTYPE html>
<html>
<body>

<h1>TOM v1</h1>

<h2>Gear: <span id="gear">{{gear}}</span></h2>

<button onclick="sendCmd('UP')">Gear +</button>
<button onclick="sendCmd('DOWN')">Gear -</button>
<br><br>
<button onclick="sendCmd('LEFT')">Left</button>
<button onclick="sendCmd('RIGHT')">Right</button>

<h3 style="position:fixed; top:10px; right:20px;">
<span id="num">{{num}}</span>
</h3>

<script>
function sendCmd(cmd){
  fetch("/cmd/" + cmd);
}

setInterval(() => {
  fetch("/num")
    .then(r => r.text())
    .then(t => document.getElementById("num").innerText = t);

  fetch("/gear")
    .then(r => r.text())
    .then(g => document.getElementById("gear").innerText = g);
}, 300);
</script>

</body>
</html>
"""

# ---------- background threads ----------
def connect_control():
    global ctrl_sock
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, CTRL_PORT))
            ctrl_sock = s
            print("Web → connected to control")
            break
        except:
            time.sleep(1)

def recv_numbers():
    global latest_num
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, BRIDGE_PORT))
            print("Web → connected to bridge")
            while True:
                latest_num = s.recv(1024).decode().strip()
        except:
            time.sleep(1)

def recv_gear():
    global current_gear
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, CTRL_PORT))
            while True:
                msg = s.recv(1024).decode().strip()
                if msg.startswith("GEAR:"):
                    current_gear = msg.split(":")[1]
        except:
            time.sleep(1)

# ---------- routes ----------
@app.route("/")
def index():
    return render_template_string(HTML, num=latest_num, gear=current_gear)

@app.route("/cmd/<c>")
def cmd(c):
    if ctrl_sock:
        try:
            ctrl_sock.sendall(c.encode())
        except:
            pass
    return "OK"

@app.route("/num")
def num():
    return latest_num

@app.route("/gear")
def gear():
    return current_gear

# ---------- start ----------

threading.Thread(target=connect_control, daemon=True).start()
threading.Thread(target=recv_numbers, daemon=True).start()

app.run(host="0.0.0.0", port=WEB_PORT)

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket, threading

HOST = "0.0.0.0"
PORT = 8080

CTRL_PORT = 7001
BRIDGE_PORT = 6002

latest_number = "0"
led_state = "OFF"

# connect to control
ctrl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ctrl.connect(("127.0.0.1", CTRL_PORT))

def bridge_listener():
    global latest_number
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", BRIDGE_PORT))
    while True:
        latest_number = s.recv(1024).decode()

threading.Thread(target=bridge_listener, daemon=True).start()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/toggle":
            global led_state
            led_state = "OFF" if led_state == "ON" else "ON"
            ctrl.sendall(led_state.encode())
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"""
<html>
<body>
<button onclick="toggle()">LED</button>
<div style="position:fixed; top:10px; right:10px;">
{latest_number}
</div>

<script>
function toggle() {{
  fetch('/toggle');
}}
setInterval(() => location.reload(), 1000);
</script>
</body>
</html>
""".encode())

print("Web server running")
HTTPServer((HOST, PORT), Handler).serve_forever()

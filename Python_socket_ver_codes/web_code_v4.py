# web_code.py
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "0.0.0.0"
HTTP_PORT = 8080
WEB_DATA_PORT = 6002
CTRL_CMD_PORT = 6003

latest_value = "0"

def data_listener():
    global latest_value
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", WEB_DATA_PORT))

    while True:
        latest_value = sock.recv(1024).decode().strip()

def send_cmd(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", CTRL_CMD_PORT))
    s.sendall(cmd.encode())
    s.close()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/cmd/"):
            cmd = self.path.split("/")[-1]
            send_cmd(cmd)
            self.send_response(200)
            self.end_headers()
            return

        html = f"""
        <html>
        <body>
        <div style="position:fixed;top:10px;right:10px;font-size:24px;">
        {latest_value}
        </div>

        <h2>TOM v1</h2>
        <button onclick="location.href='/cmd/UP'">Gear +</button>
        <button onclick="location.href='/cmd/DOWN'">Gear -</button><br><br>
        <button onclick="location.href='/cmd/L'">Left</button>
        <button onclick="location.href='/cmd/R'">Right</button>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

threading.Thread(target=data_listener, daemon=True).start()
HTTPServer((HOST, HTTP_PORT), Handler).serve_forever()

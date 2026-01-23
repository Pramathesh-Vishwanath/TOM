import asyncio
import socket
from aiohttp import web
import websockets
from zeroconf import Zeroconf, ServiceInfo
import threading

BRIDGE_HOST = "127.0.0.1"
BRIDGE_PORT = 6000

latest_value = "—"

# ---------- TCP client to bridge ----------
def bridge_listener():
    global latest_value
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((BRIDGE_HOST, BRIDGE_PORT))
            print("Connected to bridge")

            while True:
                data = s.recv(1024).decode()
                if not data:
                    break
                latest_value = data.strip()
        except:
            print("Waiting for bridge...")
            import time
            time.sleep(1)

# ---------- WebSocket handler ----------
async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    while True:
        await ws.send_str(latest_value)
        await asyncio.sleep(0.5)

# ---------- HTTP handler ----------
async def index(request):
    return web.Response(
        text="""
<!DOCTYPE html>
<html>
<head>
  <title>TOM Dashboard</title>
  <style>
    body {
      background: #0f0f0f;
      color: #00ffcc;
      font-family: monospace;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      font-size: 80px;
    }
  </style>
</head>
<body>
  <div id="num">—</div>

  <script>
    const ws = new WebSocket("ws://" + location.host + "/ws");
    ws.onmessage = (e) => {
      document.getElementById("num").innerText = e.data;
    };
  </script>
</body>
</html>
""",
        content_type="text/html"
    )

# ---------- mDNS ----------
def advertise_mdns():
    zeroconf = Zeroconf()
    info = ServiceInfo(
        "_http._tcp.local.",
        "tomv1._http._tcp.local.",
        addresses=[socket.inet_aton("0.0.0.0")],
        port=8080,
    )
    zeroconf.register_service(info)

# ---------- Main ----------
def main():
    threading.Thread(target=bridge_listener, daemon=True).start()
    threading.Thread(target=advertise_mdns, daemon=True).start()

    app = web.Application()
    app.add_routes([
        web.get("/", index),
        web.get("/ws", ws_handler),
    ])

    web.run_app(app, port=8080)

if __name__ == "__main__":
    main()
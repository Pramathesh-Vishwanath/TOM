import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from flask import Flask
import threading

app = Flask(__name__)

ros_node = None


class WebNode(Node):

    def __init__(self):
        super().__init__('web_node')

        self.publisher = self.create_publisher(String, '/web_cmd', 10)

    def send_cmd(self, cmd):

        msg = String()
        msg.data = cmd

        self.publisher.publish(msg)

        self.get_logger().info(f"WEB → {cmd}")


@app.route('/')
def home():
    return """
    <h1>TOM Control</h1>

<button onclick="fetch('/cmd/UP')">Gear +</button>
<button onclick="fetch('/cmd/DOWN')">Gear -</button>

<br><br>

<button onclick="fetch('/cmd/LEFT')">LEFT</button>
<button onclick="fetch('/cmd/RIGHT')">RIGHT</button>

<br><br>

<button onclick="fetch('/cmd/STOP')">STOP</button>
    """


@app.route('/cmd/<c>')
def cmd(c):

    if ros_node:
        ros_node.send_cmd(c)

    return "OK"


def ros_thread():

    global ros_node

    rclpy.init()

    ros_node = WebNode()

    rclpy.spin(ros_node)


def main():

    t = threading.Thread(target=ros_thread)
    t.daemon = True
    t.start()

    app.run(host="0.0.0.0", port=8080)


if __name__ == '__main__':
    main()
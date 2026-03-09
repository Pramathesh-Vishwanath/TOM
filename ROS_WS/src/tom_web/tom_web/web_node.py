import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class WebNode(Node):

    def __init__(self):
        super().__init__('web_node')

        self.publisher = self.create_publisher(String, '/web_cmd', 10)

        self.timer = self.create_timer(2.0, self.send_cmd)

        self.commands = ["UP", "UP", "LEFT", "UP", "RIGHT", "DOWN"]
        self.index = 0

    def send_cmd(self):

        cmd = self.commands[self.index]

        msg = String()
        msg.data = cmd

        self.publisher.publish(msg)

        self.get_logger().info(f"WEB → {cmd}")

        self.index = (self.index + 1) % len(self.commands)


def main(args=None):
    rclpy.init(args=args)
    node = WebNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
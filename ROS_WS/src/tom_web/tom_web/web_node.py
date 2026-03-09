import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class WebNode(Node):

    def __init__(self):
        super().__init__('web_node')

        self.publisher = self.create_publisher(String, 'web_cmd', 10)

        self.timer = self.create_timer(2.0, self.publish_cmd)

        self.commands = ["UP", "LEFT", "RIGHT", "DOWN"]
        self.index = 0

    def publish_cmd(self):

        msg = String()
        msg.data = self.commands[self.index]

        self.publisher.publish(msg)

        self.get_logger().info(f"WEB → {msg.data}")

        self.index = (self.index + 1) % len(self.commands)


def main(args=None):
    rclpy.init(args=args)
    node = WebNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
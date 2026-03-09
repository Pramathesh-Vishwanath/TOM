import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class WebNode(Node):

    def __init__(self):
        super().__init__('web_node')

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        self.timer = self.create_timer(2.0, self.send_command)

        self.commands = [
            ("FORWARD", 0.5, 0.0),
            ("LEFT", 0.0, 1.0),
            ("RIGHT", 0.0, -1.0),
            ("STOP", 0.0, 0.0)
        ]

        self.index = 0

    def send_command(self):

        name, lin, ang = self.commands[self.index]

        msg = Twist()
        msg.linear.x = lin
        msg.angular.z = ang

        self.publisher.publish(msg)

        self.get_logger().info(
            f"WEB → {name} | linear={lin} angular={ang}"
        )

        self.index = (self.index + 1) % len(self.commands)


def main(args=None):
    rclpy.init(args=args)
    node = WebNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class ControlNode(Node):

    def __init__(self):
        super().__init__('control_node')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10)

        self.publisher = self.create_publisher(
            String,
            '/motor_cmd',
            10)

        self.wheel_base = 0.2

    def cmd_callback(self, msg):

        v = msg.linear.x
        w = msg.angular.z

        left = v - (w * self.wheel_base / 2)
        right = v + (w * self.wheel_base / 2)

        motor_msg = String()
        motor_msg.data = f"L:{left:.2f},R:{right:.2f}"

        self.publisher.publish(motor_msg)

        self.get_logger().info(
            f"CONTROL → left={left:.2f} right={right:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
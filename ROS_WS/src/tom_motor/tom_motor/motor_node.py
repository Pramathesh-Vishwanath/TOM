import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MotorNode(Node):

    def __init__(self):
        super().__init__('motor_node')

        self.subscription = self.create_subscription(
            String,
            'motor_cmd',
            self.motor_callback,
            10)

    def motor_callback(self, msg):

        cmd = msg.data

        self.get_logger().info(f"MOTOR executing: {cmd}")


def main(args=None):
    rclpy.init(args=args)
    node = MotorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
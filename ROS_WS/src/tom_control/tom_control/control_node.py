import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ControlNode(Node):

    def __init__(self):
        super().__init__('control_node')

        self.subscription = self.create_subscription(
            String,
            'web_cmd',
            self.cmd_callback,
            10)

        self.publisher = self.create_publisher(
            String,
            'motor_cmd',
            10)

    def cmd_callback(self, msg):

        cmd = msg.data
        self.get_logger().info(f"CONTROL received: {cmd}")

        motor_msg = String()

        if cmd == "UP":
            motor_msg.data = "FWD"
        elif cmd == "DOWN":
            motor_msg.data = "REV"
        elif cmd == "LEFT":
            motor_msg.data = "TURN_LEFT"
        elif cmd == "RIGHT":
            motor_msg.data = "TURN_RIGHT"
        else:
            motor_msg.data = "STOP"

        self.publisher.publish(motor_msg)

        self.get_logger().info(f"CONTROL → motor: {motor_msg.data}")


def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
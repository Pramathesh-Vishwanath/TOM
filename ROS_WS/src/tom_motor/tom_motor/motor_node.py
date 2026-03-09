import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial


SERIAL_PORT = "/dev/ttyUSB0"
BAUD = 115200


class BridgeNode(Node):

    def __init__(self):
        super().__init__('bridge_node')

        try:
            self.serial = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
            self.get_logger().info("ESP32 connected")

        except:
            self.serial = None
            self.get_logger().warn("ESP32 not connected")

        self.subscription = self.create_subscription(
            String,
            '/motor_cmd',
            self.motor_callback,
            10)

    def motor_callback(self, msg):

        cmd = msg.data

        self.get_logger().info(f"BRIDGE → {cmd}")

        if self.serial:
            self.serial.write((cmd + "\n").encode())


def main(args=None):
    rclpy.init(args=args)
    node = BridgeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
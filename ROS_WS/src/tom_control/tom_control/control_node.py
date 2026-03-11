import rclpy
from rclpy.node import Node
from std_msgs.msg import String


GEARS = ["R", "N", "1", "2", "3"]

GEAR_PWM = {
    "R": 64,
    "N": 0,
    "1": 64,
    "2": 128,
    "3": 255
}


class ControlNode(Node):

    def __init__(self):
        super().__init__('control_node')

        self.subscription = self.create_subscription(
            String,
            '/web_cmd',
            self.cmd_callback,
            10)

        self.publisher = self.create_publisher(
            String,
            '/motor_cmd',
            10)

        self.gear_index = GEARS.index("N")
        self.current_gear = "N"

    def cmd_callback(self, msg):

        cmd = msg.data

        if cmd == "UP":
            if self.gear_index < len(GEARS) - 1:
                self.gear_index += 1

        elif cmd == "DOWN":
            if self.gear_index > 0:
                self.gear_index -= 1

        elif cmd == "LEFT":
            self.gear_index = GEARS.index("N")
            self.current_gear = "N"

            motor_msg = String()
            motor_msg.data = "LEFT"
            self.publisher.publish(motor_msg)

            self.get_logger().info("CONTROL → LEFT")
            return

        elif cmd == "RIGHT":
            self.gear_index = GEARS.index("N")
            self.current_gear = "N"

            motor_msg = String()
            motor_msg.data = "RIGHT"
            self.publisher.publish(motor_msg)

            self.get_logger().info("CONTROL → RIGHT")
            return
        
        elif cmd == "STOP":
            motor_msg = String()
            self.current_gear = "N"
            self.gear_index = 1
            motor_msg.data = "STOP"
            self.publisher.publish(motor_msg)
            self.get_logger().info("CONTROL → STOP")
            return
        
        self.current_gear = GEARS[self.gear_index]

        pwm = GEAR_PWM[self.current_gear]

        motor_msg = String()

        if self.current_gear == "R":
            motor_msg.data = f"REV:{pwm}"

        elif self.current_gear == "N":
            motor_msg.data = "STOP"

        else:
            motor_msg.data = f"FWD:{pwm}"

        self.publisher.publish(motor_msg)

        self.get_logger().info(
            f"CONTROL → Gear {self.current_gear} | {motor_msg.data}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
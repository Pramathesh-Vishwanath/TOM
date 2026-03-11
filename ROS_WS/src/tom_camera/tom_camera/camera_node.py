import rclpy
from rclpy.node import Node
import cv2
from flask import Flask, Response
import threading

app = Flask(__name__)

cap = cv2.VideoCapture(0)


class CameraNode(Node):

    def __init__(self):
        super().__init__('camera_node')
        self.get_logger().info("Camera node started")


def generate():

    while True:

        success, frame = cap.read()

        if not success:
            continue

        ret, buffer = cv2.imencode('.jpg', frame)

        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def video():

    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def ros_thread():

    rclpy.init()

    node = CameraNode()

    rclpy.spin(node)


def main():

    t = threading.Thread(target=ros_thread)
    t.daemon = True
    t.start()

    app.run(host='0.0.0.0', port=8081)


if __name__ == '__main__':
    main()
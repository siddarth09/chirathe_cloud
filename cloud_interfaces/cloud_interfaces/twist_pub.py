import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import json
import websockets


class TwistPublisher(Node):
    def __init__(self):
        super().__init__("twist_pub")
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.json_data={}

    async def get_data(self):
        uri = "ws://172.25.60.254:8000"
        self.get_logger().info(f"Connecting to {uri}")
        try:
            async with websockets.connect(uri) as websocket:
                self.get_logger().info("Connected to WebSocket")
                json_data = await websocket.recv()
            
        except websockets.exceptions.WebSocketException as e:
            self.get_logger().error(f"WebSocket connection error: {str(e)}")
            
           

    def twist_pub(self):
        while rclpy.ok():
            data = self.json_data
            msg = Twist()
            msg.linear.x = data['linear']['x']
            msg.angular.z = data['angular']['z']
            self.pub.publish(msg)
            self.get_logger().info("Publishing velocity")


def main():
    rclpy.init(args=None)
    robot_vel = TwistPublisher()
    try:
        rclpy.spin(robot_vel)
    except KeyboardInterrupt:
        pass
    finally:
        robot_vel.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

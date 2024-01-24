import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import json
import websockets
import asyncio

class TwistPublisher(Node):
    def _init_(self):
        super()._init_("twist_pub")
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.json_data={}
        self.timer=self.create_timer(10.0,self.twist_pub)

    # async def get_data(self):
    #     uri = "ws://172.25.60.254:8000"
    #     self.get_logger().info(f"Connecting to {uri}")
    #     try:
    #         async with websockets.connect(uri) as websocket:
    #             self.get_logger().info("Connected to WebSocket")
    #             json_data = await websocket.recv()
            
    #     except websockets.exceptions.WebSocketException as e:
    #         self.get_logger().error(f"WebSocket connection error: {str(e)}")

    async def websocket_client(self,uri):
        async with websockets.connect(uri) as websocket:
            while True:
                # Receive data from the WebSocket
                    print("CONNECTED")
                    data = await websocket.recv()
                    self.json_data=data
                    print(f"Received data from WebSocket: {data}")
                    
            
           

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
    websocket_uri = 'ws://172.25.60.254:8000'
    asyncio.get_event_loop().run_until_complete(robot_vel.websocket_client(websocket_uri))
    try:
        rclpy.spin(robot_vel)
    except KeyboardInterrupt:
        pass
    finally:
        robot_vel.destroy_node()
        rclpy.shutdown()


if __name__ == "_main_":
    main()
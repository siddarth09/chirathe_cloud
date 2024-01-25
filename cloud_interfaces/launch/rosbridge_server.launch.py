from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_rosbridge_server = "rosbridge_server"
    pkg_launch = "cloud_interfaces"  # Replace with the name of your ROS 2 package

    # Arguments
    rosbridge_address_arg = DeclareLaunchArgument(
        "address",
        default_value="ws://127.0.0.1",
        description="ROSbridge server IP address"
    )

    rosbridge_port_arg = DeclareLaunchArgument(
        "port",
        default_value="9090",
        description="ROSbridge server port"
    )

    # Launch the ROSbridge server
    rosbridge_server_node = Node(
        package=pkg_rosbridge_server,
        executable="rosbridge_websocket",
        name="rosbridge_websocket",
        output="screen",
        parameters=[{"param_name": "param_value"}],  # Add parameters if needed
        arguments=[
            LaunchConfiguration("address"),
            LaunchConfiguration("port"),
        ],
    )

    return LaunchDescription([
        rosbridge_address_arg,
        rosbridge_port_arg,
        rosbridge_server_node,
    ])

import rclpy

from navigator import Navigator

rclpy.init()

nav = Navigator()

nav.navigate_to("kitchen")

nav.destroy_node()

rclpy.shutdown()

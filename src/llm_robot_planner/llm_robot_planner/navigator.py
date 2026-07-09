import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from world_map import ROOMS


class Navigator(Node):

    def __init__(self):

        super().__init__("navigator")

        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0

        self.odom_received = False

        self.cmd_pub = self.create_publisher(
            Twist,
            "/cmd_vel",
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            "/model/mobile_robot/odometry",
            self.odom_callback,
            10
        )

        self.get_logger().info(
            "Navigator Started"
        )

    def odom_callback(self, msg):

        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation

        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)

        self.current_yaw = math.atan2(
            siny,
            cosy
        )

        self.odom_received = True

    def stop(self):

        msg = Twist()

        self.cmd_pub.publish(msg)

    def navigate_to(self, room):

        if room not in ROOMS:

            self.get_logger().error(
                f"Unknown room: {room}"
            )

            return

        self.get_logger().info(
            "Waiting for odometry..."
        )

        while rclpy.ok() and not self.odom_received:

            rclpy.spin_once(
                self,
                timeout_sec=0.1
            )

        goal_x, goal_y = ROOMS[room]

        self.get_logger().info(
            f"Navigating to {room}"
        )

        while rclpy.ok():

            rclpy.spin_once(
                self,
                timeout_sec=0.05
            )

            dx = goal_x - self.current_x
            dy = goal_y - self.current_y

            distance = math.sqrt(
                dx * dx + dy * dy
            )

            target_angle = math.atan2(
                dy,
                dx
            )

            angle_error = (
                target_angle -
                self.current_yaw
            )

            while angle_error > math.pi:

                angle_error -= 2 * math.pi

            while angle_error < -math.pi:

                angle_error += 2 * math.pi

            self.get_logger().info(
                f"X={self.current_x:.2f} "
                f"Y={self.current_y:.2f} "
                f"Distance={distance:.2f} "
                f"Angle={angle_error:.2f}"
            )

            if distance < 0.20:

                self.stop()

                self.get_logger().info(
                    f"Reached {room}"
                )

                return

            msg = Twist()

            # Rotate first
            if abs(angle_error) > 0.15:

                msg.linear.x = 0.0

                if angle_error > 0:

                    msg.angular.z = 1.0

                else:

                    msg.angular.z = -1.0

            # Then move forward
            else:

                msg.linear.x = min(
                    0.5,
                    distance
                )

                msg.angular.z = (
                    0.5 * angle_error
                )

            self.cmd_pub.publish(msg)

        self.stop()


def main():

    rclpy.init()

    navigator = Navigator()

    navigator.navigate_to(
        "bedroom"
    )

    navigator.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":

    main()
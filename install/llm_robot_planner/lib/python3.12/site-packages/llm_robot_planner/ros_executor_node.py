import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

import json

from world_map import ROOMS


class ExecutorNode(Node):

    def __init__(self):

        super().__init__("executor_node")

        self.subscription = self.create_subscription(
            String,
            "task_plan",
            self.plan_callback,
            10
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            "/cmd_vel",
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            "/model/simple_robot/odometry",
            self.odom_callback,
            10
        )

        self.current_x = None
        self.current_y = None

        self.get_logger().info(
            "Executor Node Started"
        )

    def odom_callback(self, msg):

        self.current_x = (
            msg.pose.pose.position.x
        )

        self.current_y = (
            msg.pose.pose.position.y
        )

    def stop_robot(self):

        msg = Twist()

        self.cmd_pub.publish(msg)

    def wait_for_odom(self):

        self.get_logger().info(
            "Waiting for odometry..."
        )

        while rclpy.ok() and self.current_x is None:

            rclpy.spin_once(
                self,
                timeout_sec=0.1
            )

        self.get_logger().info(
            f"Odometry Ready X={self.current_x:.2f}"
        )

    def navigate_to(self, room):

        if room not in ROOMS:

            self.get_logger().error(
                f"Unknown room: {room}"
            )

            return False

        self.wait_for_odom()

        target_x, target_y = ROOMS[room]

        self.get_logger().info(
            f"Navigating to {room} "
            f"(target x={target_x})"
        )

        velocity = Twist()

        while rclpy.ok():

            rclpy.spin_once(
                self,
                timeout_sec=0.05
            )

            error = target_x - self.current_x

            if abs(error) < 0.20:

                self.stop_robot()

                self.get_logger().info(
                    f"Reached {room}"
                )

                return True

            if error > 0:

                velocity.linear.x = 0.5

            else:

                velocity.linear.x = -0.5

            self.cmd_pub.publish(
                velocity
            )

        self.stop_robot()

        return False

    def plan_callback(self, msg):

        plan = json.loads(msg.data)

        actions = plan.get("actions", [])

        self.get_logger().info(
            f"Executing {len(actions)} actions"
        )

        for step in actions:

            action = step.get("action")
            target = step.get("target")

            if action == "navigate_to":

                self.navigate_to(target)

            elif action == "detect_object":

                self.get_logger().info(
                    f"Detecting {target}"
                )

            elif action == "pick_up":

                self.get_logger().info(
                    f"Picking up {target}"
                )

            elif action == "place_object":

                self.get_logger().info(
                    f"Placing object at {target}"
                )

            elif action == "wait":

                self.get_logger().info(
                    "Waiting..."
                )

        self.get_logger().info(
            "Mission Complete"
        )


def main():

    rclpy.init()

    node = ExecutorNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
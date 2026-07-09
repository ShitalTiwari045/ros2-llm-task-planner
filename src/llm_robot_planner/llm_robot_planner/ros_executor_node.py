import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

import time


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

        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

    def plan_callback(self, msg):

        self.get_logger().info(
            "========== TEST MODE =========="
        )

        self.get_logger().info(
            "Received task plan"
        )

        self.get_logger().info(
            "Driving robot forward for 5 seconds..."
        )

        velocity = Twist()
        velocity.linear.x = 1.0
        velocity.angular.z = 0.0

        end_time = time.time() + 5.0

        while time.time() < end_time:

            self.cmd_pub.publish(velocity)

            self.get_logger().info(
                "Publishing cmd_vel..."
            )

            rclpy.spin_once(
                self,
                timeout_sec=0.0
            )

            time.sleep(0.1)

        stop = Twist()

        self.cmd_pub.publish(stop)

        self.get_logger().info(
            "Robot Stopped"
        )


def main():

    rclpy.init()

    node = ExecutorNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
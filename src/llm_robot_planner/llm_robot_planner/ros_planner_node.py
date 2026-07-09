import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import requests
import json

from normalizer import normalize_plan
from validator import validate_plan

PROMPT = """
You are a robot task planner.

Available actions:

- navigate_to(location)
- detect_object(object)
- pick_up(object)
- place_object(location)
- wait()

Rules:
1. Return ONLY valid JSON.
2. Use only available actions.
"""


class PlannerNode(Node):

    def __init__(self):

        super().__init__("planner_node")

        self.subscription = self.create_subscription(
            String,
            "task_input",
            self.task_callback,
            10
        )

        self.publisher = self.create_publisher(
            String,
            "task_plan",
            10
        )

        self.get_logger().info("Planner Node Started")

    def task_callback(self, msg):

        task = msg.data

        self.get_logger().info(
            f"Received Task: {task}"
        )

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": PROMPT + "\nTask: " + task,
                "stream": False
            }
        )

        plan_text = response.json()["response"]

        self.get_logger().info(
            f"Raw Plan: {plan_text}"
        )

        valid, message = validate_plan(plan_text)

        if not valid:

            self.get_logger().error(
                f"Validation Failed: {message}"
            )

            return

        normalized_plan = normalize_plan(plan_text)

        output = String()

        output.data = json.dumps(normalized_plan)

        self.publisher.publish(output)

        self.get_logger().info(
            "Published Valid Plan"
        )


def main():

    rclpy.init()

    node = PlannerNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
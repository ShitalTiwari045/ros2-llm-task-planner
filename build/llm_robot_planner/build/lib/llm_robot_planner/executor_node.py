import time
from navigator import navigate_to

def execute_plan(normalized_plan):

    actions = normalized_plan["actions"]

    for step in actions:

        action = step["action"]
        target = step["target"]

        print(f"\nExecuting: {action} -> {target}")

        if action == "navigate_to":

            navigate_to(target)

        elif action == "detect_object":

            print(f"Detected {target}")

        elif action == "pick_up":

            print(f"Picked up {target}")

        elif action == "place_object":

            print(f"Placed object at {target}")

        elif action == "wait":

            time.sleep(2)

        else:

            print(f"Unknown action: {action}")

        print("SUCCESS")

    print("\nMission Complete")
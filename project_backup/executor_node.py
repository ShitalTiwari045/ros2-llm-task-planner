import time

def execute_plan(normalized_plan):

    actions = normalized_plan["actions"]

    for step in actions:

        action = step["action"]
        target = step["target"]

        print(f"\nExecuting: {action} -> {target}")

        time.sleep(2)

        print("SUCCESS")

    print("\nMission Complete")
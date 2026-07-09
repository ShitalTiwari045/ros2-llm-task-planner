import requests
from validator import validate_plan
from normalizer import normalize_plan

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

user_task = input("Enter task: ")

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3:8b",
        "prompt": PROMPT + "\nTask: " + user_task,
        "stream": False
    }
)

plan_text = response.json()["response"]

print("\nGenerated Plan:\n")
print(plan_text)

valid, message = validate_plan(plan_text)

from executor_node import execute_plan

print("\nValidation Result:")
print(message)

if valid:

    normalized_plan = normalize_plan(plan_text)

    print("✅ Plan Accepted")

    execute_plan(normalized_plan)

else:

    print("❌ Plan Rejected")
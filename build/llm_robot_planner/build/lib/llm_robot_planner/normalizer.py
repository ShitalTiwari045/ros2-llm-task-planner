import json
import re

def normalize_plan(plan_text):

    # Extract JSON from LLM response
    match = re.search(r'(\{.*\}|\[.*\])', plan_text, re.DOTALL)

    if not match:
        raise ValueError("No JSON found in response")

    json_text = match.group(0)

    plan = json.loads(json_text)

    normalized = {
        "actions": []
    }

    # Handle single-action JSON
    if "action" in plan or "type" in plan:

        actions = [plan]

    else:

        actions = (
            plan.get("actions")
            or plan.get("task")
            or plan.get("steps")
            or []
        )

    for step in actions:

        action = (
            step.get("action")
            or step.get("type")
        )

        target = (
            step.get("target")
            or step.get("location")
            or step.get("object")
            or step.get("argument")
        )

        # Handle args / params / parameters
        for key in ["args", "params", "parameters", "parameter"]:

            if key in step and step[key]:

                value = step[key]

                if isinstance(value, str):

                    target = value

                if isinstance(value, list):

                    target = value[0]

                elif isinstance(value, dict):

                    target = (
                        value.get("location")
                        or value.get("object")
                        or value.get("target")
                    )

                else:

                    target = value

        normalized["actions"].append({
            "action": action,
            "target": target
        })

    print("\nNORMALIZED PLAN:")
    print(normalized)

    return normalized
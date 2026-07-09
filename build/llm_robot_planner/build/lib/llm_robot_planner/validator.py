from environment import ROOMS, OBJECTS
from normalizer import normalize_plan

VALID_ACTIONS = {
    "navigate_to",
    "detect_object",
    "pick_up",
    "place_object",
    "wait"
}

def validate_plan(plan_text):

    try:

        plan = normalize_plan(plan_text)

        actions = plan["actions"]

        for step in actions:

            action = step["action"]
            target = step["target"]

            if action not in VALID_ACTIONS:
                return False, f"Invalid action: {action}"

            if action == "navigate_to":

                if target not in ROOMS:
                    return False, f"Unknown room: {target}"

            if action in ["detect_object", "pick_up"]:

                if target not in OBJECTS:
                    return False, f"Unknown object: {target}"

        return True, "Plan valid"

    except Exception as e:
        return False, str(e)
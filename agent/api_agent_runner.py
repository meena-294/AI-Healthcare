import requests

BASE_URL = "http://127.0.0.1:8000"

def run():
    # 🔁 RESET
    res = requests.post(f"{BASE_URL}/reset?task_level=hard")
    obs = res.json()

    done = False
    step = 0

    while not done:
        print(f"\nStep {step}")
        print("Observation:", obs)

        # 🤖 DECIDE ACTION
        action = decide_action(obs)

        print("Action:", action)

        # 🔁 CALL STEP API
        res = requests.post(f"{BASE_URL}/step", json=action)
        data = res.json()

        obs = data["observation"]
        done = data["done"]

        print("Reward:", data["reward"])
        print("Done:", done)

        step += 1

    print("\n✅ TASK COMPLETED")

# 🧠 AGENT LOGIC
def decide_action(obs):
    # If incorrect code → fix it
    if obs.get("denial_reason") == "Incorrect procedure code":
        procedure = obs.get("procedure")

        # simple mapping logic
        if procedure == "X-Ray":
            return {"action_type": "correct_code", "new_code": "XRAY123"}
        elif procedure == "MRI Scan":
            return {"action_type": "correct_code", "new_code": "MRI001"}
        else:
            return {"action_type": "noop"}

    return {"action_type": "noop"}


if __name__ == "__main__":
    run()
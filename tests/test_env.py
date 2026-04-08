from env.environment import HealthcareEnv
from models.action import ClaimAction


def extract_correct_code(policy_text):
    if not policy_text:
        return None

    words = policy_text.split()
    for word in words:
        if any(char.isdigit() for char in word):
            return word
    return None


# 🔹 Single-step test (basic check)
def run_test(task_level):
    print(f"\n===== TESTING TASK LEVEL: {task_level.upper()} =====")

    env = HealthcareEnv()

    obs = env.reset(task_level=task_level)
    print("\nInitial Observation:", obs)

    correct_code = env.state_manager.get_state()["correct_code"]
    action = ClaimAction(
        action_type="correct_code",
        new_code=correct_code,
        justification="Correcting procedure code as per policy"
    )

    obs, reward, done, info = env.step(action)

    print("\nAfter Step:")
    print("Observation:", obs)
    print("Reward:", reward)
    print("Done:", done)
    print("Info:", info)


# 🔹 Negative test (wrong action)
def run_negative_test():
    print("\n===== NEGATIVE TEST =====")

    env = HealthcareEnv()
    obs = env.reset(task_level="hard")

    print("\nInitial Observation:", obs)

    bad_action = ClaimAction(
        action_type="correct_code",
        new_code="WRONG999",
        justification="random guess"
    )

    obs, reward, done, info = env.step(bad_action)

    print("\nAfter Wrong Action:")
    print("Reward:", reward)
    print("Info:", info)


# 🔥 Multi-step test (NEW - Module 4)
def run_multistep_test():
    print("\n===== MULTI-STEP TEST =====")


    env = HealthcareEnv()
    obs = env.reset(task_level="hard")

    print("\nInitial Observation:", obs)

    # Step 1: wrong action
    action1 = ClaimAction(action_type="noop")
    obs, reward, done, info = env.step(action1)
    print("\nStep 1:", reward, info)

    # Step 2: add document
    action2 = ClaimAction(action_type="add_document")
    obs, reward, done, info = env.step(action2)
    print("\nStep 2:", reward, info)

    # Step 3: correct code
    correct_code = env.state_manager.get_state()["correct_code"]

    action3 = ClaimAction(
        action_type="correct_code",
        new_code=correct_code,
        justification="Correcting code as per policy"
    )
    obs, reward, done, info = env.step(action3)
    print("\nStep 3:", reward, info)


# 🚀 MAIN ENTRY
if __name__ == "__main__":
    run_test("easy")
    run_test("medium")
    run_test("hard")

    run_negative_test()

    run_multistep_test()
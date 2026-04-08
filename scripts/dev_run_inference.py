from env.environment import HealthcareEnv
from models.action import ClaimAction
from agent.rule_based_agent import RuleBasedAgent


def run_task(task_level):
    print("\n" + "="*50)
    print(f"🚀 Running task: {task_level.upper()}")
    print("="*50)

    env = HealthcareEnv()
    agent = RuleBasedAgent()

    obs = env.reset(task_level)
    done = False
    total_reward = 0

    max_steps = 20
    step = 1

    while not done and step <= max_steps:
        print(f"\nStep {step}")
        print("Observation:", obs)

        # 🔥 Agent returns dict
        action_dict = agent.act(obs)

        # 🔥 Convert to ClaimAction (FIX)
        action = ClaimAction(**action_dict)

        print("Action:", action_dict)

        obs, reward, done, info = env.step(action)

        print("Reward:", reward)
        print("Done:", done)
        print("Info:", info)

        total_reward += reward
        step += 1

    if step > max_steps:
        print("\n⚠️ Stopped due to max step limit (possible agent issue)")

    print("\n" + "-"*50)
    print(f"✅ Final Reward: {total_reward}")
    print("-"*50)


if __name__ == "__main__":
    for level in ["easy", "medium", "hard"]:
        run_task(level)
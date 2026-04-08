from env.environment import HealthcareEnv
from agent.rule_based_agent import RuleBasedAgent
from models.action import ClaimAction


def run_episode(task_level="medium"):
    # Initialize
    env = HealthcareEnv()
    agent = RuleBasedAgent()

    obs = env.reset(task_level)
    done = False

    print("\n🚀 Starting Episode\n")

    step = 0

    while not done:
        step += 1
        print(f"\n--- Step {step} ---")

        print("Observation:", obs)

        # Agent decides
        action_dict = agent.act(obs)
        print("Action (dict):", action_dict)

        # Convert dict → ClaimAction (IMPORTANT)
        action = ClaimAction(**action_dict)

        # Step in environment
        obs, reward, done, info = env.step(action)

        print("Reward:", reward)
        print("Done:", done)
        print("Info:", info)

    print("\n✅ Episode Finished")


if __name__ == "__main__":
    run_episode("medium")
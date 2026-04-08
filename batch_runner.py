from env.environment import HealthcareEnv
from agent.rule_based_agent import RuleBasedAgent

def batch_test(n=5):
    env = HealthcareEnv()
    agent = RuleBasedAgent()

    scores = []

    for i in range(n):
        obs = env.reset("medium")
        done = False
        total_reward = 0

        while not done:
            action = agent.act(obs)
            obs, reward, done, _ = env.step(action)
            total_reward += reward

        scores.append(total_reward)

    print("\n📊 Batch Results:")
    print("Scores:", scores)
    print("Average:", sum(scores) / len(scores))


if __name__ == "__main__":
    batch_test(10)
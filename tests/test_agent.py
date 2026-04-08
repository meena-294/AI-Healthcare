from env.environment import HealthcareEnv
from agent.rule_based_agent import RuleBasedAgent

env = HealthcareEnv()
agent = RuleBasedAgent()

# Reset environment
obs = env.reset("medium")

done = False

while not done:
    print("\nObservation:", obs)

    action = agent.act(obs)
    print("Action:", action)

    obs, reward, done, info = env.step(type("Action", (), action))

    print("Reward:", reward)
    print("Done:", done)
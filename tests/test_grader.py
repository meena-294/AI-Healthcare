from env.environment import HealthcareEnv
from models.action import ClaimAction

env = HealthcareEnv()

obs = env.reset(task_level="hard")

action = ClaimAction(
    action_type="correct_code",
    new_code="MRI456",
    justification="Correcting code as per policy coverage"
)

obs, score, done, info = env.step(action)

print("Score:", score)
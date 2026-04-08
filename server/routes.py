from fastapi import APIRouter
from env.environment import HealthcareEnv
from models.action import ClaimAction

# Create router instance
router = APIRouter()

# Initialize environment
env = HealthcareEnv()

# 🔄 RESET endpoint
@router.post("/reset")
def reset(task_level: str = "easy"):
    """
    Resets the environment with a new claim
    """
    return env.reset(task_level)


# 🎮 STEP endpoint
@router.post("/step")
def step(action: dict):
    """
    Takes an action and returns next state
    """
    action_obj = ClaimAction(**action)

    obs, reward, done, info = env.step(action_obj)

    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }


# 🧠 STATE endpoint
@router.get("/state")
def state():
    """
    Returns current environment state
    """
    return env.state()
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from env.environment import HealthcareEnv
from models.action import ClaimAction

app = FastAPI()

env = HealthcareEnv()

# ✅ ROOT
@app.get("/")
def home():
    return {"message": "API running"}

# ✅ RESET (VERY IMPORTANT FIX)
@app.post("/reset")
def reset(task_level: str = "easy"):
    return env.reset(task_level)

# ✅ ALSO SUPPORT GET (checker safety)
@app.get("/reset")
def reset_get(task_level: str = "easy"):
    return env.reset(task_level)

# ✅ STATE
@app.get("/state")
def state():
    return env.state_manager.get_state()

# ✅ STEP
class StepRequest(BaseModel):
    action_type: str
    new_code: Optional[str] = None
    justification: Optional[str] = None

@app.post("/step")
def step(req: StepRequest):
    action = ClaimAction(**req.dict())
    s, r, d, i = env.step(action)

    return {
        "state": s,
        "reward": r,
        "done": d,
        "info": i
    }

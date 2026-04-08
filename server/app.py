from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn
 
from env.environment import HealthcareEnv
from models.action import ClaimAction
from agent.rule_based_agent import RuleBasedAgent
 
# ✅ GLOBAL INSTANCES
env = HealthcareEnv()
agent = RuleBasedAgent()
 
app = FastAPI()
 
 
# ROOT
@app.get("/")
def home():
    return {"message": "Healthcare Claim API is running"}
 
 
# ✅ RESET — task_level as query param: POST /reset?task_level=easy
# Also accepts POST /reset with JSON body {"task_level": "easy"}
@app.post("/reset")
def reset(task_level: str = "easy"):
    state = env.reset(task_level)
    return state
 
 
# STATE
@app.get("/state")
def get_state():
    return env.state_manager.get_state()
 
 
# STEP
class StepRequest(BaseModel):
    action_type: str
    new_code: Optional[str] = None
    justification: Optional[str] = None
 
 
@app.post("/step")
def step(request: StepRequest):
    action = ClaimAction(
        action_type=request.action_type,
        new_code=request.new_code,
        justification=request.justification
    )
    state, reward, done, info = env.step(action)
    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }
 
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
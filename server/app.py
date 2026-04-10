from fastapi import FastAPI
from pydantic import BaseModel
from env.environment import HealthcareEnv
from models.action import ClaimAction
from agent.rule_based_agent import RuleBasedAgent

app = FastAPI()

env = HealthcareEnv()
agent = RuleBasedAgent()

class StepRequest(BaseModel):
    action: dict

@app.post("/reset")
def reset(payload: dict = {}):
    difficulty = payload.get("difficulty", "easy") if payload else "easy"
    obs = env.reset(difficulty)
    return obs

@app.post("/step")
def step(request: StepRequest):
    action = ClaimAction(**request.action)
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/health")
def health():
    return {"status": "ok"}


from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from env.environment import HealthcareEnv
from models.action import ClaimAction
from agent.rule_based_agent import RuleBasedAgent

app = FastAPI()

env = HealthcareEnv()
agent = RuleBasedAgent()


# ── Request models ──────────────────────────────────────────────────────────

class ResetRequest(BaseModel):
    difficulty: Optional[str] = "easy"
    task_level: Optional[str] = None   # accept both field names just in case


class StepRequest(BaseModel):
    action: dict


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.post("/reset")
async def reset(request: Request):
    """
    OpenEnv calls POST /reset with a JSON body.
    We read it safely with request.json() so it never raises
    'Method Not Allowed' or 422 on an empty / missing body.
    """
    try:
        body = await request.json()
    except Exception:
        body = {}

    # support both 'difficulty' and 'task_level' keys
    difficulty = body.get("difficulty") or body.get("task_level") or "easy"
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
        "info": info,
    }


@app.post("/state")
def state():
    """OpenEnv also checks for a /state endpoint."""
    return env.state() if hasattr(env, "state") else {"status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}

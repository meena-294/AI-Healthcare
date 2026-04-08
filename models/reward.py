from pydantic import BaseModel

class ClaimReward(BaseModel):
    score: float
    feedback: str
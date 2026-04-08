from pydantic import BaseModel
from typing import Optional

class ClaimObservation(BaseModel):
    claim_id: str
    patient_age: int
    procedure: str
    submitted_code: str
    denial_reason: str
    policy: str
    notes: Optional[str] = None
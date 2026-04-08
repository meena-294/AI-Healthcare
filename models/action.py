from pydantic import BaseModel
from typing import Optional

class ClaimAction(BaseModel):
    action_type: str  # "correct_code", "appeal", "add_document", "noop"
    new_code: Optional[str] = None
    justification: Optional[str] = None


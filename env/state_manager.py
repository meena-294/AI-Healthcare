import uuid
from data.claim_generator import generate_claim


class StateManager:
    def __init__(self):
        self.current_claim = None
        self.step_count = 0

    def reset(self, task_level="medium"):
        claim = generate_claim(task_level)
        claim["claim_id"] = str(uuid.uuid4())

        self.current_claim = claim
        self.step_count = 0

        return self.current_claim

    def update(self, updated_claim):
        self.current_claim = updated_claim
        self.step_count += 1

    def get_state(self):
        return self.current_claim
import math


def _clamp(v):
    try:
        v = float(v)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    # This keeps scores strictly between 0.1 and 0.9
    # It ensures you never hit 0.0 or 1.0
    return max(0.1, min(v, 0.9))


class EasyGrader:
    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        submitted = self.claim.get("submitted_code", "")
        correct   = self.claim.get("correct_code", "")
        
        # Start with a base that is not 0
        raw = 0.25 

        if action.action_type == "correct_code" and action.new_code:
            if action.new_code == correct:
                raw = 0.85
            elif action.new_code != submitted:
                raw = 0.55
            else:
                raw = 0.35
        elif action.action_type == "add_document":
            raw = 0.40
        elif action.action_type == "appeal":
            raw = 0.30

        return _clamp(raw)

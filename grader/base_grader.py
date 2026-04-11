import math

_BUCKETS = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)

def _safe_bucket(v) -> float:
    try:
        v = float(v)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    if v <= 0.0: return 0.1
    if v >= 1.0: return 0.9
    return min(_BUCKETS, key=lambda b: abs(b - v))


class BaseGrader:
    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        raise NotImplementedError("Subclasses must implement grade()")

    def is_correct_code(self, action) -> bool:
        return action.new_code == self.claim.get("correct_code")

    def has_justification(self, action) -> bool:
        return bool(action.justification) and len(action.justification) > 5

    def mentions_policy(self, action) -> bool:
        if not action.justification:
            return False
        return "policy" in action.justification.lower()

    def mentions_code_fix(self, action) -> bool:
        if not action.justification:
            return False
        return "code" in action.justification.lower()

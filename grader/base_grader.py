import math


def _strict_clamp(v: float) -> float:
    """Score must be strictly in open interval (0, 1). Never 0.0 or 1.0."""
    try:
        v = float(v)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    return max(0.01, min(v, 0.99))


class BaseGrader:
    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        raise NotImplementedError("Subclasses must implement grade()")

    # ── Utility helpers ───────────────────────────────────────────────────────

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

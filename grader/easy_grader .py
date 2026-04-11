import math


def _strict_clamp(value: float) -> float:
    try:
        v = float(value)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    return max(0.1, min(v, 0.9))


class EasyGrader:
    """
    Easy task: agent must correct the procedure code.
    Score is STRICTLY in (0.1, 0.9) ⊂ (0, 1) — never 0.0 or 1.0.
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        submitted = self.claim.get("submitted_code", "")
        correct   = self.claim.get("correct_code", "")

        if action.action_type == "correct_code" and action.new_code:
            if action.new_code == correct:
                raw = 0.88
            elif action.new_code != submitted:
                raw = 0.45
            else:
                raw = 0.15
        elif action.action_type == "add_document":
            raw = 0.20
        elif action.action_type == "appeal":
            raw = 0.12
        else:
            raw = 0.10

        return _strict_clamp(raw)

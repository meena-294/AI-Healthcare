import math


def _clamp(v):
    try:
        v = float(v)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    return max(0.15, min(v, 0.85))


class EasyGrader:
    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        submitted = self.claim.get("submitted_code", "")
        correct   = self.claim.get("correct_code", "")

        if action.action_type == "correct_code" and action.new_code:
            if action.new_code == correct:
                raw = 0.82
            elif action.new_code != submitted:
                raw = 0.45
            else:
                raw = 0.20
        elif action.action_type == "add_document":
            raw = 0.22
        elif action.action_type == "appeal":
            raw = 0.18
        else:
            raw = 0.15   # noop

        return _clamp(raw)

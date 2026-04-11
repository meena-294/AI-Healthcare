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
        try:
            submitted = self.claim.get("submitted_code", "")
            correct   = self.claim.get("correct_code", "")
            if action.action_type == "correct_code" and action.new_code:
                if action.new_code == correct:        raw = 0.82
                elif action.new_code != submitted:    raw = 0.45
                else:                                 raw = 0.20
            elif action.action_type == "add_document": raw = 0.22
            elif action.action_type == "appeal":        raw = 0.18
            else:                                       raw = 0.15
            return _clamp(raw)
        except Exception:
            return 0.5

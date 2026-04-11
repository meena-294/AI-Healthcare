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


class MediumGrader:
    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        try:
            submitted = self.claim.get("submitted_code", "")
            correct   = self.claim.get("correct_code", "")
            score = 0.15
            if action.action_type == "correct_code" and action.new_code:
                if action.new_code == correct:      score += 0.42
                elif action.new_code != submitted:  score += 0.20
                else:                               score += 0.03
                j = len((action.justification or "").strip())
                if j >= 20:   score += 0.20
                elif j >= 10: score += 0.10
                elif j > 0:   score += 0.05
            elif action.action_type == "add_document": score += 0.12
            elif action.action_type == "appeal":        score += 0.08
            return _clamp(score)
        except Exception:
            return 0.5

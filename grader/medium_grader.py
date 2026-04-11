import math


def _clamp(v):
    try:
        v = float(v)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    return max(0.15, min(v, 0.85))


class MediumGrader:
    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        submitted = self.claim.get("submitted_code", "")
        correct   = self.claim.get("correct_code", "")

        score = 0.15  # safe base

        if action.action_type == "correct_code" and action.new_code:
            if action.new_code == correct:
                score += 0.42
            elif action.new_code != submitted:
                score += 0.20
            else:
                score += 0.03

            j = action.justification or ""
            j_len = len(j.strip())
            if j_len >= 20:
                score += 0.20
            elif j_len >= 10:
                score += 0.10
            elif j_len > 0:
                score += 0.05

        elif action.action_type == "add_document":
            score += 0.12
        elif action.action_type == "appeal":
            score += 0.08
        # noop stays at base 0.15

        # Max: 0.15 + 0.42 + 0.20 = 0.77 → clamped to 0.85 ✓
        return _clamp(score)

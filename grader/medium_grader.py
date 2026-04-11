import math


def _strict_clamp(value: float) -> float:
    try:
        v = float(value)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    return max(0.1, min(v, 0.9))


class MediumGrader:
    """
    Medium task: agent must correct the code AND provide justification.
    Score is STRICTLY in (0.1, 0.9) ⊂ (0, 1) — never 0.0 or 1.0.
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        submitted = self.claim.get("submitted_code", "")
        correct   = self.claim.get("correct_code", "")

        score = 0.10  # safe non-zero base

        if action.action_type == "correct_code" and action.new_code:
            if action.new_code == correct:
                score += 0.50
            elif action.new_code != submitted:
                score += 0.22
            else:
                score += 0.04

            justification = action.justification or ""
            j_len = len(justification.strip())
            if j_len >= 20:
                score += 0.25
            elif j_len >= 10:
                score += 0.13
            elif j_len > 0:
                score += 0.06

        elif action.action_type == "add_document":
            score += 0.14

        elif action.action_type == "appeal":
            score += 0.09

        return _strict_clamp(score)

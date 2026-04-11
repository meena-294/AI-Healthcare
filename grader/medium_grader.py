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


class MediumGrader:
    """
    Medium task: agent must correct the code AND provide a justification.
    Score is ALWAYS one of: 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
    NEVER 0.0 or 1.0
    Max possible raw = 0.15 + 0.42 + 0.20 = 0.77 → buckets to 0.8
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        try:
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

                j = len((action.justification or "").strip())
                if j >= 20:
                    score += 0.20
                elif j >= 10:
                    score += 0.10
                elif j > 0:
                    score += 0.05

            elif action.action_type == "add_document":
                score += 0.12
            elif action.action_type == "appeal":
                score += 0.08

            return _safe_bucket(score)

        except Exception:
            return 0.5

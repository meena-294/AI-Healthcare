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


class EasyGrader:
    """
    Easy task: agent must correct the procedure code.
    Score is ALWAYS one of: 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
    NEVER 0.0 or 1.0
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        try:
            submitted = self.claim.get("submitted_code", "")
            correct   = self.claim.get("correct_code", "")

            if action.action_type == "correct_code" and action.new_code:
                if action.new_code == correct:
                    raw = 0.85
                elif action.new_code != submitted:
                    raw = 0.50
                else:
                    raw = 0.30
            elif action.action_type == "add_document":
                raw = 0.40
            elif action.action_type == "appeal":
                raw = 0.35
            else:
                raw = 0.20   # noop / unknown

            return _safe_bucket(raw)

        except Exception:
            return 0.5

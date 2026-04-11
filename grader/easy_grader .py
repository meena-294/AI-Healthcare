import math


def _clamp(v):
    try:
        v = float(v)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    # Strictly between 0 and 1 — never 0.0 or 1.0
    return max(0.01, min(v, 0.99))


class EasyGrader:
    """
    Easy task: agent must correct the procedure code.
    Score is strictly in (0, 1) — never 0.0 or 1.0 exactly.
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        try:
            submitted = self.claim.get("submitted_code", "")
            correct   = self.claim.get("correct_code", "")

            # Start with a safe base score
            raw = 0.20

            if action.action_type == "correct_code" and action.new_code:
                if action.new_code == correct:
                    raw = 0.85      # High but never 1.0
                elif action.new_code != submitted:
                    raw = 0.50      # Attempted fix, wrong code
                else:
                    raw = 0.30      # Submitted same wrong code

            elif action.action_type == "add_document":
                raw = 0.40

            elif action.action_type == "appeal":
                raw = 0.35

            else:
                raw = 0.15          # noop / unknown

            return _clamp(raw)

        except Exception:
            return 0.5

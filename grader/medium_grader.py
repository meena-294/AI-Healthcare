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


class MediumGrader:
    """
    Medium task: agent must correct the code AND provide a justification.
    Score is strictly in (0, 1) — never 0.0 or 1.0 exactly.
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        try:
            submitted = self.claim.get("submitted_code", "")
            correct   = self.claim.get("correct_code", "")

            score = 0.15    # safe base — never starts at 0.0

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

            # Max possible: 0.15 + 0.42 + 0.20 = 0.77 → safely under 0.99
            return _clamp(score)

        except Exception:
            return 0.5

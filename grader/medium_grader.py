class MediumGrader:
    """
    Medium task: agent must correct the code AND provide a justification.
    Score is strictly in (0, 1) — never 0.0 or 1.0 exactly.
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        submitted = self.claim.get("submitted_code", "")
        correct   = self.claim.get("correct_code", "")

        score = 0.05  # base minimum

        if action.action_type == "correct_code" and action.new_code:
            # Code correctness (up to 0.6)
            if action.new_code == correct:
                score += 0.60
            elif action.new_code != submitted:
                score += 0.25  # attempted but wrong
            else:
                score += 0.05  # no change

            # Justification quality (up to 0.3)
            justification = action.justification or ""
            if len(justification) >= 20:
                score += 0.30
            elif len(justification) >= 10:
                score += 0.15
            elif len(justification) > 0:
                score += 0.08

        elif action.action_type == "add_document":
            score += 0.15

        elif action.action_type == "appeal":
            score += 0.08

        # noop stays at base 0.05

        return _clamp(score)


def _clamp(score: float) -> float:
    """Ensure score is strictly between 0 and 1 (exclusive)."""
    return max(0.01, min(score, 0.99))

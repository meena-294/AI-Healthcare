class EasyGrader:
    """
    Easy task: agent must correct the procedure code.
    Score is strictly in (0, 1) — never 0.0 or 1.0 exactly.
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        submitted = self.claim.get("submitted_code", "")
        correct   = self.claim.get("correct_code", "")

        if action.action_type == "correct_code" and action.new_code:
            if action.new_code == correct:
                # Perfect code fix → high but not exactly 1.0
                score = 0.95
            elif action.new_code != submitted:
                # Attempted a fix but wrong code → partial credit
                score = 0.45
            else:
                # Submitted same wrong code → low
                score = 0.15
        elif action.action_type == "add_document":
            # Not the right action for easy but not harmful
            score = 0.2
        elif action.action_type == "appeal":
            score = 0.1
        else:
            # noop
            score = 0.05

        # Always clamp strictly inside (0, 1)
        return _clamp(score)


def _clamp(score: float) -> float:
    """Ensure score is strictly between 0 and 1 (exclusive)."""
    return max(0.01, min(score, 0.99))

class EasyGrader:
    """
    Easy task: agent must correct the procedure code.
    Score is STRICTLY in (0, 1) — never 0.0 or 1.0 exactly.
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        submitted = self.claim.get("submitted_code", "")
        correct   = self.claim.get("correct_code", "")

        if action.action_type == "correct_code" and action.new_code:
            if action.new_code == correct:
                raw = 0.92
            elif action.new_code != submitted:
                raw = 0.45
            else:
                raw = 0.15
        elif action.action_type == "add_document":
            raw = 0.20
        elif action.action_type == "appeal":
            raw = 0.12
        else:
            raw = 0.08   # noop — was 0.05, bumped away from edge

        return _strict_clamp(raw)


def _strict_clamp(value: float) -> float:
    """Guarantee strictly open interval (0, 1) — hard floor 0.05, hard ceiling 0.95."""
    return max(0.05, min(float(value), 0.95))

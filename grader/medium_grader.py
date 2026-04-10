class MediumGrader:
    """
    Medium task: agent must correct the code AND provide justification.
    Score is STRICTLY in (0, 1) — never 0.0 or 1.0 exactly.
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        submitted = self.claim.get("submitted_code", "")
        correct   = self.claim.get("correct_code", "")

        # Start with a safe non-zero base
        score = 0.08

        if action.action_type == "correct_code" and action.new_code:
            # Code correctness — max contribution 0.55
            if action.new_code == correct:
                score += 0.55
            elif action.new_code != submitted:
                score += 0.22
            else:
                score += 0.04

            # Justification quality — max contribution 0.28
            justification = action.justification or ""
            j_len = len(justification.strip())
            if j_len >= 20:
                score += 0.28
            elif j_len >= 10:
                score += 0.14
            elif j_len > 0:
                score += 0.07

        elif action.action_type == "add_document":
            score += 0.14

        elif action.action_type == "appeal":
            score += 0.09

        # noop stays at base 0.08

        return _strict_clamp(score)


def _strict_clamp(value: float) -> float:
    """Guarantee strictly open interval (0, 1) — hard floor 0.05, hard ceiling 0.95."""
    return max(0.05, min(float(value), 0.95))

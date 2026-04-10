class RewardCalculator:
    """
    Computes final reward from grader score + efficiency + penalties.
    CRITICAL: Final reward must be strictly in (0, 1) — never 0.0 or 1.0 exactly.
    """

    def __init__(self, claim):
        self.claim = claim

    def compute(self, action, grader_score, step_count, max_steps) -> float:
        # ── Base from grader (already in (0,1) range) ─────────────────────
        reward = grader_score * 0.70

        # ── Step efficiency bonus (fewer steps = better) ──────────────────
        # Ranges from 0 (last step) to ~0.18 (first step), never hits 0.2 exactly
        efficiency = (max_steps - step_count) / max_steps
        reward += efficiency * 0.18   # capped at 0.18, not 0.2

        # ── Action-type penalties ─────────────────────────────────────────
        if action.action_type == "noop":
            reward -= 0.18   # penalise doing nothing
        elif action.action_type not in ["correct_code", "add_document", "appeal"]:
            reward -= 0.25   # penalise unknown actions

        # ── Step penalty (discourages long episodes) ──────────────────────
        reward -= 0.04 * step_count   # slightly softer than 0.05

        # ── Clamp strictly inside (0, 1) ──────────────────────────────────
        return _strict_clamp(reward)


def _strict_clamp(value: float) -> float:
    """
    Clamp value to strictly open interval (0, 1).
    Never returns exactly 0.0 or 1.0.
    """
    EPSILON = 0.01
    return max(EPSILON, min(value, 1.0 - EPSILON))

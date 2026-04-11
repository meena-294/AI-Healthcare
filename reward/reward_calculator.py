import math


def _strict_clamp(v):
    """
    Guarantee value is strictly in open interval (0, 1).
    Never returns exactly 0.0 or 1.0.
    """
    try:
        v = float(v)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    return max(0.01, min(v, 0.99))


class RewardCalculator:
    """
    Computes final reward from grader score + efficiency + penalties.
    CRITICAL: Final reward must be strictly in (0, 1) — never 0.0 or 1.0 exactly.
    """

    def __init__(self, claim):
        self.claim = claim

    def compute(self, action, grader_score, step_count, max_steps) -> float:
        # Base from grader (already clamped to (0.01, 0.99))
        reward = grader_score * 0.70

        # Step efficiency bonus — ranges 0 → 0.18 (never exactly 0.2)
        efficiency = (max_steps - step_count) / max_steps
        reward += efficiency * 0.18

        # Action-type penalties
        if action.action_type == "noop":
            reward -= 0.18
        elif action.action_type not in ["correct_code", "add_document", "appeal"]:
            reward -= 0.25

        # Step penalty — discourages long episodes
        reward -= 0.04 * step_count

        # ✅ Strict clamp — NEVER returns exact 0.0 or 1.0
        return _strict_clamp(reward)

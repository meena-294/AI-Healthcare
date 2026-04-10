class RewardCalculator:
    """
    Computes final reward from grader score + efficiency + penalties.
    CRITICAL: Output is ALWAYS strictly in (0, 1) — never 0.0 or 1.0 exactly.

    Design principles to guarantee this:
    1. grader_score is already in [0.05, 0.95] (from graders)
    2. We scale it to [0.035, 0.665] by multiplying by 0.70
    3. Efficiency bonus adds at most +0.15 (never pushes to 1.0)
    4. Penalties subtract but final clamp to [0.05, 0.95] is the hard safety net
    """

    def __init__(self, claim):
        self.claim = claim

    def compute(self, action, grader_score, step_count, max_steps) -> float:
        # ── Base from grader: grader guarantees [0.05, 0.95]
        # After * 0.70: range is [0.035, 0.665]
        reward = float(grader_score) * 0.70

        # ── Efficiency bonus: max +0.15, min +0.0 (not +0 exactly due to clamp later)
        # step_count is at least 1, max_steps is at least 1
        safe_max = max(int(max_steps), 1)
        safe_step = max(int(step_count), 1)
        efficiency = (safe_max - safe_step) / safe_max   # in [0, 1)
        reward += efficiency * 0.15

        # ── Action-type penalties
        if action.action_type == "noop":
            reward -= 0.15
        elif action.action_type not in ("correct_code", "add_document", "appeal", "noop"):
            reward -= 0.20

        # ── Step penalty (soft, discourages very long episodes)
        reward -= 0.03 * safe_step

        # ── Final hard clamp — this is the definitive safety net
        # Floor 0.05, ceiling 0.95: mathematically impossible to return 0.0 or 1.0
        return _strict_clamp(reward)


def _strict_clamp(value: float) -> float:
    """
    Hard clamp to strictly open interval (0, 1).
    Uses 0.05 / 0.95 bounds (well away from 0 and 1) for extra safety margin.
    """
    return max(0.05, min(float(value), 0.95))

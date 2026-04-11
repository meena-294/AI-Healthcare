import math


def _strict_clamp(value: float) -> float:
    """
    Hard clamp to strictly open interval (0, 1).
    Floor=0.1, ceiling=0.9 — wide safety margin from 0.0 and 1.0.
    Also handles NaN and Inf.
    """
    try:
        v = float(value)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    return max(0.1, min(v, 0.9))


class RewardCalculator:
    """
    Computes final reward from grader score + efficiency + penalties.
    Output is ALWAYS strictly in (0.1, 0.9) ⊂ (0, 1).
    """

    def __init__(self, claim):
        self.claim = claim

    def compute(self, action, grader_score, step_count, max_steps) -> float:
        # ── Base from grader (grader guarantees [0.05, 0.95])
        # After * 0.70: range is [0.035, 0.665]
        reward = float(grader_score) * 0.70

        # ── Efficiency bonus: max +0.15
        safe_max  = max(int(max_steps), 1)
        safe_step = max(int(step_count), 1)
        efficiency = (safe_max - safe_step) / safe_max   # in [0, 1)
        reward += efficiency * 0.15

        # ── Action-type penalties
        if action.action_type == "noop":
            reward -= 0.15
        elif action.action_type not in ("correct_code", "add_document", "appeal", "noop"):
            reward -= 0.20

        # ── Step penalty
        reward -= 0.03 * safe_step

        # ── Final hard clamp — always returns value in (0.1, 0.9)
        return _strict_clamp(reward)

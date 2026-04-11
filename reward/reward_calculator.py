import math


def _clamp(value: float) -> float:
    try:
        v = float(value)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    return max(0.15, min(v, 0.85))


class RewardCalculator:
    def __init__(self, claim):
        self.claim = claim

    def compute(self, action, grader_score, step_count, max_steps) -> float:
        # Base: grader_score in [0.15, 0.85], scaled by 0.70 → [0.105, 0.595]
        reward = float(grader_score) * 0.70

        # Efficiency bonus: max +0.12 (step 1 of 10 → 0.9 * 0.12 = 0.108)
        safe_max  = max(int(max_steps), 1)
        safe_step = max(int(step_count), 1)
        efficiency = (safe_max - safe_step) / safe_max
        reward += efficiency * 0.12

        # Penalties
        if action.action_type == "noop":
            reward -= 0.10
        elif action.action_type not in ("correct_code", "add_document", "appeal", "noop"):
            reward -= 0.15

        # Step cost
        reward -= 0.02 * safe_step

        # Max possible before clamp:
        # 0.85*0.70 + 0.9*0.12 = 0.595 + 0.108 = 0.703 → clamped to 0.85 ✓
        # Min possible before clamp:
        # 0.15*0.70 + 0 - 0.10 - 0.02*10 = 0.105 - 0.10 - 0.20 = -0.195 → clamped to 0.15 ✓
        return _clamp(reward)

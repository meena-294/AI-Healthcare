import math


def strict_clamp(v):
    try:
        v = float(v)
    except:
        return 0.5

    if not math.isfinite(v):
        return 0.5

    if v <= 0.0:
        return 0.01
    if v >= 1.0:
        return 0.99

    return max(0.01, min(0.99, v))


class RewardCalculator:

    def __init__(self, claim):
        self.claim = claim

    def compute(self, action, grader_score, step_count, max_steps) -> float:
        reward = grader_score * 0.70

        efficiency = (max_steps - step_count) / max_steps
        reward += efficiency * 0.18

        if action.action_type == "noop":
            reward -= 0.18
        elif action.action_type not in ["correct_code", "add_document", "appeal"]:
            reward -= 0.25

        reward -= 0.04 * step_count

        # EXTRA SAFE BUFFER (avoid edges completely)
        reward = max(0.02, min(0.98, reward))

        return strict_clamp(reward)

import math


def _clamp(v):
    try:
        v = float(v)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    return max(0.15, min(v, 0.85))


class RewardCalculator:
    def __init__(self, claim):
        self.claim = claim

    def compute(self, action, grader_score, step_count, max_steps) -> float:
        try:
            reward    = float(grader_score) * 0.70
            safe_max  = max(int(max_steps), 1)
            safe_step = max(int(step_count), 1)
            reward   += ((safe_max - safe_step) / safe_max) * 0.12

            if action.action_type == "noop":
                reward -= 0.10
            elif action.action_type not in ("correct_code", "add_document", "appeal", "noop"):
                reward -= 0.15

            reward -= 0.02 * safe_step
            return _clamp(reward)
        except Exception:
            return 0.5

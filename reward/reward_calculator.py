import math

_BUCKETS = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)

def _safe_bucket(v) -> float:
    try:
        v = float(v)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    if v <= 0.0: return 0.1
    if v >= 1.0: return 0.9
    return min(_BUCKETS, key=lambda b: abs(b - v))


class RewardCalculator:
    def __init__(self, claim):
        self.claim = claim

    def compute(self, action, grader_score, step_count, max_steps) -> float:
        # Clamp grader_score input first
        grader_score = _safe_bucket(grader_score)

        reward  = grader_score * 0.70
        eff     = (max_steps - step_count) / max(max_steps, 1)
        reward += eff * 0.18

        if action.action_type == "noop":
            reward -= 0.18
        elif action.action_type not in ["correct_code", "add_document", "appeal"]:
            reward -= 0.25

        reward -= 0.04 * step_count

        # Always return a safe bucket value
        return _safe_bucket(reward)

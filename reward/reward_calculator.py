class RewardCalculator:
    def __init__(self, claim):
        self.claim = claim

    def compute(self, action, grader_score, step_count, max_steps):
        reward = 0.0

        # Base reward from grader
        reward += grader_score * 0.7

        # Step efficiency (fewer steps = better)
        efficiency_bonus = (max_steps - step_count) / max_steps
        reward += efficiency_bonus * 0.2

        # Penalty for noop or invalid
        if action.action_type == "noop":
            reward -= 0.2

        if action.action_type not in ["correct_code", "add_document", "appeal"]:
            reward -= 0.3

        # Small step penalty (to avoid long loops)
        reward -= 0.05 * step_count

        return max(min(reward, 1.0), -1.0)
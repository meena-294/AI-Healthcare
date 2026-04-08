from grader.base_grader import BaseGrader


class HardGrader(BaseGrader):
    def grade(self, action):
        score = 0.0

        # Correct code (core)
        if self.is_correct_code(action):
            score += 0.5

        # Justification quality
        if self.has_justification(action):
            score += 0.2

        # Mentions policy (important in healthcare)
        if self.mentions_policy(action):
            score += 0.2

        # Mentions code correction explicitly
        if self.mentions_code_fix(action):
            score += 0.1

        return min(score, 1.0)
from grader.base_grader import BaseGrader


class EasyGrader(BaseGrader):
    def grade(self, action):
        score = 0.0

        # Correct code fix (main objective)
        if self.is_correct_code(action):
            score += 1.0

        return min(score, 1.0)
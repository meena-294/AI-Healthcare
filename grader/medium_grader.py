from grader.base_grader import BaseGrader

class MediumGrader(BaseGrader):
    def grade(self, action):
        score = 0.0

        # Code correction
        if self.is_correct_code(action):
            score += 0.5

        # Justification
        if self.has_justification(action):
            score += 0.15

        # Mentions fix
        if self.mentions_code_fix(action):
            score += 0.15

        # 🔥 NEW: document addition reward
        if action.action_type == "add_document":
            score += 0.2

        return min(score, 1.0)
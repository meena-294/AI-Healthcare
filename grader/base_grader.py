class BaseGrader:
    def __init__(self, claim):
        self.claim = claim

    def grade(self, action):
        raise NotImplementedError("Subclasses must implement this method")

    # Utility checks
    def is_correct_code(self, action):
        return action.new_code == self.claim["correct_code"]

    def has_justification(self, action):
        return action.justification is not None and len(action.justification) > 5

    def mentions_policy(self, action):
        if not action.justification:
            return False
        return "policy" in action.justification.lower()

    def mentions_code_fix(self, action):
        if not action.justification:
            return False
        return "code" in action.justification.lower()
import math


def _clamp(v):
    try:
        v = float(v)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    # This keeps scores strictly between 0.1 and 0.9
    # It ensures you never hit 0.0 or 1.0
    return max(0.1, min(v, 0.9))


 def grade(self, action) -> float:
        submitted = self.claim.get("submitted_code", "")
        correct   = self.claim.get("correct_code", "")

        # Start with a safe base score
        raw = 0.20 

        if action.action_type == "correct_code" and action.new_code:
            if action.new_code == correct:
                raw = 0.85 # High but not 1.0
            elif action.new_code != submitted:
                raw = 0.50 
            else:
                raw = 0.30 
        elif action.action_type == "add_document":
            raw = 0.40
        elif action.action_type == "appeal":
            raw = 0.35
        else:
            raw = 0.15 # Default for no-op/unknown actions

        return _clamp(raw)

import math


def _strict_clamp(value: float) -> float:
    try:
        v = float(value)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    return max(0.1, min(v, 0.9))


class HardGrader:
    """
    Hard task: correct code + justification + document handling.
    Score is STRICTLY in (0.1, 0.9) ⊂ (0, 1) — never 0.0 or 1.0.
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        submitted  = self.claim.get("submitted_code", "")
        correct    = self.claim.get("correct_code", "")
        documents  = self.claim.get("documents", [])
        procedure  = self.claim.get("procedure", "")
        age        = self.claim.get("patient_age", 0)

        score = 0.10  # safe non-zero base

        if action.action_type == "correct_code" and action.new_code:
            if action.new_code == correct:
                score += 0.40
            elif action.new_code != submitted:
                score += 0.18
            else:
                score += 0.03

            justification = action.justification or ""
            j_len = len(justification.strip())
            if j_len >= 30:
                score += 0.18
            elif j_len >= 15:
                score += 0.10
            elif j_len > 0:
                score += 0.05

        elif action.action_type == "add_document":
            needs_preapproval = (procedure == "MRI Scan" and "preapproval" not in documents)
            needs_senior      = (age > 60 and "senior_approval" not in documents)
            if needs_preapproval or needs_senior:
                score += 0.22
            else:
                score += 0.07

        elif action.action_type == "appeal":
            denial = self.claim.get("denial_reason", "").lower()
            if "not medically necessary" in denial or "not covered" in denial:
                score += 0.14
            else:
                score += 0.05

        policy = self.claim.get("policy", "")
        if "premium" in policy.lower():
            score += 0.04

        return _strict_clamp(score)

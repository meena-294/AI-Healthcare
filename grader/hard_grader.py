import math


def _clamp(v):
    try:
        v = float(v)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    return max(0.15, min(v, 0.85))


class HardGrader:
    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        submitted = self.claim.get("submitted_code", "")
        correct   = self.claim.get("correct_code", "")
        documents = self.claim.get("documents", [])
        procedure = self.claim.get("procedure", "")
        age       = self.claim.get("patient_age", 0)

        score = 0.15  # safe base

        if action.action_type == "correct_code" and action.new_code:
            if action.new_code == correct:
                score += 0.35
            elif action.new_code != submitted:
                score += 0.15
            else:
                score += 0.02

            j = action.justification or ""
            j_len = len(j.strip())
            if j_len >= 30:
                score += 0.16
            elif j_len >= 15:
                score += 0.08
            elif j_len > 0:
                score += 0.04

        elif action.action_type == "add_document":
            needs = (procedure == "MRI Scan" and "preapproval" not in documents)
            needs_sr = (age > 60 and "senior_approval" not in documents)
            score += 0.20 if (needs or needs_sr) else 0.06

        elif action.action_type == "appeal":
            denial = self.claim.get("denial_reason", "").lower()
            score += 0.12 if ("not medically necessary" in denial or "not covered" in denial) else 0.04

        policy = self.claim.get("policy", "")
        if "premium" in policy.lower():
            score += 0.03

        # Max: 0.15 + 0.35 + 0.16 + 0.03 = 0.69 → safe, under 0.85 ✓
        return _clamp(score)

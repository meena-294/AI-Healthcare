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


class HardGrader:
    """
    Hard task: fix code + justification + preapproval / senior docs.
    Score is ALWAYS one of: 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
    NEVER 0.0 or 1.0
    Max possible raw = 0.15 + 0.35 + 0.16 + 0.03 = 0.69 → buckets to 0.7
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        try:
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

                j = len((action.justification or "").strip())
                if j >= 30:
                    score += 0.16
                elif j >= 15:
                    score += 0.08
                elif j > 0:
                    score += 0.04

            elif action.action_type == "add_document":
                needs_pre    = (procedure == "MRI Scan" and "preapproval" not in documents)
                needs_senior = (age > 60 and "senior_approval" not in documents)
                score += 0.20 if (needs_pre or needs_senior) else 0.06

            elif action.action_type == "appeal":
                denial = self.claim.get("denial_reason", "").lower()
                if "not medically necessary" in denial or "not covered" in denial:
                    score += 0.12
                else:
                    score += 0.04

            if "premium" in self.claim.get("policy", "").lower():
                score += 0.03

            return _safe_bucket(score)

        except Exception:
            return 0.5

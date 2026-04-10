class HardGrader:
    """
    Hard task: agent must correct the code, provide justification,
    AND handle preapproval / senior approval documents.
    Score is strictly in (0, 1) — never 0.0 or 1.0 exactly.
    """

    def __init__(self, claim):
        self.claim = claim

    def grade(self, action) -> float:
        submitted  = self.claim.get("submitted_code", "")
        correct    = self.claim.get("correct_code", "")
        documents  = self.claim.get("documents", [])
        procedure  = self.claim.get("procedure", "")
        age        = self.claim.get("patient_age", 0)

        score = 0.05  # base minimum

        # ── Code correction (up to 0.45) ──────────────────────────────────
        if action.action_type == "correct_code" and action.new_code:
            if action.new_code == correct:
                score += 0.45
            elif action.new_code != submitted:
                score += 0.20
            else:
                score += 0.03

            # Justification quality (up to 0.20)
            justification = action.justification or ""
            if len(justification) >= 30:
                score += 0.20
            elif len(justification) >= 15:
                score += 0.10
            elif len(justification) > 0:
                score += 0.05

        # ── Document handling (up to 0.25) ────────────────────────────────
        elif action.action_type == "add_document":
            needs_preapproval   = (procedure == "MRI Scan" and "preapproval" not in documents)
            needs_senior        = (age > 60 and "senior_approval" not in documents)

            if needs_preapproval or needs_senior:
                score += 0.25   # adding a needed document
            else:
                score += 0.08   # adding a document that wasn't required

        # ── Appeal (up to 0.15) ───────────────────────────────────────────
        elif action.action_type == "appeal":
            denial = self.claim.get("denial_reason", "").lower()
            if "not medically necessary" in denial or "not covered" in denial:
                score += 0.15   # valid appeal scenario
            else:
                score += 0.05

        # ── Policy compliance bonus ───────────────────────────────────────
        policy = self.claim.get("policy", "")
        if "premium" in policy.lower():
            score += 0.05   # small bonus for premium plan handling

        return _clamp(score)


def _clamp(score: float) -> float:
    """Ensure score is strictly between 0 and 1 (exclusive)."""
    return max(0.01, min(score, 0.99))

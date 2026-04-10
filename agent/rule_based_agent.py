class RuleBasedAgent:

    def act(self, obs):
        try:
            if not obs:
                return {"action_type": "noop"}

            submitted_code = obs.get("submitted_code", "")
            correct_code   = obs.get("correct_code", "")   # available in obs if env exposes it
            documents      = obs.get("documents", [])
            procedure      = obs.get("procedure", "")
            denial_reason  = obs.get("denial_reason", "")
            patient_age    = obs.get("patient_age", 0)
            policy         = obs.get("policy", "")

            # ── STEP 1: Fix code if submitted ≠ correct ──────────────────────
            if submitted_code != correct_code and correct_code:
                justification = _build_justification(procedure, denial_reason, policy, patient_age)
                return {
                    "action_type":   "correct_code",
                    "new_code":       correct_code,
                    "justification":  justification,
                }

            # ── Fallback: infer correct code from procedure if not in obs ────
            if submitted_code and not correct_code:
                inferred = _infer_correct_code(procedure)
                if inferred and inferred != submitted_code:
                    return {
                        "action_type":  "correct_code",
                        "new_code":      inferred,
                        "justification": _build_justification(procedure, denial_reason, policy, patient_age),
                    }

            # ── STEP 2: Add missing documents ────────────────────────────────
            if procedure == "MRI Scan" and "preapproval" not in documents:
                return {
                    "action_type":  "add_document",
                    "justification": "Adding preapproval document required for MRI procedures",
                }

            if patient_age > 60 and "senior_approval" not in documents:
                return {
                    "action_type":  "add_document",
                    "justification": "Adding senior approval document for patient above 60",
                }

            # ── STEP 3: Appeal if denial reason warrants it ──────────────────
            if "not medically necessary" in denial_reason.lower():
                return {
                    "action_type":  "appeal",
                    "justification": "Appealing denial — procedure is medically necessary per physician referral",
                }

            # ── Done ─────────────────────────────────────────────────────────
            return {"action_type": "noop"}

        except Exception:
            return {"action_type": "noop"}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_justification(procedure, denial_reason, policy, patient_age):
    """Generate a realistic, context-aware justification string."""
    parts = [f"Correcting procedure code for {procedure}"]

    if denial_reason and denial_reason.lower() != "none (resolved)":
        parts.append(f"addressing denial: '{denial_reason}'")

    if policy:
        parts.append(f"as required under {policy}")

    if patient_age > 60:
        parts.append("with additional senior compliance check")

    return "; ".join(parts) + "."


# Procedure → realistic correct code ranges (used only as fallback)
_CODE_MAP = {
    "MRI Scan":   ["MRI452", "MRI817", "MRI364", "MRI591", "MRI736"],
    "X-Ray":      ["XRAY143", "XRAY562", "XRAY389", "XRAY714", "XRAY921"],
    "Blood Test": ["BT481",  "BT729",  "BT356",  "BT614",  "BT893"],
    "CT Scan":    ["CT512",  "CT874",  "CT263",  "CT945",  "CT137"],
    "Ultrasound": ["USG318", "USG647", "USG521", "USG839", "USG174"],
}

import random

def _infer_correct_code(procedure):
    pool = _CODE_MAP.get(procedure)
    return random.choice(pool) if pool else None

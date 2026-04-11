class RuleBasedAgent:

    def act(self, obs):
        try:
            if not obs:
                return {
                    "action_type": "appeal",
                    "justification": "Fallback action due to missing observation"
                }

            submitted = obs.get("submitted_code", "")
            correct   = obs.get("correct_code", "")
            docs      = obs.get("documents", [])
            procedure = obs.get("procedure", "")
            denial    = (obs.get("denial_reason") or "").lower()
            age       = obs.get("patient_age", 0)
            policy    = obs.get("policy", "")

            # ───────── STEP 1: FIX CODE ─────────
            if submitted != correct and correct:
                return {
                    "action_type": "correct_code",
                    "new_code": correct,
                    "justification": (
                        f"The submitted code was incorrect for {procedure}. "
                        f"It has been corrected according to policy {policy}. "
                        f"This resolves the denial reason: {denial}."
                    )
                }

            # ───────── STEP 2: MRI PREAPPROVAL ─────────
            if procedure == "MRI Scan" and "preapproval" not in docs:
                return {
                    "action_type": "add_document",
                    "justification": "Adding required preapproval for MRI as per policy"
                }

            # ───────── STEP 3: SENIOR APPROVAL ─────────
            if age > 60 and "senior_approval" not in docs:
                return {
                    "action_type": "add_document",
                    "justification": "Adding senior approval for patient above 60"
                }

            # ───────── STEP 4: APPEAL ─────────
            if "not medically necessary" in denial or "not covered" in denial:
                return {
                    "action_type": "appeal",
                    "justification": "Appealing as procedure is medically necessary and valid"
                }

            # ───────── FINAL: NEVER NOOP ─────────
            return {
                "action_type": "appeal",
                "justification": "All corrections completed, requesting approval"
            }

        except Exception:
            return {
                "action_type": "appeal",
                "justification": "Fallback due to unexpected error"
            }

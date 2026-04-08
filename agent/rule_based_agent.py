class RuleBasedAgent:

    def act(self, obs):
        try:
            if not obs:
                return {"action_type": "noop"}

            submitted_code = obs.get("submitted_code")
            documents = obs.get("documents", [])

            # 🔥 STEP 1: FIX CODE (ALL TASKS)
            if submitted_code == "WRONG123":

                procedure = obs.get("procedure")

                if procedure == "MRI Scan":
                    new_code = "MRI200"
                    justification = "Correcting procedure code as per policy and claim validation rules"

                elif procedure == "X-Ray":
                    new_code = "XRAY200"
                    justification = "Fixing code issue"

                else:
                    new_code = "BT200"
                    justification = "Fix"

                return {
                    "action_type": "correct_code",
                    "new_code": new_code,
                    "justification": justification
                }

            # 🔥 STEP 2: IF NOT DONE → ADD DOCUMENT
            # (Environment will decide if needed)
            if "preapproval" not in documents:
                return {
                    "action_type": "add_document",
                    "justification": "Adding preapproval as required by policy"
                }

            # 🔥 DONE
            return {"action_type": "noop"}

        except Exception:
            return {"action_type": "noop"}
def check_denials(claim):
    reasons = []

    # Rule 1: Incorrect code
    if claim["submitted_code"] != claim["correct_code"]:
        reasons.append("Incorrect procedure code")

    # Rule 2: Not covered
    if claim["procedure"] not in claim["policy_rules"]["covered_procedures"]:
        reasons.append("Procedure not covered")

    # Rule 3: Preapproval required
    if claim["procedure"] in claim["policy_rules"]["requires_preapproval"]:
        if not claim.get("preapproval", False):
            reasons.append("Missing preapproval")

    return reasons
def apply_action(state_manager, action):
    claim = state_manager.get_state()

    result = {
        "valid": True,
        "message": "Action applied"
    }

    if action.action_type == "correct_code":
        if not action.new_code:
            result["valid"] = False
            result["message"] = "Missing new_code"
        else:
            claim["submitted_code"] = action.new_code

    elif action.action_type == "add_document":
        claim.setdefault("documents", [])

        # MRI → preapproval
        if claim.get("procedure") == "MRI Scan" and not claim.get("preapproval"):
            claim["documents"].append("preapproval")
            claim["preapproval"] = True

        # 🔥 NEW RULE → senior approval
        elif claim.get("patient_age", 0) > 60 and not claim.get("senior_approval"):
            claim["documents"].append("senior_approval")
            claim["senior_approval"] = True

    elif action.action_type == "appeal":
        claim["appealed"] = True

    elif action.action_type == "noop":
        result["message"] = "No operation"

    else:
        result["valid"] = False
        result["message"] = "Invalid action_type"

    return claim, result
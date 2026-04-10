import random

# ── Realistic procedure code pools ────────────────────────────────────────────

PROCEDURE_DATA = {
    "MRI Scan": {
        "correct_codes": ["MRI452", "MRI817", "MRI364", "MRI591", "MRI736"],
        "wrong_codes":   ["MRI001", "MRI999", "SCN100", "IMG202", "RAD303"],
        "denial_reasons": [
            "Incorrect procedure code",
            "Preapproval not obtained",
            "Code mismatch with policy",
            "Missing authorization for MRI",
        ],
    },
    "X-Ray": {
        "correct_codes": ["XRAY143", "XRAY562", "XRAY389", "XRAY714", "XRAY921"],
        "wrong_codes":   ["XR001", "RAY999", "IMG101", "SCN050", "DXR202"],
        "denial_reasons": [
            "Incorrect procedure code",
            "Duplicate claim detected",
            "Code not covered under policy",
            "Non-matching diagnosis code",
        ],
    },
    "Blood Test": {
        "correct_codes": ["BT481", "BT729", "BT356", "BT614", "BT893"],
        "wrong_codes":   ["BT001", "LAB999", "TST202", "BLD100", "HEM303"],
        "denial_reasons": [
            "Incorrect procedure code",
            "Lab not in-network",
            "Missing referral",
            "Code not listed in plan",
        ],
    },
    "CT Scan": {
        "correct_codes": ["CT512", "CT874", "CT263", "CT945", "CT137"],
        "wrong_codes":   ["CTX001", "SCN999", "IMG404", "RAD101", "CT000"],
        "denial_reasons": [
            "Incorrect procedure code",
            "Preapproval required for CT",
            "Diagnosis not matching procedure",
            "Benefit limit exceeded",
        ],
    },
    "Ultrasound": {
        "correct_codes": ["USG318", "USG647", "USG521", "USG839", "USG174"],
        "wrong_codes":   ["US001", "ULT999", "SON202", "IMG303", "USG000"],
        "denial_reasons": [
            "Incorrect procedure code",
            "Not medically necessary",
            "Out-of-network provider",
            "Missing diagnosis code",
        ],
    },
}

POLICIES = ["Basic Plan", "Standard Plan", "Premium Plan", "Senior Care Plan", "Family Cover"]

EASY_AGES   = list(range(20, 55))
MEDIUM_AGES = list(range(30, 65))
HARD_AGES   = list(range(50, 80))   # older → more likely to need extra docs


def generate_claim(task_level="medium"):
    procedure = random.choice(list(PROCEDURE_DATA.keys()))
    data      = PROCEDURE_DATA[procedure]

    correct_code  = random.choice(data["correct_codes"])
    wrong_code    = random.choice(data["wrong_codes"])
    denial_reason = random.choice(data["denial_reasons"])
    policy        = random.choice(POLICIES)

    if task_level == "easy":
        age = random.choice(EASY_AGES)
    elif task_level == "medium":
        age = random.choice(MEDIUM_AGES)
    else:
        age = random.choice(HARD_AGES)

    claim = {
        "procedure":      procedure,
        "submitted_code": wrong_code,
        "correct_code":   correct_code,
        "denial_reason":  denial_reason,
        "patient_age":    age,
        "policy":         policy,
        "documents":      [],
    }

    # Hard mode: MRI always needs preapproval (handled by env/transition_logic)
    if task_level == "hard" and procedure == "MRI Scan":
        claim["denial_reason"] = "Preapproval not obtained"

    return claim

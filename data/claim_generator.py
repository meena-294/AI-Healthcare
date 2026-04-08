import random


def generate_claim(level="medium"):
    procedures = ["X-Ray", "MRI Scan", "Blood Test"]

    procedure = random.choice(procedures)

    correct_codes = {
        "X-Ray": "XRAY200",
        "MRI Scan": "MRI200",
        "Blood Test": "BT200"
    }

    return {
        "patient_age": random.randint(20, 70),
        "procedure": procedure,
        "submitted_code": "WRONG123",
        "correct_code": correct_codes[procedure],
        "denial_reason": "Incorrect procedure code",
        "policy": random.choice(["Basic Plan", "Premium Plan"]),
        "documents": [],
        "preapproval": False,
        "appealed": False
    }
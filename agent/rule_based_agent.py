import os

# ── LLM client via hackathon-injected proxy ──────────────────────────────────
# The validator checks that ALL LLM calls go through the provided LiteLLM proxy.
# Always read credentials from environment variables; never hardcode them.
try:
    from openai import OpenAI as _OpenAI
    _llm = _OpenAI(
        base_url=os.environ.get("API_BASE_URL", ""),
        api_key=os.environ.get("API_KEY", ""),
    )
    LLM_AVAILABLE = True
except Exception:
    _llm = None
    LLM_AVAILABLE = False


def _llm_justify(prompt: str, fallback: str) -> str:
    """Call the LLM proxy to generate a justification string.
    Falls back to `fallback` if the proxy is unavailable."""
    if not LLM_AVAILABLE or not _llm:
        return fallback
    try:
        resp = _llm.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80,
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return fallback


class RuleBasedAgent:

    def act(self, obs):
        try:
            if not obs:
                return {
                    "action_type": "appeal",
                    "justification": _llm_justify(
                        "Provide a one-sentence justification for appealing a healthcare claim when no observation data is available.",
                        "Fallback action due to missing observation"
                    )
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
                justification = _llm_justify(
                    f"Provide a one-sentence justification for correcting a healthcare claim code "
                    f"from '{submitted}' to '{correct}' for procedure '{procedure}' under policy '{policy}'. "
                    f"Denial reason: {denial}.",
                    (
                        f"The submitted code was incorrect for {procedure}. "
                        f"It has been corrected according to policy {policy}. "
                        f"This resolves the denial reason: {denial}."
                    )
                )
                return {
                    "action_type": "correct_code",
                    "new_code": correct,
                    "justification": justification
                }

            # ───────── STEP 2: MRI PREAPPROVAL ─────────
            if procedure == "MRI Scan" and "preapproval" not in docs:
                justification = _llm_justify(
                    "Provide a one-sentence justification for adding a preapproval document for an MRI Scan claim.",
                    "Adding required preapproval for MRI as per policy"
                )
                return {
                    "action_type": "add_document",
                    "justification": justification
                }

            # ───────── STEP 3: SENIOR APPROVAL ─────────
            if age > 60 and "senior_approval" not in docs:
                justification = _llm_justify(
                    f"Provide a one-sentence justification for adding a senior approval document for a patient aged {age}.",
                    "Adding senior approval for patient above 60"
                )
                return {
                    "action_type": "add_document",
                    "justification": justification
                }

            # ───────── STEP 4: APPEAL ─────────
            if "not medically necessary" in denial or "not covered" in denial:
                justification = _llm_justify(
                    f"Provide a one-sentence justification for appealing a healthcare claim denied as: '{denial}'.",
                    "Appealing as procedure is medically necessary and valid"
                )
                return {
                    "action_type": "appeal",
                    "justification": justification
                }

            # ───────── FINAL: NEVER NOOP ─────────
            justification = _llm_justify(
                "Provide a one-sentence justification for submitting a final appeal after all corrections are complete.",
                "All corrections completed, requesting approval"
            )
            return {
                "action_type": "appeal",
                "justification": justification
            }

        except Exception:
            return {
                "action_type": "appeal",
                "justification": "Fallback due to unexpected error"
            }

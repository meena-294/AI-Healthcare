import math

from env.state_manager import StateManager
from env.transition_logic import apply_action
from models.action import ClaimAction

from grader.easy_grader import EasyGrader
from grader.medium_grader import MediumGrader
from grader.hard_grader import HardGrader
from reward.reward_calculator import RewardCalculator


# ✅ STRICT CLAMP — NEVER RETURNS 0.0 OR 1.0
def _strict_clamp(v: float) -> float:
    try:
        v = float(v)
    except Exception:
        return 0.5

    if not math.isfinite(v):
        return 0.5

    # HARD boundary protection
    if v <= 0.0:
        return 0.01
    if v >= 1.0:
        return 0.99

    # Extra safety buffer
    return max(0.01, min(0.99, v))


class HealthcareEnv:

    def __init__(self, max_steps=10):
        self.state_manager = StateManager()
        self.done          = False
        self.max_steps     = max_steps
        self.task_level    = "medium"

    # ── RESET ────────────────────────────────────────────────────────────────
    def reset(self, task_level="medium"):
        claim           = self.state_manager.reset(task_level)
        self.done       = False
        self.task_level = task_level
        return self._get_observation(claim)

    # ── STEP ─────────────────────────────────────────────────────────────────
    def step(self, action: ClaimAction):
        if self.done:
            return (
                self._get_observation(self.state_manager.get_state()),
                0.01,  # NEVER return 0.0
                True,
                {"message": "Episode already completed"},
            )

        claim, result = apply_action(self.state_manager, action)
        self.state_manager.update(claim)

        reward    = self._calculate_reward_with_grader(claim, action, result)
        self.done = self._check_done(claim)

        if self.done:
            claim["denial_reason"] = "None (Resolved)"

        return self._get_observation(claim), reward, self.done, {
            "action_result": result,
            "step_count":    self.state_manager.step_count,
        }

    # ── REWARD ────────────────────────────────────────────────────────────────
    def _calculate_reward_with_grader(self, claim, action, result) -> float:

        # ❌ Invalid action → small epsilon (NOT 0 or negative)
        if not result.get("valid", True):
            return 0.01

        # Select correct grader
        if self.task_level == "easy":
            grader = EasyGrader(claim)
        elif self.task_level == "medium":
            grader = MediumGrader(claim)
        else:
            grader = HardGrader(claim)

        # Already safe (0.01–0.99)
        grader_score = grader.grade(action)

        reward_calc = RewardCalculator(claim)
        reward = reward_calc.compute(
            action       = action,
            grader_score = grader_score,
            step_count   = self.state_manager.step_count,
            max_steps    = self.max_steps,
        )

        # ✅ FINAL GUARANTEE — NOTHING ESCAPES THIS
        return _strict_clamp(reward)

    # ── DONE CONDITION ───────────────────────────────────────────────────────
    def _check_done(self, claim) -> bool:
        if claim.get("submitted_code") != claim.get("correct_code"):
            return False

        if claim.get("procedure") == "MRI Scan":
            if "preapproval" not in claim.get("documents", []):
                return False

        return True

    # ── OBSERVATION ──────────────────────────────────────────────────────────
    def _get_observation(self, state) -> dict:
        return {
            "claim_id":       state.get("claim_id"),
            "patient_age":    state.get("patient_age"),
            "procedure":      state.get("procedure"),
            "submitted_code": state.get("submitted_code"),
            "correct_code":   state.get("correct_code"),
            "denial_reason":  state.get("denial_reason"),
            "policy":         state.get("policy"),
            "documents":      state.get("documents", []),
        }

    # ── STATE ────────────────────────────────────────────────────────────────
    def state(self) -> dict:
        return self.state_manager.get_state() or {"status": "running"}

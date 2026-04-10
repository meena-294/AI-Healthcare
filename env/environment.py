from env.state_manager import StateManager
from env.transition_logic import apply_action
from models.action import ClaimAction

from grader.easy_grader import EasyGrader
from grader.medium_grader import MediumGrader
from grader.hard_grader import HardGrader
from reward.reward_calculator import RewardCalculator

# Reward must NEVER be exactly 0.0 or 1.0 — use wide safe margins
_FLOOR   = 0.05
_CEILING = 0.95


def _strict_clamp(value: float) -> float:
    """Triple-safety clamp: floor=0.05, ceiling=0.95. Impossible to return 0.0 or 1.0."""
    return max(_FLOOR, min(float(value), _CEILING))


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
                _FLOOR,   # episode already done → safe floor, never 0.0
                True,
                {"message": "Episode already completed"},
            )

        claim, result = apply_action(self.state_manager, action)
        self.state_manager.update(claim)

        reward    = self._calculate_reward_with_grader(claim, action, result)
        self.done = self._check_done(claim)

        if self.done:
            claim["denial_reason"] = "None (Resolved)"

        observation = self._get_observation(claim)

        return observation, reward, self.done, {
            "action_result": result,
            "step_count":    self.state_manager.step_count,
        }

    # ── REWARD ────────────────────────────────────────────────────────────────
    def _calculate_reward_with_grader(self, claim, action, result) -> float:

        # Invalid action → safe floor (never 0.0)
        if not result.get("valid", True):
            return _FLOOR

        # Select grader
        if self.task_level == "easy":
            grader = EasyGrader(claim)
        elif self.task_level == "medium":
            grader = MediumGrader(claim)
        else:
            grader = HardGrader(claim)

        # grader.grade() already returns value in [0.05, 0.95]
        grader_score = grader.grade(action)

        reward_calc = RewardCalculator(claim)
        reward = reward_calc.compute(
            action       = action,
            grader_score = grader_score,
            step_count   = self.state_manager.step_count,
            max_steps    = self.max_steps,
        )

        # Final clamp — belt, suspenders, AND safety pin
        return _strict_clamp(reward)

    # ── DONE ─────────────────────────────────────────────────────────────────
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

    # ── STATE (OpenEnv) ──────────────────────────────────────────────────────
    def state(self) -> dict:
        return self.state_manager.get_state() or {"status": "running"}

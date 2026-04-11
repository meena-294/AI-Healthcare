import math
from env.state_manager import StateManager
from env.transition_logic import apply_action
from models.action import ClaimAction

from grader.easy_grader import EasyGrader
from grader.medium_grader import MediumGrader
from grader.hard_grader import HardGrader
from reward.reward_calculator import RewardCalculator

_FLOOR   = 0.15
_CEILING = 0.85


def _clamp(value: float) -> float:
    try:
        v = float(value)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    return max(_FLOOR, min(v, _CEILING))


class HealthcareEnv:

    def __init__(self, max_steps=10):
        self.state_manager = StateManager()
        self.done          = False
        self.max_steps     = max_steps
        self.task_level    = "easy"

    def reset(self, task_level="easy"):
        if task_level not in ("easy", "medium", "hard"):
            task_level = "easy"
        claim           = self.state_manager.reset(task_level)
        self.done       = False
        self.task_level = task_level
        return self._get_observation(claim)

    def step(self, action: ClaimAction):
        # Guard: if state is None (reset was never called), auto-reset
        if self.state_manager.current_claim is None:
            self.reset(self.task_level)

        if self.done:
            return (
                self._get_observation(self.state_manager.get_state()),
                _FLOOR,
                True,
                {"message": "Episode already completed"},
            )

        try:
            claim, result = apply_action(self.state_manager, action)
        except Exception:
            claim  = self.state_manager.get_state() or {}
            result = {"valid": False, "message": "apply_action failed"}

        self.state_manager.update(claim)

        reward    = self._compute_reward(claim, action, result)
        self.done = self._check_done(claim)

        if self.done:
            claim["denial_reason"] = "None (Resolved)"

        return self._get_observation(claim), reward, self.done, {
            "action_result": result,
            "step_count":    self.state_manager.step_count,
        }

    def _compute_reward(self, claim, action, result) -> float:
        try:
            if not result.get("valid", True):
                return _FLOOR

            grader_map = {"easy": EasyGrader, "medium": MediumGrader}
            grader_cls = grader_map.get(self.task_level, HardGrader)
            grader_score = _clamp(grader_cls(claim).grade(action))

            reward = RewardCalculator(claim).compute(
                action       = action,
                grader_score = grader_score,
                step_count   = self.state_manager.step_count,
                max_steps    = self.max_steps,
            )
            return _clamp(reward)
        except Exception:
            return _FLOOR

    def _check_done(self, claim) -> bool:
        try:
            if claim.get("submitted_code") != claim.get("correct_code"):
                return False
            if claim.get("procedure") == "MRI Scan":
                if "preapproval" not in claim.get("documents", []):
                    return False
            return True
        except Exception:
            return False

    def _get_observation(self, state) -> dict:
        if not state:
            state = {}
        return {
            "claim_id":       state.get("claim_id", "unknown"),
            "patient_age":    state.get("patient_age", 30),
            "procedure":      state.get("procedure", "X-Ray"),
            "submitted_code": state.get("submitted_code", ""),
            "correct_code":   state.get("correct_code", ""),
            "denial_reason":  state.get("denial_reason", ""),
            "policy":         state.get("policy", "Standard"),
            "documents":      state.get("documents", []),
        }

    def state(self) -> dict:
        try:
            return self.state_manager.get_state() or {"status": "running"}
        except Exception:
            return {"status": "running"}

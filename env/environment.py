from env.state_manager import StateManager
from env.transition_logic import apply_action
from models.action import ClaimAction

# ✅ NEW IMPORTS
from grader.easy_grader import EasyGrader
from grader.medium_grader import MediumGrader
from grader.hard_grader import HardGrader
from reward.reward_calculator import RewardCalculator


class HealthcareEnv:

    def __init__(self, max_steps=10):
        self.state_manager = StateManager()
        self.done = False
        self.max_steps = max_steps
        self.task_level = "medium"   # default

    # ---------------- RESET ---------------- #
    def reset(self, task_level="medium"):
        claim = self.state_manager.reset(task_level)
        self.done = False
        self.task_level = task_level  # ✅ store task level
        return self._get_observation(claim)

    # ---------------- STEP ---------------- #
    def step(self, action: ClaimAction):
        if self.done:
            return self._get_observation(self.state_manager.get_state()), 0.0, True, {
                "message": "Episode already completed"
            }

        # Apply action
        claim, result = apply_action(self.state_manager, action)

        # Update state
        self.state_manager.update(claim)

        # 🔥 NEW REWARD SYSTEM
        reward = self._calculate_reward_with_grader(claim, action, result)

        # Check done
        self.done = self._check_done(claim)

        # Clean final state
        if self.done:
            claim["denial_reason"] = "None (Resolved)"

        observation = self._get_observation(claim)

        return observation, reward, self.done, {
            "action_result": result,
            "step_count": self.state_manager.step_count
        }

    # ---------------- NEW REWARD SYSTEM ---------------- #
    def _calculate_reward_with_grader(self, claim, action, result):

        # ❌ Invalid action → strong penalty
        if not result.get("valid", True):
            return -1.0

        # 🔹 Select grader based on task
        if self.task_level == "easy":
            grader = EasyGrader(claim)
        elif self.task_level == "medium":
            grader = MediumGrader(claim)
        else:
            grader = HardGrader(claim)

        # 🔹 Get grader score (0 to 1)
        grader_score = grader.grade(action)

        # 🔹 Compute reward using RewardCalculator
        reward_calc = RewardCalculator(claim)

        reward = reward_calc.compute(
            action=action,
            grader_score=grader_score,
            step_count=self.state_manager.step_count,
            max_steps=self.max_steps
        )

        # 🔹 BONUS: small boost if fully done
        if self._check_done(claim):
            reward += 0.05

        # Clamp reward between -1 and 1
        return max(min(reward, 1.0), -1.0)

    # ---------------- DONE CONDITION ---------------- #
    def _check_done(self, claim):

    # Must fix code first
        if claim.get("submitted_code") != claim.get("correct_code"):
            return False

        # 🔥 HARD condition (MRI needs document)
        if claim.get("procedure") == "MRI Scan":
            if "preapproval" not in claim.get("documents", []):
                return False

        return True
    # ---------------- OBSERVATION ---------------- #
    def _get_observation(self, state):
        return {
            "claim_id": state.get("claim_id"),
            "patient_age": state.get("patient_age"),
            "procedure": state.get("procedure"),
            "submitted_code": state.get("submitted_code"),
            "denial_reason": state.get("denial_reason"),
            "policy": state.get("policy"),
            "documents": state.get("documents", [])
        }
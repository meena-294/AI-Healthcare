import random

class RLAgent:
    def __init__(self):
        self.q_table = {}

        self.actions = [
            {"action_type": "correct_code"},
            {"action_type": "add_document"},
            {"action_type": "noop"}
        ]

        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.2

    def get_state(self, obs):
        return (
            obs.get("procedure"),
            obs.get("denial_reason")
        )

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        return self.best_action(state)

    def best_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0] * len(self.actions)

        return self.actions[self.q_table[state].index(max(self.q_table[state]))]

    def update(self, state, action_idx, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = [0] * len(self.actions)

        if next_state not in self.q_table:
            self.q_table[next_state] = [0] * len(self.actions)

        best_next = max(self.q_table[next_state])

        self.q_table[state][action_idx] += self.alpha * (
            reward + self.gamma * best_next - self.q_table[state][action_idx]
        )
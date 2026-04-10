import gradio as gr
from env.environment import HealthcareEnv
from models.action import ClaimAction
from agent.rule_based_agent import RuleBasedAgent


# ✅ STEP FORMATTER (CLEAN + PROFESSIONAL)
def format_step(step, obs, action, reward, done, show_header=False):
    output = ""

    # Show claim info ONLY once
    if show_header:
        output += f"""
🧾 Claim ID: {obs['claim_id']}
👤 Age: {obs['patient_age']}
🏥 Procedure: {obs['procedure']}
📜 Policy: {obs['policy']}
--------------------------------------
"""

    output += f"""
🔹 Step {step}
➡ Action: {action['action_type'].replace('_', ' ').title()}
"""

    if "new_code" in action:
        output += f" → {action['new_code']}\n"

    output += f"💰 Reward: {reward}\n"

    # ✅ REALISTIC REASONING RULES
    if obs["procedure"] == "MRI Scan" and reward == 0.5:
        output += "💡 Reason: MRI requires preapproval\n"

    if obs["patient_age"] > 60 and reward == 0.5:
        output += "💡 Reason: Senior citizen requires additional approval\n"

    if obs["policy"] == "Basic Plan" and reward == 0.5:
        output += "💡 Reason: Basic plan has limited coverage\n"

    output += f"📌 Status: {'Completed ✅' if done else 'In Progress'}\n"
    output += "--------------------------------------\n"

    return output


# ✅ MAIN SIMULATION
def run_simulation(task_level):
    env = HealthcareEnv()
    agent = RuleBasedAgent()

    obs = env.reset(task_level)
    done = False

    log = ""
    step = 1
    max_steps = 10
    total_reward = 0

    while not done and step <= max_steps:
        action_dict = agent.act(obs)
        action = ClaimAction(**action_dict)

        obs, reward, done, info = env.step(action)

        # Show header only in first step
        log += format_step(step, obs, action_dict, reward, done, show_header=(step == 1))

        total_reward += reward
        step += 1

    # ✅ FINAL SUMMARY (PRO LEVEL)
    status = "APPROVED ✅" if total_reward > 0 else "REJECTED ❌"

    log += f"""
==============================
🏁 FINAL DECISION
📌 Claim Status: {status}
🏆 Total Reward: {round(total_reward, 2)}
🔁 Steps Taken: {step - 1}
💡 Insight:
Efficient claim processing with minimal steps improves approval success.
==============================
"""

    return log


# ✅ UI (GRADIO)
with gr.Blocks() as demo:
    gr.Markdown("## 🏥 AI-Powered Insurance Claim Decision System")
    gr.Markdown("Simulates multi-step insurance claim processing with intelligent decision-making")

    task = gr.Dropdown(
        ["easy", "medium", "hard"],
        value="easy",
        label="Select Task Level"
    )

    output = gr.Textbox(lines=25, label="Agent Output")

    btn = gr.Button("Run Agent 🚀")
    btn.click(fn=run_simulation, inputs=task, outputs=output)

demo.launch()

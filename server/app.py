"""
Unified server: FastAPI (OpenEnv API) + Gradio UI
Both run on port 7860 — required for HuggingFace Spaces.

Routes:
  GET  /          → Gradio UI
  POST /reset     → OpenEnv reset
  POST /step      → OpenEnv step
  POST /state     → OpenEnv state
  GET  /health    → health check
  GET  /docs      → Swagger UI
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import gradio as gr

from env.environment import HealthcareEnv
from models.action import ClaimAction
from agent.rule_based_agent import RuleBasedAgent

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(title="AI HealthCare Claims API")

env   = HealthcareEnv()
agent = RuleBasedAgent()


# ── Request models ────────────────────────────────────────────────────────────
class StepRequest(BaseModel):
    action: dict


# ── OpenEnv endpoints ─────────────────────────────────────────────────────────
@app.post("/reset")
async def reset(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    difficulty = body.get("difficulty") or body.get("task_level") or "easy"
    obs = env.reset(difficulty)
    return obs


@app.post("/step")
def step(req: StepRequest):
    action = ClaimAction(**req.action)
    obs, reward, done, info = env.step(action)
    return {"observation": obs, "reward": reward, "done": done, "info": info}


@app.post("/state")
def state():
    return env.state() if hasattr(env, "state") else {"status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ── Gradio helpers ────────────────────────────────────────────────────────────
def reward_class(r):
    if r > 0:  return "reward-pos", f"+{round(r,3)}"
    if r < 0:  return "reward-neg", str(round(r,3))
    return "reward-neu", "0.0"


def build_claim_html(obs):
    claim_id  = (obs.get("claim_id") or "")[:18] + "…"
    procedure = obs.get("procedure", "N/A")
    age       = obs.get("patient_age", "N/A")
    policy    = obs.get("policy", "N/A")
    code      = obs.get("submitted_code", "N/A")
    denial    = obs.get("denial_reason", "N/A")
    docs      = ", ".join(obs.get("documents", [])) or "None"
    return f"""
<div class="panel">
  <div class="panel-title">📋 Claim Details</div>
  <div class="claim-grid">
    <div class="claim-field"><div class="field-label">Claim ID</div>
      <div class="field-value" style="font-family:Space Mono,monospace;font-size:.8rem;color:#00c2ff">{claim_id}</div></div>
    <div class="claim-field"><div class="field-label">Procedure</div>
      <div class="field-value">🏥 {procedure}</div></div>
    <div class="claim-field"><div class="field-label">Patient Age</div>
      <div class="field-value">👤 {age} yrs</div></div>
    <div class="claim-field"><div class="field-label">Policy</div>
      <div class="field-value">📜 {policy}</div></div>
    <div class="claim-field"><div class="field-label">Submitted Code</div>
      <div class="field-value" style="font-family:Space Mono,monospace;color:#ffb800">{code}</div></div>
    <div class="claim-field"><div class="field-label">Denial Reason</div>
      <div class="field-value" style="color:#ff4d6a;font-size:.85rem">{denial}</div></div>
    <div class="claim-field" style="grid-column:span 2"><div class="field-label">Documents</div>
      <div class="field-value" style="font-size:.85rem">{docs}</div></div>
  </div>
</div>"""


def build_step_html(num, action_dict, reward):
    action_type = action_dict.get("action_type", "noop").replace("_", " ").title()
    new_code    = action_dict.get("new_code", "")
    just        = action_dict.get("justification", "")
    rc, rv      = reward_class(reward)
    parts = []
    if new_code: parts.append(f"New code: <span style='font-family:Space Mono,monospace;color:#ffb800'>{new_code}</span>")
    if just:     parts.append(f"<em>{just[:80]}</em>")
    detail = " &nbsp;·&nbsp; ".join(parts) or "&nbsp;"
    return f"""
<div class="step-item">
  <div class="step-num">{num:02d}</div>
  <div class="step-body">
    <div class="step-action">{action_type}</div>
    <div class="step-detail">{detail}</div>
  </div>
  <span class="reward-badge {rc}">{rv}</span>
</div>"""


SHARED_STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
.metric-row{display:flex;gap:16px;margin-bottom:20px}
.metric-card{flex:1;background:#0d1b2e;border:1px solid #1a3050;border-radius:14px;padding:20px 24px}
.metric-card .label{font-size:.68rem;letter-spacing:1.5px;text-transform:uppercase;color:#5a7a9a;margin-bottom:8px;font-family:Space Mono,monospace}
.metric-card .value{font-family:Space Mono,monospace;font-size:1.5rem;font-weight:700;color:#00c2ff}
.metric-card .value.green{color:#00ffa3}.metric-card .value.amber{color:#ffb800}
.panel{background:#0d1b2e;border:1px solid #1a3050;border-radius:16px;padding:24px 28px;margin-bottom:16px}
.panel-title{font-family:Space Mono,monospace;font-size:.75rem;letter-spacing:2px;text-transform:uppercase;color:#00c2ff;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #1a3050}
.claim-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.claim-field{background:#0a1628;border:1px solid #1a3050;border-radius:10px;padding:12px 16px}
.field-label{font-size:.66rem;letter-spacing:1.2px;text-transform:uppercase;color:#5a7a9a;margin-bottom:4px;font-family:Space Mono,monospace}
.field-value{font-size:.92rem;font-weight:500;color:#e8f4ff}
.step-item{display:flex;gap:14px;align-items:flex-start;padding:14px 0;border-bottom:1px solid #1a3050}
.step-item:last-child{border-bottom:none}
.step-num{width:32px;height:32px;border-radius:50%;background:rgba(0,194,255,.1);border:1px solid #00c2ff;display:flex;align-items:center;justify-content:center;font-family:Space Mono,monospace;font-size:.72rem;color:#00c2ff;flex-shrink:0}
.step-body{flex:1}.step-action{font-weight:600;font-size:.9rem;color:#e8f4ff;margin-bottom:3px}
.step-detail{font-size:.78rem;color:#5a7a9a}
.reward-badge{font-family:Space Mono,monospace;font-size:.75rem;font-weight:700;padding:3px 10px;border-radius:20px;margin-left:auto;flex-shrink:0}
.reward-pos{background:rgba(0,255,163,.1);color:#00ffa3;border:1px solid rgba(0,255,163,.3)}
.reward-neg{background:rgba(255,77,106,.1);color:#ff4d6a;border:1px solid rgba(255,77,106,.3)}
.reward-neu{background:rgba(255,184,0,.1);color:#ffb800;border:1px solid rgba(255,184,0,.3)}
.verdict{border-radius:14px;padding:22px 28px;display:flex;align-items:center;gap:20px}
.verdict.approved{background:rgba(0,255,163,.06);border:1px solid rgba(0,255,163,.3)}
.verdict.rejected{background:rgba(255,77,106,.06);border:1px solid rgba(255,77,106,.3)}
.verdict-icon{font-size:2rem}
.verdict-title{font-family:Space Mono,monospace;font-size:1rem;font-weight:700}
.verdict-title.approved{color:#00ffa3}.verdict-title.rejected{color:#ff4d6a}
.verdict-stats{font-size:.8rem;color:#5a7a9a;margin-top:4px}
</style>"""


def run_simulation(task_level):
    sim_env = HealthcareEnv()
    sim_agent = RuleBasedAgent()

    obs          = sim_env.reset(task_level)
    first_obs    = obs.copy()
    done         = False
    step         = 1
    total_reward = 0.0
    steps_html   = ""

    while not done and step <= 10:
        action_dict = sim_agent.act(obs)
        action      = ClaimAction(**action_dict)
        obs, reward, done, _ = sim_env.step(action)
        steps_html  += build_step_html(step, action_dict, reward)
        total_reward += reward
        step += 1

    steps_taken = step - 1
    approved    = total_reward > 0
    eff         = max(0, round((10 - steps_taken) / 10 * 100))
    cls         = "approved" if approved else "rejected"
    label       = "CLAIM APPROVED" if approved else "CLAIM REJECTED"
    icon        = "✅" if approved else "❌"
    score_color = "green" if approved else ""

    metrics = f"""
<div class="metric-row">
  <div class="metric-card"><div class="label">Final Score</div>
    <div class="value {score_color}" style="{'color:#ff4d6a' if not approved else ''}">{round(total_reward,3)}</div></div>
  <div class="metric-card"><div class="label">Steps Taken</div>
    <div class="value amber">{steps_taken}</div></div>
  <div class="metric-card"><div class="label">Efficiency</div>
    <div class="value">{eff}%</div></div>
  <div class="metric-card"><div class="label">Decision</div>
    <div class="value {score_color}" style="{'color:#ff4d6a' if not approved else ''}">{'APPROVE' if approved else 'REJECT'}</div></div>
</div>"""

    verdict = f"""
<div class="verdict {cls}">
  <div class="verdict-icon">{icon}</div>
  <div>
    <div class="verdict-title {cls}">{label}</div>
    <div class="verdict-stats">
      Total Reward: <strong style="color:#e8f4ff">{round(total_reward,3)}</strong>
      &nbsp;·&nbsp; Steps: <strong style="color:#e8f4ff">{steps_taken}</strong>
      &nbsp;·&nbsp; Difficulty: <strong style="color:#e8f4ff">{task_level.upper()}</strong>
    </div>
  </div>
</div>"""

    return SHARED_STYLES + metrics + build_claim_html(first_obs) + f"""
<div class="panel"><div class="panel-title">⚡ Agent Steps</div>{steps_html}</div>""" + verdict


# ── Gradio UI ─────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
:root{--bg:#060d1a;--card:#0d1b2e;--card2:#0a1628;--blue:#00c2ff;--green:#00ffa3;--amber:#ffb800;--red:#ff4d6a;--text:#e8f4ff;--muted:#5a7a9a;--border:#1a3050}
body,.gradio-container{background:var(--bg)!important;font-family:'DM Sans',sans-serif!important;color:var(--text)!important}
#hero{background:linear-gradient(135deg,#060d1a,#0a1e35 60%,#0d2840);border-bottom:1px solid var(--border);padding:32px 48px 24px;position:relative;overflow:hidden}
#hero::before{content:'';position:absolute;top:-80px;right:-80px;width:320px;height:320px;background:radial-gradient(circle,rgba(0,194,255,.08),transparent 70%);pointer-events:none}
#hero-title{font-family:'Space Mono',monospace!important;font-size:1.9rem!important;font-weight:700!important;color:var(--blue)!important;text-shadow:0 0 32px rgba(0,194,255,.4);margin:0 0 6px!important}
#hero-sub{font-size:.9rem!important;color:var(--muted)!important;margin:0!important;letter-spacing:.5px}
#task-dropdown label{font-family:'Space Mono',monospace!important;font-size:.72rem!important;letter-spacing:1.5px!important;text-transform:uppercase!important;color:var(--blue)!important}
#task-dropdown select,#task-dropdown input{background:var(--card2)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:10px!important;padding:10px 14px!important}
#run-btn{background:linear-gradient(135deg,#0088cc,#00c2ff)!important;border:none!important;border-radius:12px!important;font-family:'Space Mono',monospace!important;font-weight:700!important;font-size:.85rem!important;letter-spacing:1px!important;color:#000!important;padding:14px 28px!important;box-shadow:0 4px 20px rgba(0,194,255,.25)!important;width:100%!important;transition:all .3s!important}
#run-btn:hover{transform:translateY(-2px)!important;box-shadow:0 8px 30px rgba(0,194,255,.4)!important}
#output-box,#output-box>div{background:transparent!important;border:none!important;padding:0!important}
"""

with gr.Blocks(css=CUSTOM_CSS, title="AI HealthCare Claims") as gradio_ui:
    gr.HTML("""
    <div id="hero">
      <div id="hero-title">🏥 AI HEALTHCARE CLAIMS</div>
      <div id="hero-sub">Reinforcement Learning · Insurance Claim Decision Engine · OpenEnv Compatible</div>
    </div>""")

    with gr.Row():
        with gr.Column(scale=1, min_width=260):
            gr.HTML("""<div style="background:#0d1b2e;border:1px solid #1a3050;border-radius:16px;padding:20px 24px;margin-top:20px">
              <div style="font-family:Space Mono,monospace;font-size:.75rem;letter-spacing:2px;text-transform:uppercase;color:#00c2ff;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #1a3050">⚙ Configuration</div>
            </div>""")
            task = gr.Dropdown(choices=["easy","medium","hard"], value="easy",
                               label="Task Difficulty", elem_id="task-dropdown")
            run_btn = gr.Button("▶ RUN AGENT", elem_id="run-btn")
            gr.HTML("""
            <div style="background:#0d1b2e;border:1px solid #1a3050;border-radius:16px;padding:20px 24px;margin-top:16px">
              <div style="font-family:Space Mono,monospace;font-size:.75rem;letter-spacing:2px;text-transform:uppercase;color:#00c2ff;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #1a3050">📖 Task Levels</div>
              <div style="font-size:.82rem;line-height:1.8;color:#5a7a9a">
                <div style="margin-bottom:10px"><span style="color:#00ffa3;font-family:Space Mono,monospace;font-size:.72rem">EASY</span><br>Fix incorrect procedure code</div>
                <div style="margin-bottom:10px"><span style="color:#ffb800;font-family:Space Mono,monospace;font-size:.72rem">MEDIUM</span><br>Fix code + provide justification</div>
                <div><span style="color:#ff4d6a;font-family:Space Mono,monospace;font-size:.72rem">HARD</span><br>Fix code + policy + preapproval docs</div>
              </div>
            </div>
            <div style="background:#0d1b2e;border:1px solid #1a3050;border-radius:16px;padding:20px 24px;margin-top:16px">
              <div style="font-family:Space Mono,monospace;font-size:.75rem;letter-spacing:2px;text-transform:uppercase;color:#00c2ff;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #1a3050">🤖 Agent Info</div>
              <div style="font-size:.8rem;color:#5a7a9a;line-height:1.9">
                <div>● Rule-Based Agent</div>
                <div>● Max Steps: 10</div>
                <div>● Reward: −1.0 → +1.0</div>
                <div>● API: /reset /step /state</div>
              </div>
            </div>""")

        with gr.Column(scale=3):
            gr.HTML("<div style='height:20px'></div>")
            output = gr.HTML(
                value="""<div style="background:#0d1b2e;border:1px solid #1a3050;border-radius:16px;padding:60px 40px;text-align:center">
                  <div style="font-size:3rem;margin-bottom:16px">🏥</div>
                  <div style="font-family:Space Mono,monospace;font-size:.85rem;color:#5a7a9a;letter-spacing:2px">SELECT A DIFFICULTY AND CLICK RUN AGENT</div>
                </div>""",
                elem_id="output-box")

    run_btn.click(fn=run_simulation, inputs=task, outputs=output)


# ── Mount Gradio into FastAPI ─────────────────────────────────────────────────
# This is the KEY fix: both Gradio UI AND FastAPI routes live on port 7860
app = gr.mount_gradio_app(app, gradio_ui, path="/")


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()

import gradio as gr
from env.environment import HealthcareEnv
from models.action import ClaimAction
from agent.rule_based_agent import RuleBasedAgent

# ── Custom CSS ───────────────────────────────────────────────────────────────
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
:root {
    --bg-primary:    #060d1a;
    --bg-card:       #0d1b2e;
    --bg-card2:      #0a1628;
    --accent-blue:   #00c2ff;
    --accent-green:  #00ffa3;
    --accent-amber:  #ffb800;
    --accent-red:    #ff4d6a;
    --text-primary:  #e8f4ff;
    --text-muted:    #5a7a9a;
    --border:        #1a3050;
    --glow-blue:     0 0 24px rgba(0,194,255,0.18);
    --glow-green:    0 0 24px rgba(0,255,163,0.18);
}
/* ── Page shell ── */
body, .gradio-container {
    background: var(--bg-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
}
/* ── Hero header ── */
#hero {
    background: linear-gradient(135deg, #060d1a 0%, #0a1e35 60%, #0d2840 100%);
    border-bottom: 1px solid var(--border);
    padding: 36px 48px 28px;
    position: relative;
    overflow: hidden;
}
#hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(0,194,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
#hero-title {
    font-family: 'Space Mono', monospace !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--accent-blue) !important;
    letter-spacing: -0.5px;
    margin: 0 0 6px !important;
    text-shadow: 0 0 32px rgba(0,194,255,0.4);
}
#hero-sub {
    font-size: 0.95rem !important;
    color: var(--text-muted) !important;
    margin: 0 !important;
    letter-spacing: 0.5px;
}
/* ── Metric cards row ── */
.metric-row { display: flex; gap: 16px; margin-bottom: 0; }
.metric-card {
    flex: 1;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.metric-card:hover { border-color: var(--accent-blue); box-shadow: var(--glow-blue); }
.metric-card .label {
    font-size: 0.72rem; letter-spacing: 1.5px; text-transform: uppercase;
    color: var(--text-muted); margin-bottom: 8px; font-family: 'Space Mono', monospace;
}
.metric-card .value {
    font-family: 'Space Mono', monospace; font-size: 1.6rem; font-weight: 700;
    color: var(--accent-blue);
}
.metric-card .value.green { color: var(--accent-green); }
.metric-card .value.amber { color: var(--accent-amber); }
/* ── Panel containers ── */
.panel {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 28px;
}
.panel-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent-blue);
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}
/* ── Claim info grid ── */
.claim-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.claim-field {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
}
.claim-field .field-label {
    font-size: 0.68rem; letter-spacing: 1.2px; text-transform: uppercase;
    color: var(--text-muted); margin-bottom: 4px; font-family: 'Space Mono', monospace;
}
.claim-field .field-value { font-size: 0.95rem; font-weight: 500; color: var(--text-primary); }
/* ── Step feed ── */
.step-item {
    display: flex; gap: 14px; align-items: flex-start;
    padding: 14px 0; border-bottom: 1px solid var(--border);
    animation: fadeSlide 0.4s ease;
}
.step-item:last-child { border-bottom: none; }
@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.step-num {
    width: 32px; height: 32px; border-radius: 50%;
    background: rgba(0,194,255,0.12); border: 1px solid var(--accent-blue);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Space Mono', monospace; font-size: 0.75rem;
    color: var(--accent-blue); flex-shrink: 0;
}
.step-body { flex: 1; }
.step-action { font-weight: 600; font-size: 0.92rem; color: var(--text-primary); margin-bottom: 3px; }
.step-detail { font-size: 0.8rem; color: var(--text-muted); }
.reward-badge {
    font-family: 'Space Mono', monospace; font-size: 0.78rem; font-weight: 700;
    padding: 3px 10px; border-radius: 20px; margin-left: auto; flex-shrink: 0;
}
.reward-pos { background: rgba(0,255,163,0.12); color: var(--accent-green); border: 1px solid rgba(0,255,163,0.3); }
.reward-neg { background: rgba(255,77,106,0.12); color: var(--accent-red); border: 1px solid rgba(255,77,106,0.3); }
.reward-neu { background: rgba(255,184,0,0.12); color: var(--accent-amber); border: 1px solid rgba(255,184,0,0.3); }
/* ── Verdict banner ── */
.verdict {
    border-radius: 14px; padding: 22px 28px; margin-top: 4px;
    display: flex; align-items: center; gap: 20px;
}
.verdict.approved { background: rgba(0,255,163,0.07); border: 1px solid rgba(0,255,163,0.3); }
.verdict.rejected { background: rgba(255,77,106,0.07); border: 1px solid rgba(255,77,106,0.3); }
.verdict-icon { font-size: 2.2rem; }
.verdict-title { font-family: 'Space Mono', monospace; font-size: 1.1rem; font-weight: 700; }
.verdict-title.approved { color: var(--accent-green); }
.verdict-title.rejected { color: var(--accent-red); }
.verdict-stats { font-size: 0.82rem; color: var(--text-muted); margin-top: 4px; }
/* ── Controls ── */
#task-dropdown label { font-family: 'Space Mono', monospace !important; font-size: 0.72rem !important;
    letter-spacing: 1.5px !important; text-transform: uppercase !important; color: var(--accent-blue) !important; }
#task-dropdown select, #task-dropdown input {
    background: var(--bg-card2) !important; border: 1px solid var(--border) !important;
    color: var(--text-primary) !important; border-radius: 10px !important; font-size: 0.92rem !important;
    padding: 10px 14px !important;
}
#task-dropdown select:focus, #task-dropdown input:focus {
    border-color: var(--accent-blue) !important; box-shadow: var(--glow-blue) !important; outline: none !important;
}
#run-btn {
    background: linear-gradient(135deg, #0088cc, #00c2ff) !important;
    border: none !important; border-radius: 12px !important;
    font-family: 'Space Mono', monospace !important; font-weight: 700 !important;
    font-size: 0.85rem !important; letter-spacing: 1px !important;
    color: #000 !important; padding: 14px 28px !important;
    transition: all 0.3s !important; cursor: pointer !important;
    box-shadow: 0 4px 20px rgba(0,194,255,0.25) !important;
    width: 100% !important;
}
#run-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0,194,255,0.4) !important;
}
/* ── Output HTML box ── */
#output-box, #output-box > div {
    background: transparent !important; border: none !important;
    padding: 0 !important;
}
#output-box .prose { max-width: 100% !important; }
/* ── Status dots ── */
.status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 6px; }
.dot-green { background: var(--accent-green); box-shadow: 0 0 8px var(--accent-green); }
.dot-amber { background: var(--accent-amber); box-shadow: 0 0 8px var(--accent-amber); }
.dot-blue  { background: var(--accent-blue);  box-shadow: 0 0 8px var(--accent-blue);  }
/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
"""

# ── HTML Builders ─────────────────────────────────────────────────────────────

def build_claim_html(obs):
    denial = obs.get("denial_reason", "N/A")
    policy = obs.get("policy", "N/A")
    procedure = obs.get("procedure", "N/A")
    age = obs.get("patient_age", "N/A")
    claim_id = obs.get("claim_id", "N/A")
    code = obs.get("submitted_code", "N/A")
    docs = obs.get("documents", [])
    docs_str = ", ".join(docs) if docs else "None"

    return f"""
<div class="panel">
  <div class="panel-title">📋 Claim Details</div>
  <div class="claim-grid">
    <div class="claim-field">
      <div class="field-label">Claim ID</div>
      <div class="field-value" style="font-family:'Space Mono',monospace;font-size:0.8rem;color:#00c2ff">{claim_id[:18]}…</div>
    </div>
    <div class="claim-field">
      <div class="field-label">Procedure</div>
      <div class="field-value">🏥 {procedure}</div>
    </div>
    <div class="claim-field">
      <div class="field-label">Patient Age</div>
      <div class="field-value">👤 {age} yrs</div>
    </div>
    <div class="claim-field">
      <div class="field-label">Policy</div>
      <div class="field-value">📜 {policy}</div>
    </div>
    <div class="claim-field">
      <div class="field-label">Submitted Code</div>
      <div class="field-value" style="font-family:'Space Mono',monospace;color:#ffb800">{code}</div>
    </div>
    <div class="claim-field">
      <div class="field-label">Denial Reason</div>
      <div class="field-value" style="color:#ff4d6a;font-size:0.85rem">{denial}</div>
    </div>
    <div class="claim-field" style="grid-column:span 2">
      <div class="field-label">Documents</div>
      <div class="field-value" style="font-size:0.85rem">{docs_str}</div>
    </div>
  </div>
</div>
"""

def reward_class(r):
    if r > 0:   return "reward-pos", f"+{round(r,3)}"
    if r < 0:   return "reward-neg", str(round(r,3))
    return "reward-neu", "0.0"

def build_step_html(step_num, action_dict, reward, obs):
    action_type = action_dict.get("action_type", "noop").replace("_", " ").title()
    new_code    = action_dict.get("new_code", "")
    just        = action_dict.get("justification", "")
    rc, rv      = reward_class(reward)
    detail_parts = []
    if new_code: detail_parts.append(f"New code: <span style='font-family:Space Mono,monospace;color:#ffb800'>{new_code}</span>")
    if just:     detail_parts.append(f"<em>{just[:80]}</em>")
    detail = " &nbsp;·&nbsp; ".join(detail_parts) if detail_parts else "&nbsp;"

    return f"""
<div class="step-item">
  <div class="step-num">{step_num:02d}</div>
  <div class="step-body">
    <div class="step-action">{action_type}</div>
    <div class="step-detail">{detail}</div>
  </div>
  <span class="reward-badge {rc}">{rv}</span>
</div>
"""

def build_verdict_html(total_reward, steps, task_level):
    approved = total_reward > 0
    cls      = "approved" if approved else "rejected"
    icon     = "✅" if approved else "❌"
    label    = "CLAIM APPROVED" if approved else "CLAIM REJECTED"
    label_cls = "approved" if approved else "rejected"
    return f"""
<div class="verdict {cls}">
  <div class="verdict-icon">{icon}</div>
  <div>
    <div class="verdict-title {label_cls}">{label}</div>
    <div class="verdict-stats">
      Total Reward: <strong style="color:#e8f4ff">{round(total_reward,3)}</strong>
      &nbsp;·&nbsp; Steps: <strong style="color:#e8f4ff">{steps}</strong>
      &nbsp;·&nbsp; Difficulty: <strong style="color:#e8f4ff">{task_level.upper()}</strong>
    </div>
  </div>
</div>
"""

def build_metrics_html(total_reward, steps, task_level, approved):
    eff = max(0, round((10 - steps) / 10 * 100))
    score_color = "green" if total_reward > 0 else ""
    return f"""
<div class="metric-row">
  <div class="metric-card">
    <div class="label">Final Score</div>
    <div class="value {score_color}">{round(total_reward, 3)}</div>
  </div>
  <div class="metric-card">
    <div class="label">Steps Taken</div>
    <div class="value amber">{steps}</div>
  </div>
  <div class="metric-card">
    <div class="label">Efficiency</div>
    <div class="value">{eff}%</div>
  </div>
  <div class="metric-card">
    <div class="label">Decision</div>
    <div class="value {'green' if approved else ''}" style="{'color:var(--accent-red)' if not approved else ''}">
      {'APPROVE' if approved else 'REJECT'}
    </div>
  </div>
</div>
"""

# ── Simulation logic ──────────────────────────────────────────────────────────

def run_simulation(task_level):
    env   = HealthcareEnv()
    agent = RuleBasedAgent()

    obs       = env.reset(task_level)
    done      = False
    step      = 1
    max_steps = 10
    total_reward = 0.0
    steps_html   = ""
    first_obs    = obs.copy()

    while not done and step <= max_steps:
        action_dict = agent.act(obs)
        action      = ClaimAction(**action_dict)
        obs, reward, done, info = env.step(action)
        steps_html  += build_step_html(step, action_dict, reward, obs)
        total_reward += reward
        step += 1

    steps_taken = step - 1
    approved    = total_reward > 0

    metrics_html = build_metrics_html(total_reward, steps_taken, task_level, approved)
    claim_html   = build_claim_html(first_obs)
    verdict_html = build_verdict_html(total_reward, steps_taken, task_level)

    full_html = f"""
<style>
  .metric-row {{ display:flex; gap:16px; margin-bottom:20px; }}
  .metric-card {{ flex:1; background:#0d1b2e; border:1px solid #1a3050; border-radius:14px; padding:20px 24px; }}
  .metric-card:hover {{ border-color:#00c2ff; }}
  .metric-card .label {{ font-size:0.68rem; letter-spacing:1.5px; text-transform:uppercase; color:#5a7a9a; margin-bottom:8px; font-family:'Space Mono',monospace; }}
  .metric-card .value {{ font-family:'Space Mono',monospace; font-size:1.5rem; font-weight:700; color:#00c2ff; }}
  .metric-card .value.green {{ color:#00ffa3; }}
  .metric-card .value.amber {{ color:#ffb800; }}
  .panel {{ background:#0d1b2e; border:1px solid #1a3050; border-radius:16px; padding:24px 28px; margin-bottom:16px; }}
  .panel-title {{ font-family:'Space Mono',monospace; font-size:0.75rem; letter-spacing:2px; text-transform:uppercase; color:#00c2ff; margin-bottom:16px; padding-bottom:12px; border-bottom:1px solid #1a3050; }}
  .claim-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
  .claim-field {{ background:#0a1628; border:1px solid #1a3050; border-radius:10px; padding:12px 16px; }}
  .field-label {{ font-size:0.66rem; letter-spacing:1.2px; text-transform:uppercase; color:#5a7a9a; margin-bottom:4px; font-family:'Space Mono',monospace; }}
  .field-value {{ font-size:0.92rem; font-weight:500; color:#e8f4ff; }}
  .step-item {{ display:flex; gap:14px; align-items:flex-start; padding:14px 0; border-bottom:1px solid #1a3050; }}
  .step-item:last-child {{ border-bottom:none; }}
  .step-num {{ width:32px; height:32px; border-radius:50%; background:rgba(0,194,255,0.1); border:1px solid #00c2ff; display:flex; align-items:center; justify-content:center; font-family:'Space Mono',monospace; font-size:0.72rem; color:#00c2ff; flex-shrink:0; }}
  .step-body {{ flex:1; }}
  .step-action {{ font-weight:600; font-size:0.9rem; color:#e8f4ff; margin-bottom:3px; }}
  .step-detail {{ font-size:0.78rem; color:#5a7a9a; }}
  .reward-badge {{ font-family:'Space Mono',monospace; font-size:0.75rem; font-weight:700; padding:3px 10px; border-radius:20px; margin-left:auto; flex-shrink:0; }}
  .reward-pos {{ background:rgba(0,255,163,0.1); color:#00ffa3; border:1px solid rgba(0,255,163,0.3); }}
  .reward-neg {{ background:rgba(255,77,106,0.1); color:#ff4d6a; border:1px solid rgba(255,77,106,0.3); }}
  .reward-neu {{ background:rgba(255,184,0,0.1); color:#ffb800; border:1px solid rgba(255,184,0,0.3); }}
  .verdict {{ border-radius:14px; padding:22px 28px; display:flex; align-items:center; gap:20px; }}
  .verdict.approved {{ background:rgba(0,255,163,0.06); border:1px solid rgba(0,255,163,0.3); }}
  .verdict.rejected {{ background:rgba(255,77,106,0.06); border:1px solid rgba(255,77,106,0.3); }}
  .verdict-icon {{ font-size:2rem; }}
  .verdict-title {{ font-family:'Space Mono',monospace; font-size:1rem; font-weight:700; }}
  .verdict-title.approved {{ color:#00ffa3; }}
  .verdict-title.rejected {{ color:#ff4d6a; }}
  .verdict-stats {{ font-size:0.8rem; color:#5a7a9a; margin-top:4px; }}
</style>
{metrics_html}
{claim_html}
<div class="panel">
  <div class="panel-title">⚡ Agent Steps</div>
  {steps_html}
</div>
{verdict_html}
"""
    return full_html


# ── Gradio Layout ─────────────────────────────────────────────────────────────

with gr.Blocks(css=CUSTOM_CSS, title="AI HealthCare Claims") as demo:

    # Hero
    gr.HTML("""
    <div id="hero">
      <div id="hero-title">🏥 AI-Powered Insurance claim Decision System</div>
      <div id="hero-sub">Reinforcement Learning · Insurance Claim Decision Engine · OpenEnv Compatible</div>
    </div>
    """)

    with gr.Row():
        # Left sidebar: controls + info
        with gr.Column(scale=1, min_width=260):
            gr.HTML("""
            <div class="panel" style="margin-top:20px">
              <div class="panel-title">⚙ Configuration</div>
            </div>
            """)

            task = gr.Dropdown(
                choices=["easy", "medium", "hard"],
                value="easy",
                label="Task Difficulty",
                elem_id="task-dropdown"
            )

            run_btn = gr.Button("▶ RUN AGENT", elem_id="run-btn")

            gr.HTML("""
            <div class="panel" style="margin-top:16px">
              <div class="panel-title">📖 Task Levels</div>
              <div style="font-size:0.82rem; line-height:1.7; color:#5a7a9a">
                <div style="margin-bottom:10px">
                  <span style="color:#00ffa3;font-family:Space Mono,monospace;font-size:0.75rem">EASY</span><br>
                  Fix incorrect procedure code
                </div>
                <div style="margin-bottom:10px">
                  <span style="color:#ffb800;font-family:Space Mono,monospace;font-size:0.75rem">MEDIUM</span><br>
                  Fix code + provide justification
                </div>
                <div>
                  <span style="color:#ff4d6a;font-family:Space Mono,monospace;font-size:0.75rem">HARD</span><br>
                  Fix code + policy + preapproval docs
                </div>
              </div>
            </div>
            <div class="panel" style="margin-top:16px">
              <div class="panel-title">🤖 Agent Info</div>
              <div style="font-size:0.8rem; color:#5a7a9a; line-height:1.7">
                <div><span class="status-dot dot-green"></span>Rule-Based Agent</div>
                <div><span class="status-dot dot-blue"></span>Max Steps: 10</div>
                <div><span class="status-dot dot-blue"></span>Reward Range: −1.0 → +1.0</div>
              </div>
            </div>
            """)

        # Right: output
        with gr.Column(scale=3):
            gr.HTML("<div style='height:20px'></div>")
            output = gr.HTML(
                value="""
                <div style="background:#0d1b2e;border:1px solid #1a3050;border-radius:16px;padding:60px 40px;text-align:center;margin-top:0">
                  <div style="font-size:3rem;margin-bottom:16px">🏥</div>
                  <div style="font-family:Space Mono,monospace;font-size:0.85rem;color:#5a7a9a;letter-spacing:2px">
                    SELECT A DIFFICULTY AND CLICK RUN AGENT
                  </div>
                </div>
                """,
                elem_id="output-box"
            )

    run_btn.click(fn=run_simulation, inputs=task, outputs=output)

demo.launch(server_name="0.0.0.0", server_port=7860)

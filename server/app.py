from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from env.environment import HealthcareEnv
from models.action import ClaimAction
from agent.rule_based_agent import RuleBasedAgent
import uvicorn

app = FastAPI(title="AI HealthCare Claims API")

env = HealthcareEnv()
agent = RuleBasedAgent()


# ── Request models ──────────────────────────────────────────────────────────

class ResetRequest(BaseModel):
    difficulty: Optional[str] = "easy"
    task_level: Optional[str] = None


class StepRequest(BaseModel):
    action: dict


# ── UI Root ──────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serves a simple UI so HuggingFace Space shows something."""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>AI HealthCare Claims</title>
        <style>
            body { font-family: Arial, sans-serif; background: #0f172a; color: #e2e8f0; margin: 0; padding: 40px; }
            h1 { color: #38bdf8; }
            .card { background: #1e293b; border-radius: 12px; padding: 24px; margin: 16px 0; max-width: 700px; }
            .endpoint { background: #0f172a; border-left: 4px solid #38bdf8; padding: 10px 16px; margin: 8px 0; border-radius: 4px; font-family: monospace; }
            .badge { display: inline-block; background: #38bdf8; color: #0f172a; border-radius: 4px; padding: 2px 8px; font-size: 12px; font-weight: bold; margin-right: 8px; }
            a { color: #38bdf8; }
            button { background: #38bdf8; color: #0f172a; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; margin-top: 8px; }
            textarea { width: 100%; background: #0f172a; color: #e2e8f0; border: 1px solid #334155; border-radius: 6px; padding: 8px; font-family: monospace; box-sizing: border-box; }
            pre { background: #0f172a; padding: 12px; border-radius: 6px; overflow-x: auto; white-space: pre-wrap; }
            select { background:#0f172a; color:#e2e8f0; padding:6px; border-radius:4px; border:1px solid #334155; margin:8px 0; }
        </style>
    </head>
    <body>
        <h1>🏥 AI HealthCare Claims Environment</h1>

        <div class="card">
            <h2>About</h2>
            <p>This is an OpenEnv-compatible RL environment for healthcare insurance claim processing.
            The agent learns to approve, deny, or request more information for claims.</p>
        </div>

        <div class="card">
            <h2>API Endpoints</h2>
            <div class="endpoint"><span class="badge">POST</span>/reset — Reset environment</div>
            <div class="endpoint"><span class="badge">POST</span>/step — Take an action</div>
            <div class="endpoint"><span class="badge">POST</span>/state — Get current state</div>
            <div class="endpoint"><span class="badge">GET</span>/health — Health check</div>
            <div class="endpoint"><span class="badge">GET</span>/docs — Interactive API docs (Swagger UI)</div>
        </div>

        <div class="card">
            <h2>Try it — Reset Environment</h2>
            <label>Difficulty:</label><br/>
            <select id="difficulty">
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
            </select><br/>
            <button onclick="resetEnv()">Reset</button>
            <pre id="reset-output">Response will appear here...</pre>
        </div>

        <div class="card">
            <h2>Interactive Docs</h2>
            <p>Visit the full Swagger UI: <a href="/docs">/docs</a></p>
        </div>

        <script>
            async function resetEnv() {
                const difficulty = document.getElementById('difficulty').value;
                const out = document.getElementById('reset-output');
                out.textContent = 'Loading...';
                try {
                    const res = await fetch('/reset', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({difficulty})
                    });
                    const data = await res.json();
                    out.textContent = JSON.stringify(data, null, 2);
                } catch(e) {
                    out.textContent = 'Error: ' + e.message;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


# ── Endpoints ────────────────────────────────────────────────────────────────

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
def step(request: StepRequest):
    action = ClaimAction(**request.action)
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info,
    }


@app.post("/state")
def state():
    return env.state() if hasattr(env, "state") else {"status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)  # 7860 required for HuggingFace Spaces


if __name__ == "__main__":
    main()

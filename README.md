title: AI-Powered_Insurance_Claim_Decision_System
sdk: docker
---
title: AI HealthCare Meena
emoji: 🏥
colorFrom: blue
colorTo: cyan
sdk: docker
pinned: true
license: mit
---

<div align="center">

```
██╗  ██╗███████╗ █████╗ ██╗  ████████╗██╗  ██╗ ██████╗ █████╗ ██████╗ ███████╗
██║  ██║██╔════╝██╔══██╗██║  ╚══██╔══╝██║  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝
███████║█████╗  ███████║██║     ██║   ███████║██║     ███████║██████╔╝█████╗  
██╔══██║██╔══╝  ██╔══██║██║     ██║   ██╔══██║██║     ██╔══██║██╔══██╗██╔══╝  
██║  ██║███████╗██║  ██║███████╗██║   ██║  ██║╚██████╗██║  ██║██║  ██║███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
                        AI · CLAIMS · DECISION · ENGINE
```

# 🏥 AI-Powered Insurance Claim Decision System

**A Reinforcement Learning environment for intelligent healthcare insurance claim processing**

[![HuggingFace Space](https://img.shields.io/badge/🤗%20HuggingFace-Space-blue?style=for-the-badge)](https://huggingface.co/spaces/Meenakshid/AI-HealthCare-Meena)
[![OpenEnv Compatible](https://img.shields.io/badge/OpenEnv-Compatible-00c2ff?style=for-the-badge)](https://openenv.ai)
[![Python](https://img.shields.io/badge/Python-3.10-ffb800?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Server-00ffa3?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Gradio](https://img.shields.io/badge/Gradio-UI-ff4d6a?style=for-the-badge)](https://gradio.app)
[![Docker](https://img.shields.io/badge/Docker-Ready-0db7ed?style=for-the-badge&logo=docker)](https://docker.com)

</div>

---

## 🧠 What Is This?

**AI HealthCare Meena** is a full Reinforcement Learning (RL) environment that simulates real-world **insurance claim adjudication** — the process of deciding whether a healthcare claim should be approved or denied.

An intelligent agent examines each claim, identifies errors, corrects procedure codes, adds missing documents, and appeals wrongful denials — all autonomously. The environment is fully **OpenEnv-compatible**, meaning it can be plugged into any RL training framework.

> Think of it as a training gym where AI learns to be a smarter, faster, and fairer insurance claims processor.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 **Rule-Based Agent** | Deterministic agent with context-aware decision logic |
| 🎓 **RL Agent** | Q-learning agent that improves with experience |
| 🏋️ **3 Difficulty Levels** | Easy → Medium → Hard with escalating complexity |
| 🏥 **5 Procedure Types** | MRI, X-Ray, Blood Test, CT Scan, Ultrasound |
| 📋 **Realistic Claims** | Randomized codes, denial reasons, ages, policies |
| ⚡ **Multi-Step Episodes** | Up to 10 steps per claim with reward shaping |
| 🌐 **REST API** | Full OpenEnv `/reset`, `/step`, `/state` endpoints |
| 🎨 **Live UI** | Interactive Gradio dashboard with real-time metrics |

---

## 🎮 Try It Live

Visit the **[🚀 Live Demo](https://huggingface.co/spaces/Meenakshid/AI-HealthCare-Meena)** and:

1. Select a **difficulty level** (Easy / Medium / Hard)
2. Click **▶ RUN AGENT**
3. Watch the agent process the claim step-by-step
4. See the final **APPROVED ✅ / REJECTED ❌** verdict with metrics

---

## 🗂️ Project Structure

```
AI-HealthCare-Meena/
│
├── 📄 app.py                   # FastAPI server (OpenEnv compatible)
├── 📄 uiapp.py                 # Gradio UI (port 7860)
├── 📄 inference.py             # Inference entry point
├── 📄 Dockerfile               # Container config for HuggingFace
├── 📄 requirements.txt
│
├── 🗂️ env/                     # RL Environment
│   ├── environment.py          # Main HealthcareEnv class
│   ├── state_manager.py        # Episode state & step tracking
│   └── transition_logic.py     # Action → state transition rules
│
├── 🗂️ models/                  # Pydantic data models
│   ├── action.py               # ClaimAction model
│   ├── observation.py          # ClaimObservation model
│   └── reward.py               # ClaimReward model
│
├── 🗂️ agent/                   # Agent implementations
│   ├── rule_based_agent.py     # Deterministic rule-based agent
│   └── rl_agent.py             # Q-learning RL agent
│
├── 🗂️ grader/                  # Task-specific graders
│   ├── easy_grader.py          # Code correction grader
│   ├── medium_grader.py        # Code + justification grader
│   └── hard_grader.py          # Full compliance grader
│
├── 🗂️ reward/
│   └── reward_calculator.py    # Reward shaping logic
│
├── 🗂️ data/
│   └── claim_generator.py      # Randomized claim generation
│
└── 🗂️ tasks/
    ├── task_easy.py
    ├── task_medium.py
    └── task_hard.py
```

---

## 🎯 Task Levels

### 🟢 Easy
> Fix the incorrect procedure code submitted with the claim.

- Single action required
- Straightforward code correction
- No documents needed
- Fast, high reward for efficiency

### 🟡 Medium
> Fix the code **and** provide a valid justification.

- Code correction with clinical reasoning
- Justification evaluated for quality
- Policy compliance checked
- Moderate complexity

### 🔴 Hard
> Fix code + validate policy + handle preapproval documents.

- Multi-step episodes
- MRI procedures require preapproval documents
- Senior patients (60+) need additional approval
- Maximum reward complexity

---

## ⚡ API Reference

The FastAPI server exposes a full **OpenEnv-compatible** REST interface:

### `POST /reset`
Reset the environment and get the initial claim observation.
```json
{
  "difficulty": "easy"
}
```
**Response:**
```json
{
  "claim_id": "uuid-...",
  "patient_age": 45,
  "procedure": "MRI Scan",
  "submitted_code": "MRI001",
  "denial_reason": "Preapproval not obtained",
  "policy": "Standard Plan",
  "documents": []
}
```

### `POST /step`
Submit an action and receive the next observation + reward.
```json
{
  "action": {
    "action_type": "correct_code",
    "new_code": "MRI452",
    "justification": "Correcting MRI procedure code per Standard Plan policy."
  }
}
```
**Response:**
```json
{
  "observation": { ... },
  "reward": 0.75,
  "done": false,
  "info": { "step_count": 1 }
}
```

### `GET /health`
```json
{ "status": "ok" }
```

### `GET /docs`
Interactive Swagger UI — available at `/docs`

---

## 🤖 Action Types

| Action | Description | When to Use |
|---|---|---|
| `correct_code` | Submit the corrected procedure code | Code mismatch detected |
| `add_document` | Add a missing supporting document | Preapproval / senior approval needed |
| `appeal` | File an appeal against the denial | Denial is medically unjustified |
| `noop` | No operation | Claim already resolved |

---

## 🏆 Reward Structure

```
Final Reward = (Grader Score × 0.7)
             + (Step Efficiency × 0.2)
             - (Step Penalty × 0.05 per step)
             - (0.2 for noop actions)
             + (0.05 completion bonus)

Range: −1.0 (worst) → +1.0 (best)
```

> **Pro tip:** Fewer steps = higher efficiency bonus. Resolve claims in 1–2 steps for maximum reward.

---

## 🛠️ Run Locally

```bash
# Clone the repo
git clone https://huggingface.co/spaces/Meenakshid/AI-HealthCare-Meena
cd AI-HealthCare-Meena

# Install dependencies
pip install -r requirements.txt

# Run the Gradio UI
python uiapp.py

# OR run the FastAPI server
python app.py
```

**Docker:**
```bash
docker build -t healthcare-claims .
docker run -p 7860:7860 healthcare-claims
```

---

## 🧪 Run Tests

```bash
# Test environment
python test_env.py

# Test agent
python test_agent.py

# Test grader
python test_grader.py
```

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| **UI** | Gradio 4.x with custom CSS |
| **API Server** | FastAPI + Uvicorn |
| **RL Environment** | Custom OpenEnv-compatible env |
| **Agent** | Rule-based + Q-Learning (tabular) |
| **Data Models** | Pydantic v2 |
| **Container** | Docker on Python 3.10-slim |
| **Hosting** | HuggingFace Spaces |

---

## 📊 Example Episode (Hard Mode)

```
🧾 Claim: CT Scan | Age: 67 | Policy: Senior Care Plan
❌ Submitted: CTX001 | Denial: Benefit limit exceeded

Step 01 │ correct_code → CT874   │ Reward: +0.623
Step 02 │ add_document → senior  │ Reward: +0.541
─────────────────────────────────────────────────
✅ CLAIM APPROVED │ Total: +1.00 │ Efficiency: 80%
```

---

## 👩‍💻 Author

**Meenakshi D**  
Built for the **OpenEnv Hackathon** — Scaler School of Technology

---

<div align="center">

*"Making AI that understands healthcare, one claim at a time."*

⭐ Star this space if you found it useful!

</div>

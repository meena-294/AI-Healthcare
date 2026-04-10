title: AI-Powered_Insurance_Claim_Decision_System
sdk: docker



🏥 AI-Powered Healthcare Claim Decision System
An intelligent system that simulates multi-step healthcare insurance claim processing using rule-based reasoning and reinforcement learning concepts.

🚀 Project Overview
This project models a healthcare claim approval workflow where an AI agent interacts with an environment to resolve claim issues such as:

Incorrect procedure codes
Missing documents
Policy validation
Claim approval/denial decisions
The system evaluates actions step-by-step and assigns rewards using a grader mechanism.

🧠 Key Features
✅ Multi-step decision environment
✅ Rule-based AI agent
✅ Reward system integrated with grader
✅ Supports Easy, Medium, Hard tasks
✅ REST API using Flask
✅ Structured inference logging
✅ Dockerized for deployment
📂 Project Structure
healthcare-claim/
│
├── agent/              # Rule-based agent logic
├── env/                # Environment & state manager
├── models/             # Action and data models
├── grader/             # Reward evaluation logic
├── reward/             # Reward calculation
├── server/             # Flask API
│   └── app.py
├── tasks/              # Easy/Medium/Hard task definitions
├── inference.py        # Main evaluation script
├── requirements.txt
├── Dockerfile
└── README.md
⚙️ Installation
🔹 Local Setup
git clone <your-repo-url>
cd healthcare-claim

pip install -r requirements.txt
python server/app.py
🌐 API Endpoints
🔹 1. Reset Environment (POST)
POST /reset
Body:

{
  "task_level": "easy"
}
🔹 2. Get Current State (GET)
GET /state
🔹 3. Take Action (POST)
POST /step
Body:

{
  "action_type": "correct_code",
  "new_code": "PROC123",
  "justification": "Correct billing code"
}

🧪 Running Inference
python inference.py
Output Example
[START]
task: easy
[STEP]
{"step": 0, "action": "correct_code", "reward": 0.83}
[STEP]
{"step": 1, "action": "add_document", "reward": 0.11}
[END]
final_score: 0.94

🐳 Docker Deployment
docker build -t healthcare-claim .
docker run -p 8000:8000 healthcare-claim
🔧 Environment Variable
You can optionally control model usage:

export MODEL_NAME=gpt-4

🏆 Evaluation Criteria
✔️ Structured logging
✔️ Correct API behavior
✔️ Reward driven by grader
✔️ Multi-step task completion
✔️ Proper loop termination

📌 Tech Stack
Python
Flask
Rule-Based AI Agent
Reinforcement Learning Concepts
Docker
👩‍💻 Author
Meenakshi D

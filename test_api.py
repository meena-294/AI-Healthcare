import requests

# Step 1: Reset environment
requests.post(
    "http://127.0.0.1:8000/reset",
    json={"task_level": "easy"}
)

# Step 2: Get state
res = requests.get("http://127.0.0.1:8000/state")

print(res.json())
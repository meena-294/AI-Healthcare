FROM python:3.10-slim

# ── System deps ───────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Python dependencies ───────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy full project ─────────────────────────────────────────────────────────
# Root files
COPY uiapp.py      .
COPY server/app.py        .
COPY inference.py  .

# Package folders (must match your imports exactly)
COPY env/          ./env/
COPY models/       ./models/
COPY agent/        ./agent/
COPY grader/       ./grader/
COPY reward/       ./reward/
COPY data/         ./data/
COPY tasks/        ./tasks/

# ── HuggingFace Spaces requires port 7860 ────────────────────────────────────
EXPOSE 7860

# ── Environment variables ─────────────────────────────────────────────────────
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=7860

# ── Launch the Gradio UI ──────────────────────────────────────────────────────
CMD ["python", "uiapp.py"]

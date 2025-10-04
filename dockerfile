FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# Streamlit exposes a health endpoint but path may vary; use root as a basic check
HEALTHCHECK --interval=30s --timeout=3s CMD curl --fail http://localhost:8501/ || exit 1

# Run the project main script (dashact3.py) instead of app.py
ENTRYPOINT ["streamlit", "run", "dashact3.py", "--server.port=8501", "--server.address=0.0.0.0"]
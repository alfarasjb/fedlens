FROM python:3.11-slim

WORKDIR /usr/src/app

# Install dependencies first (better caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Streamlit runs on port 8080 for Fly.io
EXPOSE 8080

CMD ["streamlit", "run", "app.py", "--server.port=8080"]

# Backend container for free hosting (Render / Google Cloud Run / Koyeb-style hosts).
# The host injects $PORT; locally it defaults to 8000.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Run as a non-root user.
RUN useradd --create-home appuser
USER appuser

# --proxy-headers + --forwarded-allow-ips: behind the host's proxy, request.client.host
# becomes the real visitor IP, so the per-IP rate limit works per visitor, not for everyone at once.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'"]

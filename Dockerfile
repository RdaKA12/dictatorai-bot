FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends     ca-certificates &&     rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# non-root
RUN useradd -ms /bin/bash appuser
USER appuser

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import socket; print('ok')"

CMD ["python", "-m", "src.bot"]

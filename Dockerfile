FROM python:3.10-slim

RUN useradd -m appuser

WORKDIR /app 

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 
# that is to ensure we don't skip logs

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Code copy + ownership to the user
COPY --chown=appuser:appuser . .

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
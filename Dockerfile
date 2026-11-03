FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV TF_CPP_MIN_LOG_LEVEL=2

COPY docker-requirements.txt .

RUN pip install --no-cache-dir -r docker-requirements.txt

COPY web/app.py ./app.py
COPY web/templates ./templates
COPY fer2013_best_model.keras .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "120", "app:app"]

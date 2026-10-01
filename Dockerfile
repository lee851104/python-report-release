FROM python:3.12-slim

WORKDIR /app

COPY read_scores.py .
COPY data/evaluation.csv ./data/evaluation.csv

CMD ["python", "read_scores.py"]

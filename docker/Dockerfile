FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY configs ./configs
ENV PYTHONPATH=/app/src
CMD ["python", "-m", "openssh_anomaly.cli", "prepare", "--config", "configs/base.yaml"]

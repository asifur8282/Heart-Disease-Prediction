FROM python:3.14-slim

WORKDIR /app

COPY requirement_apponly.txt .

RUN pip install --no-cache-dir -r requirement_apponly.txt

COPY backend_api.py .
COPY frontend_streamlit.py .
COPY svm_heart_disease_model.pkl .
COPY scaler.pkl .

EXPOSE 8000 8501

RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

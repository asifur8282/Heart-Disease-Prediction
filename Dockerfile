FROM python:3.14-slim

WORKDIR /app

COPY requirement_apponly.txt .

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirement_apponly.txt

COPY backend_api.py .
COPY frontend_streamlit.py .
COPY svm_heart_disease_model.pkl .
COPY scaler.pkl .
COPY start.sh .

RUN chmod +x start.sh

EXPOSE 8000 8501

CMD ["./start.sh"]

#!/bin/bash
set -e

echo "Starting Heart Disease Prediction App..."
echo "========================================"

echo "[1/2] Starting Backend API on port 8000..."
uvicorn backend_api:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
sleep 3

echo "[2/2] Starting Streamlit Frontend on port 8501..."
streamlit run frontend_streamlit.py --server.port=8501 --server.address=0.0.0.0 --logger.level=info &
FRONTEND_PID=$!

echo "========================================"
echo "✓ Backend running (PID: $BACKEND_PID)"
echo "✓ Frontend running (PID: $FRONTEND_PID)"
echo "========================================"
echo ""
echo "Access the app at:"
echo "  Frontend: http://localhost:8501"
echo "  Backend API: http://localhost:8000"
echo ""

wait $BACKEND_PID $FRONTEND_PID

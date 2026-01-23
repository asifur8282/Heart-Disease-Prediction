from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np

svm_model = joblib.load("svm_heart_disease_model.pkl")
scaler = joblib.load("scaler.pkl")

app = FastAPI(title="Heart Disease Prediction API", version="1.0.0")

class PatientData(BaseModel):
    age: float = Field(..., ge=0, le=120, description="Patient age in years")
    sex: int = Field(..., ge=0, le=1, description="Sex (0=Female, 1=Male)")
    chest_pain_type: int = Field(..., ge=0, le=4, description="Chest pain type (0-4)")
    cholesterol: float = Field(..., ge=0, le=400, description="Serum cholesterol in mg/dl")
    ekg_results: int = Field(..., ge=0, le=2, description="EKG results (0-2)")
    max_hr: float = Field(..., ge=0, le=250, description="Maximum heart rate achieved")
    exercise_angina: int = Field(..., ge=0, le=1, description="Exercise induced angina (0=No, 1=Yes)")
    st_depression: float = Field(..., ge=0, le=10, description="ST depression induced by exercise")
    slope_of_st: int = Field(..., ge=0, le=3, description="Slope of ST segment (0-3)")
    number_of_vessels_fluro: int = Field(..., ge=0, le=3, description="Number of major vessels (0-3)")
    thallium: int = Field(..., ge=0, le=7, description="Thallium test result (0-7)")

class PredictionResponse(BaseModel):
    prediction: int
    confidence_score: float
    result_text: str

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Heart Disease Prediction API",
        "version": "1.0.0",
        "endpoint": "/predict"
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(patient: PatientData):
    try:
        input_data = np.array([
            patient.age,
            patient.sex,
            patient.chest_pain_type,
            patient.cholesterol,
            patient.ekg_results,
            patient.max_hr,
            patient.exercise_angina,
            patient.st_depression,
            patient.slope_of_st,
            patient.number_of_vessels_fluro,
            patient.thallium
        ]).reshape(1, -1)
        
        input_scaled = scaler.transform(input_data)
        
        prediction = svm_model.predict(input_scaled)[0]
        confidence = abs(svm_model.decision_function(input_scaled)[0])
        result_text = "⚠️ Heart Disease Detected" if prediction == 1 else "✓ No Heart Disease Detected"
        
        return PredictionResponse(
            prediction=int(prediction),
            confidence_score=float(confidence),
            result_text=result_text
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

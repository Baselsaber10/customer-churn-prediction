from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import os
from deploy.logger import log_prediction

app = FastAPI(title="Customer Churn Prediction API", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "artifacts", "model_experimentation", "models", "best_churn_model.joblib")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

class CustomerData(BaseModel):
    tenure: float
    MonthlyCharges: float
    TotalCharges: float
    Contract_Two_year: int = Field(alias="Contract_Two year")
    Contract_One_year: int = Field(alias="Contract_One year")
    PaymentMethod_Electronic_check: int = Field(alias="PaymentMethod_Electronic check")
    InternetService_Fiber_optic: int = Field(alias="InternetService_Fiber optic")
    OnlineSecurity_Yes: int = Field(alias="OnlineSecurity_Yes")
    TechSupport_Yes: int = Field(alias="TechSupport_Yes")
    Partner: int

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def read_root():
    template_path = os.path.join(BASE_DIR, "deploy", "templates", "index.html")
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<html><body><h1>UI not found</h1></body></html>"

@app.post("/predict")
def predict_churn(data: CustomerData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    input_dict = data.model_dump(by_alias=True)
    expected_cols = ["tenure", "MonthlyCharges", "TotalCharges", "Contract_Two year", 
                     "Contract_One year", "PaymentMethod_Electronic check", 
                     "InternetService_Fiber optic", "OnlineSecurity_Yes", 
                     "TechSupport_Yes", "Partner"]
    
    df = pd.DataFrame([input_dict], columns=expected_cols)
    
    try:
        prediction = int(model.predict(df)[0])
        probability = float(model.predict_proba(df)[0][1])
        
        log_prediction(input_dict, prediction, probability)
        
        return {
            "prediction": prediction,
            "churn_probability": probability
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

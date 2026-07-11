# Milestone 4: MLOps, Deployment, and Monitoring Report

## 1. Overview
This report details the MLOps practices, deployment strategy, and monitoring setup for the Customer Churn Prediction model. The objective of this milestone is to transition the machine learning model from an experimental phase into a production-ready system.

## 2. MLOps Practices & MLFlow Integration
To ensure reproducibility, traceability, and proper model registry, we integrated **MLFlow**.
- **Tracking Script**: `mlops/train_track.py` loads the best performing model (`HistGradientBoosting`) and logs its hyperparameters and performance metrics (Accuracy, F1-Score, ROC-AUC) to a local MLFlow SQLite database (`mlflow.db`).
- **Artifacts**: The trained model and the preprocessing pipeline are registered as artifacts in MLFlow, making it easy to version and deploy specific models in the future.

## 3. Model Deployment
The model is deployed as a REST API using **FastAPI** to allow real-time predictions.
- **Application**: `deploy/app.py` exposes a `/predict` POST endpoint.
- **Input Schema**: It uses Pydantic to strictly validate incoming JSON payloads containing customer features (e.g., `tenure`, `MonthlyCharges`, `Contract_One year`, etc.).
- **Execution**: The incoming payload is converted into a Pandas DataFrame, passed through the pre-fitted preprocessing pipeline, and fed into the model for inference.
- **Running Locally**: 
  ```bash
  pip install -r deploy/requirements.txt
  uvicorn deploy.app:app --reload
  ```

## 4. Monitoring Setup
Continuous monitoring is crucial to ensure the model's predictions remain accurate over time.
- **Request Logging**: The `deploy/logger.py` module captures every incoming request, along with the model's prediction and probability, and appends it to a local `logs/predictions.jsonl` file.
- **Data Drift Detection**: The `monitoring/data_drift_report.py` script leverages **Evidently AI** to compare the incoming production data (from the logs) against a reference dataset (the baseline training data). This generates an interactive HTML report (`monitoring/data_drift_report.html`) highlighting any significant shifts in feature distributions.

## 5. Next Steps
- Consider setting up a cron job or scheduled task to run the drift report weekly.
- If scaling is required, the FastAPI application can easily be containerized using Docker and deployed to a cloud provider.

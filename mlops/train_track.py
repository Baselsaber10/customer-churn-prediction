import mlflow
import joblib
import pandas as pd
import os
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned", "customer_churn_selected.csv")
MODEL_PATH = os.path.join(BASE_DIR, "artifacts", "model_experimentation", "models", "best_churn_model.joblib")

def run_mlflow_tracking():
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("Customer_Churn_Prediction")

    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=["Churn"])
    y = df["Churn"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run(run_name="HistGradientBoosting_Retrain") as run:
        params = {
            'min_samples_leaf': 30,
            'max_iter': 200,
            'max_depth': 3,
            'learning_rate': 0.03
        }
        mlflow.log_params(params)

        model = HistGradientBoostingClassifier(**params, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred),
            "roc_auc": roc_auc_score(y_test, y_prob)
        }
        mlflow.log_metrics(metrics)

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(model, MODEL_PATH)

        mlflow.sklearn.log_model(model, "churn_model")
        
        print("Model retrained and logged to MLFlow successfully!")
        print(f"Run ID: {run.info.run_id}")

if __name__ == "__main__":
    run_mlflow_tracking()

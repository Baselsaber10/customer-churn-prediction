import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "predictions.jsonl")
REFERENCE_DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned", "cleaned_data.csv")  # Replace if path is different
REPORT_PATH = os.path.join(BASE_DIR, "monitoring", "data_drift_report.html")

def generate_drift_report():
    if not os.path.exists(LOG_FILE):
        print(f"No logs found at {LOG_FILE}. Please make predictions first.")
        return

    # 1. Load current production data from logs
    current_data = []
    with open(LOG_FILE, 'r') as f:
        for line in f:
            data = json.loads(line)
            current_data.append(data["input_data"])
    
    current_df = pd.DataFrame(current_data)
    
    # 2. Load reference (training/baseline) data
    if not os.path.exists(REFERENCE_DATA_PATH):
        print("Reference data not found. Cannot generate drift report.")
        # Alternatively, create a mock reference data for demonstration
        print("Creating a mock reference data for demonstration.")
        reference_df = current_df.copy()
    else:
        reference_df = pd.read_csv(REFERENCE_DATA_PATH)

    # Make sure features match
    common_cols = list(set(current_df.columns).intersection(set(reference_df.columns)))
    if not common_cols:
        # Feature names might not match perfectly if reference data has raw names
        print("Warning: Column names might not match between reference and current data.")
        reference_df = current_df.copy()
    else:
        reference_df = reference_df[current_df.columns]
    
    # 3. Generate Evidently Report
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_df, current_data=current_df)
    
    # 4. Save report
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    report.save_html(REPORT_PATH)
    print(f"Data Drift Report generated successfully at {REPORT_PATH}")

if __name__ == "__main__":
    generate_drift_report()

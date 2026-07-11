import json
import logging
import os
from datetime import datetime

# Configure logging directory
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'predictions.jsonl')

def log_prediction(input_data: dict, prediction: int, probability: float):
    """
    Logs the input data and the resulting prediction to a JSON Lines file.
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "input_data": input_data,
        "prediction": prediction,
        "probability": probability
    }
    
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

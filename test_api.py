import requests
import json
import time

API_URL = "http://127.0.0.1:8000/predict"

# Mock customer data based on the features the model expects
mock_customers = [
    {
        "tenure": 12.0,
        "MonthlyCharges": 70.5,
        "TotalCharges": 846.0,
        "Contract_Two year": 0,
        "Contract_One year": 1,
        "PaymentMethod_Electronic check": 1,
        "InternetService_Fiber optic": 1,
        "OnlineSecurity_Yes": 0,
        "TechSupport_Yes": 1,
        "Partner": 1
    },
    {
        "tenure": 1.0,
        "MonthlyCharges": 20.0,
        "TotalCharges": 20.0,
        "Contract_Two year": 0,
        "Contract_One year": 0,
        "PaymentMethod_Electronic check": 1,
        "InternetService_Fiber optic": 0,
        "OnlineSecurity_Yes": 0,
        "TechSupport_Yes": 0,
        "Partner": 0
    },
    {
        "tenure": 72.0,
        "MonthlyCharges": 110.5,
        "TotalCharges": 7956.0,
        "Contract_Two year": 1,
        "Contract_One year": 0,
        "PaymentMethod_Electronic check": 0,
        "InternetService_Fiber optic": 1,
        "OnlineSecurity_Yes": 1,
        "TechSupport_Yes": 1,
        "Partner": 1
    }
]

def test_api():
    print("Testing Customer Churn Prediction API...\n")
    for i, customer in enumerate(mock_customers):
        print(f"Sending request for Customer {i+1}...")
        try:
            response = requests.post(API_URL, json=customer)
            if response.status_code == 200:
                result = response.json()
                print(f"Prediction: {'Churn' if result['prediction'] == 1 else 'No Churn'}")
                print(f"Probability: {result['churn_probability']:.2%}")
            else:
                print(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            print("Failed to connect to the API. Is Uvicorn running on port 8000?")
        print("-" * 30)
        time.sleep(1)

if __name__ == "__main__":
    test_api()

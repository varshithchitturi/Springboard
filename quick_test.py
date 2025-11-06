import requests
import json

# Test the prediction endpoint
test_data = {
    "magnitude": 7.5,
    "depth": 10,
    "latitude": 35.0,
    "longitude": 139.0,
    "alert": "red",
    "country": "Japan",
    "continent": "Asia",
    "magType": "mw"
}

try:
    response = requests.post(
        "http://localhost:5000/predict",
        json=test_data,
        headers={'Content-Type': 'application/json'},
        timeout=5
    )
    
    print("Status Code:", response.status_code)
    result = response.json()
    print("Response:", json.dumps(result, indent=2))
    
except Exception as e:
    print("Error:", e)
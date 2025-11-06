"""
Debug the prediction issue
"""

import requests
import json

def debug_prediction():
    print("🔍 Debugging Prediction Issue")
    print("=" * 40)
    
    # Simple test data
    test_data = {
        "magnitude": 6.5,
        "depth": 20,
        "alert": "green",
        "magType": "mw",
        "cdi": 5,
        "mmi": 4,
        "sig": 500
    }
    
    try:
        print("📊 Sending test data:")
        print(json.dumps(test_data, indent=2))
        
        response = requests.post(
            "http://localhost:5002/predict",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n📋 Full Response:")
            print(json.dumps(result, indent=2))
            
            if result.get('success'):
                predictions = result.get('predictions', {})
                print(f"\n🎯 Available Predictions: {list(predictions.keys())}")
                
                for model_name, pred in predictions.items():
                    print(f"\n🤖 {model_name}:")
                    for key, value in pred.items():
                        print(f"   {key}: {value}")
            else:
                print(f"\n❌ Error: {result.get('error')}")
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")

if __name__ == "__main__":
    debug_prediction()
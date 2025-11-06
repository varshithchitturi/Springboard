"""
Simple test for Random Forest earthquake prediction
"""

import requests
import json

def test_prediction_endpoint():
    print("🧪 Testing Random Forest Prediction Endpoint")
    print("=" * 50)
    
    # Test data
    test_earthquake = {
        "magnitude": 7.0,
        "depth": 25.0,
        "latitude": 35.0,
        "longitude": 139.0,
        "cdi": 6,
        "mmi": 5,
        "sig": 700,
        "magType": "mw",
        "alert": "yellow"
    }
    
    try:
        print("📊 Testing with earthquake data:")
        for key, value in test_earthquake.items():
            print(f"   {key}: {value}")
        
        print("\\n🔄 Making prediction request...")
        
        response = requests.post(
            "http://localhost:5000/predict",
            json=test_earthquake,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print("✅ Prediction successful!")
                
                predictions = result.get('predictions', {})
                model_info = result.get('model_info', {})
                
                print("\\n🎯 Predictions:")
                for model_name, pred in predictions.items():
                    model_display = model_name.replace('_', ' ').title()
                    probability = pred.get('probability', 0)
                    risk_level = pred.get('risk_level', 'Unknown')
                    
                    print(f"   {model_display}:")
                    print(f"      Probability: {probability:.1%}")
                    print(f"      Risk Level: {risk_level}")
                
                print("\\n🤖 Model Information:")
                print(f"   Type: {model_info.get('type', 'Unknown')}")
                print(f"   Dataset: {model_info.get('dataset_size', 'Unknown')}")
                print(f"   Features: {model_info.get('features_used', 'Unknown')}")
                
                print("\\n📈 Model Accuracies:")
                print(f"   High Impact: {model_info.get('high_impact_accuracy', 'Unknown')}")
                print(f"   Tsunami Risk: {model_info.get('tsunami_risk_accuracy', 'Unknown')}")
                print(f"   High Alert: {model_info.get('high_alert_accuracy', 'Unknown')}")
                
            else:
                print(f"❌ Prediction failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print("\\n" + "=" * 50)
    print("🎉 Random Forest Test Complete!")

if __name__ == "__main__":
    test_prediction_endpoint()
import requests
import json

print("🧪 Simple API Test")

try:
    # Test the prediction endpoint
    response = requests.post(
        "http://localhost:5000/predict",
        json={
            "magnitude": 6.5,
            "depth": 15,
            "alert": "yellow",
            "country": "Japan"
        },
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("Success:", result.get('success'))
        
        if result.get('success'):
            predictions = result.get('predictions', {})
            print("\nPredictions:")
            
            if 'high_impact' in predictions:
                hi = predictions['high_impact']
                print(f"  High Impact: {hi['probability']:.2%} ({hi['risk_level']})")
            
            if 'tsunami' in predictions:
                ts = predictions['tsunami']
                print(f"  Tsunami: {ts['probability']:.2%} ({ts['risk_level']})")
                
            print("\n✅ API is working correctly!")
        else:
            print("❌ Prediction failed:", result.get('error'))
    else:
        print("❌ HTTP Error:", response.text)

except Exception as e:
    print(f"❌ Error: {e}")
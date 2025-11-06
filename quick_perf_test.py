import requests
import time

# Quick performance test
start = time.time()

try:
    response = requests.post(
        "http://localhost:5000/predict",
        json={
            "magnitude": 7.2,
            "depth": 12,
            "latitude": 35.0,
            "longitude": 139.0,
            "alert": "orange"
        },
        headers={'Content-Type': 'application/json'},
        timeout=2
    )
    
    end = time.time()
    response_time = (end - start) * 1000
    
    print(f"Response Time: {response_time:.1f}ms")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            print("✅ Prediction successful!")
            print(f"High Impact: {result['predictions']['high_impact']['probability']:.1%}")
            print(f"Tsunami Risk: {result['predictions']['tsunami']['probability']:.1%}")
        else:
            print("❌ Prediction failed")
    
    if response_time < 100:
        print("🚀 EXCELLENT performance!")
    elif response_time < 300:
        print("✅ GOOD performance!")
    else:
        print("⚠️ Could be faster")
        
except Exception as e:
    print(f"Error: {e}")
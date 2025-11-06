import requests
import json

print("🧪 Testing Fixed Application")
print("=" * 30)

try:
    # Test basic connectivity
    response = requests.get("http://localhost:5000", timeout=5)
    print(f"✅ Server Status: {response.status_code}")
    
    # Test prediction endpoint
    test_data = {
        "magnitude": 6.5,
        "depth": 15,
        "latitude": 35.0,
        "longitude": 139.0,
        "alert": "yellow"
    }
    
    print("📡 Testing prediction...")
    response = requests.post(
        "http://localhost:5000/predict",
        json=test_data,
        headers={'Content-Type': 'application/json'},
        timeout=5
    )
    
    print(f"📨 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success: {result['success']}")
        
        if result['success']:
            predictions = result['predictions']
            print(f"📊 High Impact: {predictions['high_impact']['probability']:.1%} ({predictions['high_impact']['risk_level']})")
            print(f"🌊 Tsunami Risk: {predictions['tsunami']['probability']:.1%} ({predictions['tsunami']['risk_level']})")
            print("🎉 Application is working correctly!")
        else:
            print(f"❌ Prediction failed: {result.get('error')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Error: {e}")

print("\n🌐 Open http://localhost:5000 in your browser to test the UI")
import requests
import json
import time

def test_loading_behavior():
    """Test the loading behavior of the app"""
    
    print("🧪 Testing Loading Behavior")
    print("=" * 30)
    
    # Test data
    test_data = {
        "magnitude": 6.5,
        "depth": 15,
        "latitude": 35.0,
        "longitude": 139.0,
        "alert": "yellow",
        "country": "Japan",
        "continent": "Asia"
    }
    
    print("📊 Sending prediction request...")
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:5000/predict",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"⏱️ Response time: {response_time:.2f} seconds")
        print(f"📡 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Prediction successful!")
                predictions = result['predictions']
                print(f"   High Impact: {predictions['high_impact']['probability']:.1%}")
                print(f"   Tsunami Risk: {predictions['tsunami']['probability']:.1%}")
            else:
                print(f"❌ Prediction failed: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - loading might be stuck")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_loading_behavior()
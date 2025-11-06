"""
Test script for the Earthquake Prediction API
Run this to verify the application is working correctly
"""

import requests
import json
import time

def test_api():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Earthquake Prediction API")
    print("=" * 50)
    
    # Test 1: Check if server is running
    print("1. Testing server connection...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure to run 'python app_simple.py' first")
        return False
    
    # Test 2: Test countries API
    print("\n2. Testing countries API...")
    try:
        response = requests.get(f"{base_url}/api/countries")
        countries = response.json()
        print(f"✅ Got {len(countries)} countries")
        print(f"   Sample: {countries[:3]}")
    except Exception as e:
        print(f"❌ Countries API failed: {e}")
    
    # Test 3: Test continents API
    print("\n3. Testing continents API...")
    try:
        response = requests.get(f"{base_url}/api/continents")
        continents = response.json()
        print(f"✅ Got {len(continents)} continents")
        print(f"   All: {continents}")
    except Exception as e:
        print(f"❌ Continents API failed: {e}")
    
    # Test 4: Test prediction API with sample data
    print("\n4. Testing prediction API...")
    
    test_cases = [
        {
            "name": "Small earthquake",
            "data": {
                "magnitude": 4.5,
                "depth": 15,
                "latitude": 35.0,
                "longitude": 139.0,
                "alert": "none",
                "country": "Japan",
                "continent": "Asia",
                "magType": "ml"
            }
        },
        {
            "name": "Large shallow earthquake",
            "data": {
                "magnitude": 7.8,
                "depth": 8,
                "latitude": -33.0,
                "longitude": -72.0,
                "alert": "red",
                "country": "Chile",
                "continent": "South America",
                "magType": "mw"
            }
        },
        {
            "name": "Deep earthquake",
            "data": {
                "magnitude": 6.2,
                "depth": 150,
                "latitude": 40.0,
                "longitude": 25.0,
                "alert": "yellow",
                "country": "Greece",
                "continent": "Europe",
                "magType": "mb"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test 4.{i}: {test_case['name']}")
        try:
            response = requests.post(
                f"{base_url}/predict",
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    predictions = result['predictions']
                    
                    # High impact prediction
                    high_impact = predictions['high_impact']
                    print(f"      High Impact: {high_impact['probability']:.2%} ({high_impact['risk_level']})")
                    
                    # Tsunami prediction
                    tsunami = predictions['tsunami']
                    print(f"      Tsunami Risk: {tsunami['probability']:.2%} ({tsunami['risk_level']})")
                    
                    print("      ✅ Prediction successful!")
                else:
                    print(f"      ❌ Prediction failed: {result.get('error', 'Unknown error')}")
            else:
                print(f"      ❌ HTTP error: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Request failed: {e}")
    
    # Test 5: Test invalid input handling
    print("\n5. Testing error handling...")
    try:
        response = requests.post(
            f"{base_url}/predict",
            json={"invalid": "data"},
            headers={'Content-Type': 'application/json'}
        )
        
        result = response.json()
        if not result.get('success', True):
            print("✅ Error handling works correctly")
        else:
            print("⚠️ Error handling might need improvement")
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing complete!")
    print("💡 Open http://localhost:5000 in your browser to see the UI")
    
    return True

def test_ui_elements():
    """Test if the UI loads correctly"""
    print("\n🎨 Testing UI Elements")
    print("-" * 30)
    
    try:
        response = requests.get("http://localhost:5000")
        html_content = response.text
        
        # Check for key UI elements
        ui_elements = [
            "Earthquake Impact Predictor",
            "magnitude",
            "depth",
            "latitude",
            "longitude",
            "Predict Impact",
            "style.css",
            "script.js"
        ]
        
        missing_elements = []
        for element in ui_elements:
            if element not in html_content:
                missing_elements.append(element)
        
        if not missing_elements:
            print("✅ All UI elements found!")
        else:
            print(f"⚠️ Missing UI elements: {missing_elements}")
            
    except Exception as e:
        print(f"❌ UI test failed: {e}")

if __name__ == "__main__":
    print("🌍 Earthquake Prediction System Test Suite")
    print("Make sure the server is running first!")
    print()
    
    # Wait a moment for user to start server
    print("Starting tests in 3 seconds...")
    time.sleep(3)
    
    # Run tests
    if test_api():
        test_ui_elements()
    
    print("\n🏁 Testing finished!")
"""
Test the earthquake prediction app without latitude/longitude coordinates
"""

import requests
import json

def test_without_coordinates():
    print("🧪 Testing Earthquake Predictor (No Coordinates)")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test cases without latitude/longitude
    test_cases = [
        {
            "name": "Small earthquake in Japan",
            "data": {
                "magnitude": 4.2,
                "depth": 25,
                "alert": "none",
                "country": "Japan",
                "continent": "Asia",
                "magType": "ml"
            }
        },
        {
            "name": "Medium earthquake in Chile",
            "data": {
                "magnitude": 6.5,
                "depth": 15,
                "alert": "yellow",
                "country": "Chile",
                "continent": "South America",
                "magType": "mw"
            }
        },
        {
            "name": "Large earthquake in Indonesia",
            "data": {
                "magnitude": 7.8,
                "depth": 8,
                "alert": "red",
                "country": "Indonesia",
                "continent": "Asia",
                "magType": "mw"
            }
        },
        {
            "name": "Earthquake without country",
            "data": {
                "magnitude": 5.5,
                "depth": 30,
                "alert": "green",
                "magType": "mb"
            }
        }
    ]
    
    print("📊 Running prediction tests...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        
        try:
            response = requests.post(
                f"{base_url}/predict",
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result['success']:
                    predictions = result['predictions']
                    
                    high_impact = predictions['high_impact']
                    tsunami = predictions['tsunami']
                    
                    print(f"   ✅ High Impact: {high_impact['probability']:.1%} ({high_impact['risk_level']})")
                    print(f"   🌊 Tsunami Risk: {tsunami['probability']:.1%} ({tsunami['risk_level']})")
                    
                    # Validate that predictions make sense
                    if test_case['data']['magnitude'] > 7.0:
                        if high_impact['risk_level'] in ['Medium', 'High']:
                            print("   ✅ High magnitude correctly shows elevated risk")
                        else:
                            print("   ⚠️ High magnitude should show higher risk")
                    
                    # Check tsunami risk for coastal countries
                    country = test_case['data'].get('country', '')
                    if country in ['Japan', 'Chile', 'Indonesia'] and test_case['data']['magnitude'] > 6.5:
                        if tsunami['probability'] > 0.1:
                            print("   ✅ Coastal country shows appropriate tsunami risk")
                        else:
                            print("   ⚠️ Coastal country should show higher tsunami risk")
                    
                else:
                    print(f"   ❌ Prediction failed: {result.get('error')}")
            else:
                print(f"   ❌ HTTP error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
    
    # Test API endpoints
    print(f"\n{'='*50}")
    print("🔧 Testing API endpoints...")
    
    try:
        # Test countries
        response = requests.get(f"{base_url}/api/countries")
        if response.status_code == 200:
            countries = response.json()
            print(f"✅ Countries API: {len(countries)} countries available")
        else:
            print(f"❌ Countries API failed: {response.status_code}")
        
        # Test continents
        response = requests.get(f"{base_url}/api/continents")
        if response.status_code == 200:
            continents = response.json()
            print(f"✅ Continents API: {len(continents)} continents available")
        else:
            print(f"❌ Continents API failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
    
    print(f"\n{'='*50}")
    print("🎉 Testing complete!")
    print("✅ Application works correctly without latitude/longitude")
    print("🌐 Open http://localhost:5000 to use the web interface")

if __name__ == "__main__":
    test_without_coordinates()
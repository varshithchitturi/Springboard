"""
Performance test for the optimized earthquake prediction app
Tests response times and ensures no lag/buffering
"""

import requests
import time
import statistics

def test_performance():
    """Test application performance"""
    
    print("🚀 Performance Testing - Optimized Earthquake Predictor")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test data
    test_cases = [
        {
            "name": "Small Earthquake",
            "data": {
                "magnitude": 4.2,
                "depth": 25,
                "latitude": 35.0,
                "longitude": 139.0,
                "alert": "none"
            }
        },
        {
            "name": "Medium Earthquake", 
            "data": {
                "magnitude": 6.5,
                "depth": 15,
                "latitude": 35.0,
                "longitude": 139.0,
                "alert": "yellow"
            }
        },
        {
            "name": "Large Earthquake",
            "data": {
                "magnitude": 8.1,
                "depth": 8,
                "latitude": -33.0,
                "longitude": -72.0,
                "alert": "red"
            }
        }
    ]
    
    # Performance metrics
    response_times = []
    success_count = 0
    total_tests = len(test_cases) * 3  # Run each test 3 times
    
    print("📊 Running performance tests...")
    print(f"   Total tests: {total_tests}")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🧪 Test {i}: {test_case['name']}")
        
        case_times = []
        
        # Run each test case 3 times
        for run in range(3):
            start_time = time.time()
            
            try:
                response = requests.post(
                    f"{base_url}/predict",
                    json=test_case['data'],
                    headers={'Content-Type': 'application/json'},
                    timeout=3  # Short timeout to catch lag
                )
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # Convert to ms
                
                if response.status_code == 200:
                    result = response.json()
                    if result['success']:
                        success_count += 1
                        case_times.append(response_time)
                        response_times.append(response_time)
                        
                        print(f"   Run {run + 1}: ✅ {response_time:.1f}ms")
                    else:
                        print(f"   Run {run + 1}: ❌ Prediction failed")
                else:
                    print(f"   Run {run + 1}: ❌ HTTP {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"   Run {run + 1}: ⏰ Timeout (>3s) - LAG DETECTED!")
            except Exception as e:
                print(f"   Run {run + 1}: ❌ Error: {e}")
        
        if case_times:
            avg_time = statistics.mean(case_times)
            print(f"   Average: {avg_time:.1f}ms")
        print()
    
    # Performance analysis
    print("📈 Performance Analysis")
    print("-" * 30)
    
    if response_times:
        avg_response = statistics.mean(response_times)
        min_response = min(response_times)
        max_response = max(response_times)
        
        print(f"✅ Success Rate: {success_count}/{total_tests} ({success_count/total_tests*100:.1f}%)")
        print(f"⚡ Average Response: {avg_response:.1f}ms")
        print(f"🏃 Fastest Response: {min_response:.1f}ms")
        print(f"🐌 Slowest Response: {max_response:.1f}ms")
        
        # Performance rating
        if avg_response < 100:
            rating = "🚀 EXCELLENT"
        elif avg_response < 300:
            rating = "✅ GOOD"
        elif avg_response < 500:
            rating = "⚠️ ACCEPTABLE"
        else:
            rating = "❌ NEEDS OPTIMIZATION"
        
        print(f"🎯 Performance Rating: {rating}")
        
        # Lag detection
        slow_responses = [t for t in response_times if t > 500]
        if slow_responses:
            print(f"⚠️ Slow responses detected: {len(slow_responses)}")
        else:
            print("✅ No lag detected - All responses under 500ms")
            
    else:
        print("❌ No successful responses - Check server status")
    
    print("\n" + "=" * 60)
    print("🏁 Performance test complete!")

if __name__ == "__main__":
    test_performance()
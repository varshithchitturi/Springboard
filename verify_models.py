"""
Script to verify that the trained models are working correctly
"""

import joblib
import numpy as np
import pandas as pd
from pathlib import Path

def verify_models():
    """Verify that both models can make predictions"""
    print("🔍 Verifying Earthquake Impact Predictor Models")
    print("=" * 50)
    
    models_dir = Path("models")
    
    # Test data - realistic earthquake parameters
    test_cases = [
        {
            "name": "Major Japan Earthquake",
            "data": [7.2, 15.0, 35.6762, 139.6503, 8.0, 7.5, 800, "red", "mw", "us", "Asia", "Japan"]
        },
        {
            "name": "Moderate California Earthquake", 
            "data": [5.8, 25.0, 34.0522, -118.2437, 5.0, 4.5, 300, "yellow", "ml", "ci", "North America", "USA"]
        },
        {
            "name": "Deep Chile Earthquake",
            "data": [6.5, 120.0, -33.4489, -70.6693, 3.0, 4.0, 450, "orange", "mb", "us", "South America", "Chile"]
        }
    ]
    
    feature_names = ['magnitude', 'depth', 'latitude', 'longitude', 'cdi', 'mmi', 'sig', 
                    'alert', 'magType', 'net', 'continent', 'country']\n    
    # Check if models exist\n    high_impact_path = models_dir / \"rf_high_impact.joblib\"\n    tsunami_path = models_dir / \"rf_tsunami.joblib\"\n    \n    if not high_impact_path.exists():\n        print(f\"❌ High impact model not found at {high_impact_path}\")\n        return False\n        \n    if not tsunami_path.exists():\n        print(f\"❌ Tsunami model not found at {tsunami_path}\")\n        return False\n    \n    try:\n        # Load models\n        print(\"📥 Loading models...\")\n        high_impact_model = joblib.load(high_impact_path)\n        tsunami_model = joblib.load(tsunami_path)\n        print(\"✅ Models loaded successfully\")\n        \n        # Test predictions\n        print(\"\\n🧪 Testing predictions...\")\n        \n        for i, test_case in enumerate(test_cases, 1):\n            print(f\"\\n--- Test Case {i}: {test_case['name']} ---\")\n            \n            # Prepare input data\n            input_data = np.array([test_case['data']])\n            \n            try:\n                # High impact prediction\n                high_impact_prob = high_impact_model.predict_proba(input_data)\n                high_impact_score = high_impact_prob[0][1] if len(high_impact_prob[0]) > 1 else high_impact_prob[0][0]\n                \n                # Tsunami prediction  \n                tsunami_prob = tsunami_model.predict_proba(input_data)\n                tsunami_score = tsunami_prob[0][1] if len(tsunami_prob[0]) > 1 else tsunami_prob[0][0]\n                \n                # Display results\n                print(f\"📊 Input: M{test_case['data'][0]} at {test_case['data'][1]}km depth\")\n                print(f\"🎯 High Impact: {high_impact_score:.1%} ({get_risk_level(high_impact_score)})\")\n                print(f\"🌊 Tsunami Risk: {tsunami_score:.1%} ({get_risk_level(tsunami_score)})\")\n                \n            except Exception as e:\n                print(f\"❌ Prediction failed for {test_case['name']}: {e}\")\n                return False\n        \n        print(\"\\n✅ All model tests passed!\")\n        print(\"🎉 Models are working correctly and ready for use.\")\n        return True\n        \n    except Exception as e:\n        print(f\"❌ Error loading or testing models: {e}\")\n        return False\n\ndef get_risk_level(probability):\n    \"\"\"Convert probability to risk level\"\"\"\n    if probability < 0.3:\n        return 'Low'\n    elif probability < 0.7:\n        return 'Medium'\n    else:\n        return 'High'\n\ndef check_model_info():\n    \"\"\"Display information about the loaded models\"\"\"\n    print(\"\\n📋 Model Information:\")\n    \n    models_dir = Path(\"models\")\n    \n    for model_name in [\"rf_high_impact.joblib\", \"rf_tsunami.joblib\"]:\n        model_path = models_dir / model_name\n        if model_path.exists():\n            try:\n                model = joblib.load(model_path)\n                print(f\"\\n🤖 {model_name}:\")\n                \n                # Try to get model info\n                if hasattr(model, 'named_steps'):\n                    classifier = model.named_steps.get('classifier')\n                    if classifier and hasattr(classifier, 'n_estimators'):\n                        print(f\"   - Type: Random Forest\")\n                        print(f\"   - Estimators: {classifier.n_estimators}\")\n                        if hasattr(classifier, 'max_depth'):\n                            print(f\"   - Max Depth: {classifier.max_depth}\")\n                    else:\n                        print(f\"   - Type: Custom Model\")\n                else:\n                    print(f\"   - Type: Unknown\")\n                    \n                print(f\"   - File Size: {model_path.stat().st_size / 1024:.1f} KB\")\n                \n            except Exception as e:\n                print(f\"   ❌ Error reading {model_name}: {e}\")\n        else:\n            print(f\"\\n❌ {model_name}: Not found\")\n\nif __name__ == \"__main__\":\n    success = verify_models()\n    \n    if success:\n        check_model_info()\n        print(\"\\n🚀 Ready to start the application!\")\n        print(\"Run: python app.py\")\n    else:\n        print(\"\\n🔧 Please run 'python extract_models.py' to fix model issues.\")
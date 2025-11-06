"""
Project Status Checker - Earthquake Impact Predictor
This script checks the status of all project components
"""

import os
import sys
from pathlib import Path
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Python Version Check:")
    version = sys.version_info
    print(f"   Current: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Compatible")
        return True
    else:
        print("   ❌ Requires Python 3.8+")
        return False

def check_required_packages():
    """Check if all required packages are installed"""
    print("\n📦 Package Dependencies:")
    
    required_packages = {
        'flask': 'Flask',
        'numpy': 'NumPy', 
        'pandas': 'Pandas',
        'sklearn': 'Scikit-learn',
        'joblib': 'Joblib'
    }
    
    missing_packages = []
    
    for package, display_name in required_packages.items():
        try:
            importlib.import_module(package)
            print(f"   ✅ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   ⚠️  {len(missing_packages)} packages missing!")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("   ✅ All packages installed")
        return True

def check_project_files():
    """Check if all project files exist"""
    print("\\n📁 Project Files:")
    
    required_files = {
        'Core Files': [
            'app.py',
            'extract_models.py',
            'requirements.txt',
            'README.md'
        ],
        'Frontend': [
            'templates/index.html',
            'static/css/style.css', 
            'static/js/script.js'
        ],
        'Models': [
            'models/rf_high_impact.joblib',
            'models/rf_tsunami.joblib'
        ],
        'Data': [
            'earthquake_1995-2023.csv'
        ]
    }
    
    all_good = True
    
    for category, files in required_files.items():
        print(f\"\\n   {category}:\")\n        \n        for file_path in files:\n            if Path(file_path).exists():\n                size = Path(file_path).stat().st_size\n                if size > 1024:\n                    size_str = f\"{size/1024:.1f} KB\"\n                else:\n                    size_str = f\"{size} bytes\"\n                print(f\"     ✅ {file_path} ({size_str})\")\n            else:\n                print(f\"     ❌ {file_path} (missing)\")\n                if category != 'Data':  # Data file is optional\n                    all_good = False\n    \n    return all_good\n\ndef check_models():\n    \"\"\"Check model status and functionality\"\"\"\n    print(\"\\n🤖 Model Status:\")\n    \n    models_dir = Path(\"models\")\n    if not models_dir.exists():\n        print(\"   ❌ Models directory not found\")\n        return False\n    \n    model_files = ['rf_high_impact.joblib', 'rf_tsunami.joblib']\n    models_ok = True\n    \n    for model_file in model_files:\n        model_path = models_dir / model_file\n        if model_path.exists():\n            try:\n                import joblib\n                model = joblib.load(model_path)\n                print(f\"   ✅ {model_file} (loaded successfully)\")\n            except Exception as e:\n                print(f\"   ⚠️  {model_file} (load error: {e})\")\n                models_ok = False\n        else:\n            print(f\"   ❌ {model_file} (missing)\")\n            models_ok = False\n    \n    if not models_ok:\n        print(\"\\n   🔧 To fix model issues:\")\n        print(\"      python extract_models.py\")\n    \n    return models_ok\n\ndef check_dataset():\n    \"\"\"Check if the earthquake dataset is available\"\"\"\n    print(\"\\n📊 Dataset Status:\")\n    \n    dataset_path = Path(\"earthquake_1995-2023.csv\")\n    if dataset_path.exists():\n        try:\n            import pandas as pd\n            df = pd.read_csv(dataset_path)\n            print(f\"   ✅ Dataset found ({len(df):,} records)\")\n            \n            # Check key columns\n            required_cols = ['magnitude', 'depth', 'latitude', 'longitude']\n            missing_cols = [col for col in required_cols if col not in df.columns]\n            \n            if missing_cols:\n                print(f\"   ⚠️  Missing columns: {missing_cols}\")\n            else:\n                print(\"   ✅ All required columns present\")\n                \n            return True\n            \n        except Exception as e:\n            print(f\"   ❌ Dataset error: {e}\")\n            return False\n    else:\n        print(\"   ⚠️  Dataset not found (using dummy models)\")\n        return False\n\ndef get_overall_status(checks):\n    \"\"\"Determine overall project status\"\"\"\n    print(\"\\n\" + \"=\" * 50)\n    print(\"📋 OVERALL STATUS\")\n    print(\"=\" * 50)\n    \n    passed = sum(checks.values())\n    total = len(checks)\n    \n    if passed == total:\n        print(\"🎉 ALL SYSTEMS GO!\")\n        print(\"   Your Earthquake Impact Predictor is ready to use.\")\n        print(\"\\n🚀 Next steps:\")\n        print(\"   1. Run: python app.py\")\n        print(\"   2. Open: http://localhost:5000\")\n        print(\"   3. Start predicting earthquake impacts!\")\n        return True\n    else:\n        print(f\"⚠️  {passed}/{total} checks passed\")\n        print(\"\\n🔧 Issues found:\")\n        \n        for check_name, status in checks.items():\n            if not status:\n                print(f\"   - {check_name}\")\n        \n        print(\"\\n💡 Recommended actions:\")\n        if not checks.get('Packages', True):\n            print(\"   1. Install packages: pip install -r requirements.txt\")\n        if not checks.get('Models', True):\n            print(\"   2. Setup models: python extract_models.py\")\n        if not checks.get('Files', True):\n            print(\"   3. Ensure all project files are present\")\n            \n        print(\"\\n   Or run the automated setup: python setup.py\")\n        return False\n\ndef main():\n    \"\"\"Main status check function\"\"\"\n    print(\"🌍 Earthquake Impact Predictor - Status Check\")\n    print(\"=\" * 50)\n    \n    # Run all checks\n    checks = {\n        'Python Version': check_python_version(),\n        'Packages': check_required_packages(),\n        'Files': check_project_files(),\n        'Models': check_models(),\n        'Dataset': check_dataset()\n    }\n    \n    # Overall status\n    success = get_overall_status(checks)\n    \n    if success:\n        print(\"\\n🎯 Ready for earthquake impact prediction!\")\n    else:\n        print(\"\\n🔧 Please address the issues above before running the app.\")\n    \n    return success\n\nif __name__ == \"__main__\":\n    main()
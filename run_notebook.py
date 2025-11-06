"""
Script to run the Jupyter notebook and extract trained models
This will execute the notebook and prepare the real ML models
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "jupyter", "nbconvert"])
        print("✅ Jupyter packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def run_notebook():
    """Execute the Jupyter notebook"""
    notebook_path = "infosis (1).ipynb"
    
    if not Path(notebook_path).exists():
        print(f"❌ Notebook file '{notebook_path}' not found!")
        return False
    
    print("🚀 Running Jupyter notebook...")
    print("⏳ This may take several minutes...")
    
    try:
        # Execute the notebook
        result = subprocess.run([
            sys.executable, "-m", "jupyter", "nbconvert", 
            "--to", "notebook", 
            "--execute", 
            "--inplace",
            notebook_path
        ], capture_output=True, text=True, timeout=600)  # 10 minute timeout
        
        if result.returncode == 0:
            print("✅ Notebook executed successfully!")
            return True
        else:
            print(f"❌ Error executing notebook: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Notebook execution timed out (10 minutes)")
        return False
    except Exception as e:
        print(f"❌ Error running notebook: {e}")
        return False

def check_models():
    """Check if models were created"""
    model_files = ["rf_high_impact.joblib", "rf_tsunami.joblib"]
    models_dir = Path("models")
    
    found_models = []
    for model_file in model_files:
        # Check in current directory
        if Path(model_file).exists():
            found_models.append(model_file)
        # Check in models directory
        elif (models_dir / model_file).exists():
            found_models.append(model_file)
    
    if len(found_models) == len(model_files):
        print("🎉 All models found!")
        return True
    else:
        print(f"⚠️ Only {len(found_models)}/{len(model_files)} models found")
        return False

def setup_models():
    """Move models to the correct directory"""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    model_files = ["rf_high_impact.joblib", "rf_tsunami.joblib"]
    
    for model_file in model_files:
        if Path(model_file).exists():
            # Move to models directory
            Path(model_file).rename(models_dir / model_file)
            print(f"📁 Moved {model_file} to models directory")

def main():
    print("🌍 Earthquake Model Setup")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Run notebook
    if run_notebook():
        # Check if models were created
        if check_models():
            setup_models()
            print("\n🎉 Setup complete!")
            print("✅ Real ML models are now available")
            print("🚀 You can now run: python app.py")
        else:
            print("\n⚠️ Models not found after notebook execution")
            print("💡 You can still use the demo version: python app_simple.py")
    else:
        print("\n❌ Failed to run notebook")
        print("💡 You can use the demo version: python app_simple.py")

if __name__ == "__main__":
    main()
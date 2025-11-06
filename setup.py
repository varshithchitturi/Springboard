"""
Setup script for the Earthquake Impact Predictor
This script will help you get everything up and running
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def setup_models():
    """Setup models by running extract_models.py"""
    print("\n🤖 Setting up machine learning models...")
    try:
        subprocess.check_call([sys.executable, "extract_models.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting up models: {e}")
        return False

def check_files():
    """Check if all required files exist"""
    print("📋 Checking required files...")
    
    required_files = [
        "app.py",
        "extract_models.py", 
        "requirements.txt",
        "templates/index.html",
        "static/css/style.css",
        "static/js/script.js"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
            print(f"❌ Missing: {file_path}")
        else:
            print(f"✅ Found: {file_path}")
    
    if missing_files:
        print(f"\n⚠️  {len(missing_files)} files are missing!")
        return False
    else:
        print("\n✅ All required files found!")
        return True

def main():
    """Main setup function"""
    print("🌍 Earthquake Impact Predictor - Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ Please run this script from the project directory!")
        return
    
    # Check files
    if not check_files():
        print("\n❌ Setup cannot continue due to missing files.")
        return
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed during package installation.")
        return
    
    # Setup models
    if not setup_models():
        print("\n❌ Setup failed during model preparation.")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 To start the application:")
    print("   python app.py")
    print("\n🧪 To test the application:")
    print("   python test_app.py")
    print("\n📖 Open your browser and go to:")
    print("   http://localhost:5000")
    
    # Ask if user wants to start the app now
    try:
        start_now = input("\n❓ Would you like to start the app now? (y/n): ").lower().strip()
        if start_now in ['y', 'yes']:
            print("\n🚀 Starting the application...")
            subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Setup completed. You can start the app later with: python app.py")

if __name__ == "__main__":
    main()
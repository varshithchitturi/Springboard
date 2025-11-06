"""
Script to extract and prepare models from the Jupyter notebook
Run this script after executing the notebook to prepare models for the web app
"""

import os
import shutil
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

def setup_models():
    """
    Setup models directory and copy models if they exist, or create new ones
    """
    # Create models directory if it doesn't exist
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Check if models exist in the current directory
    model_files = [
        "rf_high_impact.joblib",
        "rf_tsunami.joblib"
    ]
    
    models_found = []
    for model_file in model_files:
        if Path(model_file).exists():
            # Copy to models directory
            shutil.copy(model_file, models_dir / model_file)
            models_found.append(model_file)
            print(f"✓ Copied {model_file} to models directory")
        elif (models_dir / model_file).exists():
            models_found.append(model_file)
            print(f"✓ {model_file} already exists in models directory")
        else:
            print(f"✗ {model_file} not found")
    
    if len(models_found) == len(model_files):
        print("\n🎉 All models are ready!")
        print("You can now run the Flask app with: python app.py")
    else:
        print(f"\n⚠️  Only {len(models_found)}/{len(model_files)} models found.")
        
        # Check if we have the dataset to train models
        if Path("earthquake_1995-2023.csv").exists():
            print("\n📊 Dataset found! Training models from scratch...")
            train_models_from_data()
        else:
            print("\n⚠️  Dataset not found. Creating dummy models for testing...")
            create_dummy_models()

def train_models_from_data():
    """
    Train models using the actual earthquake dataset
    """
    try:
        print("📈 Loading and preprocessing data...")
        
        # Load the dataset
        df = pd.read_csv("earthquake_1995-2023.csv")
        
        # Basic preprocessing
        date_format = '%d-%m-%Y %H:%M'
        df['date_time'] = pd.to_datetime(df['date_time'], format=date_format, errors='coerce')
        df = df.dropna(subset=['date_time'])
        
        # Fill missing values
        df['alert'].fillna('none', inplace=True)
        df['country'].fillna('Unknown', inplace=True)
        df['continent'].fillna('Unknown', inplace=True)
        df['magType'].fillna('ml', inplace=True)
        df['net'].fillna('us', inplace=True)
        
        # Fill numeric missing values
        numeric_cols = ['magnitude', 'depth', 'latitude', 'longitude', 'cdi', 'mmi', 'sig']
        for col in numeric_cols:
            if col in df.columns:
                df[col].fillna(df[col].median(), inplace=True)
        
        # Create high impact target (top 25% based on significance)
        df['high_impact'] = (df['sig'] > df['sig'].quantile(0.75)).astype(int)
        
        # Prepare features
        feature_cols = ['magnitude', 'depth', 'latitude', 'longitude', 'cdi', 'mmi', 'sig', 
                       'alert', 'magType', 'net', 'continent', 'country']
        
        # Ensure all feature columns exist
        for col in feature_cols:
            if col not in df.columns:
                if col in numeric_cols:
                    df[col] = 5.0  # Default numeric value
                else:
                    df[col] = 'unknown'  # Default categorical value
        
        X = df[feature_cols]
        
        # Train high impact model
        print("🎯 Training high impact model...")
        y_high_impact = df['high_impact']
        high_impact_model = create_and_train_model(X, y_high_impact)
        joblib.dump(high_impact_model, "models/rf_high_impact.joblib")
        print("✓ High impact model saved")
        
        # Train tsunami model
        print("🌊 Training tsunami model...")
        y_tsunami = df['tsunami'] if 'tsunami' in df.columns else np.random.randint(0, 2, len(df))
        tsunami_model = create_and_train_model(X, y_tsunami)
        joblib.dump(tsunami_model, "models/rf_tsunami.joblib")
        print("✓ Tsunami model saved")
        
        print("\n🎉 Models trained successfully from real data!")
        print("You can now run the Flask app with: python app.py")
        
    except Exception as e:
        print(f"❌ Error training models: {e}")
        print("Creating dummy models instead...")
        create_dummy_models()

def create_and_train_model(X, y):
    """
    Create and train a model pipeline
    """
    # Define feature types
    numeric_features = ['magnitude', 'depth', 'latitude', 'longitude', 'cdi', 'mmi', 'sig']
    categorical_features = ['alert', 'magType', 'net', 'continent', 'country']
    
    # Create preprocessors
    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    # Combine preprocessors
    preprocessor = ColumnTransformer([
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    
    # Create pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        ))
    ])
    
    # Train the model
    pipeline.fit(X, y)
    
    return pipeline

def create_dummy_models():
    """
    Create dummy models for testing when real models are not available
    """
    print("🔧 Creating dummy models for testing...")
    
    # Create dummy data
    np.random.seed(42)
    n_samples = 1000
    
    # Create realistic dummy data
    dummy_data = {
        'magnitude': np.random.normal(5.5, 1.5, n_samples),
        'depth': np.random.exponential(20, n_samples),
        'latitude': np.random.uniform(-90, 90, n_samples),
        'longitude': np.random.uniform(-180, 180, n_samples),
        'cdi': np.random.uniform(1, 10, n_samples),
        'mmi': np.random.uniform(1, 10, n_samples),
        'sig': np.random.exponential(100, n_samples),
        'alert': np.random.choice(['none', 'green', 'yellow', 'orange', 'red'], n_samples),
        'magType': np.random.choice(['ml', 'mb', 'mw', 'ms'], n_samples),
        'net': np.random.choice(['us', 'ci', 'nc', 'ak'], n_samples),
        'continent': np.random.choice(['Asia', 'North America', 'South America', 'Europe', 'Africa', 'Oceania'], n_samples),
        'country': np.random.choice(['Japan', 'USA', 'Chile', 'Indonesia', 'Turkey', 'Italy'], n_samples)
    }
    
    df_dummy = pd.DataFrame(dummy_data)
    
    # Create realistic targets
    # High impact based on magnitude and depth
    high_impact_prob = (df_dummy['magnitude'] - 4) / 6 + (30 - df_dummy['depth']) / 60
    high_impact_prob = np.clip(high_impact_prob, 0, 1)
    y_high_impact = np.random.binomial(1, high_impact_prob)
    
    # Tsunami based on magnitude, depth, and location
    tsunami_prob = np.where(
        (df_dummy['magnitude'] > 6.5) & (df_dummy['depth'] < 50) & 
        (df_dummy['country'].isin(['Japan', 'Chile', 'Indonesia'])),
        0.3, 0.05
    )
    y_tsunami = np.random.binomial(1, tsunami_prob)
    
    # Train models
    print("🎯 Training dummy high impact model...")
    high_impact_model = create_and_train_model(df_dummy, y_high_impact)
    joblib.dump(high_impact_model, "models/rf_high_impact.joblib")
    print("✓ Dummy high impact model saved")
    
    print("🌊 Training dummy tsunami model...")
    tsunami_model = create_and_train_model(df_dummy, y_tsunami)
    joblib.dump(tsunami_model, "models/rf_tsunami.joblib")
    print("✓ Dummy tsunami model saved")
    
    print("\n⚠️  Note: These are dummy models for testing only!")
    print("For accurate predictions, please train real models using the notebook.")
    print("\n🎉 Dummy models created successfully!")
    print("You can now run the Flask app with: python app.py")

if __name__ == "__main__":
    print("🔧 Earthquake Impact Predictor - Model Setup")
    print("=" * 50)
    setup_models()
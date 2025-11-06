"""
Random Forest Training Script for Earthquake Dataset
Trains models to predict earthquake impact and tsunami risk
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def load_earthquake_dataset():
    """Load and examine the earthquake dataset"""
    print("🌍 Loading earthquake dataset...")
    
    try:
        # Try earthquake.csv first, then fallback to earthquake_1995-2023.csv
        if Path('earthquake.csv').exists():
            df = pd.read_csv('earthquake.csv')
            filename = 'earthquake.csv'
        else:
            df = pd.read_csv('earthquake_1995-2023.csv')
            filename = 'earthquake_1995-2023.csv'
            
        print(f"✅ Dataset loaded successfully from {filename}!")
        print(f"   📈 Shape: {df.shape}")
        print(f"   📋 Columns: {list(df.columns)}")
        
        # Display basic info
        print(f"\n📊 Dataset Overview:")
        print(f"   Total earthquakes: {len(df):,}")
        print(f"   Date range: {df['date_time'].min()} to {df['date_time'].max()}")
        
        # Check data types
        print(f"\n🔍 Data Types:")
        for col, dtype in df.dtypes.items():
            print(f"   {col}: {dtype}")
        
        # Check for missing values
        missing_data = df.isnull().sum()
        print(f"\n❓ Missing Values:")
        for col, missing in missing_data.items():
            if missing > 0:
                print(f"   {col}: {missing} ({missing/len(df)*100:.1f}%)")
        
        # Basic statistics for key columns
        if 'magnitude' in df.columns:
            print(f"\n📊 Magnitude Statistics:")
            print(f"   Range: {df['magnitude'].min():.1f} - {df['magnitude'].max():.1f}")
            print(f"   Mean: {df['magnitude'].mean():.2f}")
            print(f"   Median: {df['magnitude'].median():.2f}")
        
        if 'depth' in df.columns:
            print(f"\n🕳️ Depth Statistics:")
            print(f"   Range: {df['depth'].min():.1f} - {df['depth'].max():.1f} km")
            print(f"   Mean: {df['depth'].mean():.2f} km")
            print(f"   Median: {df['depth'].median():.2f} km")
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

def preprocess_earthquake_data(df):
    """Preprocess the earthquake data for Random Forest training"""
    print("\n🔄 Preprocessing earthquake data...")
    
    # Make a copy
    df_processed = df.copy()
    
    # Handle missing values
    print("   🧹 Handling missing values...")
    
    # Numeric columns
    numeric_cols = ['magnitude', 'depth', 'latitude', 'longitude', 'cdi', 'mmi', 'sig', 'nst', 'dmin', 'gap']
    for col in numeric_cols:
        if col in df_processed.columns:
            df_processed[col] = df_processed[col].fillna(df_processed[col].median())
    
    # Categorical columns
    categorical_cols = ['alert', 'magType', 'net', 'location', 'continent', 'country']
    for col in categorical_cols:
        if col in df_processed.columns:
            df_processed[col] = df_processed[col].fillna('unknown')
    
    # Create target variables
    print("   🎯 Creating target variables...")
    
    # High Impact Target (based on multiple factors)
    impact_score = 0
    
    # Magnitude factor (40% weight)
    if 'magnitude' in df_processed.columns:
        mag_normalized = (df_processed['magnitude'] - df_processed['magnitude'].min()) / \
                        (df_processed['magnitude'].max() - df_processed['magnitude'].min())
        impact_score += mag_normalized * 0.4
    
    # Depth factor (30% weight) - shallow earthquakes more dangerous
    if 'depth' in df_processed.columns:
        depth_normalized = 1 - ((df_processed['depth'] - df_processed['depth'].min()) / \
                               (df_processed['depth'].max() - df_processed['depth'].min()))
        impact_score += depth_normalized * 0.3
    
    # Significance factor (20% weight)
    if 'sig' in df_processed.columns:
        sig_normalized = (df_processed['sig'] - df_processed['sig'].min()) / \
                        (df_processed['sig'].max() - df_processed['sig'].min())
        impact_score += sig_normalized * 0.2
    
    # CDI factor (10% weight)
    if 'cdi' in df_processed.columns:
        cdi_normalized = df_processed['cdi'] / 10.0  # CDI is typically 0-10
        impact_score += cdi_normalized * 0.1
    
    # Create binary high impact target (top 30% are high impact)
    impact_threshold = impact_score.quantile(0.7)
    df_processed['high_impact'] = (impact_score >= impact_threshold).astype(int)
    
    # Tsunami Target (use existing tsunami column or create based on conditions)
    if 'tsunami' in df_processed.columns:
        df_processed['tsunami_risk'] = df_processed['tsunami'].fillna(0).astype(int)
    else:
        # Create tsunami risk based on magnitude and depth
        tsunami_conditions = (df_processed['magnitude'] >= 6.5) & (df_processed['depth'] <= 50)
        df_processed['tsunami_risk'] = tsunami_conditions.astype(int)
    
    # Alert Level Target (if available)
    if 'alert' in df_processed.columns:
        alert_mapping = {'green': 0, 'yellow': 1, 'orange': 2, 'red': 3, 'unknown': 0}
        df_processed['alert_level'] = df_processed['alert'].map(alert_mapping).fillna(0)
        df_processed['high_alert'] = (df_processed['alert_level'] >= 2).astype(int)
    else:
        df_processed['high_alert'] = (df_processed['magnitude'] >= 7.0).astype(int)
    
    print(f"✅ Preprocessing complete!")
    print(f"   High impact events: {df_processed['high_impact'].sum()} ({df_processed['high_impact'].mean():.1%})")
    print(f"   Tsunami risk events: {df_processed['tsunami_risk'].sum()} ({df_processed['tsunami_risk'].mean():.1%})")
    print(f"   High alert events: {df_processed['high_alert'].sum()} ({df_processed['high_alert'].mean():.1%})")
    
    return df_processed

def prepare_features(df):
    """Prepare features for Random Forest training"""
    print("\n🔧 Preparing features for Random Forest...")
    
    # Select numeric features
    numeric_features = []
    potential_numeric = ['magnitude', 'depth', 'latitude', 'longitude', 'cdi', 'mmi', 'sig', 'nst', 'dmin', 'gap']
    
    for col in potential_numeric:
        if col in df.columns:
            numeric_features.append(col)
    
    # Create feature matrix
    X = df[numeric_features].copy()
    
    # Feature engineering
    print("   ⚙️ Engineering features...")
    
    # Magnitude-based features
    if 'magnitude' in X.columns:
        X['magnitude_squared'] = X['magnitude'] ** 2
        X['magnitude_cubed'] = X['magnitude'] ** 3
        
        if 'depth' in X.columns:
            X['mag_depth_ratio'] = X['magnitude'] / (X['depth'] + 1)  # +1 to avoid division by zero
            X['mag_depth_interaction'] = X['magnitude'] * np.log1p(X['depth'])
    
    # Depth-based features
    if 'depth' in X.columns:
        X['depth_log'] = np.log1p(X['depth'])
        X['depth_sqrt'] = np.sqrt(X['depth'])
        X['shallow_earthquake'] = (X['depth'] <= 70).astype(int)  # Shallow earthquake indicator
    
    # Location-based features
    if 'latitude' in X.columns and 'longitude' in X.columns:
        X['distance_from_equator'] = np.abs(X['latitude'])
        X['location_risk'] = np.sqrt(X['latitude']**2 + X['longitude']**2)  # Distance from origin
    
    # Significance-based features
    if 'sig' in X.columns:
        X['sig_log'] = np.log1p(X['sig'])
        X['high_significance'] = (X['sig'] >= 600).astype(int)
    
    # Handle categorical features
    categorical_features = ['magType', 'net', 'alert']
    encoders = {}
    
    for col in categorical_features:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = df[col].fillna('unknown')
            X[f'{col}_encoded'] = le.fit_transform(df[col])
            encoders[col] = le
    
    # Handle any remaining missing values
    imputer = SimpleImputer(strategy='median')
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns, index=X.index)
    
    print(f"✅ Features prepared: {X_imputed.shape[1]} features")
    print(f"   Numeric features: {len(numeric_features)}")
    print(f"   Engineered features: {X_imputed.shape[1] - len(numeric_features) - len(encoders)}")
    print(f"   Encoded categorical: {len(encoders)}")
    
    return X_imputed, encoders, imputer

def train_random_forest_models(X, df):
    """Train Random Forest models for different prediction tasks"""
    print("\n🤖 Training Random Forest models...")
    
    models = {}
    scalers = {}
    results = {}
    
    # Random Forest parameters
    rf_params = {
        'n_estimators': 200,
        'max_depth': 20,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'max_features': 'sqrt',
        'random_state': 42,
        'n_jobs': -1
    }
    
    targets = {
        'high_impact': df['high_impact'],
        'tsunami_risk': df['tsunami_risk'],
        'high_alert': df['high_alert']
    }
    
    for target_name, y in targets.items():
        print(f"\n📊 Training {target_name} model...")
        
        # Check if target has enough positive cases
        if y.sum() < 5:
            print(f"   ⚠️ Skipping {target_name} - insufficient positive cases ({y.sum()})")
            continue
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train Random Forest
        rf = RandomForestClassifier(**rf_params)
        rf.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = rf.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(rf, X_train_scaled, y_train, cv=5)
        
        print(f"   ✅ {target_name} Accuracy: {accuracy:.3f}")
        print(f"   📊 CV Score: {cv_scores.mean():.3f} (±{cv_scores.std()*2:.3f})")
        
        # Classification report
        target_names = ['Low Risk', 'High Risk'] if 'high' in target_name else ['No', 'Yes']
        print(f"   📋 Classification Report:")
        print(classification_report(y_test, y_pred, target_names=target_names))
        
        # Store model and results
        models[target_name] = rf
        scalers[target_name] = scaler
        results[target_name] = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
    
    return models, scalers, results

def analyze_feature_importance(models, feature_names):
    """Analyze and display feature importance"""
    print("\n🔍 Feature Importance Analysis...")
    
    for model_name, model in models.items():
        print(f"\n📊 {model_name.replace('_', ' ').title()} Model - Top 10 Features:")
        
        # Get feature importance
        importance = model.feature_importances_
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        # Display top 10
        for idx, row in feature_importance.head(10).iterrows():
            print(f"   {row['feature']}: {row['importance']:.3f}")

def save_models(models, scalers, encoders, imputer):
    """Save all trained models and preprocessors"""
    print("\n💾 Saving trained models...")
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Save models
    for name, model in models.items():
        joblib.dump(model, models_dir / f"rf_{name}.pkl")
        print(f"   ✅ Saved {name} model")
    
    # Save scalers
    for name, scaler in scalers.items():
        joblib.dump(scaler, models_dir / f"scaler_{name}.pkl")
        print(f"   ✅ Saved {name} scaler")
    
    # Save encoders and imputer
    joblib.dump(encoders, models_dir / "encoders.pkl")
    joblib.dump(imputer, models_dir / "imputer.pkl")
    
    print(f"✅ All models saved to {models_dir.absolute()}")

def main():
    """Main training pipeline"""
    print("🌍 Random Forest Training for Earthquake Prediction")
    print("=" * 60)
    
    # Load data
    df = load_earthquake_dataset()
    if df is None:
        return
    
    # Preprocess data
    df_processed = preprocess_earthquake_data(df)
    
    # Prepare features
    X, encoders, imputer = prepare_features(df_processed)
    
    # Train models
    models, scalers, results = train_random_forest_models(X, df_processed)
    
    if not models:
        print("❌ No models were trained successfully")
        return
    
    # Analyze feature importance
    analyze_feature_importance(models, X.columns)
    
    # Save models
    save_models(models, scalers, encoders, imputer)
    
    # Summary
    print(f"\n{'='*60}")
    print("🎉 Random Forest Training Complete!")
    print(f"📊 Dataset size: {len(df_processed):,} earthquakes")
    print(f"🔧 Features used: {X.shape[1]}")
    print(f"🤖 Models trained: {len(models)}")
    
    for name, result in results.items():
        print(f"✅ {name.replace('_', ' ').title()}: {result['accuracy']:.1%} accuracy")
    
    print("🚀 Models ready for deployment!")

if __name__ == "__main__":
    main()
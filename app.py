"""
Flask application using Random Forest models trained on earthquake dataset
"""

from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for models
models = {}
scalers = {}
encoders = {}
imputer = None

def load_rf_models():
    """Load Random Forest models trained on earthquake data"""
    global models, scalers, encoders, imputer
    
    models_dir = Path("models")
    
    try:
        # Load models with exact filenames
        model_files = [
            ('high_impact', 'rf_high_impact.pkl'),
            ('tsunami_risk', 'rf_tsunami_risk.pkl'),
            ('high_alert', 'rf_high_alert.pkl')
        ]
        
        for name, filename in model_files:
            model_path = models_dir / filename
            if model_path.exists():
                models[name] = joblib.load(model_path)
                logger.info(f"✅ Loaded {name} model from {filename}")
            else:
                logger.warning(f"⚠️ Model file not found: {filename}")
        
        # Load scalers with exact filenames
        scaler_files = [
            ('high_impact', 'scaler_high_impact.pkl'),
            ('tsunami_risk', 'scaler_tsunami_risk.pkl'),
            ('high_alert', 'scaler_high_alert.pkl')
        ]
        
        for name, filename in scaler_files:
            scaler_path = models_dir / filename
            if scaler_path.exists():
                scalers[name] = joblib.load(scaler_path)
                logger.info(f"✅ Loaded {name} scaler from {filename}")
            else:
                logger.warning(f"⚠️ Scaler file not found: {filename}")
        
        # Load encoders and imputer
        encoders_path = models_dir / "encoders.pkl"
        imputer_path = models_dir / "imputer.pkl"
        
        if encoders_path.exists():
            encoders = joblib.load(encoders_path)
            logger.info(f"✅ Loaded encoders: {list(encoders.keys())}")
        else:
            logger.warning("⚠️ Encoders file not found")
        
        if imputer_path.exists():
            imputer = joblib.load(imputer_path)
            logger.info("✅ Loaded imputer")
        else:
            logger.warning("⚠️ Imputer file not found")
        
        logger.info(f"🤖 Total models loaded: {len(models)}")
        logger.info(f"📊 Available models: {list(models.keys())}")
        return len(models) > 0
        
    except Exception as e:
        logger.error(f"❌ Error loading models: {e}")
        return False

def prepare_features(data):
    """Prepare input data for Random Forest models"""
    try:
        # Extract input values with defaults
        magnitude = float(data.get('magnitude', 6.5))
        depth = float(data.get('depth', 30.0))
        latitude = float(data.get('latitude', 0.0))
        longitude = float(data.get('longitude', 0.0))
        cdi = int(data.get('cdi', 5))
        mmi = int(data.get('mmi', 4))
        sig = int(data.get('sig', 500))
        nst = int(data.get('nst', 50))
        dmin = float(data.get('dmin', 1.0))
        gap = float(data.get('gap', 50.0))
        
        # Categorical features
        magType = data.get('magType', 'mw')
        net = data.get('net', 'us')
        alert = data.get('alert', 'green')
        
        # Create feature vector (matching training order)
        features = pd.DataFrame({
            'magnitude': [magnitude],
            'depth': [depth],
            'latitude': [latitude],
            'longitude': [longitude],
            'cdi': [cdi],
            'mmi': [mmi],
            'sig': [sig],
            'nst': [nst],
            'dmin': [dmin],
            'gap': [gap]
        })
        
        # Feature engineering (same as training)
        features['magnitude_squared'] = features['magnitude'] ** 2
        features['magnitude_cubed'] = features['magnitude'] ** 3
        features['mag_depth_ratio'] = features['magnitude'] / (features['depth'] + 1)
        features['mag_depth_interaction'] = features['magnitude'] * np.log1p(features['depth'])
        features['depth_log'] = np.log1p(features['depth'])
        features['depth_sqrt'] = np.sqrt(features['depth'])
        features['shallow_earthquake'] = (features['depth'] <= 70).astype(int)
        features['distance_from_equator'] = np.abs(features['latitude'])
        features['location_risk'] = np.sqrt(features['latitude']**2 + features['longitude']**2)
        features['sig_log'] = np.log1p(features['sig'])
        features['high_significance'] = (features['sig'] >= 600).astype(int)
        
        # Encode categorical variables
        for cat_feature in ['magType', 'net', 'alert']:
            if cat_feature in encoders:
                try:
                    if cat_feature == 'magType':
                        value = magType
                    elif cat_feature == 'net':
                        value = net
                    else:  # alert
                        value = alert
                    
                    if value in encoders[cat_feature].classes_:
                        features[f'{cat_feature}_encoded'] = encoders[cat_feature].transform([value])
                    else:
                        features[f'{cat_feature}_encoded'] = 0
                except Exception as e:
                    logger.warning(f"Encoding error for {cat_feature}: {e}")
                    features[f'{cat_feature}_encoded'] = 0
            else:
                features[f'{cat_feature}_encoded'] = 0
        
        # Apply imputer if available
        if imputer is not None:
            features_imputed = pd.DataFrame(
                imputer.transform(features), 
                columns=features.columns
            )
        else:
            features_imputed = features
        
        logger.info(f"Features prepared: {features_imputed.shape}")
        return features_imputed
        
    except Exception as e:
        logger.error(f"Error preparing features: {e}")
        raise

def make_predictions(data):
    """Make predictions using all loaded Random Forest models"""
    try:
        # Prepare features
        features = prepare_features(data)
        
        predictions = {}
        
        # Make predictions for each loaded model
        for model_name in models.keys():
            if model_name in scalers:
                logger.info(f"Making prediction with {model_name} model")
                
                # Scale features
                features_scaled = scalers[model_name].transform(features)
                
                # Predict
                prediction = models[model_name].predict(features_scaled)[0]
                probabilities = models[model_name].predict_proba(features_scaled)[0]
                
                predictions[model_name] = {
                    'prediction': int(prediction),
                    'probability': float(probabilities[1]),  # Probability of positive class
                    'risk_level': get_risk_level(probabilities[1]),
                    'confidence': float(max(probabilities))
                }
                
                logger.info(f"{model_name}: {probabilities[1]:.3f} ({get_risk_level(probabilities[1])})")
            else:
                logger.warning(f"No scaler found for {model_name}")
        
        return predictions
        
    except Exception as e:
        logger.error(f"Error making predictions: {e}")
        raise

def get_risk_level(probability):
    """Convert probability to risk level"""
    if probability < 0.3:
        return 'Low'
    elif probability < 0.7:
        return 'Medium'
    else:
        return 'High'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        logger.info(f"Received prediction request: {data}")
        
        # Check if models are loaded
        if not models:
            return jsonify({
                'success': False,
                'error': 'Random Forest models not loaded. Please restart the server.'
            })
        
        # Make predictions
        predictions = make_predictions(data)
        
        logger.info(f"Predictions completed: {list(predictions.keys())}")
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'input_data': data,
            'model_info': {
                'type': 'Random Forest',
                'dataset_size': '1,000 earthquakes',
                'models_used': list(predictions.keys()),
                'high_impact_accuracy': '93.5%',
                'tsunami_risk_accuracy': '91.0%',
                'high_alert_accuracy': '98.5%',
                'features_used': 24,
                'training_data': 'Real earthquake dataset (1996-2019)'
            }
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({
            'success': False,
            'error': f'Prediction failed: {str(e)}'
        })

@app.route('/api/countries')
def get_countries():
    """Get list of earthquake-prone countries"""
    countries = [
        'Japan', 'Indonesia', 'Chile', 'Turkey', 'Iran', 'Italy', 'Greece',
        'Philippines', 'Mexico', 'Peru', 'New Zealand', 'United States',
        'China', 'India', 'Afghanistan', 'Pakistan', 'Ecuador', 'Guatemala'
    ]
    return jsonify(countries)

@app.route('/api/continents')
def get_continents():
    """Get list of continents"""
    continents = ['Asia', 'North America', 'South America', 'Europe', 'Africa', 'Oceania']
    return jsonify(continents)

@app.route('/api/model-status')
def get_model_status():
    """Get detailed status of loaded models"""
    return jsonify({
        'models_loaded': len(models) > 0,
        'available_models': list(models.keys()),
        'model_count': len(models),
        'scalers_loaded': list(scalers.keys()),
        'encoders_loaded': len(encoders) > 0,
        'imputer_loaded': imputer is not None,
        'model_type': 'Random Forest',
        'dataset_info': {
            'source': 'Earthquake dataset (1996-2019)',
            'size': '1,000 earthquakes',
            'features': 24,
            'accuracies': {
                'high_impact': 0.935,
                'tsunami_risk': 0.910,
                'high_alert': 0.985
            }
        }
    })

@app.route('/api/test-prediction')
def test_prediction():
    """Test endpoint with sample data"""
    sample_data = {
        'magnitude': 7.0,
        'depth': 25.0,
        'latitude': 35.0,
        'longitude': 139.0,
        'cdi': 6,
        'mmi': 5,
        'sig': 700,
        'magType': 'mw',
        'alert': 'yellow'
    }
    
    try:
        predictions = make_predictions(sample_data)
        return jsonify({
            'success': True,
            'sample_input': sample_data,
            'predictions': predictions,
            'models_used': list(predictions.keys())
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("🌍 Random Forest Earthquake Prediction System")
    print("=" * 55)
    
    # Load models
    if load_rf_models():
        print("🚀 Starting server with Random Forest models...")
        print(f"🤖 Models loaded: {len(models)}")
        print(f"📊 Available models: {list(models.keys())}")
        print("📊 Dataset: 1,000 earthquakes (1996-2019)")
        print("🎯 Accuracies: High Impact 93.5%, Tsunami 91.0%, Alert 98.5%")
        print("🌐 Server starting at: http://localhost:5002")
        app.run(debug=True, host='0.0.0.0', port=5002)
    else:
        print("❌ Failed to load Random Forest models.")
        print("💡 Run: python train_earthquake_rf.py")
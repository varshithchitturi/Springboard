# 🌍 Earthquake Impact Predictor

A stunning AI-powered web application that predicts earthquake impact and tsunami risk using machine learning models trained on historical seismic data.

## ✨ Features

- **🎯 Dual Prediction Models**: High Impact Risk & Tsunami Risk assessment
- **🎨 Stunning Modern UI**: Responsive design with animations and interactive elements
- **📊 Real-time Predictions**: Instant ML-powered risk assessment
- **🗺️ Geographic Intelligence**: Auto-location filling based on country selection
- **📱 Mobile Responsive**: Works perfectly on all devices
- **💡 Smart Recommendations**: Context-aware emergency response suggestions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Easy Installation (Recommended)

1. **Download the project files**

2. **Run the automated setup**
   ```bash
   python setup.py
   ```
   This will automatically:
   - Install all required packages
   - Set up machine learning models
   - Verify everything is working
   - Optionally start the application

### Manual Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare the models**
   
   **Option A: Use existing trained models (Recommended)**
   ```bash
   python extract_models.py
   ```
   
   **Option B: Train new models from dataset**
   - Ensure `earthquake_1995-2023.csv` is in the project directory
   - Run: `python extract_models.py`
   - The script will automatically detect and use the dataset
   
   **Option C: Train models using Jupyter notebook**
   - Run the `infosis (1).ipynb` notebook to train the models
   - Then run: `python extract_models.py`

3. **Start the application**
   ```bash
   python app.py
   ```

4. **Test the application (Optional)**
   ```bash
   python test_app.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:5000`
   - Start predicting earthquake impacts! 🎉

## 🏗️ Project Structure

```
earthquake-predictor/
├── app.py                 # Flask backend application
├── extract_models.py      # Model preparation script
├── requirements.txt       # Python dependencies
├── infosis (1).ipynb     # Original ML training notebook
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── css/
│   │   └── style.css     # Stunning UI styles
│   └── js/
│       └── script.js     # Interactive frontend logic
└── models/               # Trained ML models directory
    ├── rf_high_impact.joblib
    └── rf_tsunami.joblib
```

## 🎯 How It Works

### Machine Learning Models

The application uses two Random Forest classifiers with intelligent preprocessing:

1. **High Impact Classifier**: Predicts if an earthquake will cause significant damage
   - **Features**: Magnitude, depth, location, CDI, MMI, significance, alert level
   - **Target**: Top 25% of earthquakes by impact score (significance-based)
   - **Preprocessing**: StandardScaler for numeric features, OneHotEncoder for categorical
   - **Algorithm**: Random Forest with 100 estimators, max depth 10

2. **Tsunami Classifier**: Predicts tsunami occurrence probability
   - **Features**: Same as high impact model plus geographic factors
   - **Target**: Historical tsunami occurrences from earthquake database
   - **Special consideration**: Coastal proximity and underwater earthquake depth
   - **Algorithm**: Random Forest optimized for tsunami prediction patterns

### Input Parameters

- **📍 Location**: Latitude, longitude, country, continent
- **📊 Magnitude**: Richter scale measurement (1.0-10.0)
- **⬇️ Depth**: Earthquake depth in kilometers (0-700)
- **🚨 Alert Level**: None, Green, Yellow, Orange, Red
- **⚙️ Technical**: Magnitude type, monitoring network

### Prediction Output

- **Risk Probability**: Percentage likelihood (0-100%)
- **Risk Level**: Low, Medium, High classification
- **Visual Indicators**: Color-coded cards and animated probability circles
- **Smart Recommendations**: Context-aware emergency response suggestions

## 🎨 UI Features

- **Gradient Backgrounds**: Beautiful color transitions
- **Glass Morphism**: Modern frosted glass effects
- **Smooth Animations**: CSS animations and transitions
- **Interactive Elements**: Hover effects and micro-interactions
- **Responsive Design**: Perfect on desktop, tablet, and mobile
- **Loading States**: Elegant loading animations
- **Real-time Validation**: Instant input feedback

## 🔧 API Endpoints

### Main Endpoints
- `GET /` - Main application interface
- `POST /predict` - Earthquake prediction endpoint

### Data Endpoints  
- `GET /api/countries` - Available countries list
- `GET /api/continents` - Available continents list

### Prediction Request Format
```json
{
  "magnitude": 7.2,
  "depth": 15.0,
  "latitude": 35.6762,
  "longitude": 139.6503,
  "cdi": 8.0,
  "mmi": 7.5,
  "sig": 800,
  "alert": "red",
  "magType": "mw",
  "net": "us",
  "continent": "Asia",
  "country": "Japan"
}
```

### Prediction Response Format
```json
{
  "success": true,
  "predictions": {
    "high_impact": {
      "prediction": 1,
      "probability": 0.85,
      "risk_level": "High"
    },
    "tsunami": {
      "prediction": 1,
      "probability": 0.72,
      "risk_level": "High"
    }
  },
  "input_data": {...}
}
```

## 📊 Use Cases

### 🏙️ Urban Risk Assessment
Predict earthquake impact in populated regions for city planning and emergency preparedness.

### 🏗️ Infrastructure Planning  
Guide construction policies and building codes in high-risk seismic zones.

### 🚨 Emergency Response
Prioritize rescue operations and resource allocation based on predicted impact levels.

### 🌊 Tsunami Warning Systems
Early tsunami risk assessment for coastal evacuation planning.

## 🛠️ Technical Details

### Backend (Flask)
- **Framework**: Flask 2.3.3 with optimized performance settings
- **ML Pipeline**: Scikit-learn with joblib model serialization
- **Preprocessing**: ColumnTransformer with StandardScaler and OneHotEncoder
- **Caching**: Intelligent prediction caching for improved response times
- **Error Handling**: Graceful fallback to simulation algorithms if models fail
- **API Design**: RESTful endpoints with comprehensive JSON responses

### Machine Learning Pipeline
- **Data Processing**: Automated missing value imputation
- **Feature Engineering**: Numeric standardization and categorical encoding
- **Model Architecture**: Random Forest with hyperparameter optimization
- **Validation**: Cross-validation and performance metrics tracking
- **Deployment**: Joblib serialization for fast model loading

### Frontend (Vanilla JS)
- **Modern JavaScript**: ES6+ with async/await patterns
- **API Integration**: Fetch API for seamless backend communication
- **User Experience**: Real-time form validation and loading states
- **Responsive Design**: Mobile-first approach with progressive enhancement
- **Animations**: Smooth transitions and micro-interactions

### Styling (CSS3)
- **Layout**: CSS Grid and Flexbox for responsive layouts
- **Design System**: Consistent color palette and typography
- **Animations**: CSS transitions and keyframe animations
- **Accessibility**: WCAG compliant color contrasts and focus states
- **Performance**: Optimized CSS with minimal render blocking

## 🔮 Future Enhancements

### Immediate Roadmap
- **🗺️ Interactive Maps**: Plotly/Leaflet integration for geographic visualization
- **📈 Historical Data**: Charts showing earthquake trends and patterns
- **🔔 Real-time Alerts**: WebSocket integration for live earthquake feeds
- **📊 Model Performance**: Real-time accuracy metrics and model comparison

### Advanced Features
- **📱 PWA Support**: Offline functionality and mobile app features
- **🌐 Multi-language**: Internationalization support (i18n)
- **🤖 Advanced ML**: Deep learning models and ensemble methods
- **📊 Advanced Analytics**: Detailed risk assessment reports and insights
- **🔗 API Integration**: Real-time earthquake data feeds (USGS, EMSC)
- **👥 User Accounts**: Personalized dashboards and alert preferences

### Technical Improvements
- **⚡ Performance**: Redis caching and database optimization
- **🔒 Security**: Authentication, rate limiting, and input sanitization
- **📈 Scalability**: Docker containerization and cloud deployment
- **🧪 Testing**: Comprehensive unit and integration test suites
- **📝 Documentation**: API documentation with Swagger/OpenAPI

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup
1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Install dependencies: `python setup.py`
4. Create a feature branch: `git checkout -b feature/amazing-feature`
5. Make your changes
6. Test your changes: `python test_app.py`
7. Commit your changes: `git commit -m 'Add amazing feature'`
8. Push to the branch: `git push origin feature/amazing-feature`
9. Open a Pull Request

### Areas for Contribution
- 🐛 **Bug Fixes**: Report and fix issues
- ✨ **New Features**: Implement enhancements from the roadmap
- 📚 **Documentation**: Improve README, add code comments
- 🧪 **Testing**: Add unit tests and integration tests
- 🎨 **UI/UX**: Improve the user interface and experience
- 🤖 **ML Models**: Enhance prediction accuracy and add new models

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Write tests for new features

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

### Data Sources
- **Seismic Data**: Global earthquake databases (USGS, EMSC)
- **Geographic Data**: Country and continent mapping datasets
- **Historical Records**: Tsunami occurrence databases

### Technology Stack
- **ML Framework**: Scikit-learn for robust machine learning pipelines
- **Web Framework**: Flask for lightweight and efficient web services
- **Data Processing**: Pandas and NumPy for data manipulation
- **Visualization**: Matplotlib and Seaborn for data analysis

### Design & Inspiration
- **UI/UX**: Modern web design principles and accessibility standards
- **Icons**: Font Awesome icon library
- **Color Palette**: Earthquake-themed color schemes
- **Typography**: Clean, readable font selections

### Special Thanks
- **Open Source Community**: For the amazing tools and libraries
- **Seismology Research**: Scientists and researchers providing earthquake data
- **Disaster Preparedness**: Organizations working on earthquake safety
- **Beta Testers**: Early users who provided valuable feedback

---

## 📞 Support

If you encounter any issues or have questions:

1. **Check the troubleshooting section** in this README
2. **Run the test script**: `python test_app.py`
3. **Check the console output** for error messages
4. **Verify all files are present** using the setup script

### Common Issues

**Models not loading?**
- Run `python extract_models.py` to regenerate models
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**App won't start?**
- Check if port 5000 is available
- Verify Python version (3.8+ required)
- Run `python setup.py` for automated troubleshooting

**Predictions seem inaccurate?**
- Dummy models are used if real training data isn't available
- Train with actual earthquake data for better accuracy
- Check that `earthquake_1995-2023.csv` is in the project directory

---

**Built with ❤️ for earthquake preparedness and public safety**

*Empowering communities with AI-driven earthquake impact predictions to enhance disaster preparedness and save lives.*

🌍 **Making the world safer, one prediction at a time** 🌍
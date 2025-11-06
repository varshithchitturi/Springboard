// Random Forest Earthquake Prediction Script
console.log('🚀 Random Forest Earthquake Predictor Script Loaded');

// Global variables
let predictionForm, resultsSection, loadingOverlay, countrySelect, continentSelect;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 DOM Content Loaded');
    
    // Get DOM elements
    predictionForm = document.getElementById('predictionForm');
    resultsSection = document.getElementById('resultsSection');
    loadingOverlay = document.getElementById('loadingOverlay');
    countrySelect = document.getElementById('country');
    continentSelect = document.getElementById('continent');
    
    console.log('🔍 Elements check:');
    console.log('   Form:', !!predictionForm);
    console.log('   Results:', !!resultsSection);
    console.log('   Loading:', !!loadingOverlay);
    console.log('   Country:', !!countrySelect);
    console.log('   Continent:', !!continentSelect);
    
    // Load data
    loadCountries();
    loadContinents();
    
    // Setup event listeners
    if (predictionForm) {
        predictionForm.addEventListener('submit', handleFormSubmit);
    }
    
    if (countrySelect) {
        countrySelect.addEventListener('change', function() {
            autoFillContinent(this.value);
        });
    }
    
    console.log('✅ Random Forest initialization complete');
});

// Load countries from API
async function loadCountries() {
    console.log('📡 Loading countries...');
    
    if (!countrySelect) {
        console.error('❌ Country select element not found');
        return;
    }
    
    try {
        const response = await fetch('/api/countries');
        console.log('📨 Countries API response:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const countries = await response.json();
        console.log('📊 Countries received:', countries.length, 'countries');
        
        // Clear and populate
        countrySelect.innerHTML = '<option value="">Select Country</option>';
        
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            countrySelect.appendChild(option);
        });
        
        console.log('✅ Countries loaded successfully');
        
    } catch (error) {
        console.error('❌ Error loading countries:', error);
        showNotification('Failed to load countries', 'error');
    }
}

// Load continents from API
async function loadContinents() {
    console.log('📡 Loading continents...');
    
    if (!continentSelect) {
        console.error('❌ Continent select element not found');
        return;
    }
    
    try {
        const response = await fetch('/api/continents');
        console.log('📨 Continents API response:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const continents = await response.json();
        console.log('📊 Continents received:', continents);
        
        // Clear and populate
        continentSelect.innerHTML = '<option value="">Select Continent</option>';
        
        continents.forEach(continent => {
            const option = document.createElement('option');
            option.value = continent;
            option.textContent = continent;
            continentSelect.appendChild(option);
        });
        
        console.log('✅ Continents loaded successfully');
        
    } catch (error) {
        console.error('❌ Error loading continents:', error);
        showNotification('Failed to load continents', 'error');
    }
}

// Auto-fill continent based on country
function autoFillContinent(country) {
    const countryToContinent = {
        'Japan': 'Asia',
        'Indonesia': 'Asia',
        'Chile': 'South America',
        'Turkey': 'Asia',
        'Iran': 'Asia',
        'Italy': 'Europe',
        'Greece': 'Europe',
        'Philippines': 'Asia',
        'Mexico': 'North America',
        'Peru': 'South America',
        'New Zealand': 'Oceania',
        'United States': 'North America',
        'China': 'Asia',
        'India': 'Asia',
        'Afghanistan': 'Asia',
        'Pakistan': 'Asia',
        'Ecuador': 'South America',
        'Guatemala': 'North America'
    };
    
    if (countryToContinent[country] && continentSelect) {
        continentSelect.value = countryToContinent[country];
        console.log(`🗺️ Auto-filled continent: ${countryToContinent[country]} for ${country}`);
    }
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    console.log('📝 Form submitted for Random Forest prediction');
    
    // Get form data
    const formData = new FormData(predictionForm);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        if (value !== '') {
            if (['magnitude', 'depth', 'cdi', 'mmi', 'sig', 'nst', 'dmin', 'gap', 'latitude', 'longitude'].includes(key)) {
                data[key] = parseFloat(value);
            } else {
                data[key] = value;
            }
        }
    }
    
    // Add defaults for Random Forest model
    data.cdi = data.cdi || 5;
    data.mmi = data.mmi || 4;
    data.sig = data.sig || 500;
    data.nst = data.nst || 50;
    data.dmin = data.dmin || 1.0;
    data.gap = data.gap || 50.0;
    data.net = data.net || 'us';
    data.latitude = data.latitude || 0.0;
    data.longitude = data.longitude || 0.0;
    
    console.log('📊 Sending Random Forest data:', data);
    
    // Show loading
    showLoading();
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        console.log('📨 Random Forest prediction response:', response.status);
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('📊 Random Forest prediction result:', result);
        
        if (result.success) {
            displayRandomForestResults(result.predictions, result.model_info);
            showNotification('Random Forest prediction completed successfully!', 'success');
        } else {
            throw new Error(result.error || 'Random Forest prediction failed');
        }
        
    } catch (error) {
        console.error('❌ Random Forest prediction error:', error);
        showNotification(`Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Display Random Forest results
function displayRandomForestResults(predictions, modelInfo) {
    console.log('🎯 Displaying Random Forest results:', predictions);
    
    if (!resultsSection) {
        console.error('❌ Results section not found');
        return;
    }
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Update cards based on available predictions
    if (predictions.high_impact) {
        updateResultCard('highImpact', predictions.high_impact);
    }
    
    if (predictions.tsunami_risk) {
        updateResultCard('tsunamiRisk', predictions.tsunami_risk);
    }
    
    if (predictions.high_alert) {
        updateResultCard('highAlert', predictions.high_alert);
    }
    
    // Update model info display
    updateModelInfo(modelInfo);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Update result card
function updateResultCard(type, prediction) {
    const probability = Math.round(prediction.probability * 100);
    const riskLevel = prediction.risk_level.toLowerCase();
    
    // Get elements
    const circle = document.getElementById(`${type}Circle`);
    const probSpan = document.getElementById(`${type}Prob`);
    const levelDiv = document.getElementById(`${type}Level`);
    const textDiv = document.getElementById(`${type}Text`);
    const card = document.getElementById(`${type}Card`);
    
    if (!circle || !probSpan || !levelDiv || !textDiv || !card) {
        console.error(`❌ Missing elements for ${type} card`);
        return;
    }
    
    // Update probability display
    probSpan.textContent = `${probability}%`;
    
    // Update circle gradient based on risk level
    let circleColor;
    if (riskLevel === 'high') {
        circleColor = '#e53e3e';
    } else if (riskLevel === 'medium') {
        circleColor = '#dd6b20';
    } else {
        circleColor = '#38a169';
    }
    
    const angle = (probability / 100) * 360;
    circle.style.background = `conic-gradient(${circleColor} 0deg, ${circleColor} ${angle}deg, #e2e8f0 ${angle}deg)`;
    
    // Update risk level
    levelDiv.textContent = prediction.risk_level;
    levelDiv.className = `risk-level ${riskLevel}`;
    
    // Update card styling
    card.className = `result-card ${riskLevel}-risk`;
    
    // Update text based on Random Forest predictions
    const texts = {
        highImpact: {
            high: 'High probability of significant damage and casualties',
            medium: 'Moderate probability of damage and some casualties',
            low: 'Low probability of significant impact'
        },
        tsunamiRisk: {
            high: 'High probability of tsunami generation',
            medium: 'Moderate probability of local tsunami',
            low: 'Low probability of tsunami occurrence'
        },
        highAlert: {
            high: 'High probability of emergency alert activation',
            medium: 'Moderate probability of alert activation',
            low: 'Low probability of emergency alert'
        }
    };
    
    if (texts[type] && texts[type][riskLevel]) {
        textDiv.textContent = texts[type][riskLevel];
    }
    
    console.log(`✅ Updated ${type} card: ${probability}% (${prediction.risk_level})`);
}

// Update model info display
function updateModelInfo(modelInfo) {
    if (!modelInfo) return;
    
    // Create or update model info section
    let modelInfoSection = document.getElementById('modelInfoSection');
    if (!modelInfoSection) {
        modelInfoSection = document.createElement('div');
        modelInfoSection.id = 'modelInfoSection';
        modelInfoSection.className = 'model-info-section';
        resultsSection.appendChild(modelInfoSection);
    }
    
    modelInfoSection.innerHTML = `
        <h3><i class="fas fa-robot"></i> Random Forest Model Information</h3>
        <div class="model-info-grid">
            <div class="info-item">
                <span class="info-label">Model Type:</span>
                <span class="info-value">${modelInfo.type || 'Random Forest'}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Dataset Size:</span>
                <span class="info-value">${modelInfo.dataset_size || 'Unknown'}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Features Used:</span>
                <span class="info-value">${modelInfo.features_used || 'Unknown'}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Training Data:</span>
                <span class="info-value">${modelInfo.training_data || 'Unknown'}</span>
            </div>
        </div>
        <div class="accuracy-info">
            <h4>Model Accuracies:</h4>
            <div class="accuracy-grid">
                <div class="accuracy-item">
                    <span>High Impact:</span>
                    <span class="accuracy-value">${modelInfo.high_impact_accuracy || 'N/A'}</span>
                </div>
                <div class="accuracy-item">
                    <span>Tsunami Risk:</span>
                    <span class="accuracy-value">${modelInfo.tsunami_risk_accuracy || 'N/A'}</span>
                </div>
                <div class="accuracy-item">
                    <span>High Alert:</span>
                    <span class="accuracy-value">${modelInfo.high_alert_accuracy || 'N/A'}</span>
                </div>
            </div>
        </div>
    `;
}

// Show loading overlay
function showLoading() {
    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
        const loadingText = document.getElementById('loadingText');
        if (loadingText) {
            loadingText.textContent = 'Processing with Random Forest models...';
        }
        console.log('🔄 Loading overlay shown');
    }
}

// Hide loading overlay
function hideLoading() {
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
        console.log('✅ Loading overlay hidden');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    console.log(`📢 ${type.toUpperCase()}: ${message}`);
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">×</button>
    `;
    
    // Add styles if not present
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 10px;
                color: white;
                z-index: 10000;
                display: flex;
                align-items: center;
                gap: 10px;
                animation: slideIn 0.3s ease;
                max-width: 400px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            .notification.success { background: #48bb78; }
            .notification.error { background: #f56565; }
            .notification.info { background: #4299e1; }
            .notification button {
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                padding: 0;
                margin-left: auto;
            }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            .model-info-section {
                margin-top: 20px;
                padding: 20px;
                background: #f7fafc;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
            }
            .model-info-grid, .accuracy-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 10px;
                margin-top: 10px;
            }
            .info-item, .accuracy-item {
                display: flex;
                justify-content: space-between;
                padding: 8px 12px;
                background: white;
                border-radius: 6px;
                border: 1px solid #e2e8f0;
            }
            .info-label {
                font-weight: 600;
                color: #4a5568;
            }
            .info-value, .accuracy-value {
                color: #2d3748;
                font-weight: 500;
            }
            .accuracy-value {
                color: #38a169;
                font-weight: 600;
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}
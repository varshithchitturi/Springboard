// DOM Elements
let predictionForm, resultsSection, loadingOverlay, countrySelect, continentSelect;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('App Initializing...');
    
    // Get DOM elements
    predictionForm = document.getElementById('predictionForm');
    resultsSection = document.getElementById('resultsSection');
    loadingOverlay = document.getElementById('loadingOverlay');
    countrySelect = document.getElementById('country');
    continentSelect = document.getElementById('continent');
    
    // Check if all required elements exist
    if (!predictionForm || !resultsSection || !loadingOverlay || !countrySelect || !continentSelect) {
        console.error('Missing required elements');
        return;
    }
    
    console.log('All elements found');
    
    loadCountries();
    loadContinents();
    setupEventListeners();
    
    console.log('App initialization complete');
});

// Load countries from API
async function loadCountries() {
    try {
        console.log('Loading countries...');
        const response = await fetch('/api/countries');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const countries = await response.json();
        console.log('Countries loaded:', countries);
        
        // Clear existing options except the first one
        countrySelect.innerHTML = '<option value="">Select Country</option>';
        
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            countrySelect.appendChild(option);
        });
        
        console.log('Country dropdown populated');
    } catch (error) {
        console.error('Error loading countries:', error);
        // Add some default countries if API fails
        const defaultCountries = ['Japan', 'Indonesia', 'Chile', 'Turkey', 'United States'];
        defaultCountries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            countrySelect.appendChild(option);
        });
    }
}

// Load continents from API
async function loadContinents() {
    try {
        console.log('Loading continents...');
        const response = await fetch('/api/continents');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const continents = await response.json();
        console.log('Continents loaded:', continents);
        
        // Clear existing options except the first one
        continentSelect.innerHTML = '<option value="">Select Continent</option>';
        
        continents.forEach(continent => {
            const option = document.createElement('option');
            option.value = continent;
            option.textContent = continent;
            continentSelect.appendChild(option);
        });
        
        console.log('Continent dropdown populated');
    } catch (error) {
        console.error('Error loading continents:', error);
        // Add some default continents if API fails
        const defaultContinents = ['Asia', 'North America', 'South America', 'Europe', 'Africa', 'Oceania'];
        defaultContinents.forEach(continent => {
            const option = document.createElement('option');
            option.value = continent;
            option.textContent = continent;
            continentSelect.appendChild(option);
        });
    }
}

// Setup event listeners
function setupEventListeners() {
    predictionForm.addEventListener('submit', handleFormSubmit);
    
    // Auto-fill location based on country selection
    countrySelect.addEventListener('change', function() {
        console.log('Country changed to:', this.value);
        autoFillLocation(this.value);
    });
}

// Auto-fill continent based on country selection
function autoFillLocation(country) {
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
    
    if (countryToContinent[country]) {
        continentSelect.value = countryToContinent[country];
        console.log('Auto-filled continent:', countryToContinent[country]);
    }
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    console.log('Form submitted');
    
    // Prevent multiple submissions
    const submitBtn = event.target.querySelector('.predict-btn');
    if (submitBtn.disabled) return;
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    
    showLoading();
    
    // Collect form data
    const formData = new FormData(predictionForm);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        if (value !== '') {
            // Convert numeric fields
            if (['magnitude', 'depth'].includes(key)) {
                data[key] = parseFloat(value);
            } else {
                data[key] = value;
            }
        }
    }
    
    // Add default values for missing fields
    data.cdi = data.cdi || 0;
    data.mmi = data.mmi || 0;
    data.sig = data.sig || 0;
    data.net = data.net || 'us';
    
    console.log('Sending data:', data);
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Prediction result:', result);
        
        if (result.success) {
            displayResults(result.predictions);
        } else {
            showError(result.error || 'Prediction failed');
        }
    } catch (error) {
        console.error('Request failed:', error);
        showError('Cannot connect to server. Please check if the application is running.');
    } finally {
        hideLoading();
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-brain"></i> Predict Impact';
    }
}

// Display prediction results
function displayResults(predictions) {
    console.log('Displaying results:', predictions);
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Update high impact prediction
    if (predictions.high_impact) {
        updateResultCard('highImpact', predictions.high_impact);
    }
    
    // Update tsunami prediction
    if (predictions.tsunami) {
        updateResultCard('tsunami', predictions.tsunami);
    }
    
    // Generate recommendations
    generateRecommendations(predictions);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Update individual result card
function updateResultCard(type, prediction) {
    console.log(`Updating ${type} card:`, prediction);
    
    const probability = Math.round(prediction.probability * 100);
    const riskLevel = prediction.risk_level.toLowerCase();
    
    // Update probability circle
    const circle = document.getElementById(`${type}Circle`);
    const probSpan = document.getElementById(`${type}Prob`);
    const levelDiv = document.getElementById(`${type}Level`);
    const textDiv = document.getElementById(`${type}Text`);
    const card = document.getElementById(`${type}Card`);
    
    if (!circle || !probSpan || !levelDiv || !textDiv || !card) {
        console.error(`Missing elements for ${type}`);
        return;
    }
    
    // Update probability display
    probSpan.textContent = `${probability}%`;
    
    // Update circle gradient based on probability
    const angle = (probability / 100) * 360;
    circle.style.background = `conic-gradient(#667eea 0deg, #764ba2 ${angle}deg, #e1e5e9 ${angle}deg)`;
    
    // Update risk level
    levelDiv.textContent = prediction.risk_level;
    levelDiv.className = `risk-level ${riskLevel}`;
    
    // Update card styling
    card.className = `result-card ${riskLevel}-risk`;
    
    // Update prediction text
    const predictionTexts = {
        highImpact: {
            high: 'High probability of significant damage and casualties',
            medium: 'Moderate probability of damage and some casualties',
            low: 'Low probability of significant impact'
        },
        tsunami: {
            high: 'High probability of tsunami generation',
            medium: 'Moderate probability of local tsunami',
            low: 'Low probability of tsunami occurrence'
        }
    };
    
    textDiv.textContent = predictionTexts[type][riskLevel];
    
    console.log(`${type} card updated successfully`);
}

// Generate recommendations based on predictions
function generateRecommendations(predictions) {
    const recommendationsList = document.getElementById('recommendationsList');
    const recommendations = [];
    
    // High impact recommendations
    if (predictions.high_impact) {
        const highImpactRisk = predictions.high_impact.risk_level.toLowerCase();
        
        if (highImpactRisk === 'high') {
            recommendations.push({
                icon: 'fas fa-exclamation-triangle',
                text: 'Immediate evacuation of vulnerable structures and areas prone to landslides.'
            });
            recommendations.push({
                icon: 'fas fa-hospital',
                text: 'Alert emergency services and prepare medical facilities for potential casualties.'
            });
        } else if (highImpactRisk === 'medium') {
            recommendations.push({
                icon: 'fas fa-shield-alt',
                text: 'Review building safety protocols and prepare emergency response teams.'
            });
        }
    }
    
    // Tsunami recommendations
    if (predictions.tsunami) {
        const tsunamiRisk = predictions.tsunami.risk_level.toLowerCase();
        
        if (tsunamiRisk === 'high') {
            recommendations.push({
                icon: 'fas fa-water',
                text: 'Issue tsunami warning for coastal areas and initiate immediate evacuation.'
            });
        } else if (tsunamiRisk === 'medium') {
            recommendations.push({
                icon: 'fas fa-eye',
                text: 'Monitor sea level changes and prepare coastal evacuation plans.'
            });
        }
    }
    
    // General recommendations
    recommendations.push({
        icon: 'fas fa-phone',
        text: 'Ensure communication systems are operational for emergency coordination.'
    });
    
    recommendations.push({
        icon: 'fas fa-users',
        text: 'Inform the public about earthquake safety measures and evacuation routes.'
    });
    
    // Render recommendations
    recommendationsList.innerHTML = recommendations.map(rec => `
        <div class="recommendation-item">
            <i class="${rec.icon}"></i>
            ${rec.text}
        </div>
    `).join('');
}

// Show loading overlay
function showLoading() {
    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
    }
}

// Hide loading overlay
function hideLoading() {
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
}

// Show error message
function showError(message) {
    console.error('Error:', message);
    alert('Error: ' + message);
}
document.addEventListener('DOMContentLoaded', function() {
    // Set default date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const tomorrowStr = tomorrow.toISOString().split('T')[0];
    document.getElementById('date').value = tomorrowStr;
    
    // Get DOM elements
    const predictBtn = document.getElementById('predict-btn');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    
    predictBtn.addEventListener('click', async function() {
        // Clear previous results/errors
        resultDiv.style.display = 'none';
        errorDiv.style.display = 'none';
        
        // Get form values
        const date = document.getElementById('date').value;
        const currentTemp = document.getElementById('current_temp').value;
        const humidity = document.getElementById('humidity').value;
        const pressure = document.getElementById('pressure').value;
        const windSpeed = document.getElementById('wind_speed').value;
        const windDirection = document.getElementById('wind_direction').value;
        const cloudCover = document.getElementById('cloud_cover').value;
        const climateCondition = document.getElementById('climate_condition').value;
        
        // Validate date is in the future
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const selectedDate = new Date(date);
        
        if (selectedDate <= today) {
            showError("Please select a future date for prediction.");
            return;
        }
        
        try {
            // Show loading state
            predictBtn.disabled = true;
            predictBtn.textContent = 'Predicting...';
            
            // Make API request
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    date: date,
                    current_temp: currentTemp,
                    humidity: humidity,
                    pressure: pressure,
                    wind_speed: windSpeed,
                    wind_direction: windDirection,
                    cloud_cover: cloudCover,
                    climate_condition: climateCondition
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showPrediction(data.prediction);
            } else {
                showError(data.error || "Prediction failed. Please try again.");
            }
        } catch (error) {
            console.error('Error:', error);
            showError("Failed to connect to the prediction server.");
        } finally {
            // Reset button state
            predictBtn.disabled = false;
            predictBtn.textContent = 'Predict Weather';
        }
    });
    
    function showPrediction(prediction) {
        // Update DOM with prediction data
        document.getElementById('prediction-date').textContent = 
            prediction.date;
        document.getElementById('prediction-temp').textContent = 
            `${prediction.predicted_temp}°C`;
        document.getElementById('prediction-climate').textContent = 
            prediction.climate_condition;
        document.getElementById('prediction-precip').textContent = 
            `${prediction.predicted_precip} mm`;
        document.getElementById('prediction-visibility').textContent = 
            `${prediction.predicted_visibility} km`;
        
        // Show result card with animation
        resultDiv.style.display = 'block';
        resultDiv.style.animation = 'fadeIn 0.5s ease forwards';
    }
    
    function showError(message) {
        errorDiv.querySelector('.error-message').textContent = message;
        errorDiv.style.display = 'block';
        errorDiv.style.animation = 'fadeIn 0.5s ease forwards';
    }
});
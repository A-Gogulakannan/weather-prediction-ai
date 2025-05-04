document.addEventListener('DOMContentLoaded', function() {
    const predictBtn = document.getElementById('predict-btn');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    
    // Set default date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    document.getElementById('date').value = tomorrow.toISOString().split('T')[0];
    
    predictBtn.addEventListener('click', async function() {
        // Clear previous results
        resultDiv.style.display = 'none';
        errorDiv.style.display = 'none';
        
        // Get all input values
        const inputs = {
            date: document.getElementById('date').value,
            current_temp: document.getElementById('current_temp').value,
            humidity: document.getElementById('humidity').value,
            pressure: document.getElementById('pressure').value,
            wind_speed: document.getElementById('wind_speed').value,
            wind_direction: document.getElementById('wind_direction').value,
            cloud_cover: document.getElementById('cloud_cover').value,
            climate_condition: document.getElementById('climate_condition').value
        };
        
        // Validate date is in the future
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const selectedDate = new Date(inputs.date);
        
        if (selectedDate <= today) {
            showError("Please select a future date for prediction.");
            return;
        }
        
        try {
            // Show loading state
            predictBtn.disabled = true;
            predictBtn.textContent = 'Calculating...';
            
            // Make API request
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(inputs)
            });
            
            const data = await response.json();
            
            if (data.success) {
                console.log("Prediction data:", data);
                showPrediction(data.prediction);
                document.getElementById('calculation-time').textContent = 
                    `Calculated at: ${data.calculation_time}`;
            } else {
                showError(data.error || "Prediction calculation failed");
            }
        } catch (error) {
            console.error('Error:', error);
            showError("Failed to connect to prediction service");
        } finally {
            // Reset button
            predictBtn.disabled = false;
            predictBtn.textContent = 'Calculate Prediction';
        }
    });
    
    function showPrediction(prediction) {
        // Update all prediction fields
        document.getElementById('prediction-date').textContent = prediction.date;
        document.getElementById('prediction-temp').textContent = `${prediction.predicted_temp}°C`;
        document.getElementById('prediction-climate').textContent = prediction.likely_climate;
        document.getElementById('prediction-precip').textContent = `${prediction.predicted_precip} mm`;
        document.getElementById('prediction-visibility').textContent = `${prediction.predicted_visibility} km`;
        document.getElementById('prediction-cloud').textContent = `${prediction.predicted_cloud}%`;
        document.getElementById('prediction-wind').textContent = 
            `${prediction.predicted_wind_speed.toFixed(1)} km/h at ${prediction.input_parameters.wind_direction}°`;
        
        // Show result
        resultDiv.style.display = 'block';
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    }
    
    function showError(message) {
        errorDiv.querySelector('.error-message').textContent = message;
        errorDiv.style.display = 'block';
    }
});
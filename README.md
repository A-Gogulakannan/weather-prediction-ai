# Weather Prediction Web Application

A Flask-based web application that predicts weather conditions using machine learning (Random Forest Regressor).

## Features

- Predict temperature, precipitation, and cloud cover
- Interactive web interface
- Machine learning model trained on historical weather patterns
- Real-time predictions based on input parameters

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. The application will automatically:
   - Generate sample weather data (if not present)
   - Train the prediction model (on first run)
   - Start the web server on port 5000

## Usage

1. Enter the required weather parameters in the web interface:
   - Date
   - Current temperature (optional)
   - Humidity (%)
   - Atmospheric pressure (hPa)
   - Wind speed (km/h)
   - Wind direction (degrees)
   - Cloud cover (%)
   - Climate condition

2. Click "Predict" to get weather predictions including:
   - Predicted temperature
   - Predicted precipitation
   - Predicted cloud cover
   - Predicted visibility
   - Likely climate condition

## Project Structure

```
.
├── app.py              # Flask application and routes
├── model.py            # ML model training and prediction logic
├── requirements.txt    # Python dependencies
├── data/              # Generated weather data
├── templates/         # HTML templates
├── static/            # CSS, JavaScript, images
└── weather_model.pkl  # Trained model (generated on first run)
```

## Dependencies

- Flask 2.0.1
- pandas 1.3.3
- scikit-learn 0.24.2
- numpy 1.21.2
- matplotlib 3.4.3

## Notes

- The model uses Random Forest Regressor with 200 estimators
- Sample data covers weather patterns from 2020-2023
- The application runs in debug mode by default
- Model retraining can be triggered by deleting `weather_model.pkl`
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime

def generate_sample_data():
    """Generate more comprehensive sample weather data"""
    dates = pd.date_range(start="2020-01-01", end="2023-12-31")
    temps = np.sin(np.linspace(0, 10*np.pi, len(dates))) * 15 + 25  # Seasonal pattern
    
    df = pd.DataFrame({
        'date': dates,
        'temperature': temps + np.random.normal(0, 3, len(dates)),
        'humidity': np.clip(np.random.normal(60, 15, len(dates)), 20, 95),
        'pressure': np.clip(np.random.normal(1013, 7, len(dates)), 980, 1040),
        'wind_speed': np.clip(np.random.weibull(2, len(dates)) * 10),  # km/h
        'wind_direction': np.random.randint(0, 360, len(dates)),
        'precipitation': np.random.exponential(0.5, len(dates)),
        'cloud_cover': np.random.randint(0, 100, len(dates)),  # percentage
        'visibility': np.clip(np.random.normal(10, 3, len(dates)), 1, 20),  # km
        'climate_condition': np.random.choice(['Clear', 'Partly Cloudy', 'Cloudy', 'Rain', 'Thunderstorm'], len(dates))
    })
    
    # Convert climate condition to numerical values
    climate_map = {'Clear': 0, 'Partly Cloudy': 1, 'Cloudy': 2, 'Rain': 3, 'Thunderstorm': 4}
    df['climate_code'] = df['climate_condition'].map(climate_map)
    
    df.to_csv('data/weather_data.csv', index=False)

def train_model():
    """Train the enhanced weather prediction model"""
    if not os.path.exists('data/weather_data.csv'):
        generate_sample_data()
    
    df = pd.read_csv('data/weather_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_year'] = df['date'].dt.dayofyear
    df['year'] = df['date'].dt.year
    
    # Features for prediction
    X = df[['day_of_year', 'year', 'humidity', 'pressure', 
            'wind_speed', 'wind_direction', 'cloud_cover', 
            'climate_code']]
    
    # What we want to predict
    y = df[['temperature', 'precipitation', 'visibility']]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=150, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, 'weather_model.pkl')
    return model

def predict_weather(date, current_temp=None, humidity=50, pressure=1013, 
                   wind_speed=10, wind_direction=180, cloud_cover=30, 
                   climate_condition='Partly Cloudy'):
    """Make enhanced weather predictions"""
    if not os.path.exists('weather_model.pkl'):
        model = train_model()
    else:
        model = joblib.load('weather_model.pkl')
    
    try:
        date = pd.to_datetime(date)
        day_of_year = date.dayofyear
        year = date.year
        
        # Map climate condition to code
        climate_map = {'Clear': 0, 'Partly Cloudy': 1, 'Cloudy': 2, 'Rain': 3, 'Thunderstorm': 4}
        climate_code = climate_map.get(climate_condition, 1)
        
        # If current temperature is provided, use it as a feature
        temp_feature = current_temp if current_temp is not None else 20  # Default if not provided
        
        features = np.array([[day_of_year, year, humidity, pressure, 
                             wind_speed, wind_direction, cloud_cover, 
                             climate_code]])
        
        prediction = model.predict(features)
        
        return {
            'predicted_temp': float(round(prediction[0][0], 1)),
            'predicted_precip': float(round(max(0, prediction[0][1]), 1)),
            'predicted_visibility': float(round(prediction[0][2], 1)),
            'date': date.strftime('%Y-%m-%d'),
            'climate_condition': climate_condition
        }
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return None

if __name__ == '__main__':
    # Test prediction with more parameters
    print(predict_weather('2024-06-15', current_temp=25, humidity=65, 
                         pressure=1012, wind_speed=15, wind_direction=270,
                         cloud_cover=40, climate_condition='Partly Cloudy'))
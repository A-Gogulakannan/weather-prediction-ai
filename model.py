import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime

def generate_sample_data():
    """Generate realistic weather data with seasonal patterns"""
    dates = pd.date_range(start="2020-01-01", end="2023-12-31")
    num_days = len(dates)
    
    # Base patterns
    base_temp = 15 + 10 * np.sin(2 * np.pi * dates.dayofyear / 365)
    humidity_pattern = 50 + 20 * np.sin(2 * np.pi * dates.dayofyear / 365 + np.pi/2)
    
    df = pd.DataFrame({
        'date': dates,
        'temperature': base_temp + np.random.normal(0, 3, num_days),
        'humidity': np.clip(humidity_pattern + np.random.normal(0, 10, num_days), 20, 95),
        'pressure': np.clip(1015 + np.random.normal(0, 7, num_days), 980, 1040),
        'wind_speed': np.clip(np.random.weibull(1.5, num_days) * 15),  # km/h
        'wind_direction': np.random.randint(0, 360, num_days),
        'precipitation': np.clip(np.random.exponential(0.3, num_days), 0, 10),
        'cloud_cover': np.random.randint(0, 100, num_days),
        'climate_condition': np.random.choice(['Clear', 'Partly Cloudy', 'Cloudy', 'Rain', 'Thunderstorm'], num_days)
    })
    
    # Make weather conditions consistent with other parameters
    df.loc[df['precipitation'] > 2, 'climate_condition'] = 'Rain'
    df.loc[df['precipitation'] > 5, 'climate_condition'] = 'Thunderstorm'
    df.loc[df['cloud_cover'] < 20, 'climate_condition'] = 'Clear'
    df.loc[(df['cloud_cover'] >= 20) & (df['cloud_cover'] < 70), 'climate_condition'] = 'Partly Cloudy'
    df.loc[df['cloud_cover'] >= 70, 'climate_condition'] = 'Cloudy'
    
    df.to_csv('data/weather_data.csv', index=False)

def train_model():
    """Train the weather prediction model with realistic patterns"""
    if not os.path.exists('data/weather_data.csv'):
        generate_sample_data()
    
    df = pd.read_csv('data/weather_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_year'] = df['date'].dt.dayofyear
    df['month'] = df['date'].dt.month
    df['season'] = (df['month'] % 12 + 3) // 3
    
    # Convert climate condition to numerical values
    climate_map = {'Clear': 0, 'Partly Cloudy': 1, 'Cloudy': 2, 'Rain': 3, 'Thunderstorm': 4}
    df['climate_code'] = df['climate_condition'].map(climate_map)
    
    # Features and target
    features = ['day_of_year', 'season', 'humidity', 'pressure', 
               'wind_speed', 'wind_direction', 'cloud_cover', 'climate_code']
    targets = ['temperature', 'precipitation', 'cloud_cover']
    
    X = df[features]
    y = df[targets]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, 'weather_model.pkl')
    return model

def predict_weather(date, current_temp=None, humidity=50, pressure=1013, 
                   wind_speed=10, wind_direction=180, cloud_cover=30, 
                   climate_condition='Partly Cloudy'):
    """Make dynamic predictions based on inputs"""
    if not os.path.exists('weather_model.pkl'):
        model = train_model()
    else:
        model = joblib.load('weather_model.pkl')
    
    try:
        date = pd.to_datetime(date)
        day_of_year = date.dayofyear
        month = date.month
        season = (month % 12 + 3) // 3
        
        climate_map = {'Clear': 0, 'Partly Cloudy': 1, 'Cloudy': 2, 'Rain': 3, 'Thunderstorm': 4}
        climate_code = climate_map.get(climate_condition, 1)
        
        # Prepare input features
        features = np.array([[
            day_of_year, season, humidity, pressure,
            wind_speed, wind_direction, cloud_cover, climate_code
        ]])
        
        # Get prediction
        prediction = model.predict(features)
        
        # Calculate derived values
        predicted_temp = float(round(prediction[0][0], 1))
        predicted_precip = float(round(max(0, prediction[0][1]), 1))
        predicted_cloud = int(round(prediction[0][2]))
        
        # Determine likely climate condition based on predictions
        if predicted_precip > 5:
            likely_climate = 'Thunderstorm'
        elif predicted_precip > 2:
            likely_climate = 'Rain'
        elif predicted_cloud < 20:
            likely_climate = 'Clear'
        elif predicted_cloud < 70:
            likely_climate = 'Partly Cloudy'
        else:
            likely_climate = 'Cloudy'
        
        return {
            'predicted_temp': predicted_temp,
            'predicted_precip': predicted_precip,
            'predicted_cloud': predicted_cloud,
            'predicted_visibility': max(1, 20 - int(predicted_precip * 2)),  # km
            'predicted_wind_speed': wind_speed + np.random.uniform(-2, 2),  # Small variation
            'likely_climate': likely_climate,
            'date': date.strftime('%Y-%m-%d'),
            'input_parameters': {
                'humidity': humidity,
                'pressure': pressure,
                'wind_speed': wind_speed,
                'wind_direction': wind_direction
            }
        }
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return None
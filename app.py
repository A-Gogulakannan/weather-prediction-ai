from flask import Flask, render_template, request, jsonify
from model import predict_weather
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    try:
        # Required field
        date = data['date']
        
        # Optional fields with defaults
        current_temp = float(data.get('current_temp', '')) if data.get('current_temp') else None
        humidity = float(data.get('humidity', 50))
        pressure = float(data.get('pressure', 1013))
        wind_speed = float(data.get('wind_speed', 10))
        wind_direction = float(data.get('wind_direction', 180))
        cloud_cover = float(data.get('cloud_cover', 30))
        climate_condition = data.get('climate_condition', 'Partly Cloudy')
        
        prediction = predict_weather(
            date=date,
            current_temp=current_temp,
            humidity=humidity,
            pressure=pressure,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            cloud_cover=cloud_cover,
            climate_condition=climate_condition
        )
        
        if prediction:
            return jsonify({'success': True, 'prediction': prediction})
        else:
            return jsonify({'success': False, 'error': 'Prediction failed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
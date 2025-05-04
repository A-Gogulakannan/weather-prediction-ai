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
        required_fields = ['date', 'humidity', 'pressure', 'wind_speed', 
                         'wind_direction', 'cloud_cover', 'climate_condition']
        
        # Validate required fields
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'})
        
        # Get parameters with defaults
        current_temp = float(data['current_temp']) if 'current_temp' in data else None
        humidity = float(data['humidity'])
        pressure = float(data['pressure'])
        wind_speed = float(data['wind_speed'])
        wind_direction = float(data['wind_direction'])
        cloud_cover = float(data['cloud_cover'])
        climate_condition = data['climate_condition']
        
        # Make prediction
        prediction = predict_weather(
            date=data['date'],
            current_temp=current_temp,
            humidity=humidity,
            pressure=pressure,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            cloud_cover=cloud_cover,
            climate_condition=climate_condition
        )
        
        if prediction:
            return jsonify({
                'success': True,
                'prediction': prediction,
                'calculation_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return jsonify({'success': False, 'error': 'Prediction failed'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask, jsonify, request
from flask_cors import CORS
import paho.mqtt.client as mqtt
import json
import threading
from datetime import datetime
from collections import deque

app = Flask(__name__)
CORS(app)

# Store latest weather data and history (last 100 readings)
weather_data = {
    'temperature': 0.0,
    'humidity': 0.0,
    'wind_direction': 0.0,
    'wind_speed': 0.0,
    'last_updated': None
}

# Store historical data for charts
weather_history = {
    'temperature': deque(maxlen=100),
    'humidity': deque(maxlen=100),
    'wind_speed': deque(maxlen=100),
    'timestamps': deque(maxlen=100)
}

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "weather/data"

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    """Callback when MQTT client connects to broker"""
    if rc == 0:
        print(f"✓ Connected to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        print(f"✓ Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"✗ Failed to connect to MQTT Broker, return code {rc}")

def on_message(client, userdata, msg):
    """Callback when MQTT message is received"""
    try:
        payload = json.loads(msg.payload.decode())

        # Update current weather data
        weather_data['temperature'] = payload.get('temperature', 0.0)
        weather_data['humidity'] = payload.get('humidity', 0.0)
        weather_data['wind_direction'] = payload.get('wind_direction', 0.0)
        weather_data['wind_speed'] = payload.get('wind_speed', 0.0)
        weather_data['last_updated'] = datetime.now().isoformat()

        # Add to history
        timestamp = datetime.now().isoformat()
        weather_history['temperature'].append(payload.get('temperature', 0.0))
        weather_history['humidity'].append(payload.get('humidity', 0.0))
        weather_history['wind_speed'].append(payload.get('wind_speed', 0.0))
        weather_history['timestamps'].append(timestamp)

        print(f"📊 Weather data updated: Temp={payload.get('temperature')}°C, "
              f"Humidity={payload.get('humidity')}%, "
              f"Wind Speed={payload.get('wind_speed')}km/h")
    except Exception as e:
        print(f"✗ Error processing MQTT message: {e}")

def on_disconnect(client, userdata, rc):
    """Callback when MQTT client disconnects"""
    if rc != 0:
        print(f"⚠ Unexpected MQTT disconnection. Code: {rc}")

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect

def start_mqtt_client():
    """Start MQTT client in background thread"""
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_forever()
    except Exception as e:
        print(f"✗ MQTT Client Error: {e}")

# REST API Endpoints

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Weather Dashboard API',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/weather/current', methods=['GET'])
def get_current_weather():
    """Get current weather data"""
    if weather_data['last_updated'] is None:
        return jsonify({
            'error': 'No weather data available yet',
            'message': 'Waiting for data from MQTT broker'
        }), 404

    return jsonify({
        'status': 'success',
        'data': weather_data
    })

@app.route('/api/weather/history', methods=['GET'])
def get_weather_history():
    """Get historical weather data"""
    limit = request.args.get('limit', default=100, type=int)

    # Convert deques to lists and apply limit
    history_data = {
        'temperature': list(weather_history['temperature'])[-limit:],
        'humidity': list(weather_history['humidity'])[-limit:],
        'wind_speed': list(weather_history['wind_speed'])[-limit:],
        'timestamps': list(weather_history['timestamps'])[-limit:]
    }

    return jsonify({
        'status': 'success',
        'count': len(history_data['timestamps']),
        'data': history_data
    })

@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    """Get statistical summary of weather data"""
    if not weather_history['temperature']:
        return jsonify({
            'error': 'No historical data available'
        }), 404

    temps = list(weather_history['temperature'])
    humidity = list(weather_history['humidity'])
    wind_speeds = list(weather_history['wind_speed'])

    stats = {
        'temperature': {
            'current': temps[-1] if temps else 0,
            'min': min(temps) if temps else 0,
            'max': max(temps) if temps else 0,
            'avg': sum(temps) / len(temps) if temps else 0
        },
        'humidity': {
            'current': humidity[-1] if humidity else 0,
            'min': min(humidity) if humidity else 0,
            'max': max(humidity) if humidity else 0,
            'avg': sum(humidity) / len(humidity) if humidity else 0
        },
        'wind_speed': {
            'current': wind_speeds[-1] if wind_speeds else 0,
            'min': min(wind_speeds) if wind_speeds else 0,
            'max': max(wind_speeds) if wind_speeds else 0,
            'avg': sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0
        }
    }

    return jsonify({
        'status': 'success',
        'data': stats
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API documentation"""
    return jsonify({
        'service': 'Weather Dashboard API',
        'version': '1.0.0',
        'student_code': 'M24W0295',
        'endpoints': {
            'GET /api/health': 'Health check',
            'GET /api/weather/current': 'Get current weather data',
            'GET /api/weather/history?limit=100': 'Get historical weather data',
            'GET /api/weather/stats': 'Get weather statistics'
        }
    })

if __name__ == '__main__':
    # Start MQTT client in background thread
    mqtt_thread = threading.Thread(target=start_mqtt_client, daemon=True)
    mqtt_thread.start()

    print("=" * 60)
    print("🌤️  Weather Dashboard Flask Backend")
    print("=" * 60)
    print(f"📡 MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"📋 MQTT Topic: {MQTT_TOPIC}")
    print("🌐 Starting Flask server on http://localhost:5000")
    print("=" * 60)

    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

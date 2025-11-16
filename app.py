from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime
from collections import deque

app = Flask(__name__)
CORS(app)

# City coordinates
CITIES = {
    'Tokyo': {'lat': 35.6895, 'lon': 139.6917, 'name': 'Tokyo'},
    'Kyoto': {'lat': 35.0116, 'lon': 135.7681, 'name': 'Kyoto'},
    'Osaka': {'lat': 34.6937, 'lon': 135.5023, 'name': 'Osaka'},
    'Hokkaido': {'lat': 43.0642, 'lon': 141.3469, 'name': 'Hokkaido'},
    'New Delhi': {'lat': 28.6139, 'lon': 77.2090, 'name': 'New Delhi'},
    'Beijing': {'lat': 39.9042, 'lon': 116.4074, 'name': 'Beijing'},
    'Shanghai': {'lat': 31.2304, 'lon': 121.4737, 'name': 'Shanghai'},
    'New York': {'lat': 40.7128, 'lon': -74.0060, 'name': 'New York'},
    'Frankfurt': {'lat': 50.1109, 'lon': 8.6821, 'name': 'Frankfurt'}
}

OPEN_METEO_API = "https://api.open-meteo.com/v1/forecast"

def fetch_current_weather(city_data):
    """Fetch current weather from Open-Meteo API"""
    try:
        params = {
            'latitude': city_data['lat'],
            'longitude': city_data['lon'],
            'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m'
        }

        response = requests.get(OPEN_METEO_API, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            'temperature': data['current']['temperature_2m'],
            'humidity': data['current']['relative_humidity_2m'],
            'wind_speed': data['current']['wind_speed_10m'],
            'wind_direction': data['current']['wind_direction_10m'],
            'last_updated': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"✗ Error fetching current weather: {e}")
        return None

def fetch_hourly_history(city_data, hours=24):
    """Fetch hourly weather history from Open-Meteo API"""
    try:
        params = {
            'latitude': city_data['lat'],
            'longitude': city_data['lon'],
            'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m',
            'past_days': 1,
            'forecast_days': 1
        }

        response = requests.get(OPEN_METEO_API, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        hourly = data.get('hourly', {})
        # Get last 'hours' entries
        temp_data = hourly.get('temperature_2m', [])[-hours:]
        humidity_data = hourly.get('relative_humidity_2m', [])[-hours:]
        wind_speed_data = hourly.get('wind_speed_10m', [])[-hours:]
        time_data = hourly.get('time', [])[-hours:]

        return {
            'temperature': temp_data,
            'humidity': humidity_data,
            'wind_speed': wind_speed_data,
            'timestamps': time_data
        }
    except Exception as e:
        print(f"✗ Error fetching hourly history: {e}")
        return {
            'temperature': [],
            'humidity': [],
            'wind_speed': [],
            'timestamps': []
        }

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
    """Get current weather data for a specific city"""
    city = request.args.get('city', 'Tokyo')

    if city not in CITIES:
        return jsonify({
            'error': 'Invalid city',
            'available_cities': list(CITIES.keys())
        }), 400

    city_data = CITIES[city]
    weather_data = fetch_current_weather(city_data)

    if weather_data is None:
        return jsonify({
            'error': 'Failed to fetch weather data',
            'message': 'Unable to connect to weather service'
        }), 503

    return jsonify({
        'status': 'success',
        'city': city,
        'data': weather_data
    })

@app.route('/api/weather/history', methods=['GET'])
def get_weather_history():
    """Get hourly weather history for a city"""
    city = request.args.get('city', 'Tokyo')
    limit = request.args.get('limit', default=24, type=int)

    if city not in CITIES:
        return jsonify({
            'error': 'Invalid city',
            'available_cities': list(CITIES.keys())
        }), 400

    city_data = CITIES[city]
    history_data = fetch_hourly_history(city_data, min(limit, 48))

    return jsonify({
        'status': 'success',
        'city': city,
        'count': len(history_data['timestamps']),
        'data': history_data
    })

@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    """Get statistical summary of weather data for a city"""
    city = request.args.get('city', 'Tokyo')

    if city not in CITIES:
        return jsonify({
            'error': 'Invalid city',
            'available_cities': list(CITIES.keys())
        }), 400

    city_data = CITIES[city]
    history_data = fetch_hourly_history(city_data, 24)

    if not history_data['temperature']:
        return jsonify({
            'error': 'No historical data available'
        }), 404

    temps = history_data['temperature']
    humidity = history_data['humidity']
    wind_speeds = history_data['wind_speed']

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
        'city': city,
        'data': stats
    })

@app.route('/api/weather/forecast', methods=['GET'])
def get_weather_forecast():
    """Get 7-day weather forecast for a specific city"""
    city = request.args.get('city', 'Tokyo')

    if city not in CITIES:
        return jsonify({
            'error': 'Invalid city',
            'available_cities': list(CITIES.keys())
        }), 400

    city_data = CITIES[city]

    try:
        # Fetch 7-day forecast from Open-Meteo API
        params = {
            'latitude': city_data['lat'],
            'longitude': city_data['lon'],
            'daily': 'temperature_2m_max,temperature_2m_min,relative_humidity_2m_mean,wind_speed_10m_max,wind_direction_10m_dominant',
            'timezone': 'auto'
        }

        response = requests.get(OPEN_METEO_API, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Format the forecast data
        daily = data.get('daily', {})
        forecast = []

        for i in range(min(7, len(daily.get('time', [])))):
            forecast.append({
                'date': daily['time'][i],
                'temperature_max': daily['temperature_2m_max'][i],
                'temperature_min': daily['temperature_2m_min'][i],
                'humidity': daily['relative_humidity_2m_mean'][i],
                'wind_speed': daily['wind_speed_10m_max'][i],
                'wind_direction': daily['wind_direction_10m_dominant'][i]
            })

        return jsonify({
            'status': 'success',
            'city': city,
            'data': forecast
        })

    except Exception as e:
        print(f"✗ Error fetching forecast: {e}")
        return jsonify({
            'error': 'Failed to fetch weather forecast',
            'message': str(e)
        }), 500

@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Get list of available cities"""
    return jsonify({
        'status': 'success',
        'cities': list(CITIES.keys())
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API documentation"""
    return jsonify({
        'service': 'Weather Dashboard API',
        'version': '2.0.0',
        'student_code': 'M24W0295',
        'description': 'Simple weather API using Open-Meteo',
        'endpoints': {
            'GET /api/health': 'Health check',
            'GET /api/weather/current?city=Tokyo': 'Get current weather for a city',
            'GET /api/weather/history?city=Tokyo&limit=24': 'Get hourly weather history',
            'GET /api/weather/stats?city=Tokyo': 'Get weather statistics',
            'GET /api/weather/forecast?city=Tokyo': 'Get 7-day forecast for a city',
            'GET /api/cities': 'Get list of available cities'
        }
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🌤️  Weather Dashboard - Simplified API")
    print("=" * 60)
    print("🌍 Data Source: Open-Meteo API")
    print("🌐 Starting Flask server on http://localhost:5001")
    print(f"📍 Available Cities: {', '.join(CITIES.keys())}")
    print("=" * 60)

    # Start Flask app
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
